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

cookies = {
    'PHPSESSID': 'boqq88cq2pk3m8fkicko1jv7la',
    'YII_CSRF_TOKEN': '069f2bbd43e82e7a2d977d3872bc2a8356358651s%3A40%3A%223acbcbd6a9283e4f45c2e376ef830feae6d6b503%22%3B',
    '_gid': 'GA1.2.1019380953.1757395459',
    '_tt_enable_cookie': '1',
    '_ttp': '01K4PEX7G2JS0X17VHGY3XTA0N_.tt.1',
    'appFloatingAppButton1015': '1',
    '_ga_B1X2VHE3TK': 'GS2.1.s1757395459$o1$g1$t1757395659$j32$l0$h0',
    '_ga': 'GA1.1.1093648019.1757395459',
    'ttcsid': '1757395459602::2K8L7fHOxASipaqN6zs7.1.1757395659623',
    'ttcsid_D0O31FBC77U7M2KJ8VJ0': '1757395459601::v-X-QKzokT-d0QIuN_5R.1.1757395659869',
}

headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'en-US,en;q=0.9',
    'cache-control': 'max-age=0',
    'priority': 'u=0, i',
    'referer': 'https://www.k24klik.com/',
    'sec-ch-ua': '"Chromium";v="140", "Not=A?Brand";v="24", "Google Chrome";v="140"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36',
    # 'cookie': 'PHPSESSID=boqq88cq2pk3m8fkicko1jv7la; YII_CSRF_TOKEN=069f2bbd43e82e7a2d977d3872bc2a8356358651s%3A40%3A%223acbcbd6a9283e4f45c2e376ef830feae6d6b503%22%3B; _gid=GA1.2.1019380953.1757395459; _tt_enable_cookie=1; _ttp=01K4PEX7G2JS0X17VHGY3XTA0N_.tt.1; appFloatingAppButton1015=1; _ga_B1X2VHE3TK=GS2.1.s1757395459$o1$g1$t1757395659$j32$l0$h0; _ga=GA1.1.1093648019.1757395459; ttcsid=1757395459602::2K8L7fHOxASipaqN6zs7.1.1757395659623; ttcsid_D0O31FBC77U7M2KJ8VJ0=1757395459601::v-X-QKzokT-d0QIuN_5R.1.1757395659869',
}
class KlikCateSpider(PricemateBaseSpider):
    name = "klik_cate"

    def __init__(self, retailer, region, *args, **kwargs):
        super().__init__(retailer=retailer, region=region, *args, **kwargs)

    # def start_requests(self):
    #     url = 'https://www.k24klik.com/kategori'
    #
    #     yield scrapy.Request(
    #         url=url,
    #         cookies=cookies,
    #         headers=headers,
    #         callback=self.parse,
    #         meta={
    #             "filename": f"Cate_{self.generate_hash_id(url)}.html",
    #             "should_be": ["all-menu-page"],
    #         })
    # def parse(self,response):
    #     cate = response.xpath('//div[@class="all-menu-page"]//div[@class="uk-width-1-4 uk-container-center kategori"]/a/@href').getall()
    #     for cate_url in cate:
    #
    #         hash_id = self.generate_hash_id(cate_url, self.retailer, self.region)
    #         self.category_input.update_one(
    #             {"_id": hash_id},
    #             {"$set": {"url": cate_url, "Status": "Pending", "retailer": self.retailer, "region": self.region}},
    #             upsert=True
    #         )
    #         print(f"inserted: {cate_url}")

    def start_requests(self):
        url = 'https://www.k24klik.com/sitemap.xml'
        yield scrapy.Request(
            url=url,
            cookies=cookies,
            headers=headers,
            callback=self.parse,
            meta={
                'sitemap_url': url,
                "filename": f"PL_{self.generate_hash_id(url)}.html",
                "should_be": ["/p/"]
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
                if "/p/" not in cate_url:
                    continue

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

    execute("scrapy crawl klik_cate -a retailer=k24klik-id -a region=id -a Type=eshop -a RetailerCode=k24klik_id".split())