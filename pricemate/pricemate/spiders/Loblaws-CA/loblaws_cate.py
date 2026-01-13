import json
import re
import time

from lxml import etree
from parsel import Selector
from urllib.parse import quote
import scrapy
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from pricemate.spiders.base_spider import PricemateBaseSpider

headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,/;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8,hi;q=0.7',
    'referer': 'https://www.loblaws.ca/sitemap.xml',
    'sec-ch-ua': '"Chromium";v="136", "Google Chrome";v="136", "Not.A/Brand";v="99"',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36',
}


class loblawsCateSpider(PricemateBaseSpider):
    name = "loblaws_cate"

    def __init__(self, retailer, region, *args, **kwargs):
        super().__init__(retailer=retailer, region=region, *args, **kwargs)

    def start_requests(self):
        url = 'https://www.loblaws.ca/sitemap.xml'
        yield scrapy.Request(
            url=url,
            headers=headers,
            callback=self.parse,
            meta={
                'sitemap_url': url,
                "filename": f"PL_{self.generate_hash_id(url)}.html",
                "should_be": ["loc"]
            }

        )

    def parse(self, response):
        sitemap_url = response.meta['sitemap_url']
        namespaces = {'ns': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
        try:
            root = etree.fromstring(response.body)

            loc_elements = root.xpath('//ns:loc', namespaces=namespaces)

            for loc in loc_elements:
                cate_url = loc.text.strip()

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
                print(f"inserted: {cate_url}")

        except Exception as e:
            print(f"Failed to fetch sitemap {sitemap_url}: {e}")

    def close(self, reason):
        self.mongo_client.close()


if __name__ == '__main__':
    from scrapy.cmdline import execute
    execute("scrapy crawl loblaws_cate -a retailer=loblaws-ca -a region=ca -a Type=eshop -a RetailerCode=loblaws_ca".split())