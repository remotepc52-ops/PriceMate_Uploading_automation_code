import json
import re
import time
from parsel import Selector
from urllib.parse import urlencode
import scrapy
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from pricemate.spiders.base_spider import PricemateBaseSpider


headers = {
    'accept': 'application/json, text/javascript, */*; q=0.01',
    'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
    'origin': 'https://www.waltermartdelivery.com.ph',
    'priority': 'u=1, i',
    'referer': 'https://www.waltermartdelivery.com.ph/shop/shop_by_category/food_pantry/d/1496146',
    'sec-ch-ua': '"Chromium";v="142", "Google Chrome";v="142", "Not_A Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'cross-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36',
}

class WaltermartPlSpider(PricemateBaseSpider):
    name = "walter_pl"

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
            store = url.split("/")[-1]
            slug = url.split("/")[-3]
            current_proxy = '2c6ea6e6d8c14216a62781b8f850cd5b'

            proxy_host = "api.zyte.com"
            proxy_port = "8011"
            proxy_auth = f"{current_proxy}:"

            proxy_url = f"https://{proxy_auth}@{proxy_host}:{proxy_port}"
            meta = {
                "proxy": proxy_url,
                "url": url,
                "_id": hash_id,
                "store": store,
                "slug": slug,
                "limit": 24,
                "skip": 0,
                "filename": f"PL_{slug}_page.html",
                "should_be": ["items"]
            }

            yield self.build_request(meta)

    def build_request(self, meta):
        """Helper function to construct the API URL with pagination."""
        base_url = "https://api.freshop.ncrcloud.com/1/products?"
        params = {
            "app_key": "walter_mart",
            "department_id": f"{meta['store']}",
            "department_id_cascade": "true",
            "fields": "id,identifier,attribution_token,reference_id,reference_ids,upc,name,store_id,department_id,size,cover_image,price,sale_price,sale_price_md,sale_start_date,sale_finish_date,price_disclaimer,sale_price_disclaimer,is_favorite,relevance,popularity,shopper_walkpath,fulfillment_walkpath,quantity_step,quantity_minimum,quantity_initial,quantity_label,quantity_label_singular,varieties,quantity_size_ratio_description,status,status_id,sale_configuration_type_id,fulfillment_type_id,fulfillment_type_ids,other_attributes,clippable_offer,slot_message,call_out,has_featured_offer,tax_class_label,promotion_text,sale_offer,store_card_required,average_rating,review_count,like_code,shelf_tag_ids,offers,is_place_holder_cover_image,video_config,enforce_product_inventory,disallow_adding_to_cart,substitution_type_ids,unit_price,offer_sale_price,canonical_url,offered_together,sequence",
            "include_offered_together": "true",
            "limit": meta["limit"],
            "skip": meta["skip"],
            "sort": "popularity",
            "popularity_sort": "asc",
            "render_id": "1763976135951",
            "store_id": "6483",
            "token": "c0fd243769fa2b504f7794a6437efda4"
        }

        api_url = base_url + urlencode(params)

        return scrapy.Request(
            url=api_url,
            headers=headers,
            callback=self.parse_pl,
            meta=meta
        )

    def parse_pl(self, response):
        meta = response.meta
        doc_id = meta["_id"]
        data = json.loads(response.text)

        total = data.get("total", 0)
        items = data.get("items", [])
        skip = meta["skip"]
        limit = meta["limit"]

        # ✅ Save each product
        for prod in items:
            pdp_url = prod.get('canonical_url')
            if not pdp_url:
                continue

            product_hash = self.generate_hash_id(pdp_url, self.retailer, self.region)
            item = {
                "_id": product_hash,
                "ProductURL": pdp_url,
                "Status": "Pending",
                "retailer": self.retailer,
                "region": self.region,
            }
            self.save_product(item)
            print(f"Inserted: {pdp_url}")

        # ✅ Pagination
        next_skip = skip + limit
        if next_skip < total:
            meta["skip"] = next_skip
            print(f"➡ Going to next page: skip={next_skip}")
            yield self.build_request(meta)
        else:
            print(f"✅ Completed all pages for {meta['slug']}")

        self.category_input.update_one({"_id": doc_id}, {"$set": {"Status": "Done"}})


    def close(self, reason):
        self.mongo_client.close()

if __name__ == '__main__':
    from scrapy.cmdline import execute
    execute("scrapy crawl walter_pl -a retailer=waltermart-ph -a region=ph -a Type=eshop -a RetailerCode=waltermart_ph".split())