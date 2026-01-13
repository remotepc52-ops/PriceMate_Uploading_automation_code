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
    'G_ENABLED_IDPS': 'google',
    '_fbp': 'fb.2.1758525308771.53630574256007009',
    'callbell_uid': 'e175a960-9783-11f0-87cc-c94817329ed9',
    'XSRF-TOKEN': 'eyJpdiI6IjA4T0daMGU1MjdBTmxhNkVYaVRmNUE9PSIsInZhbHVlIjoiUWZRWGlhZEVaaTNVQXBIXC9zWVd1Mll2YXNLZTZaeExsamo0ZlluTVFxenFSQytjcGFPdWNPZFQ2bkEzWFpwTW8iLCJtYWMiOiIzNzY2MGJhMTEyZWFiYmUxZTM5OTFkYThjYTdmZjNmNGQzZWU1YWUwYzhjZjYyZTE4NmQxOTEyYzZiNDY4ZTdhIn0%3D',
    'yogya_online_session': 'eyJpdiI6ImpPa1c3Z2c5SFpJM0R0Nyt2a3NZbGc9PSIsInZhbHVlIjoiTjBHQ1NaOEdPSTY2K0VHZ1VKb0lNMXNOYVZJNDRRdktsaEQxS2FNRmZhU21HcksyZm9LSTNUWTFxKzJ4dm1MTiIsIm1hYyI6IjdlN2Q2Y2Q5OTliNjkzYTBjYjk0YzUzOTFkZDQ1NDU3M2NmYjI1YzU2Y2EyYTA1ODQxZmYwYzljZWY5YTkyYzkifQ%3D%3D',
    'TScfcaf399027': '08adbf8ca3ab20005cf38087ae6057623c5086de93b3e2690a38092ccfd4ebc86cb0a04c71c5287308700e16cf1130006a96c7bae3ba24910a2e6208b10e978bf9eb301302f0ff5ae79fa5e75167f149de3806fa1b52dd18b7e93efce1d3a295',
}

headers = {
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8',
    'Connection': 'keep-alive',
    'Referer': 'https://supermarket.yogyaonline.co.id/',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36',
    'X-CSRF-TOKEN': 'K8VpJrFwfd1IYiv6Kq9WnmuTBPA3nD4uXOj2x2RB',
    'X-Requested-With': 'XMLHttpRequest',
    'X-XSRF-TOKEN': 'eyJpdiI6IjA4T0daMGU1MjdBTmxhNkVYaVRmNUE9PSIsInZhbHVlIjoiUWZRWGlhZEVaaTNVQXBIXC9zWVd1Mll2YXNLZTZaeExsamo0ZlluTVFxenFSQytjcGFPdWNPZFQ2bkEzWFpwTW8iLCJtYWMiOiIzNzY2MGJhMTEyZWFiYmUxZTM5OTFkYThjYTdmZjNmNGQzZWU1YWUwYzhjZjYyZTE4NmQxOTEyYzZiNDY4ZTdhIn0=',
    'sec-ch-ua': '"Chromium";v="140", "Not=A?Brand";v="24", "Google Chrome";v="140"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    # 'Cookie': 'G_ENABLED_IDPS=google; _fbp=fb.2.1758525308771.53630574256007009; callbell_uid=e175a960-9783-11f0-87cc-c94817329ed9; XSRF-TOKEN=eyJpdiI6IjA4T0daMGU1MjdBTmxhNkVYaVRmNUE9PSIsInZhbHVlIjoiUWZRWGlhZEVaaTNVQXBIXC9zWVd1Mll2YXNLZTZaeExsamo0ZlluTVFxenFSQytjcGFPdWNPZFQ2bkEzWFpwTW8iLCJtYWMiOiIzNzY2MGJhMTEyZWFiYmUxZTM5OTFkYThjYTdmZjNmNGQzZWU1YWUwYzhjZjYyZTE4NmQxOTEyYzZiNDY4ZTdhIn0%3D; yogya_online_session=eyJpdiI6ImpPa1c3Z2c5SFpJM0R0Nyt2a3NZbGc9PSIsInZhbHVlIjoiTjBHQ1NaOEdPSTY2K0VHZ1VKb0lNMXNOYVZJNDRRdktsaEQxS2FNRmZhU21HcksyZm9LSTNUWTFxKzJ4dm1MTiIsIm1hYyI6IjdlN2Q2Y2Q5OTliNjkzYTBjYjk0YzUzOTFkZDQ1NDU3M2NmYjI1YzU2Y2EyYTA1ODQxZmYwYzljZWY5YTkyYzkifQ%3D%3D; TScfcaf399027=08adbf8ca3ab20005cf38087ae6057623c5086de93b3e2690a38092ccfd4ebc86cb0a04c71c5287308700e16cf1130006a96c7bae3ba24910a2e6208b10e978bf9eb301302f0ff5ae79fa5e75167f149de3806fa1b52dd18b7e93efce1d3a295',
}

class YogyaCateSpider(PricemateBaseSpider):
    name = "yogya_cate"

    def __init__(self, retailer, region, *args, **kwargs):
        super().__init__(retailer=retailer, region=region, *args, **kwargs)

    def start_requests(self):
        url = 'https://supermarket.yogyaonline.co.id/category-web/load'

        current_proxy = '2c6ea6e6d8c14216a62781b8f850cd5b'

        proxy_host = "api.zyte.com"
        proxy_port = "8011"
        proxy_auth = f"{current_proxy}:"

        proxy_url = f"https://{proxy_auth}@{proxy_host}:{proxy_port}"

        yield scrapy.Request(
            url=url,
            cookies=cookies,
            headers=headers,
            callback=self.parse_cat,
            meta={
                "proxy": proxy_url,
                "filename": f"PL_{self.generate_hash_id(url)}.html",
                "should_be": ["html"],
                "direct_requests": True,
            })

    def parse_cat(self, response):
        try:
            data = json.loads(response.text)
        except Exception as e:
            self.logger.error(f"JSON decode failed: {e}")
            return

        html_content = data.get("html", "")
        if not html_content:
            self.logger.error("No HTML found in response JSON")
            return

        sel = Selector(text=html_content)

        json_strs = sel.xpath('//div[contains(@class,"show-category-level-3")]/@data-child-sub-category').getall()

        for json_str in json_strs:
            try:
                categories = json.loads(json_str)
            except Exception as e:
                self.logger.error(f"JSON parse failed for sub-category: {e}")
                continue

            for cat in categories:
                category_slug = cat.get("category_slug")
                if not category_slug:
                    continue

                cate_url = f"https://supermarket.yogyaonline.co.id/supermarket/{category_slug}/category"
                hash_id = self.generate_hash_id(cate_url, self.retailer, self.region)

                self.category_input.update_one(
                    {"_id": hash_id},
                    {"$set": {
                        "url": cate_url,
                        "cat_id":cat_id,
                        "Status": "Pending",
                        "retailer": self.retailer,
                        "region": self.region
                    }},
                    upsert=True
                )
                self.logger.info(f"Inserted sub-category: {cate_url}")
        for onclick in sel.xpath('//div[@class="yo-category-card"]/@onclick').getall():
            match = re.search(r'`(https://supermarket\.yogyaonline\.co\.id/supermarket[^\s`"]+)`', onclick)
            if match:
                cate_url = match.group(1)
                hash_id = self.generate_hash_id(cate_url, self.retailer, self.region)

                self.category_input.update_one(
                    {"_id": hash_id},
                    {"$set": {
                        "url": cate_url,
                        "Status": "Pending",
                        "retailer": self.retailer,
                        "region": self.region
                    }},
                    upsert=True
                )
                self.logger.info(f"Inserted main category: {cate_url}")
        for onclick in sel.xpath('//div[@class="col-sm-12 pt-0 pl-0"]/@onclick').getall():
            match = re.search(r'`(https://supermarket\.yogyaonline\.co\.id/supermarket[^\s`"]+)`', onclick)
            if match:
                cate_url = match.group(1)
                hash_id = self.generate_hash_id(cate_url, self.retailer, self.region)

                self.category_input.update_one(
                    {"_id": hash_id},
                    {"$set": {
                        "url": cate_url,
                        "Status": "Pending",
                        "retailer": self.retailer,
                        "region": self.region
                    }},
                    upsert=True
                )
                self.logger.info(f"Inserted category: {cate_url}")


    def close(self, reason):
        self.mongo_client.close()

if __name__ == '__main__':
    from scrapy.cmdline import execute
    execute("scrapy crawl yogya_cate -a retailer=yogya-id -a region=id -a Type=eshop -a RetailerCode=yogya_id".split())