import json
import re
import time

from Common_Modual.common_functionality import Rprint
from lxml import etree
from urllib.parse import quote
import scrapy
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from pricemate.spiders.base_spider import PricemateBaseSpider


headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
    'cache-control': 'no-cache',
    'pragma': 'no-cache',
    'priority': 'u=0, i',
    'sec-ch-ua': '"Google Chrome";v="141", "Not?A_Brand";v="8", "Chromium";v="141"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'none',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36',
    # 'cookie': 'localization=MY; _shopify_y=85c1be1d-560c-4ef3-a8d4-1684e93e301b; WISHLIST_TOTAL=0; WISHLIST_PRODUCTS_IDS={}; WISHLIST_PRODUCTS_IDS_SET=1; WISHLIST_UUID=null; WISHLIST_IP_ADDRESS=146.70.14.23; bb_page-9560cac402cb492cb4836e0a_token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VySWQiOiJiYi02U25vc0pza3Bsc19uQWQ5UDR0Q1AiLCJwYWdlSWQiOiJwYWdlLTk1NjBjYWM0MDJjYjQ5MmNiNDgzNmUwYSIsImJvdElkIjoiYm90LU9WU25Qa3BLdiIsImlhdCI6MTc1OTEyOTU4NiwiaXNzIjoiYm90Ym9ubmllX3dlYmNoYXQifQ.WWiEwnbp00dE0IgYieyOo4ueEQn704efkXj98zwsdOU; bb_page-9560cac402cb492cb4836e0a_uuid=bb-6SnosJskpls_nAd9P4tCP; _fbp=fb.1.1759129587482.789288308822170372; _shopify_essential=:AZmUSzImAAEAnmv0vPbnMy4mf1DTnWXulspsTFKpTToUUeqohufctK55WVj6lZ_yuVzjpNXqYpe94KwoxpgywYyHVMzgcQ7RK8UrYepEl0cE9Nx7jeZzF574d-f0RTGE5Q1ru8-hPCSdEyqLl4z5XfR47kcGMiQ5nAl4yXLBjYncNV1xKKmD2OtQJBeG3BGBCMhswA2u5vb2NEUV89CHMpYBbwl8xMLWoNf52bg6P-cWa5Ev-NGnNRguSLv2RAmLJ6Cy9NUTFiHHwGnJGPVEzL8lQk-VosmS00OmKqJ3_FsF5leQfWVVKDgzzsI8roEnoGEdVOM_DUt8pTRCZHqhafutFVTBswNt8mDD29FA4EOZJ2IGd1Drn41-:; _shopify_analytics=:AZokyZ6YAAEADkcUoeazeSoq6ZFFnXulT2Ve6wWOcWyMizzZXST4Cb_3i5w3Q09y1KsXD_AoTHErhWcx7QbubMQlDwamk4tgxdeWfd9If1TucTWNGpdlf_-z-sf2cgKI87k:; _shopify_s=d045ad5f-79b6-4b1e-b49a-5878ee79e344; keep_alive=eyJ2IjoyLCJ0cyI6MTc2MTU1Mzc5ODg2OCwiZW52Ijp7IndkIjowLCJ1YSI6MSwiY3YiOjEsImJyIjoxfSwiYmh2Ijp7Im1hIjoxLCJjYSI6MCwia2EiOjAsInNhIjowLCJrYmEiOjAsInRhIjowLCJ0IjoxMSwibm0iOjAsIm1zIjowLCJtaiI6MCwibXNwIjowLCJ2YyI6MCwiY3AiOjAsInJjIjowLCJraiI6MCwia2kiOjAsInNzIjowLCJzaiI6MCwic3NtIjowLCJzcCI6MCwidHMiOjAsInRqIjowLCJ0cCI6MCwidHNtIjowfSwic2VzIjp7InAiOjEsInMiOjE3NjE1NTM3ODc2NjgsImQiOjEwfX0%3D',
}


class EstorePdpSpider(PricemateBaseSpider):
    name = "estore_pdp"

    def __init__(self, retailer, region, *args, **kwargs):
        super().__init__(retailer=retailer, region=region, *args, **kwargs)

    def start_requests(self):

        docs = self.category_input.find({
            "retailer": self.retailer,
            "region": self.region,
            "Status": "Pending"
        })
        for doc in docs:
            current_proxy = '2c6ea6e6d8c14216a62781b8f850cd5b'

            proxy_host = "api.zyte.com"
            proxy_port = "8011"
            proxy_auth = f"{current_proxy}:"

            proxy_url = f"https://{proxy_auth}@{proxy_host}:{proxy_port}"

            url = doc["url"]
            hash_id = doc.get("_id")
            slug = url.split("/products/")[-1]
            meta = {
                "proxy" : proxy_url,
                "url": url,
                "Prod_url": url,
                "_id": hash_id,
                "filename": f"{slug}_page.html",
                "should_be": ["application/ld+json"]
            }

            yield scrapy.Request(
                url=url,
                headers=headers,
                callback=self.parse_pdp,
                meta=meta,
            )

    def parse_pdp(self, response):
        meta = response.meta

        referer_url = meta.get("url")
        doc_id = meta.get("_id")

        name = response.xpath('//h1[@class="yv-product-detail-title h5"]/text()').get()
        if name:
            name = name.strip()

        raw_price = response.xpath(
            '//div[@class="yv-prizebox no-js-hidden "]//span[@class="yv-product-price h2"]/text()').get()
        raw_was_price = response.xpath(
            '//div[@class="yv-compare-price-box"]//span[@class="yv-product-compare-price"]/text()').get()

        price = raw_price.replace("RM", "").replace(",", "").strip() if raw_price else None
        was_price = raw_was_price.replace("RM", "").replace(",", "").strip() if raw_was_price else None

        orignal_price = float(price.replace('"', '').strip()) if price else None
        compare_price = float(was_price.replace('"', '').strip()) if was_price else None
        if compare_price == None:
            compare_price = ""
        print(price)
        brand = response.xpath('//a[@class="product-vendor"]/text()').get()
        if brand:
            brand = brand.title()
        retail = "Caring Pharmacy"
        parent_id = response.xpath('//p[@class="yv-product-sku"]/text()').get()
        script = response.xpath('//script[@data-name="variant-json"]/text()').get()
        if script:
            try:
                data = json.loads(script)
                product_id = data[0].get('id')
                is_available = data[0].get('available')
            except json.JSONDecodeError:
                self.logger.warning(f"Invalid JSON in {referer_url}")
                product_id = None
                is_available = None
        else:
            self.logger.warning(f"No variant-json found in {referer_url}")
            # Fallback: extract product ID / availability from HTML if possible
            product_id = response.xpath('//p[@class="yv-product-sku"]/text()').get()
            # For availability, fallback to a class/text indicating "Out of stock"
            avail_text = response.xpath('//div[contains(@class,"product-stock")]/text()').get()
            is_available = True if avail_text and "in stock" in avail_text.lower() else False
        offer_info = response.xpath('//span[@class="yv-product-percent-off"]/text()').get() or ""
        image = response.xpath('//div[@class="product-slider-item-wrapper"]//a/@href').get()
        bread = response.xpath('//div[@class="breadcrumb"]//li/a/text()').getall()
        breadcrumb_path = ' > '.join(bread)
        if not was_price or price == was_price:
            rrp_price = price
            was_price = ''
        else:
            rrp_price = was_price
        if rrp_price:
            rrp_price = float(rrp_price)
        else:
            rrp_price = None

        match = re.search(r"(\d+\s*[A-Za-z]+$|\d+\s*[xX]\s*\d+|\d+SX\d+|\d+\s*(ml|g|mg|kg|l))", name, re.IGNORECASE)
        pack_size = match.group(1) if match else ""

        barcode = response.xpath('//script[contains(text(), "avadaVariants")]/text()').re_first(r'"barcode":"(\d+)"')
        product_hash = self.generate_hash_id(referer_url, self.retailer, self.region)

        if orignal_price == 0:
            self.product_table.update_one(
                {'_id': doc_id}, {"$set": {"Status": 'Not Found'}})
            Rprint("Price Not Found...")

        item = {"_id": product_hash,"Name": name, "Promo_Type": "", "Price": orignal_price, "per_unit_price": "",
                 "WasPrice": compare_price,
                 "Offer_info": offer_info, "Pack_size": pack_size, "Barcode": barcode,
                 "Images": f"https://{image}",
                 "ProductURL": referer_url, "is_available": is_available,
                 "Status": "Done", "ParentCode": parent_id, "ProductCode": product_id,
                 "retailer_name": "estore",
                 "Category_Hierarchy": breadcrumb_path, "Brand": brand, "RRP": rrp_price}
        try:
            self.save_product(item)
            print(f"✓ Successfully inserted {referer_url}")
            if doc_id:
                self.category_input.update_one(
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
            "--domain", "estore.caring2u.com"
        ]
        subprocess.run(cmd, cwd=r"E:\pricemate_service")
        self.mongo_client.close()

if __name__ == '__main__':
    from scrapy.cmdline import execute
    execute("scrapy crawl estore_pdp -a retailer=caring-my -a region=my -a Type=eshop -a RetailerCode=caring_my".split())