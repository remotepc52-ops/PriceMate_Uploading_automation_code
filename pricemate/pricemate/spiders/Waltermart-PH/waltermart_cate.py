import json
import time
from lxml import etree
from urllib.parse import quote
import scrapy
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from pricemate.spiders.base_spider import PricemateBaseSpider

headers = {
    'accept': 'application/json, text/javascript, */*; q=0.01',
    'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
    'origin': 'https://www.waltermartdelivery.com.ph',
    'priority': 'u=1, i',
    'referer': 'https://www.waltermartdelivery.com.ph/shop',
    'sec-ch-ua': '"Google Chrome";v="141", "Not?A_Brand";v="8", "Chromium";v="141"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'cross-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36',
}

class WaltermartCateSpider(PricemateBaseSpider):
    name = "walter_cate"

    def __init__(self, retailer, region, *args, **kwargs):
        super().__init__(retailer=retailer, region=region, *args, **kwargs)

    def start_requests(self):
        url = 'https://api.freshop.ncrcloud.com/1/products?app_key=walter_mart&department_id_cascade=true&include_departments=true&limit=0&render_id=1760597578445&store_id=2038&token=c0fd243769fa2b504f7794a6437efda4'

        yield scrapy.Request(
            url,
            # cookies=cookies,
            headers=headers,
            callback=self.get_cate,
            meta={
                'url': url,
                "filename": f"Cate_{self.generate_hash_id(url)}.html",
                "should_be": ["departments"]
            }
        )
    def get_cate(self, response):

        data = json.loads(response.text)
        for dept in data['departments']:
            url = dept.get('canonical_url')
            if url:
                cate_url = url
                hash_id = self.generate_hash_id(cate_url, self.retailer, self.region)
                self.category_input.update_one(
                    {"_id": hash_id},
                    {"$set": {"url": cate_url, "Status": "Pending", "retailer": self.retailer, "region": self.region}},
                    upsert=True
                )
                print(f"inserted: {cate_url}")


    def close(self, reason):
        self.mongo_client.close()

if __name__ == '__main__':
    from scrapy.cmdline import execute
    execute(
        "scrapy crawl walter_cate -a retailer=waltermart-ph -a region=ph -a Type=eshop -a RetailerCode=waltermart_ph".split())