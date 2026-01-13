import re
from typing import Iterable, Any

import scrapy
import time
from urllib.parse import urljoin
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from pricemate.spiders.base_spider import PricemateBaseSpider



cookies = {
    'superweb-locale': 'en',
    'pickUpStoreId': '',
    'shipmentType': '1',
    'venderId': '5',
    'longitude': '114.1249695',
    'latitude': '22.3433916',
    'store': '642',
    '_fbp': 'fb.1.1755837532803.578329380108000599',
    'ec-pixel-config': 'JTdCJTIyc2hvcElkJTIyJTNBbnVsbCUyQyUyMnNob3BQbGF0Zm9ybSUyMiUzQSUyMm93bnNpdGUlMjIlMkMlMjJ0ZWFtJTIyJTNBJTIyTWFya2V0JTIwUGxhY2UlMjIlMkMlMjJlY2lkJTIyJTNBJTIyNmJjNjY2NTQtMGIxOC00ZTljLTk5MzUtOWI1YTMzMGRhYzM2JTIyJTJDJTIyZW5hYmxlUGl4ZWwlMjIlM0F0cnVlJTJDJTIydHhMaW5rVHJhY2tpbmdMaWZldGltZSUyMiUzQTMwJTdE',
    'ec-token': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc0Fub255bW91cyI6InRydWUiLCJyb2xlIjowLCJ0IjoiTWFya2V0IFBsYWNlIiwiZCI6Imt0NkN5NnBoNUw2dWRLY1lDRVhSbnF6eEhscy9zZnZNOUF6ZEFHYU5pZmM9IiwiZSI6Imt0NkN5NnBoNUw2dWRLY1lDRVhSbnBYb3hjeGpRMUQ3MGxQNkZ0RjNsakI1K1hqQlRxVlRKYTRDa3RkYVgwM0J4SE4yYW5MT0RlMFpta3VmS3FCTFRnPT0iLCJpc0FkbWluIjoiZmFsc2UiLCJzc28iOiJmYWxzZSJ9.-dDEaY1IFeMvPjON2Z5Yv7GW9DnMlCH2wEX6Qo2x0Rs',
    '_ga': 'GA1.1.1079108034.1755837538',
    '_ga_C2J4GHSH66': 'GS2.1.s1755837537$o1$g1$t1755839840$j60$l0$h0',
}

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Language': 'en-US,en;q=0.9',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-User': '?1',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36',
    'sec-ch-ua': '"Not;A=Brand";v="99", "Google Chrome";v="139", "Chromium";v="139"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
}

class MarketCateSpider(PricemateBaseSpider):
    name = "market_cate"

    def __init__(self, retailer, region, *args, **kwargs):
        super().__init__(retailer=retailer, region=region, *args, **kwargs)

    def start_requests(self):
        url = 'https://www.marketplacehk.com/en'
        yield scrapy.Request(
            url=url,
            cookies=cookies,
            headers=headers,
            callback=self.parse,
            meta={
                "filename": f"PL_{self.generate_hash_id(url)}.html",
                "should_be": ["cascader-menu-4983-0-0"]
            }

        )

    def parse(self, response):
        menu_items = response.xpath('.//div[@class="cascader__content"]//a/@href').getall()
        for menu in menu_items:
            # urls = menu.xpath('.//a/@href').getall()
            url = f'https://www.marketplacehk.com/en{menu}'
            # for url in all_urls:
            hash_id = self.generate_hash_id(url, self.retailer, self.region)
            self.category_input.update_one(
                {"_id": hash_id},
                {"$set": {"url": url, "Status": "Pending", "retailer": self.retailer, "region": self.region}},
                upsert=True
            )

        # Start crawling this category
            yield scrapy.Request(
            url,
            headers=headers,
            callback=self.parse_category_page,
            meta={
                "category_url": url,
                "category_id": hash_id,
                "page": 1,
                "filename": f"PL_{hash_id}_page_1.html",
                # "should_be": ["card "]
            }
        )

        self.logger.info(f"Found {len(url)} category URLs")

    def parse_category_page(self, response):
        meta = response.meta
        category_url = meta["category_url"]
        match = re.search(r"/category/(\d+)/", category_url)
        parent_id = match.group(1) if match else ""
        category_id = meta["category_id"]
        page = meta["page"]

        pdp_urls = response.xpath('//div[@class="ware-wrapper"]/a/@href').getall()

        # check before looping
        if not pdp_urls:
            self.logger.info(f"No more products on page {page} for {category_url}")
            self.update_category_status(category_id, "Done")
            return

        for link in pdp_urls:
            pdp_url = f'https://www.marketplacehk.com{link}'
            product_hash = self.generate_hash_id(pdp_url, self.retailer, self.region)

            item = {
                "_id": product_hash,
                "ProductURL": pdp_url,
                "Parent_id":parent_id,
                "Status": "Pending",
                "retailer": self.retailer,
                "region": self.region,
                "category_url": category_url
            }
            self.save_product(item)

        self.logger.info(f"Page {page}: Collected {len(pdp_urls)} product URLs from {category_url}")

        next_page = response.xpath('//a[contains(@class,"next")]/@href').get()
        if next_page:
            yield scrapy.Request(
                url=response.urljoin(next_page),
                callback=self.parse_category_page,
                cookies=cookies,
                headers=headers,
                meta={
                    "category_url": category_url,
                    "category_id": category_id,
                    "page": page + 1,
                    "filename": f"PL_{category_id}_page_{page + 1}.html",
                    # "should_be": ["card "]
                }
            )
        else:
            self.update_category_status(category_id, "Done")

    def close(self, reason):
        self.mongo_client.close()

if __name__ == '__main__':
    from scrapy.cmdline import execute
    execute("scrapy crawl market_cate -a retailer=marketplace-hk -a region=hk -a Type=eshop -a RetailerCode=marketplace_hk".split())