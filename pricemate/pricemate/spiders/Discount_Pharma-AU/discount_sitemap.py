import json
import time
from lxml import etree
from urllib.parse import quote
import scrapy
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from pricemate.spiders.base_spider import PricemateBaseSpider

cookies = {
    '_lscache_vary': '4e2d753d1a511fdc17ed08e4377c544c',
    '_fbp': 'fb.2.1760337978781.930606449728821423',
    'widget_prefix': 'sigma',
    'PHPSESSID': 'f80df3351ae43c5e50bca75d56e6f250',
    '__stripe_mid': 'fd95a6c2-2ee5-453e-89de-d049b63cfa6f5bf33a',
    '__stripe_sid': '0acd15fd-8b51-4b8c-9a15-829d81296a5f00da57',
    'guest_id': '14411850',
    'guest_session_id': '6Ywxxl4gzGypTO0xmrjhFmJItrcjI5HiraitTRPo',
    'cart_session_id': '6Ywxxl4gzGypTO0xmrjhFmJItrcjI5HiraitTRPo',
    'sf_recently_viewed': '%5B%7B%22drug%22%3A%22Swisse%20Ultiboost%20High%20Strength%20Magnesium%20Powder%20Orange%20%20%20180g%22%2C%22drugcode%22%3A%22MMC-O100022428%22%2C%22PhotoID_s3%22%3A%22https%3A%2F%2Ffile.medmate.com.au%2Fcatalouge%2F13373386915870.jpg%22%2C%22slug%22%3A%22swisse-ultiboost-high-strength-magnesium-powder-orange-180g%22%7D%2C%7B%22drug%22%3A%22Nutricia%20Souvenaid%20Memory%20Drink%20Vanilla%20%20%204%20x%20125mL%22%2C%22drugcode%22%3A%22MMC-O100021455%22%2C%22PhotoID_s3%22%3A%22https%3A%2F%2Ffile.medmate.com.au%2Fcatalouge%2F13377138098206.jpg%22%2C%22slug%22%3A%22nutricia-souvenaid-memory-drink-vanilla-4-x-125ml%22%7D%5D',
}

headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
    'cache-control': 'max-age=0',
    'priority': 'u=0, i',
    'referer': 'https://www.discountdrugstores.com.au/sitemap_index.xml',
    'sec-ch-ua': '"Google Chrome";v="141", "Not?A_Brand";v="8", "Chromium";v="141"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36',
    # 'cookie': '_lscache_vary=4e2d753d1a511fdc17ed08e4377c544c; _fbp=fb.2.1760337978781.930606449728821423; widget_prefix=sigma; PHPSESSID=f80df3351ae43c5e50bca75d56e6f250; __stripe_mid=fd95a6c2-2ee5-453e-89de-d049b63cfa6f5bf33a; __stripe_sid=0acd15fd-8b51-4b8c-9a15-829d81296a5f00da57; guest_id=14411850; guest_session_id=6Ywxxl4gzGypTO0xmrjhFmJItrcjI5HiraitTRPo; cart_session_id=6Ywxxl4gzGypTO0xmrjhFmJItrcjI5HiraitTRPo; sf_recently_viewed=%5B%7B%22drug%22%3A%22Swisse%20Ultiboost%20High%20Strength%20Magnesium%20Powder%20Orange%20%20%20180g%22%2C%22drugcode%22%3A%22MMC-O100022428%22%2C%22PhotoID_s3%22%3A%22https%3A%2F%2Ffile.medmate.com.au%2Fcatalouge%2F13373386915870.jpg%22%2C%22slug%22%3A%22swisse-ultiboost-high-strength-magnesium-powder-orange-180g%22%7D%2C%7B%22drug%22%3A%22Nutricia%20Souvenaid%20Memory%20Drink%20Vanilla%20%20%204%20x%20125mL%22%2C%22drugcode%22%3A%22MMC-O100021455%22%2C%22PhotoID_s3%22%3A%22https%3A%2F%2Ffile.medmate.com.au%2Fcatalouge%2F13377138098206.jpg%22%2C%22slug%22%3A%22nutricia-souvenaid-memory-drink-vanilla-4-x-125ml%22%7D%5D',
}

class DiscountSpider(PricemateBaseSpider):
    name = "discount_cate"

    def __init__(self, retailer, region, *args, **kwargs):
        super().__init__(retailer=retailer, region=region, *args, **kwargs)

    def start_requests(self):
        sitemaps = 'https://www.discountdrugstores.com.au/shop-category-sitemap.xml'

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
    execute("scrapy crawl discount_cate -a retailer=discount_drug-au -a region=au -a Type=eshop -a RetailerCode=discount_drug_au".split())