import json
import time
from lxml import etree
from urllib.parse import quote
import scrapy
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from pricemate.spiders.base_spider_me import PricemateBaseSpider

cookies = {
    '_fbp': 'fb.2.1760340417954.774740630627335305',
    'prism_799653711': '1c43409d-98b7-49f8-a742-d3a04ebfc02a',
    '_gcl_au': '1.1.1387298492.1761317519',
    '_ga': 'GA1.1.1661461026.1761317520',
    '_hjSessionUser_6367077': 'eyJpZCI6ImE5NTdjMzRmLWYyOGYtNWYyNC04ZmNiLWIwZDdiNjY3MWRlNiIsImNyZWF0ZWQiOjE3NjEzMTc1MjAxODcsImV4aXN0aW5nIjp0cnVlfQ==',
    '_tt_enable_cookie': '1',
    '_ttp': '01K8BB94YQWCPV7K25NW0P0AKV_.tt.2',
    '_ga_4YWY5WMQG5': 'GS2.1.s1761317519$o1$g1$t1761317593$j59$l0$h0',
    '_uetvid': 'ff9d4ab0b0e811f09f96818830d9e534',
    'ttcsid': '1761317524445::HqVGWRXi6HkTk6NKEwC4.1.1761317596649.0',
    'ttcsid_CAPB05BC77UFDAKTC3IG': '1761317524444::CGfTYRAT_GKD3DjblmUi.1.1761317596649.0',
    '_I_': 'de0c8efb6b752e6b5580e6ea80c0e055aea86a8285c7a6bdbcde6db0b9cb720d-1762755068',
    'SSESS511a7bcc5c76b391214fee9f12fa0d7b': 'QZUFj2YVoFSg_w9EEbm4uoKqQilaJF3ijAx7VAUFESg',
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
    # 'cookie': '_fbp=fb.2.1760340417954.774740630627335305; prism_799653711=1c43409d-98b7-49f8-a742-d3a04ebfc02a; _gcl_au=1.1.1387298492.1761317519; _ga=GA1.1.1661461026.1761317520; _hjSessionUser_6367077=eyJpZCI6ImE5NTdjMzRmLWYyOGYtNWYyNC04ZmNiLWIwZDdiNjY3MWRlNiIsImNyZWF0ZWQiOjE3NjEzMTc1MjAxODcsImV4aXN0aW5nIjp0cnVlfQ==; _tt_enable_cookie=1; _ttp=01K8BB94YQWCPV7K25NW0P0AKV_.tt.2; _ga_4YWY5WMQG5=GS2.1.s1761317519$o1$g1$t1761317593$j59$l0$h0; _uetvid=ff9d4ab0b0e811f09f96818830d9e534; ttcsid=1761317524445::HqVGWRXi6HkTk6NKEwC4.1.1761317596649.0; ttcsid_CAPB05BC77UFDAKTC3IG=1761317524444::CGfTYRAT_GKD3DjblmUi.1.1761317596649.0; _I_=de0c8efb6b752e6b5580e6ea80c0e055aea86a8285c7a6bdbcde6db0b9cb720d-1762755068; SSESS511a7bcc5c76b391214fee9f12fa0d7b=QZUFj2YVoFSg_w9EEbm4uoKqQilaJF3ijAx7VAUFESg',
}


class MainCateSpider(PricemateBaseSpider):
    name = "wiz_cate"

    def __init__(self, retailer, region, *args, **kwargs):
        super().__init__(retailer=retailer, region=region, *args, **kwargs)

    def start_requests(self):
        url = 'https://www.wizardpharmacy.com.au/allcategories'

        yield scrapy.Request(
            url=url,
            cookies=cookies,
            headers=headers,
            callback=self.parse,
            meta={
                'url': url,
                "filename": f"Cate_{self.generate_hash_id(url)}.html",
                "should_be": ["all-categories"]
            }

        )

    def parse(self, response):
       #get all category url
        href = response.xpath('//div[@class="all-categories"]//li/a/@href').getall()
        for link in href:
            cate_url = f"https://www.wizardpharmacy.com.au{link}"
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
            print("Inserted URL:", cate_url)




    def close(self, reason):
        self.mongo_client.close()

if __name__ == '__main__':
    from scrapy.cmdline import execute
    execute(
        "scrapy crawl wiz_cate -a retailer=wizardpharmacy-au -a region=au -a Type=eshop -a RetailerCode=wizardpharmacy_au".split())
