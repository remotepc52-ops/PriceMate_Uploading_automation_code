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
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'en-US,en;q=0.9',
    'apps': '{"app_version":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:143.0) Gecko/20100101 Firefox/143.0","device_class":"browser|browser","device_family":"none","device_id":"b4f25d42-b2f4-4398-a582-feb4bc9226cb","os_name":"Windows","os_version":"10"}',
    # 'if-none-match': '"s1fkji0d75mlr"',
    'origin': 'https://www.klikindomaret.com',
    'priority': 'u=1, i',
    'referer': 'https://www.klikindomaret.com/',
    'sec-ch-ua': '"Chromium";v="140", "Not=A?Brand";v="24", "Google Chrome";v="140"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'Host':'ap-mc.klikindomaret.com',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:143.0) Gecko/20100101 Firefox/143.0',
    'x-correlation-id': '2a3853c5-6e3b-4da3-bc09-f99cf4c8c1c0',
}


class KlikindoPlSpider(PricemateBaseSpider):
    name = "klikindo_pl"

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
            for ur in url:
                path = ur.split("category/")[-1]
                parts = path.split("/")

                main_cate = parts[0] if len(parts) > 0 else ""
                sub_cate = parts[1] if len(parts) > 1 else ""
                sub_sub_cate = parts[2] if len(parts) > 2 else ""
            meta = {
                "url": url,
                "_id": hash_id,
                "slug":slug,
                "main_cate": main_cate,
                "sub_cate": sub_cate,
                "sub_sub_cate": sub_sub_cate,
                "filename": f"{slug}_page.html",
                "should_be": ["data"]
            }
            yield scrapy.Request(
                url = f'https://ap-mc.klikindomaret.com/assets-klikidmgroceries/api/get/catalog-xpress/api/webapp/search/result?metaCategories={main_cate}&page=0&size=20&storeCode=TJKT&latitude=-6.1763897&longitude=106.82667&mode=DELIVERY&districtId=141100100&categories={sub_cate}&subCategories={sub_sub_cate}',
                headers=headers,
                callback=self.parse_pl,
                meta=meta
            )

    def parse_pl(self, response):
        meta = response.meta
        doc_id = meta.get("_id")
        slug = meta.get("slug")
        main_cate = meta.get("main_cate")
        sub_cate = meta.get("sub_cate")
        sub_sub_cate = meta.get("sub_sub_cate")
        try:
            data = response.json()
        except Exception as e:
            self.logger.error(f"JSON failed : {e}")
            return
        content_list = data.get("data", {}).get("content", [])
        total_pages = data.get("data", {}).get("totalPages", 1)
        current_page = data.get("data", {}).get("number", 0)
        for product in content_list:
            prod_id = product.get("productId")
            prod_slug = product.get("permalink")
            if not prod_slug:
                continue

            pdp_url = f'https://www.klikindomaret.com/xpress/{prod_slug}'
            product_hash = self.generate_hash_id(pdp_url, self.retailer, self.region)

            item = {
                "_id": product_hash,
                "ProductURL": pdp_url,
                "ProductCode": prod_id,
                "Status": "Pending",
                "retailer": self.retailer,
                "region": self.region,
            }
            self.save_product(item)
            self.logger.info(f"Product URL: {pdp_url}")
            self.category_input.update_one(
                {"_id": doc_id},
                {"$set": {"Status": "Done"}}
            )
            if current_page + 1 < total_pages:
                next_page = current_page + 1
                api_url = (
                    "https://ap-mc.klikindomaret.com/assets-klikidmgroceries/api/get/catalog-xpress/api/webapp/search/result"
                    f"?metaCategories={meta['main_cate']}&page={next_page}&size=20&storeCode=TJKT&latitude=-6.1763897&longitude=106.82667"
                    f"&mode=DELIVERY&districtId=141100100&categories={meta['sub_cate']}&subCategories={meta['sub_sub_cate']}"
                )
                meta = {
                    "slug": slug,
                    "main_cate": main_cate,
                    "sub_cate": sub_cate,
                    "sub_sub_cate": sub_sub_cate,
                    "filename": f"{slug}_{next_page}_page.html",
                    "should_be": ["data"]
                }
                yield scrapy.Request(
                    url=api_url,
                    headers=headers,
                    callback=self.parse_pl,
                    meta=meta
                )



    def close(self, reason):
        self.mongo_client.close()

if __name__ == '__main__':
    from scrapy.cmdline import execute
    execute("scrapy crawl klikindo_pl -a retailer=klikindomaret-id -a region=id -a Type=eshop -a RetailerCode=klikindomaret_id".split())