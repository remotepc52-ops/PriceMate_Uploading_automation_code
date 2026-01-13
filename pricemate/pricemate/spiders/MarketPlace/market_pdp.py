import json
import re
from typing import Iterable, Any

import scrapy
import time
from urllib.parse import urlparse
from urllib.parse import urljoin
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from pricemate.spiders.base_spider import PricemateBaseSpider


cookies = {
    'pickUpStoreId': '',
    'shipmentType': '1',
    'venderId': '5',
    'longitude': '114.1249695',
    'latitude': '22.3433916',
    'store': '642',
    '_fbp': 'fb.1.1755837532803.578329380108000599',
    'ec-pixel-config': 'JTdCJTIyc2hvcElkJTIyJTNBbnVsbCUyQyUyMnNob3BQbGF0Zm9ybSUyMiUzQSUyMm93bnNpdGUlMjIlMkMlMjJ0ZWFtJTIyJTNBJTIyTWFya2V0JTIwUGxhY2UlMjIlMkMlMjJlY2lkJTIyJTNBJTIyNmJjNjY2NTQtMGIxOC00ZTljLTk5MzUtOWI1YTMzMGRhYzM2JTIyJTJDJTIyZW5hYmxlUGl4ZWwlMjIlM0F0cnVlJTJDJTIydHhMaW5rVHJhY2tpbmdMaWZldGltZSUyMiUzQTMwJTdE',
    'ec-token': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc0Fub255bW91cyI6InRydWUiLCJyb2xlIjowLCJ0IjoiTWFya2V0IFBsYWNlIiwiZCI6Imt0NkN5NnBoNUw2dWRLY1lDRVhSbnF6eEhscy9zZnZNOUF6ZEFHYU5pZmM9IiwiZSI6Imt0NkN5NnBoNUw2dWRLY1lDRVhSbnBYb3hjeGpRMUQ3MGxQNkZ0RjNsakI1K1hqQlRxVlRKYTRDa3RkYVgwM0J4SE4yYW5MT0RlMFpta3VmS3FCTFRnPT0iLCJpc0FkbWluIjoiZmFsc2UiLCJzc28iOiJmYWxzZSJ9.-dDEaY1IFeMvPjON2Z5Yv7GW9DnMlCH2wEX6Qo2x0Rs',
    '_ga': 'GA1.1.1079108034.1755837538',
    'superweb-locale': 'en_US',
    '__ocmm': '-180357582',
    '__ocssid': 'ccsum80n-mempn3ku.1755859886813.1755859886827',
    '_ga_C2J4GHSH66': 'GS2.1.s1755837537$o1$g1$t1755859912$j17$l0$h0',
}

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Language': 'en-US,en;q=0.9',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-User': '?1',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36',
    'sec-ch-ua': '"Not;A=Brand";v="99", "Google Chrome";v="139", "Chromium";v="139"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
}

class MarketPdpSpider(PricemateBaseSpider):
    name = "market_pdp"

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

            # Extract product slug for filename
            match = re.search(r"/i/(\d+)\.html", url)
            product_slug = match.group(1)

            meta = {
                "url": url,
                "_id": hash_id,
                "product_slug": product_slug,
                "filename": f"{product_slug}_page.html",
                # "should_be": ["productView-title"]
            }
            yield scrapy.Request(
                url,
                headers=headers,
                callback=self.parse_pdp,
                meta=meta
            )

    def parse_pdp(self, response):
        try:
            meta = response.meta
            doc_id = meta.get('_id')
            product_slug = meta.get('product_slug')
            referer_url = meta.get('referer_url', response.url)
            prod = response.xpath('//div[@class="info-content"]')
            # Extract basic product info
            name = response.xpath('//div[@class="info-content"]//div[@class="title"]/text()').get()
            orignal_price = prod.xpath('//div[@class="price-line"]/span[@class="price"]/text()').get()
            price_small = prod.xpath('//div[@class="price-line"]/span[@class="price-small"]/text()').get()
            if price_small:
                orignal_price = orignal_price + price_small
            was_price = prod.xpath('//div[@class="price-line"]/span[@class="old-price"]/text()').get()
            orignal_price = float(orignal_price.replace("$", "").replace(",", "").strip()) if orignal_price else None
            was_price = float(was_price.replace("$", "").replace(",", "").strip()) if was_price else None
            if was_price:
                rrp = was_price
            else:
                rrp = orignal_price
            size = response.xpath('.//div[@class="size-line"]//div[@class="value"]//text()').get()
            img_url = response.xpath('.//div[@class="small-img"]//img/@src').getall()
            image_urls = " | ".join(img_url)
            bread = f'Home>{name}'
            item_code = response.xpath('.//div[@class="item-code"]//text()').get()
            pro_code = item_code.split(":")[1].strip()

            brand_name = response.xpath('//script[@type="application/ld+json"]/text()').get()
            if brand_name:
                data = json.loads(brand_name)
                brand_name = data.get("brand", {}).get("name")
            else:
                brand_name = ""
            stock = response.xpath('.//div[@class="actions"]//div[@class="sold-out"]')
            if stock:
                stock = False
            else:
                stock = True
            name1 = response.xpath('.//div[@class="row-1 single-line-text"]/text()').get()
            offer = response.xpath('.//div[@class="offer-item"]//div[@class="tag"]/text()').getall()
            offers = " | ".join(offer)

            script_text = response.xpath('//script[contains(text(),"Case Deal")]/text()').get()
            if script_text:
                skus = re.findall(r'\b\d{9}\b', script_text)  # extract all 9-digit SKUs
                for sku in skus:
                    pdp_url1 = f'https://www.marketplacehk.com/en/p/{name1}/i/{sku}.html'
                    product_hash1 = self.generate_hash_id(pdp_url1, self.retailer, self.region)

                    items = {
                        "_id": product_hash1,
                        "ProductURL": pdp_url1,
                        "Parent_id": product_slug,
                        "Status": "Pending",
                        "retailer": self.retailer,
                        "region": self.region,
                        "category_url": referer_url
                    }
                    try:
                        self.product_table.insert_one(items)
                    except Exception as e:
                        print("varaitaion already inserted !!")

            item = {
                "_id": doc_id,
                "Name": name,
                "Promo_Type": '',
                "Price": orignal_price,
                "per_unit_price": '',
                "WasPrice": was_price,
                "Offer_info": offers,
                "Pack_size": size,
                "Barcode": "",
                "is_available": stock,
                "Images": image_urls,
                "ProductURL": referer_url,
                "Status": "Done",
                "ParentCode": product_slug,
                "ProductCode": pro_code,
                "retailer_name": "marketplace",
                "Category_Hierarchy": bread or '',
                "Brand": brand_name,
                "RRP": rrp,
            }
            try:
                self.save_product(item)
                # self.product_table.insert_one(item)
                print(f"✓ Successfully inserted {referer_url}")
                if doc_id:
                    self.product_table.update_one(
                        {"_id": doc_id},
                        {"$set": {"Status": "Done"}}
                    )
            except Exception as e:
                print(e)
        except Exception as e:
            print(f"Data not Found {e}")

    def close(self, reason):
        self.mongo_client.close()



if __name__ == '__main__':
    from scrapy.cmdline import execute
    execute("scrapy crawl market_pdp -a retailer=marketplace-hk -a region=hk -a Type=eshop -a RetailerCode=marketplace_hk".split())