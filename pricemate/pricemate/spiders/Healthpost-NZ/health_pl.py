import json
import time
from lxml import etree
from urllib.parse import quote
import scrapy
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from pricemate.spiders.bs_spider import PricemateBaseSpider

cookies = {
    '__cf_bm': 'lk9LNYHwE.1K.7TLS9RWmK2QqKszng5xjNy8FopRrh0-1764745321-1.0.1.1-_9p1S6HABt5RjL_V7.ccLCW11DvhExW7i6dSfbw83xVLVBZXmu5w26mbyvkYQh9q0xO4Fn04yvkv5bUa1Jp67qByZgmpF1_J6rdkW_DE478',
}

headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
    'cache-control': 'max-age=0',
    'priority': 'u=0, i',
    'sec-ch-ua': '"Chromium";v="142", "Google Chrome";v="142", "Not_A Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'none',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36',
    # 'cookie': '__cf_bm=lk9LNYHwE.1K.7TLS9RWmK2QqKszng5xjNy8FopRrh0-1764745321-1.0.1.1-_9p1S6HABt5RjL_V7.ccLCW11DvhExW7i6dSfbw83xVLVBZXmu5w26mbyvkYQh9q0xO4Fn04yvkv5bUa1Jp67qByZgmpF1_J6rdkW_DE478',
}

class HealthPlSpider(PricemateBaseSpider):
    name = "health_pl"

    def __init__(self, retailer, region, *args, **kwargs):
        super().__init__(retailer=retailer, region=region, *args, **kwargs)

    def start_requests(self):
        url = "https://www.healthpost.co.nz/xmlsitemap.php?type=products&page=1"

        current_proxy = '2c6ea6e6d8c14216a62781b8f850cd5b'

        proxy_host = "api.zyte.com"
        proxy_port = "8011"
        proxy_auth = f"{current_proxy}:"

        proxy_url = f"https://{proxy_auth}@{proxy_host}:{proxy_port}"

        yield scrapy.Request(
            url=url,
            cookies=cookies,
            headers=headers,
            callback=self.parse_pl,
            meta={
                "proxy": proxy_url,
                'sitemap_url': url,
                "filename": f"PL_{self.generate_hash_id(url)}.html",
                "should_be": ["loc"]
            }

        )

    def parse_pl(self, response):
        sitemap_url = response.meta['sitemap_url']
        namespaces = {'ns': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
        try:
            root = etree.fromstring(response.body)

            loc_elements = root.xpath('//ns:loc', namespaces=namespaces)

            for loc in loc_elements:
                cate_url = loc.text.strip()
                hash_id = self.generate_hash_id(cate_url, self.retailer, self.region)
                self.product_url.update_one(
                    {"_id": hash_id},
                    {"$set": {"ProductURL": cate_url, "Status": "Pending", "retailer": self.retailer, "region": self.region}},
                    upsert=True
                )
                print(f"inserted: {cate_url}")

        except Exception as e:
            print(f"Failed to fetch sitemap {sitemap_url}:{e}")



    def close(self, reason):
        self.mongo_client.close()

if __name__ == '__main__':
    from scrapy.cmdline import execute
    execute("scrapy crawl health_pl -a retailer=healthpost-nz -a region=nz -a Type=eshop -a RetailerCode=healthpost_nz".split())