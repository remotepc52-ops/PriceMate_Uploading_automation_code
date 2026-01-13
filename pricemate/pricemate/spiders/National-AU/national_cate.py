from lxml import etree
import scrapy
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from pricemate.spiders.bs_spider import PricemateBaseSpider

cookies = {
    'sbjs_migrations': '1418474375998%3D1',
    'sbjs_current_add': 'fd%3D2025-10-14%2004%3A25%3A35%7C%7C%7Cep%3Dhttps%3A%2F%2Fwww.nationalpharmacies.com.au%2F%7C%7C%7Crf%3D%28none%29',
    'sbjs_first_add': 'fd%3D2025-10-14%2004%3A25%3A35%7C%7C%7Cep%3Dhttps%3A%2F%2Fwww.nationalpharmacies.com.au%2F%7C%7C%7Crf%3D%28none%29',
    'sbjs_current': 'typ%3Dtypein%7C%7C%7Csrc%3D%28direct%29%7C%7C%7Cmdm%3D%28none%29%7C%7C%7Ccmp%3D%28none%29%7C%7C%7Ccnt%3D%28none%29%7C%7C%7Ctrm%3D%28none%29%7C%7C%7Cid%3D%28none%29%7C%7C%7Cplt%3D%28none%29%7C%7C%7Cfmt%3D%28none%29%7C%7C%7Ctct%3D%28none%29',
    'sbjs_first': 'typ%3Dtypein%7C%7C%7Csrc%3D%28direct%29%7C%7C%7Cmdm%3D%28none%29%7C%7C%7Ccmp%3D%28none%29%7C%7C%7Ccnt%3D%28none%29%7C%7C%7Ctrm%3D%28none%29%7C%7C%7Cid%3D%28none%29%7C%7C%7Cplt%3D%28none%29%7C%7C%7Cfmt%3D%28none%29%7C%7C%7Ctct%3D%28none%29',
    'sbjs_udata': 'vst%3D2%7C%7C%7Cuip%3D%28none%29%7C%7C%7Cuag%3DMozilla%2F5.0%20%28Windows%20NT%2010.0%3B%20Win64%3B%20x64%29%20AppleWebKit%2F537.36%20%28KHTML%2C%20like%20Gecko%29%20Chrome%2F141.0.0.0%20Safari%2F537.36',
    'sbjs_session': 'pgs%3D1%7C%7C%7Ccpg%3Dhttps%3A%2F%2Fwww.nationalpharmacies.com.au%2Fproduct%2Foriental-botanicals-curcumin-excel-30-pack%2F',
}

headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
    'cache-control': 'max-age=0',
    'if-modified-since': 'Tue, 14 Oct 2025 09:46:46 GMT',
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
    # 'cookie': 'sbjs_migrations=1418474375998%3D1; sbjs_current_add=fd%3D2025-10-14%2004%3A25%3A35%7C%7C%7Cep%3Dhttps%3A%2F%2Fwww.nationalpharmacies.com.au%2F%7C%7C%7Crf%3D%28none%29; sbjs_first_add=fd%3D2025-10-14%2004%3A25%3A35%7C%7C%7Cep%3Dhttps%3A%2F%2Fwww.nationalpharmacies.com.au%2F%7C%7C%7Crf%3D%28none%29; sbjs_current=typ%3Dtypein%7C%7C%7Csrc%3D%28direct%29%7C%7C%7Cmdm%3D%28none%29%7C%7C%7Ccmp%3D%28none%29%7C%7C%7Ccnt%3D%28none%29%7C%7C%7Ctrm%3D%28none%29%7C%7C%7Cid%3D%28none%29%7C%7C%7Cplt%3D%28none%29%7C%7C%7Cfmt%3D%28none%29%7C%7C%7Ctct%3D%28none%29; sbjs_first=typ%3Dtypein%7C%7C%7Csrc%3D%28direct%29%7C%7C%7Cmdm%3D%28none%29%7C%7C%7Ccmp%3D%28none%29%7C%7C%7Ccnt%3D%28none%29%7C%7C%7Ctrm%3D%28none%29%7C%7C%7Cid%3D%28none%29%7C%7C%7Cplt%3D%28none%29%7C%7C%7Cfmt%3D%28none%29%7C%7C%7Ctct%3D%28none%29; sbjs_udata=vst%3D2%7C%7C%7Cuip%3D%28none%29%7C%7C%7Cuag%3DMozilla%2F5.0%20%28Windows%20NT%2010.0%3B%20Win64%3B%20x64%29%20AppleWebKit%2F537.36%20%28KHTML%2C%20like%20Gecko%29%20Chrome%2F141.0.0.0%20Safari%2F537.36; sbjs_session=pgs%3D1%7C%7C%7Ccpg%3Dhttps%3A%2F%2Fwww.nationalpharmacies.com.au%2Fproduct%2Foriental-botanicals-curcumin-excel-30-pack%2F',
}

class NationalSpider(PricemateBaseSpider):
    name = "national_cate"

    def __init__(self, retailer, region, *args, **kwargs):
        super().__init__(retailer=retailer, region=region, *args, **kwargs)

    def start_requests(self):
        sitemaps = ['https://www.nationalpharmacies.com.au/product-sitemap.xml', 'https://www.nationalpharmacies.com.au/product-sitemap2.xml', 'https://www.nationalpharmacies.com.au/product-sitemap3.xml',
                    'https://www.nationalpharmacies.com.au/product-sitemap4.xml', 'https://www.nationalpharmacies.com.au/product-sitemap5.xml', 'https://www.nationalpharmacies.com.au/product-sitemap6.xml', 'https://www.nationalpharmacies.com.au/product-sitemap7.xml']

        for sitemap_url in sitemaps:
            api_key = "21ed11ef5c872bc7727680a52233027db4578a0e"
            target_url = sitemap_url
            zenrows_url = "https://api.zenrows.com/v1/"

            params = {
                "apikey": api_key,
                "url": target_url,
                "js_render": "true",
                "premium_proxy": "true"
            }
            query = "&".join([f"{k}={v}" for k, v in params.items()])
            full_url = f"{zenrows_url}?{query}"

            yield scrapy.Request(
                url=full_url,
                cookies=cookies,
                headers=headers,
                callback=self.get_pl_data,
                meta={
                'sitemap_url': sitemap_url,
                "filename": f"Cate_{self.generate_hash_id(sitemap_url)}.html",
                "should_be": ["urlset"]
            }

        )

    def get_pl_data(self, response):
        sitemap_url = response.meta['sitemap_url']
        namespaces = {'ns': 'http://www.sitemaps.org/schemas/sitemap/0.9'}

        try:
            parser = etree.XMLParser(recover=True)
            root = etree.fromstring(response.body, parser=parser)

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
    execute("scrapy crawl national_cate -a retailer=nationalpharmacies-au -a region=au -a Type=eshop -a RetailerCode=nationalpharmacies_au".split())