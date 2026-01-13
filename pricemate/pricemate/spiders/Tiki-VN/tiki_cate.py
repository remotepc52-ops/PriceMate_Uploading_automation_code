import json
import time
from urllib.parse import quote
import scrapy
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from pricemate.spiders.base_spider import PricemateBaseSpider

# cookies = {
#     '_trackity': '1e80fe0f-8359-4b5d-ffac-86483cf899ac',
#     'TOKENS': '{%22access_token%22:%22yckNibgTaOo490GfjdxR8ZYe7lwXVFtK%22}',
# }

headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
    'origin': 'https://tiki.vn',
    'priority': 'u=1, i',
    'referer': 'https://tiki.vn/',
    'sec-ch-ua': '"Google Chrome";v="143", "Chromium";v="143", "Not A(Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36',
    'x-guest-token': 'yckNibgTaOo490GfjdxR8ZYe7lwXVFtK',
    'cookie': '_trackity=1e80fe0f-8359-4b5d-ffac-86483cf899ac; TOKENS={%22access_token%22:%22yckNibgTaOo490GfjdxR8ZYe7lwXVFtK%22}',
}

class TikiCateSpider(PricemateBaseSpider):
    name = "tiki_cate"

    def __init__(self, retailer, region, *args, **kwargs):
        super().__init__(retailer=retailer, region=region, *args, **kwargs)

    def start_requests(self):
        url = 'https://api.tiki.vn/raiden/v2/menu-config?platform=desktop'

        yield scrapy.Request(
            url=url,
            headers=headers,
            callback=self.get_cate,
            meta={
                "filename": f"Cate_{self.generate_hash_id(url)}.json",
                "should_be": ["menu_block"]
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

        menu_block = data.get("menu_block", {})
        all_data = menu_block.get("items", [])

        for main in all_data:
            cate_url = main.get("link")


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
    execute("scrapy crawl tiki_cate -a retailer=tiki-vn -a region=vn -a Type=eshop -a RetailerCode=tiki_vn".split())