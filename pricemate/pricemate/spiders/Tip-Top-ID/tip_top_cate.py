import json
import re
import time
from urllib.parse import quote
import scrapy
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from pricemate.spiders.bs_spider import PricemateBaseSpider


headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'en-US,en;q=0.9',
    # 'if-none-match': 'W/"39cbc-Wog2jhq66WVZjt3z/8n/jJDVKGo"',
    'origin': 'https://shop.tiptop.co.id',
    'priority': 'u=1, i',
    'referer': 'https://shop.tiptop.co.id/',
    'sec-ch-ua': '"Not;A=Brand";v="99", "Google Chrome";v="139", "Chromium";v="139"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36',
    'x-api-key': '29ea3dcf-67c3-45f6-b5c4-d2628f7e09fa',
    'x-requested-with': 'XMLHttpRequest',
}

class TiptopCateSpider(PricemateBaseSpider):
    name = "tiptop_cate"

    def __init__(self, retailer, region, *args, **kwargs):
        super().__init__(retailer=retailer, region=region, *args, **kwargs)

    def start_requests(self):
        url = 'https://api.tiptop.co.id/api/web/product-category?sortName=sort&page=1&limit=20&outletId=63bcfc340bcec42a8f284bfd'

        yield scrapy.Request(
            url=url,
            headers=headers,
            callback=self.parse,
            meta={
                "filename": f"PL_{self.generate_hash_id(url)}.html",
                "should_be": ["data"]
            })

    def parse(self, response):
        data = response.json()
        for cate in data.get("data", []):
            cate_id = cate.get("_id")
            name = cate.get("name")
            cate_name = re.sub(r"[ ,]+", "-", name.replace("&", "and"))
            cate_url = f'https://shop.tiptop.co.id/outlet/Rawamangun/category/{cate_name}?key={cate_id}'

            hash_id = self.generate_hash_id(cate_url, self.retailer, self.region)
            self.category_input.update_one(
                {"_id": hash_id},
                {"$set": {"url": cate_url, "cate_id":cate_id,"Status": "Pending", "retailer": self.retailer, "region": self.region}},
                upsert=True
            )
            print(f"inserted: {cate_url}")


    def close(self, reason):
        self.mongo_client.close()

if __name__ == '__main__':
    from scrapy.cmdline import execute
    execute("scrapy crawl tiptop_cate -a retailer=tiptop-id -a region=id -a Type=eshop -a RetailerCode=tiptop_id".split())