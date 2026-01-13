import scrapy
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from pricemate.spiders.base_spider import PricemateBaseSpider

headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
    'authorization': 'Token eyJhbGciOiJIUzI1NiJ9.eyJpZCI6MTU0NDIxODgsInR5cGUiOiJndWVzdCIsInNob3AtaWQiOjIxMjQsImlhdCI6MTc2MzQ2MjkwN30.DgdFMjsY634_q98q-2P_KQySdlhvYrH5FAO5OcBqZaE',
    'origin': 'https://www.metromart.com',
    'priority': 'u=1, i',
    'referer': 'https://www.metromart.com/',
    'sec-ch-ua': '"Chromium";v="142", "Google Chrome";v="142", "Not_A Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36',
    'x-client-platform': 'Web',
    'x-powered-by': 'ARM JS Library/2.5.2',
}

class SmHyperCateSpider(PricemateBaseSpider):
    name = "sm_hyper_cate"

    def __init__(self, retailer, region, *args, **kwargs):
        super().__init__(retailer=retailer, region=region, *args, **kwargs)

    def start_requests(self):
        url = 'https://api.metromart.com/api/v2/departments?filter%5Bshop-id%5D=2110&filter%5Bproduct.status%5D=available&fields%5Baisles%5D=name,priority,available-products-count,department&fields%5Bdepartments%5D=name,available-products-count,priority,special,special-text-color,special-background-color,special-on-hover-text-color,special-on-hover-background-color,name-background-color,logo-background-color,image-url,aisles&include=aisles&sort=special%3D%5Btrue%5D,-priority,name'

        yield scrapy.Request(
            url=url,
            # cookies=cookies,
            headers=headers,
            callback=self.get_cate,
            meta={
                'url': url,
                "filename": f"Cate_{self.generate_hash_id(url)}.html",
                "should_be": ["data"]
            }

        )
    def get_cate(self, response):
        json_data = response.json()

        for item in json_data.get("data", []):
            dept_id = item.get("id")
            if dept_id:
                cate_url = f"https://www.metromart.com/shops/sm-hypermarket-north-edsa/departments/{dept_id}"
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
                print(f" ✅ Inserted: {cate_url}")

    def close(self, reason):
        self.mongo_client.close()

if __name__ == '__main__':
    from scrapy.cmdline import execute
    execute("scrapy crawl sm_hyper_cate -a retailer=metromart_sm_hypermarket-ph -a region=ph -a Type=eshop -a RetailerCode=metromart_sm_hypermarket_ph".split())