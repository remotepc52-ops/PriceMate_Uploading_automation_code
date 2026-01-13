import json
import time
from urllib.parse import quote
import scrapy
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from pricemate.spiders.base_spider import PricemateBaseSpider


headers = {
    'accept': '*/*',
    'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
    'if-none-match': 'W/"93e8wyhxilvdl"',
    'priority': 'u=1, i',
    'referer': 'https://www.igashop.com.au/',
    'sec-ch-ua': '"Chromium";v="140", "Not=A?Brand";v="24", "Google Chrome";v="140"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'Host': 'www.igashop.com.au',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36',
    'x-shopping-mode': '11111111-1111-1111-1111-111111111111',
    'cookie': '__Host-next-auth.csrf-token=38a15933127e72be77d848f427c49f73915fec239c51247c6083ca4a43bcd4bd%7C1947995151322d16d531d5e0f4feb49e9b9e0d726c0cc69dab16b35621bf125f; __Secure-next-auth.callback-url=https%3A%2F%2Fwww.igashop.com.au',
}


class IgaCateSpider(PricemateBaseSpider):
    name = "iga_cate"

    def __init__(self, retailer, region, *args, **kwargs):
        super().__init__(retailer=retailer, region=region, *args, **kwargs)

    def start_requests(self):
        url = f'https://www.igashop.com.au/api/storefront/stores/32600/categoryHierarchy'

        yield scrapy.Request(
            url=url,
            # cookies=cookies,
            headers=headers,
            callback=self.get_cate,
            meta={
                "filename": f"PL_{self.generate_hash_id(url)}.html",
                "should_be": ["children"]
            }

        )

    def get_cate(self, response):
        if response.status != 200:
            self.logger.warning(f"Skipping non-200 response ({response.status}) for {response.url}")
            return
        try:
            data = response.json()
        except Exception as e:
            self.logger.error(f"JSON decode failed for {response.url}: {e}")
            return
        for parent in data.get("children", []):  # 1st level
            parent_name = parent.get("identifier")
            for child in parent.get("children", []):  # 2nd level
                sub_name = child.get("identifier")
                sub = quote(sub_name)
                for grandchild in child.get("children", []):  # 3rd level
                    thirdCategory = grandchild.get("identifier")
                    third = quote(thirdCategory)
                    cate_url = f'https://www.igashop.com.au/categories/{sub}/{third}/1'
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
    execute("scrapy crawl iga_cate -a retailer=iga-au -a region=au -a Type=eshop -a RetailerCode=iga_au".split())