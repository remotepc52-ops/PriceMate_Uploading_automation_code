import json
import os, sys
from scrapy.http import JsonRequest
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from pricemate.spiders.base_spider import PricemateBaseSpider

headers = {
    'Accept': '*/*',
    'Accept-Language': 'en',
    'Connection': 'keep-alive',
    'Origin': 'https://www.fairprice.com.sg',
    'Referer': 'https://www.fairprice.com.sg/',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-site',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36',
    'sec-ch-ua': '"Google Chrome";v="143", "Chromium";v="143", "Not A(Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'traceparent': '00-00000000000000007ddcfb73934265ea-6af2bcb409da5fed-01',
    'x-datadog-origin': 'rum',
    'x-datadog-parent-id': '7706429393829781485',
    'x-datadog-sampling-priority': '1',
    'x-datadog-trace-id': '9069400223427749354',
}
class FairpriceCateSpider(PricemateBaseSpider):
    name = "fairprice_cate"

    def __init__(self, retailer, region, *args, **kwargs):
        super().__init__(retailer=retailer, region=region, *args, **kwargs)

    def start_requests(self):
        url = 'https://website-api.omni.fairprice.com.sg/api/nav?storeId=165'
        yield JsonRequest(
            url=url,
            callback=self.parse_json,
            headers=headers,
            meta={
                "filename": f"PL_{self.generate_hash_id(url)}.html",
                "should_be": ["data"],
            }
        )
    def parse_json(self,response):
        data = json.loads(response.body)
        for section in data.get("data", []):
            for menu in section:
                for sub_menu in menu.get("menu", []):
                    for sub_sub_menu in sub_menu.get("menu", []):
                        sub_id = sub_sub_menu.get("id")
                        sub_url = sub_sub_menu.get("url")
                        cate_url = f'https://www.fairprice.com.sg{sub_url}'
                        hash_id = self.generate_hash_id(cate_url, self.retailer, self.region)

                        self.category_input.update_one(
                            {"_id": hash_id},
                            {"$set": {
                                "url": cate_url,
                                "Parent_id": sub_id,
                                "Status": "Pending",
                                "retailer": self.retailer,
                                "region": self.region
                            }},
                            upsert=True
                        )
                        self.logger.info(f"Inserted main category: {cate_url}")

    def close(self, reason):
        self.mongo_client.close()

if __name__ == '__main__':
    from scrapy.cmdline import execute
    execute("scrapy crawl fairprice_cate -a retailer=ntuc-fairprice-sg -a region=sg -a Type=eshop -a RetailerCode=ntuc_fairprice_sg".split())