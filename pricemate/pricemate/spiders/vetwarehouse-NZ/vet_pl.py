import json
import time
from lxml import etree
from urllib.parse import quote
import scrapy
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from pricemate.spiders.base_spider import PricemateBaseSpider

cookies = {
    'breakdance_session_count': '1',
    'sbjs_migrations': '1418474375998%3D1',
    'sbjs_current_add': 'fd%3D2025-12-08%2009%3A01%3A47%7C%7C%7Cep%3Dhttps%3A%2F%2Fvetwarehouse.co.nz%2F%7C%7C%7Crf%3D%28none%29',
    'sbjs_first_add': 'fd%3D2025-12-08%2009%3A01%3A47%7C%7C%7Cep%3Dhttps%3A%2F%2Fvetwarehouse.co.nz%2F%7C%7C%7Crf%3D%28none%29',
    'sbjs_current': 'typ%3Dtypein%7C%7C%7Csrc%3D%28direct%29%7C%7C%7Cmdm%3D%28none%29%7C%7C%7Ccmp%3D%28none%29%7C%7C%7Ccnt%3D%28none%29%7C%7C%7Cid%3D%28none%29%7C%7C%7Ctrm%3D%28none%29%7C%7C%7Cmtke%3D%28none%29',
    'sbjs_first': 'typ%3Dtypein%7C%7C%7Csrc%3D%28direct%29%7C%7C%7Cmdm%3D%28none%29%7C%7C%7Ccmp%3D%28none%29%7C%7C%7Ccnt%3D%28none%29%7C%7C%7Cid%3D%28none%29%7C%7C%7Ctrm%3D%28none%29%7C%7C%7Cmtke%3D%28none%29',
    'sbjs_udata': 'vst%3D1%7C%7C%7Cuip%3D%28none%29%7C%7C%7Cuag%3DMozilla%2F5.0%20%28Windows%20NT%2010.0%3B%20Win64%3B%20x64%29%20AppleWebKit%2F537.36%20%28KHTML%2C%20like%20Gecko%29%20Chrome%2F142.0.0.0%20Safari%2F537.36',
    'mtk_src_trk': '%7B%22type%22%3A%22typein%22%2C%22url%22%3A%22(none)%22%2C%22mtke%22%3A%22(none)%22%2C%22utm_campaign%22%3A%22(none)%22%2C%22utm_source%22%3A%22(direct)%22%2C%22utm_medium%22%3A%22(none)%22%2C%22utm_content%22%3A%22(none)%22%2C%22utm_id%22%3A%22(none)%22%2C%22utm_term%22%3A%22(none)%22%2C%22session_entry%22%3A%22https%3A%2F%2Fvetwarehouse.co.nz%2F%22%2C%22session_start_time%22%3A%222025-12-08%2009%3A01%3A47%22%2C%22session_pages%22%3A%221%22%2C%22session_count%22%3A%221%22%7D',
    '_fbp': 'fb.2.1765186311243.958253617538888820',
    'breakdance_view_count': '1',
    'sbjs_session': 'pgs%3D4%7C%7C%7Ccpg%3Dhttps%3A%2F%2Fvetwarehouse.co.nz%2Fshop-all%2F',
    'PHPSESSID': 'ktr4k5802qugr8amj61c0mkqf9',
    'breakdance_last_session_id': 'ktr4k5802qugr8amj61c0mkqf9',
}

headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
    'cache-control': 'max-age=0',
    'priority': 'u=0, i',
    'referer': 'https://vetwarehouse.co.nz/sitemaps.xml',
    'sec-ch-ua': '"Chromium";v="142", "Google Chrome";v="142", "Not_A Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36',
    # 'cookie': 'breakdance_session_count=1; sbjs_migrations=1418474375998%3D1; sbjs_current_add=fd%3D2025-12-08%2009%3A01%3A47%7C%7C%7Cep%3Dhttps%3A%2F%2Fvetwarehouse.co.nz%2F%7C%7C%7Crf%3D%28none%29; sbjs_first_add=fd%3D2025-12-08%2009%3A01%3A47%7C%7C%7Cep%3Dhttps%3A%2F%2Fvetwarehouse.co.nz%2F%7C%7C%7Crf%3D%28none%29; sbjs_current=typ%3Dtypein%7C%7C%7Csrc%3D%28direct%29%7C%7C%7Cmdm%3D%28none%29%7C%7C%7Ccmp%3D%28none%29%7C%7C%7Ccnt%3D%28none%29%7C%7C%7Cid%3D%28none%29%7C%7C%7Ctrm%3D%28none%29%7C%7C%7Cmtke%3D%28none%29; sbjs_first=typ%3Dtypein%7C%7C%7Csrc%3D%28direct%29%7C%7C%7Cmdm%3D%28none%29%7C%7C%7Ccmp%3D%28none%29%7C%7C%7Ccnt%3D%28none%29%7C%7C%7Cid%3D%28none%29%7C%7C%7Ctrm%3D%28none%29%7C%7C%7Cmtke%3D%28none%29; sbjs_udata=vst%3D1%7C%7C%7Cuip%3D%28none%29%7C%7C%7Cuag%3DMozilla%2F5.0%20%28Windows%20NT%2010.0%3B%20Win64%3B%20x64%29%20AppleWebKit%2F537.36%20%28KHTML%2C%20like%20Gecko%29%20Chrome%2F142.0.0.0%20Safari%2F537.36; mtk_src_trk=%7B%22type%22%3A%22typein%22%2C%22url%22%3A%22(none)%22%2C%22mtke%22%3A%22(none)%22%2C%22utm_campaign%22%3A%22(none)%22%2C%22utm_source%22%3A%22(direct)%22%2C%22utm_medium%22%3A%22(none)%22%2C%22utm_content%22%3A%22(none)%22%2C%22utm_id%22%3A%22(none)%22%2C%22utm_term%22%3A%22(none)%22%2C%22session_entry%22%3A%22https%3A%2F%2Fvetwarehouse.co.nz%2F%22%2C%22session_start_time%22%3A%222025-12-08%2009%3A01%3A47%22%2C%22session_pages%22%3A%221%22%2C%22session_count%22%3A%221%22%7D; _fbp=fb.2.1765186311243.958253617538888820; breakdance_view_count=1; sbjs_session=pgs%3D4%7C%7C%7Ccpg%3Dhttps%3A%2F%2Fvetwarehouse.co.nz%2Fshop-all%2F; PHPSESSID=ktr4k5802qugr8amj61c0mkqf9; breakdance_last_session_id=ktr4k5802qugr8amj61c0mkqf9',
}

class VetPlSpider(PricemateBaseSpider):
    name = "vet_pl"

    def __init__(self, retailer, region, *args, **kwargs):
        super().__init__(retailer=retailer, region=region, *args, **kwargs)

    def start_requests(self):
        docs = self.category_input.find({
            # "retailer": self.retailer,
            # "region": self.region,
            "Status": "Pending"
        })

        for doc in docs:
            url = doc["url"]
            hash_id = doc.get("_id")

            yield scrapy.Request(
            url=url,
            cookies=cookies,
            headers=headers,
            callback=self.parse,
            meta={
                'sitemap_url': sitemaps,
                "filename": f"Cate_{self.generate_hash_id(sitemaps)}.html",
                "should_be": ["item-loc"]
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
                self.product_table.update_one(
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
    execute("scrapy crawl vet_pl -a retailer=vetwarehouse-nz -a region=nz -a Type=eshop -a RetailerCode=vetwarehouse_nz".split())