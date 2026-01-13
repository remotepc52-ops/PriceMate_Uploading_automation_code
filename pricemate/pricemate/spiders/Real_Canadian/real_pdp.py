import json
import re
from typing import Iterable, Any

import scrapy
import time
from urllib.parse import urlparse
from urllib.parse import urljoin
import os, sys

from scrapy.http import JsonRequest

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from pricemate.spiders.base_spider import PricemateBaseSpider


headers = {
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'en',
    'Business-User-Agent': 'PCXWEB',
    'Connection': 'keep-alive',
    'Content-Type': 'application/json',
    'Origin': 'https://www.realcanadiansuperstore.ca',
    'Origin_Session_Header': 'B',
    'Referer': 'https://www.realcanadiansuperstore.ca/',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'cross-site',
    'Sec-Fetch-Storage-Access': 'active',
    'Site-Banner': 'superstore',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36',
    'sec-ch-ua': '"Not;A=Brand";v="99", "Google Chrome";v="139", "Chromium";v="139"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'x-apikey': 'C1xujSegT5j3ap3yexJjqhOfELwGKYvz',
}

class RealPdpSpider(PricemateBaseSpider):
    name = "real_pdp"

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
            # match = re.search(r"/i/(\d+)\.html", url)
            # product_slug = match.group(1)
            #Extract product id from urls
            match1 = re.search(r"/p/([^/?]+)", url)
            product_id = match1.group(1)


            meta = {
                "url": url,
                "_id": hash_id,
                # "product_slug": product_slug,
                "product_id":product_id,
                "filename": f"{product_id}_page.html",
                # "should_be": ["productView-title"]
            }
            yield scrapy.Request(
                url,
                headers=headers,
                callback=self.parse_pdp,
                meta=meta
            )

    def parse_pdp(self, response):

        meta = response.meta
        doc_id = meta.get('_id')
        product_id = meta.get('product_id')
        # product_slug = meta.get('product_slug')
        referer_url = meta.get('referer_url', response.url)
        new_url = f'https://api.pcexpress.ca/pcx-bff/api/v1/products/{product_id}?lang=en&date=26082025&pickupType=STORE&storeId=1530&banner=superstore'
        try:
            yield JsonRequest(
                url=new_url,
                callback=self.parse_json,
                headers=headers,
                meta={
                    "doc_id": doc_id,
                    "product_id": product_id,
                    "referer_url": referer_url,

                }
            )
        except Exception as e:
            print(f"Data not Found {e}")

    def parse_json(self, response):
        meta = response.meta
        doc_id = meta.get('doc_id')
        product_id = meta.get('product_id')
        referer_url = meta.get('referer_url', response.url)

        data = json.loads(response.body)

        name = data.get('name')
        brand = data.get('brand')
        parent_code = data.get("breadcrumbs", [{}])[-1].get("categoryCode")

        img_url = [img["largeUrl"] for img in data.get("imageAssets", []) if img.get("largeUrl")]
        img_url = "|".join(img_url)
        breadcrumb = " > ".join([b["name"] for b in data.get("breadcrumbs", [])])

        offer = data.get("offers", [{}])[0]

        original_price = offer.get("price", {}).get("value")

        comparison_str = (
            f"${offers[0]['comparisonPrices'][0]['value']:.2f}/ {offers[0]['comparisonPrices'][0]['quantity']}{offers[0]['comparisonPrices'][0]['unit']}"
            if (offers := data.get("offers")) and offers and offers[0].get("comparisonPrices")
            else ""
        )

        was_price = None
        if offer.get("wasPrice") is not None:
            was_price = offer["wasPrice"].get("value")

        promo_text = None
        if offer.get("dealPrice") is not None:
            promo_text = (
                offer.get("badges", {}).get("dealBadge", {}).get("text")
            )
        if was_price:
            rrp = was_price
        else:
            rrp = original_price
        is_available = offer.get('stockStatus')
        if is_available == "OK":
            is_available = True
        else:
            is_available = False
        pack_size = data.get('packageSize')

        item = {
            "_id": doc_id,
            "Name": name,
            "Promo_Type": "",
            "Price": original_price,
            "per_unit_price": comparison_str,
            "WasPrice": was_price,
            "Offer_info": promo_text,
            "Pack_size": pack_size,
            "Barcode": "",
            "is_available": is_available,
            "Images": img_url,
            "ProductURL": referer_url,
            "Status": "Done",
            "ParentCode": parent_code,
            "ProductCode": product_id,
            "retailer_name": "realcanadian",
            "Category_Hierarchy": breadcrumb,
            "Brand": brand,
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


if __name__ == '__main__':
    from scrapy.cmdline import execute
    execute("scrapy crawl real_pdp -a retailer=realcanadian-ca -a region=ca -a Type=eshop -a RetailerCode=realcanadian_ca".split())