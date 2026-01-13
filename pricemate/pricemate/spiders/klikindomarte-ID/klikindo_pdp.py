import json
import re
import time
from parsel import Selector
from urllib.parse import quote
import scrapy
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from pricemate.spiders.base_spider import PricemateBaseSpider

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:143.0) Gecko/20100101 Firefox/143.0',
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'en-US,en;q=0.5',
    # 'Accept-Encoding': 'gzip, deflate, br, zstd',
    'x-correlation-id': '4bebd7c8-7145-4a9a-89ef-970201cdea17',
    'apps': '{"app_version":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:143.0) Gecko/20100101 Firefox/143.0","device_class":"browser|browser","device_family":"none","device_id":"3693a9cf-301a-465b-b578-7c29c4f7ab10","os_name":"Windows","os_version":"10"}',
    'page': 'page',
    'Origin': 'https://www.klikindomaret.com',
    'Connection': 'keep-alive',
    'Referer': 'https://www.klikindomaret.com/',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-site',
    'Pragma': 'no-cache',
    'Cache-Control': 'no-cache',
    # Requests doesn't support trailers
    # 'TE': 'trailers',
}

class KlikindoPdpSpider(PricemateBaseSpider):
    name = "klikindo_pdp"

    def __init__(self, retailer, region, *args, **kwargs):
        super().__init__(retailer=retailer, region=region, *args, **kwargs)

    def start_requests(self):
        docs = self.product_table.find({
            "retailer": self.retailer,
            "region": self.region,
            "Status": "Pending"
        })
        for doc in docs:
            url = doc["ProductURL"]
            hash_id = doc.get("_id")
            slug = url.split("/")[-1]

            meta = {
                "url": url,
                "_id": hash_id,
                "slug": slug,
                "filename": f"{slug}_page.html",
                "should_be": ["data"],
                "direct_request": True,
            }
            yield scrapy.Request(
                url=f'https://ap-mc.klikindomaret.com/assets-klikidmgroceries/api/get/catalog-xpress/api/webapp/product/detail-page?storeCode=TJKT&latitude=-6.1763897&longitude=106.82667&mode=DELIVERY&districtId=141100100&permalink={slug}',
                headers=headers,
                callback=self.parse_pdp,
                meta=meta
            )

    def parse_pdp(self, response):
        # print(response.status_code)
        meta = response.meta
        prod_url = meta.get("url")
        doc_id = meta.get('_id')

        try:
            data = response.json()
        except Exception as e:
            self.logger.error(f"JSON failed : {e}")
            return
        product = data.get("data", {}).get("product", {})

        prod_id = product.get("productId")
        name = product.get("productName")
        barcode = product.get("plu")
        was_price = product.get("price")
        price = product.get("finalPrice")
        if price is None:
            price = was_price
            rrp = was_price
            was_price = ""
        else:
            price = price
            rrp = was_price
        promo = product.get("promoType") if product.get("promoType") else ""
        discount = product.get("discountText") if product.get("discountText") else ""
        brand = product.get("brandName") if product.get("brandName") else ""
        pack_size = product.get("size") if product.get("size") else ""
        img = "|".join(product.get("images", []))
        breadcrumb = f'Home>{name}'
        in_stock = not product.get("blacklist", True)

        product_hash = self.generate_hash_id(prod_url, self.retailer, self.region)
        item = {"_id": product_hash, "Name": name, "Promo_Type": promo, "Price": price, "per_unit_price": "",
                "WasPrice": was_price,
                "Offer_info": discount, "Pack_size": pack_size, "Barcode": barcode,
                "Images": img,
                "ProductURL": prod_url, "is_available": in_stock,
                "Status": "Done", "ParentCode": "", "ProductCode": prod_id,
                "retailer_name": "klikindomart-id",
                "Category_Hierarchy": breadcrumb, "Brand": brand, "RRP": rrp}
        try:
            self.save_product(item)
            print(f"✓ Successfully inserted {prod_url}")
            if doc_id:
                self.product_table.update_one(
                    {"_id": doc_id},
                    {"$set": {"Status": "Done"}}
                )
        except Exception as e:
            print(e)


    def close(self, reason):
        import subprocess
        cmd = [
            "python",
            "upload_to_s3_direct.py",
            "--domain", "klikindomaret.com"
        ]
        subprocess.run(cmd, cwd=r"E:\pricemate_service")
        self.mongo_client.close()

if __name__ == '__main__':
    from scrapy.cmdline import execute
    execute("scrapy crawl klikindo_pdp -a retailer=klikindomaret-id -a region=id -a Type=eshop -a RetailerCode=klikindomaret_id".split())