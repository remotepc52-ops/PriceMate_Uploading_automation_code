import json
import re
import time
from parsel import Selector
from urllib.parse import quote, urlencode
import scrapy
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from pricemate.spiders.bs_spider import PricemateBaseSpider

headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
    'priority': 'u=1, i',
    'referer': 'https://tiki.vn/nha-sach-tiki/c8322',
    'sec-ch-ua': '"Google Chrome";v="143", "Chromium";v="143", "Not A(Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36',
    'x-guest-token': 'yckNibgTaOo490GfjdxR8ZYe7lwXVFtK',
    'cookie': '_trackity=1e80fe0f-8359-4b5d-ffac-86483cf899ac; TOKENS={%22access_token%22:%22yckNibgTaOo490GfjdxR8ZYe7lwXVFtK%22}',
}


class TikiPlSpider(PricemateBaseSpider):
    name = "tiki_pl"

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
            slug = url.split("/")[-1]
            m = re.search(r"/c(\d+)", url)
            cat_id = m.group(1) if m else None
            # print(cat_id)

            meta = {
                "url": url,
                "_id": hash_id,
                "slug":slug,
                "cat_id":cat_id,
                "page":1,
                "filename": f"{slug}_page.html",
                "should_be": ["data"]
            }
            params = {
                'limit': '40',
                'include': 'advertisement',
                'aggregations': '2',
                'version': 'home-persionalized',
                'trackity_id': '1e80fe0f-8359-4b5d-ffac-86483cf899ac',
                'urlKey': 'nha-sach-tiki',
                'category': cat_id,
                'page': '1'
            }
            api_url = f'https://tiki.vn/api/personalish/v1/blocks/listings?{urlencode(params)}'

            yield scrapy.Request(
                url=api_url,
                headers=headers,
                callback=self.parse_pl,
                meta=meta
            )

    def parse_pl(self, response):
        meta = response.meta
        doc_id = meta.get("_id")
        slug = meta.get("slug")
        cat_id = meta.get("cat_id")

        try:
            data = response.json()
        except Exception as e:
            self.logger.error(f"JSON Decode failed for {response.url}: {e}")
            return


        product_list = data.get("data", [])

        if not product_list:
            self.logger.info(f"No products found. Marking category {doc_id} as Not Found.")
            self.category_input.update_one({"_id": doc_id}, {"$set": {"Status": "Not Found"}})
            return

        for product in product_list:
            # Skip if it is an advertisement/banner without proper product data
            if "id" not in product:
                continue

            slug_id = product.get("id")
            spid = product.get("seller_product_id")

            # Get URL Path from JSON, falling back to url_key if necessary
            url_part = product.get("url_path")
            if not url_part:
                url_part = f"{product.get('url_key')}.html"

            pdp_url = f'https://tiki.vn/{url_part}'

            # Use base spider method to generate hash
            product_hash = self.generate_hash_id(pdp_url, self.retailer, self.region)

            item = {
                "_id": product_hash,
                "slug_id": slug_id,
                "spid": spid,
                "ProductURL": pdp_url,
                "Status": "Pending",
                "retailer": self.retailer,
                "region": self.region,

            }

            self.save_product(item)
            # self.logger.info(f"Saved: {pdp_url}")

        # 2. Handle Pagination
        # In your JSON, pagination is inside data["paging"]
        paging = data.get("paging", {})
        current_page = paging.get("current_page", 1)
        last_page = paging.get("last_page", 1)

        print(f"Processed Page {current_page} of {last_page} for CatID: {cat_id}")

        if current_page < last_page:
            next_page = current_page + 1

            # Update meta for the next request


            # Construct Next URL
            params = {
                'limit': '40',
                'include': 'advertisement',
                'aggregations': '2',
                'version': 'home-persionalized',
                'trackity_id': '1e80fe0f-8359-4b5d-ffac-86483cf899ac',
                'urlKey': 'nha-sach-tiki',
                'category': cat_id,
                'page': str(next_page)
            }
            next_api_url = f'https://tiki.vn/api/personalish/v1/blocks/listings?{urlencode(params)}'
            meta = {
                "url": next_api_url,
                "slug": slug,
                "cat_id": cat_id,
                "page": str(next_page),
                "filename": f"{slug}_page_{next_page}.html",
                "should_be": ["data"]
            }
            yield scrapy.Request(
                url=next_api_url,
                headers=headers,
                callback=self.parse_pl,
                meta=meta
            )

            # If we reached the last page, update the category status in Mongo
        self.category_input.update_one(
            {"_id": doc_id},
            {"$set": {"Status": "Done"}}
        )
        print(f"Category {cat_id} COMPLETED.")


    def close(self, reason):
        self.mongo_client.close()

if __name__ == '__main__':
    from scrapy.cmdline import execute
    execute("scrapy crawl tiki_pl -a retailer=tiki-vn -a region=vn -a Type=eshop -a RetailerCode=tiki_vn".split())