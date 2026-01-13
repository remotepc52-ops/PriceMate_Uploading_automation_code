import json
import time
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
    # 'x-correlation-id': 'd2470448-8459-4213-b7cb-0c753bcf4ed7',
    'apps': '{"app_version":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:143.0) Gecko/20100101 Firefox/143.0","device_class":"browser|browser","device_family":"none","device_id":"9562517a-3217-4602-b689-830ac3ec7844","os_name":"Windows","os_version":"10"}',
    'page': 'unpage',
    'Host': 'ap-mc.klikindomaret.com',
    'Origin': 'https://www.klikindomaret.com',
    'Connection': 'keep-alive',
    'Referer': 'https://www.klikindomaret.com/',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-site',
    'x-correlation-id': 'c16f9279-13b7-4b3c-93b6-006d3c1aff89',
    # Requests doesn't support trailers
    # 'TE': 'trailers',
}

class KlikindoCateSpider(PricemateBaseSpider):
    name = "klikindo_cate"

    def __init__(self, retailer, region, *args, **kwargs):
        super().__init__(retailer=retailer, region=region, *args, **kwargs)

    def start_requests(self):
        url = 'https://ap-mc.klikindomaret.com/assets-klikidmgroceries/api/get/catalog-xpress/api/webapp/category/meta?storeCode=TJKT&latitude=-6.1763897&longitude=106.82667&mode=DELIVERY&districtId=141100100'

        yield scrapy.Request(
            url=url,
            headers=headers,
            callback=self.get_cate,
            meta={
                "filename": f"PL_{self.generate_hash_id(url)}.html",
                "should_be": ["data"]
                # "direct_requests": True
            }
            # dont_filter= True,
        )

    def get_cate(self, response):
        try:
            data = response.json()
        except Exception as e:
            self.logger.error(f"JSON failed : {e}")
            return

        base_url = "https://www.klikindomaret.com/xpress/category"
        all_data = data.get("data", [])

        for main in all_data:
            main_slug = main.get("permalink")
            if not main_slug:
                continue

            # Insert main category
            self._insert_category(f"{base_url}/{main_slug}")

            for cat in main.get("categories", []):
                sub_slug = cat.get("permalink")
                if not sub_slug:
                    continue

                # Insert main + sub
                self._insert_category(f"{base_url}/{main_slug}/{sub_slug}")

                for sub in cat.get("subCategories", []):
                    sub_sub_slug = sub.get("permalink")
                    if not sub_sub_slug:
                        continue

                    # Insert main + sub + sub-sub
                    self._insert_category(f"{base_url}/{main_slug}/{sub_slug}/{sub_sub_slug}")

    def _insert_category(self, cate_url):
        hash_id = self.generate_hash_id(cate_url, self.retailer, self.region)
        self.category_input.update_one(
            {"_id": hash_id},
            {
                "$set": {
                    "url": cate_url,
                    "Status": "Pending",
                    "retailer": self.retailer,
                    "region": self.region,
                }
            },
            upsert=True,
        )
        self.logger.info(f"Inserted: {cate_url}")

    def close(self, reason):
        self.mongo_client.close()

if __name__ == '__main__':
    from scrapy.cmdline import execute
    execute("scrapy crawl klikindo_cate -a retailer=klikindomaret-id -a region=id -a Type=eshop -a RetailerCode=klikindomaret_id".split())