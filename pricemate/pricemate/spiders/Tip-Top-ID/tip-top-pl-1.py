import json
import re
import os
import scrapy
from scrapy.http import JsonRequest
from pricemate.spiders.bs_spider import PricemateBaseSpider


headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
    # 'if-none-match': 'W/"578c1-9Lq2D5DA7YM1Zlz3//4uB3Y5Z3w"',
    'origin': 'https://shop.tiptop.co.id',
    'priority': 'u=1, i',
    'referer': 'https://shop.tiptop.co.id/',
    'sec-ch-ua': '"Chromium";v="142", "Google Chrome";v="142", "Not_A Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36',
    'x-api-key': '29ea3dcf-67c3-45f6-b5c4-d2628f7e09fa',
    'x-requested-with': 'XMLHttpRequest',
}

class TiptopPlSpider(PricemateBaseSpider):
    name = "tiptop_pl"

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
            cate_id = doc["cate_id"]
            hash_id = doc.get("_id")

            meta = {
                "url": url,
                "_id": hash_id,
                "cate_id": cate_id,
                "filename": f"{cate_id}_page.html",
                "should_be": ["data"],
                "direct_requests" :True,
            }
            yield scrapy.Request(
                url = f'https://api.tiptop.co.id/api/web/product?page=1&limit=200&sortBy=desc&categoryId={cate_id}&subCategoryId=&outletId=63bcfc340bcec42a8f284bfd',
                headers=headers,
                callback=self.parse_json,
                meta=meta
            )



    def parse_json(self, response):
        meta = response.meta
        doc_id = meta.get('_id')
        cate_id = meta.get('cate_id')
        current_page = meta.get('page', 1)
        # referer_url = meta.get("referer_url", response.url)

        try:
            data = response.json()
        except Exception:
            self.logger.error(f"Failed to parse JSON for {response.url}")
            return
        paging = data.get("paging", {})

        # Save each product
        for cate in data.get("data", []):
            prod_id = cate.get("_id")
            name = cate.get("name")
            prod_name = re.sub(r"[ ,]+", "-", name.replace("&", "and"))
            pdp_url = f'https://shop.tiptop.co.id/outlet/Rawamangun/product/{prod_name}?key={prod_id}'

            hash_id = self.generate_hash_id(pdp_url, self.retailer, self.region)
            item = {
                "_id": hash_id,
                "ProductCode": prod_id,
                "ProductURL": pdp_url,
                "Status": "Pending",
                "retailer": self.retailer,
                "region": self.region
            }

            self.save_url(item)
            print(f"Inserted: {pdp_url}")

        # Pagination
        total_pages = paging.get("totalPage", 1)
        next_page = paging.get("nextPage")
        if next_page and next_page <= total_pages:
            next_url = re.sub(r"page=\d+", f"page={next_page}", response.url)
            yield JsonRequest(
                url=next_url,
                headers=headers,
                callback=self.parse_json,
                meta={
                    "_id": doc_id,
                    "cate_id": cate_id,
                    "page": next_page,
                    "url":next_url,
                    # "referer_url": referer_url,
                    "filename": f"{cate_id}_{next_page}_page.html",
                    "should_be": ["data"],
                    "direct_requests": True
                },
                dont_filter=True,
            )
        else:
            self.category_input.update_one(
            {"_id": doc_id},
            {"$set": {"Status": "Done"}}
        )


    def close(self, reason):
        self.mongo_client.close()


if __name__ == '__main__':
    from scrapy.cmdline import execute
    execute("scrapy crawl tiptop_pl -a retailer=tiptop-id -a region=id -a Type=eshop -a RetailerCode=tiptop_id".split())