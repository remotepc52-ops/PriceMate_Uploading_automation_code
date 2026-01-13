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
    '_ga': 'GA1.1.547981432.1749189992',
    'mp_d7f79c10b89f9fa3026f2fb08d3cf36d_mixpanel': '%7B%22distinct_id%22%3A%20%22%24device%3A19743d91b718a6-063cd8524c853c-26011e51-144000-19743d91b718a6%22%2C%22%24device_id%22%3A%20%2219743d91b718a6-063cd8524c853c-26011e51-144000-19743d91b718a6%22%2C%22%24initial_referrer%22%3A%20%22%24direct%22%2C%22%24initial_referring_domain%22%3A%20%22%24direct%22%7D',
    '_ga_MN0XLNH39T': 'GS2.1.s1749189992$o1$g1$t1749190038$j14$l0$h0',
}

headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8,hi;q=0.7',
    'if-none-match': 'W/"1db1-o+LVrK9xjtMK5zagDBjKbE2DPb0"',
    'origin': 'https://www.mydin.my',
    'priority': 'u=1, i',
    'referer': 'https://www.mydin.my/',
    'sec-ch-ua': '"Google Chrome";v="137", "Chromium";v="137", "Not/A)Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36',
}


class MydinCatSpider(PricemateBaseSpider):
    name = "mydin_cat"

    def __init__(self, retailer, region, *args, **kwargs):
        super().__init__(retailer=retailer, region=region, *args, **kwargs)

    def start_requests(self):
        url = 'https://myapi.mydin.my/magento/categories?body=[%7B%22filters%22:%7B%22url_key%22:%7B%22eq%22:%22all-products%22%7D%7D%7D,%7B%22categories%22:%22categories-custom-query%22,%22metadata%22:%7B%22fields%22:%22%5Cn++++++++++++++++++++++++items+%7B%5Cn++++++++++++++++++++++++++++id%5Cn++++++++++++++++++++++++++++image%5Cn++++++++++++++++++++++++++++name%5Cn++++++++++++++++++++++++++++category_bm_name%5Cn++++++++++++++++++++++++++++url_key%5Cn++++++++++++++++++++++++++++meta_title%5Cn++++++++++++++++++++++++++++product_count%5Cn++++++++++++++++++++++++++++children+%7B%5Cn++++++++++++++++++++++++++++++++id%5Cn++++++++++++++++++++++++++++++++image%5Cn++++++++++++++++++++++++++++++++name%5Cn++++++++++++++++++++++++++++++++category_bm_name%5Cn++++++++++++++++++++++++++++++++url_key%5Cn++++++++++++++++++++++++++++++++meta_title%5Cn++++++++++++++++++++++++++++++++product_count%5Cn++++++++++++++++++++++++++++%7D%5Cn++++++++++++++++++++++++%7D%5Cn++++++++++++++++++++%22%7D%7D,%7B%7D]'

        current_proxy = '2c6ea6e6d8c14216a62781b8f850cd5b'

        proxy_host = "api.zyte.com"
        proxy_port = "8011"
        proxy_auth = f"{current_proxy}:"

        proxy_url = f"https://{proxy_auth}@{proxy_host}:{proxy_port}"

        yield scrapy.Request(
            url=url,
            cookies=cookies,
            headers=headers,
            callback=self.parse,
            meta={
                "proxy": proxy_url,
                "filename": f"PL_{self.generate_hash_id(url)}.html",
                "should_be": ["items"],
                })

    def parse(self, response):
        data = json.loads(response.text)
        categories = data.get('data', {}).get('categories', {})
        items = categories.get('items', [])

        for item in items:
            children = item.get('children', [])
            for child in children:
                url_key = child.get('url_key')
                cat_id = child.get('id')
                cate_url = f'https://www.mydin.my/category/{url_key}'

                hash_id = self.generate_hash_id(cate_url, self.retailer, self.region)

                self.category_input.update_one(
                    {"_id": hash_id},
                    {"$set": {
                        "url": cate_url,
                        "cat_id": cat_id,
                        "Status": "Pending",
                        "retailer": self.retailer,
                        "region": self.region
                    }},
                    upsert=True
                )
                self.logger.info(f"Insert")
    def close(self, reason):
        self.mongo_client.close()

if __name__ == '__main__':
    from scrapy.cmdline import execute
    execute('scrapy crawl mydin_cat -a retailer=mydin-my -a region=my -a Type=eshop -a RetailerCode=mydin_my'.split())