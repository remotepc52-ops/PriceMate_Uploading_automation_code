import json
import time
from lxml import etree
from urllib.parse import quote
import scrapy
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from pricemate.spiders.base_spider import PricemateBaseSpider

cookies = {
    'PHPSESSID': 'ishm8i5r6ln97b0qnsh2kdpc3i',
    '_lscache_vary': '769f74cc97c99ba0a5d9d41eab626853',
    'sbjs_migrations': '1418474375998%3D1',
    'sbjs_current_add': 'fd%3D2025-10-17%2007%3A58%3A55%7C%7C%7Cep%3Dhttps%3A%2F%2Fpetloverscentre.com.ph%2F%7C%7C%7Crf%3Dhttps%3A%2F%2Fpetloverscentre.com.ph%2F',
    'sbjs_first_add': 'fd%3D2025-10-17%2007%3A58%3A55%7C%7C%7Cep%3Dhttps%3A%2F%2Fpetloverscentre.com.ph%2F%7C%7C%7Crf%3Dhttps%3A%2F%2Fpetloverscentre.com.ph%2F',
    'sbjs_current': 'typ%3Dtypein%7C%7C%7Csrc%3D%28direct%29%7C%7C%7Cmdm%3D%28none%29%7C%7C%7Ccmp%3D%28none%29%7C%7C%7Ccnt%3D%28none%29%7C%7C%7Ctrm%3D%28none%29%7C%7C%7Cid%3D%28none%29%7C%7C%7Cplt%3D%28none%29%7C%7C%7Cfmt%3D%28none%29%7C%7C%7Ctct%3D%28none%29',
    'sbjs_first': 'typ%3Dtypein%7C%7C%7Csrc%3D%28direct%29%7C%7C%7Cmdm%3D%28none%29%7C%7C%7Ccmp%3D%28none%29%7C%7C%7Ccnt%3D%28none%29%7C%7C%7Ctrm%3D%28none%29%7C%7C%7Cid%3D%28none%29%7C%7C%7Cplt%3D%28none%29%7C%7C%7Cfmt%3D%28none%29%7C%7C%7Ctct%3D%28none%29',
    'sbjs_udata': 'vst%3D2%7C%7C%7Cuip%3D%28none%29%7C%7C%7Cuag%3DMozilla%2F5.0%20%28Windows%20NT%2010.0%3B%20Win64%3B%20x64%29%20AppleWebKit%2F537.36%20%28KHTML%2C%20like%20Gecko%29%20Chrome%2F141.0.0.0%20Safari%2F537.36',
    'sbjs_session': 'pgs%3D2%7C%7C%7Ccpg%3Dhttps%3A%2F%2Fpetloverscentre.com.ph%2F',
}

headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
    'cache-control': 'max-age=0',
    'priority': 'u=0, i',
    'sec-ch-ua': '"Google Chrome";v="141", "Not?A_Brand";v="8", "Chromium";v="141"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'none',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36',
    # 'cookie': 'PHPSESSID=ishm8i5r6ln97b0qnsh2kdpc3i; _lscache_vary=769f74cc97c99ba0a5d9d41eab626853; sbjs_migrations=1418474375998%3D1; sbjs_current_add=fd%3D2025-10-17%2007%3A58%3A55%7C%7C%7Cep%3Dhttps%3A%2F%2Fpetloverscentre.com.ph%2F%7C%7C%7Crf%3Dhttps%3A%2F%2Fpetloverscentre.com.ph%2F; sbjs_first_add=fd%3D2025-10-17%2007%3A58%3A55%7C%7C%7Cep%3Dhttps%3A%2F%2Fpetloverscentre.com.ph%2F%7C%7C%7Crf%3Dhttps%3A%2F%2Fpetloverscentre.com.ph%2F; sbjs_current=typ%3Dtypein%7C%7C%7Csrc%3D%28direct%29%7C%7C%7Cmdm%3D%28none%29%7C%7C%7Ccmp%3D%28none%29%7C%7C%7Ccnt%3D%28none%29%7C%7C%7Ctrm%3D%28none%29%7C%7C%7Cid%3D%28none%29%7C%7C%7Cplt%3D%28none%29%7C%7C%7Cfmt%3D%28none%29%7C%7C%7Ctct%3D%28none%29; sbjs_first=typ%3Dtypein%7C%7C%7Csrc%3D%28direct%29%7C%7C%7Cmdm%3D%28none%29%7C%7C%7Ccmp%3D%28none%29%7C%7C%7Ccnt%3D%28none%29%7C%7C%7Ctrm%3D%28none%29%7C%7C%7Cid%3D%28none%29%7C%7C%7Cplt%3D%28none%29%7C%7C%7Cfmt%3D%28none%29%7C%7C%7Ctct%3D%28none%29; sbjs_udata=vst%3D2%7C%7C%7Cuip%3D%28none%29%7C%7C%7Cuag%3DMozilla%2F5.0%20%28Windows%20NT%2010.0%3B%20Win64%3B%20x64%29%20AppleWebKit%2F537.36%20%28KHTML%2C%20like%20Gecko%29%20Chrome%2F141.0.0.0%20Safari%2F537.36; sbjs_session=pgs%3D2%7C%7C%7Ccpg%3Dhttps%3A%2F%2Fpetloverscentre.com.ph%2F',
}
class PetCateSpider(PricemateBaseSpider):
    name = "pets_cate"

    def __init__(self, retailer, region, *args, **kwargs):
        super().__init__(retailer=retailer, region=region, *args, **kwargs)

    def start_requests(self):
        url = 'https://petloverscentre.com.ph/'

        yield scrapy.Request(
            url=url,
            cookies=cookies,
            headers=headers,
            callback=self.parse,
            meta={
                'url': url,
                "filename": f"Cate_{self.generate_hash_id(url)}.html",
                "should_be": ["submenu"]
            })

    def parse(self, response):
       #get all category url
        href = response.xpath('//div[@data-id="f5c1549"]/div//li/a/@href').getall()
        for link in href:
            cate_url = f"https://petloverscentre.com.ph{link}"
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
        "scrapy crawl pets_cate -a retailer=petloverscentre-ph -a region=ph -a Type=eshop -a RetailerCode=petloverscentre_ph".split())
