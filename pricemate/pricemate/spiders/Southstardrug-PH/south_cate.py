import json
import time
from lxml import etree
from urllib.parse import quote
import scrapy
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from pricemate.spiders.base_spider import PricemateBaseSpider

cookies = {
    'localization': 'PH',
    '_shopify_y': '39fcce3c-6897-4fcd-9499-0cec4bf7ee53',
    '_shopify_analytics': ':AZsCpUu5AAEA17NwCOOu_A3K8OEEA2wAcTrm-EaRRJsaKG-CaJ2pnBsCnoeTDVBLCMwSeD4GAucRC190GefRdAQOQKrCw03naoodVer7uXfQdlY9AOCpvnl2yFZfWiaSvPl43y9q9dz_IAmS:',
    'WISHLIST_TOTAL': '0',
    'WISHLIST_PRODUCTS_IDS': '{}',
    'WISHLIST_PRODUCTS_IDS_SET': '1',
    'WISHLIST_UUID': 'null',
    'WISHLIST_IP_ADDRESS': '103.108.231.238',
    '_fbp': 'fb.2.1765275954325.529302755572936648',
    '_shopify_s': 'feaed047-e5a7-476f-804d-1b9fcd1a5199',
    '_shopify_essential': ':AZsCpUlMAAEADM2pLG--2d8BlscB-GlENfcwI7tsHL15s83x7jjgN_Dytql7gH_LYjs_10jpfWvIWMiu15Od2ehHftiyR2bhAHN54zwXHC_59A9-eGEGEfsV49QSQrpGZsMQT3IwynY8OXdpK4Iqh5PtRePFsItmx1FXFr5-V_eVe80OWIaStQHzGKhiWXKsaibjTuWjvREu4sLlYbfoNafnU0ojWvrMKWA94MGkc1wMZt6dBsSG9fdOu7wQtFmBGgDSVgwsll009zIgX4mAp95lxvmNTSY8lHg2VPXflvb90zDY72wj09dJToeSxhxgdDGluzsfd9DpDZJCa11Fu_WiBVYxoDlmmI2emCBPmxQKeF7SszkhieBfV04:',
}

headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
    'cache-control': 'max-age=0',
    'if-none-match': '"page_cache:25718849583:SitemapCollectionsController:c50594dd364d9718f6ddba17ef71050a"',
    'priority': 'u=0, i',
    'sec-ch-ua': '"Google Chrome";v="143", "Chromium";v="143", "Not A(Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'none',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36',
    # 'cookie': 'localization=PH; _shopify_y=39fcce3c-6897-4fcd-9499-0cec4bf7ee53; _shopify_analytics=:AZsCpUu5AAEA17NwCOOu_A3K8OEEA2wAcTrm-EaRRJsaKG-CaJ2pnBsCnoeTDVBLCMwSeD4GAucRC190GefRdAQOQKrCw03naoodVer7uXfQdlY9AOCpvnl2yFZfWiaSvPl43y9q9dz_IAmS:; WISHLIST_TOTAL=0; WISHLIST_PRODUCTS_IDS={}; WISHLIST_PRODUCTS_IDS_SET=1; WISHLIST_UUID=null; WISHLIST_IP_ADDRESS=103.108.231.238; _fbp=fb.2.1765275954325.529302755572936648; _shopify_s=feaed047-e5a7-476f-804d-1b9fcd1a5199; _shopify_essential=:AZsCpUlMAAEADM2pLG--2d8BlscB-GlENfcwI7tsHL15s83x7jjgN_Dytql7gH_LYjs_10jpfWvIWMiu15Od2ehHftiyR2bhAHN54zwXHC_59A9-eGEGEfsV49QSQrpGZsMQT3IwynY8OXdpK4Iqh5PtRePFsItmx1FXFr5-V_eVe80OWIaStQHzGKhiWXKsaibjTuWjvREu4sLlYbfoNafnU0ojWvrMKWA94MGkc1wMZt6dBsSG9fdOu7wQtFmBGgDSVgwsll009zIgX4mAp95lxvmNTSY8lHg2VPXflvb90zDY72wj09dJToeSxhxgdDGluzsfd9DpDZJCa11Fu_WiBVYxoDlmmI2emCBPmxQKeF7SszkhieBfV04:',
}

class SouthCateSpider(PricemateBaseSpider):
    name = "south_cate"

    def __init__(self, retailer, region, *args, **kwargs):
        super().__init__(retailer=retailer, region=region, *args, **kwargs)

    def start_requests(self):
        sitemaps = 'https://southstardrug.com.ph/sitemap_collections_1.xml?from=157515612207&to=306386206767'

        yield scrapy.Request(
            url=sitemaps,
            cookies=cookies,
            headers=headers,
            callback=self.parse,
            meta={
                'sitemap_url': sitemaps,
                "filename": f"Cate_{self.generate_hash_id(sitemaps)}.html",
                "should_be": ["url"]
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
                    {"$set": {"url": cate_url, "Status": "Pending", "retailer": self.retailer, "region": self.region}},
                    upsert=True
                )
                print(f"inserted: {cate_url}")

        except Exception as e:
            print(f"Failed to fetch sitemap {sitemap_url}:{e}")



    def close(self, reason):
        self.mongo_client.close()

if __name__ == '__main__':
    from scrapy.cmdline import execute
    execute("scrapy crawl south_cate -a retailer=southstardrug-ph -a region=ph -a Type=eshop -a RetailerCode=southstardrug_ph".split())