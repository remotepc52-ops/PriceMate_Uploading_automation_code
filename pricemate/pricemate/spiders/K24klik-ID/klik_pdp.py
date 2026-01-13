import json
import re
import time
from parsel import Selector
from urllib.parse import quote
import scrapy
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from pricemate.spiders.base_spider import PricemateBaseSpider

cookies = {
    'YII_CSRF_TOKEN': '0bd47f32a1fcecda58a41a4270dad43eefbfbaefs%3A40%3A%22a0e006a73f05f1d0b49ff12650f51655a5cf8ff6%22%3B',
    '_gid': 'GA1.2.1019380953.1757395459',
    '_tt_enable_cookie': '1',
    '_ttp': '01K4PEX7G2JS0X17VHGY3XTA0N_.tt.1',
    '_fbp': 'fb.1.1757398355298.267345781960445113',
    'EShoppingCart': '85b99fea8a049dea52aa7e7f170302924204e5d4s%3A115%3A%2269c2253057a39d59b7d43738a24025e8affaddf2a%3A1%3A%7Bs%3A12%3A%22Product29489%22%3Ba%3A2%3A%7Bs%3A2%3A%22id%22%3Bs%3A12%3A%22Product29489%22%3Bs%3A3%3A%22qty%22%3Bi%3A1%3B%7D%7D%22%3B',
    'PHPSESSID': '1hbccge7a7pn7vuirou9n96akl',
    '2d0de97669ee3a3e232fdbbc5a1824fd8d5b505f': '28711%2C518%2C2350%2C35576%2C21923%2C29489',
    '_ga_B1X2VHE3TK': 'GS2.1.s1757407808$o3$g1$t1757411125$j60$l0$h0',
    '_ga': 'GA1.1.1093648019.1757395459',
    'ttcsid': '1757407817969::sMtD05SyXu0VfGbvHuMG.4.1757411126639',
    'ttcsid_D0O31FBC77U7M2KJ8VJ0': '1757407817953::N1Um3-Cuzk7TdBB7pXFo.3.1757411142574',
}

headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'en-US,en;q=0.9',
    'cache-control': 'max-age=0',
    'priority': 'u=0, i',
    'sec-ch-ua': '"Chromium";v="140", "Not=A?Brand";v="24", "Google Chrome";v="140"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'none',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36',
}


class KlikPdpSpider(PricemateBaseSpider):
    name = "klik_pdp"

    def __init__(self, retailer, region, *args, **kwargs):
        super().__init__(retailer=retailer, region=region, *args, **kwargs)

    def start_requests(self):
        docs = self.category_input.find({
            "retailer": self.retailer,
            "region": self.region,
            "Status": "Pending"
        })
        for doc in docs:
            url = doc["url"]
            hash_id = doc.get("_id")
            slug = url.split("/")[-1].split("?")[0]

            meta = {
                "url": url,
                "_id": hash_id,
                "slug": slug,
                "filename": f"Pdp_{slug}_page.html",
                "should_be": ["k24-df-on k24-width-100 k24-df-direct-column k24-gap-8"]
            }
            yield scrapy.Request(
                url,
                cookies=cookies,
                headers=headers,
                callback=self.parse_pdp,
                meta=meta
            )

    def parse_pdp(self, response):
        meta = response.meta
        doc_id = meta.get('_id')
        prod_url = meta.get('url')

        name = response.xpath('//h1[@itemprop="name"]/text()').get(default="").strip()
        price = response.xpath('//meta[@property="product:amount"]/@content').get()
        was_price_text = response.xpath('normalize-space(//span[contains(@style,"line-through")]//span/text())').get()

        # price = re.search(r'[\d\.,]+', price_text or "").group(0) if price_text else ""
        was_price = re.search(r'[\d\.,]+', was_price_text or "").group(0) if was_price_text else ""

        orignal_price = f"{int(float(price.replace('.', '').replace(',', ''))):,}".replace(",", "") if price else ""
        was_price_main = f"{int(float(was_price.replace('.', '').replace(',', ''))):,}".replace(",","") if was_price else ""

        rrp = was_price_main if was_price_main != "" else orignal_price
        per_price = response.xpath('//span[@itemprop="offers"]/text()').re_first(r'Rp.*')
        offers = response.xpath('normalize-space(//span[@itemprop="offers"]//text())').get(default="")
        offer = " ".join(offers.split())
        img = response.xpath('//div[@id="loadMultiplePhotoSectionWrapper"]//img/@data-src').get()
        prod_id = response.xpath('//meta[@property="product:retailer_item_id"]/@content').get()
        pack_size = response.xpath('//h2[contains(text(),"Kemasan:")]/following-sibling::span/text()').get(default="").strip()
        stock_text = response.xpath('//meta[@itemprop="availability"]/@content').get()
        stock = True if "InStock" in stock_text else False
        promo_type = "Cashback" if "Cashback" in offer else ""
        brand = response.xpath('//div[@itemprop="brand"]/meta/@content').get(default="").strip().replace('-','')
        tags = response.xpath('//a[contains(@href,"/cariObat/tag:")]/div/p/text()').getall()
        breadcrumb = " > ".join([t.strip() for t in tags if t.strip()])
        bread = f'{breadcrumb}>{name}'
        product_hash = self.generate_hash_id(prod_url, self.retailer, self.region)

        item = {
            "_id": product_hash,
            "Name": name,
            "Promo_Type": promo_type,
            "Price": orignal_price,
            "per_unit_price": per_price,
            "WasPrice": was_price_main,
            "Offer_info": offer,
            "Pack_size": pack_size,
            "Barcode": "",
            "is_available": stock,
            "Images": img,
            "ProductURL": prod_url,
            "Status": "Done",
            "ParentCode": "",
            "ProductCode": prod_id,
            "retailer_name": "k24klik",
            "Category_Hierarchy": bread,
            "Brand": brand,
            "RRP": rrp,
        }
        try:
            self.save_product(item)
            print(f"✓ Successfully inserted {prod_url}")
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
            "--domain", "k24klik.com"
        ]
        subprocess.run(cmd, cwd=r"E:\pricemate_service")

        self.mongo_client.close()


if __name__ == '__main__':
    from scrapy.cmdline import execute
    execute("scrapy crawl klik_pdp -a retailer=k24klik-id -a region=id -a Type=eshop -a RetailerCode=k24klik_id".split())