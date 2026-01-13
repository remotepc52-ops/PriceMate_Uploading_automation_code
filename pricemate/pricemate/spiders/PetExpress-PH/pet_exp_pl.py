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
    '_shopify_y': '53a3fc3a-a773-4921-ad8c-d474acb20ab6',
    '_tracking_consent': '3.AMPS_IDJK_f_f_fBEIQ6JmTKelFYg9jDU6kg',
    '_orig_referrer': '',
    '_landing_page': '%2F',
    'WISHLIST_TOTAL': '0',
    'WISHLIST_PRODUCTS_IDS': '{}',
    'WISHLIST_PRODUCTS_IDS_SET': '1',
    'WISHLIST_UUID': 'null',
    'WISHLIST_IP_ADDRESS': '45.8.25.32',
    '_fbp': 'fb.2.1758009374874.955357043559420247',
    '_gid': 'GA1.3.557831823.1758009375',
    '_gat_gtag_UA_164243679_1': '1',
    '_shopify_essential': ':AZlRhj1oAAEAT828ix4BIFPVEVlIS9pssvl09AqPgsKMhCcNTlhfwhf5lma213qUPLmuZONw6IhtFDZaYN7iz4hpwPb9-DdZtSgyigNlRRycujXdfVG4uU0JwpLz1JXXuv9kfOkFK6cuLz1vuN9RUB56M88Ab0yD4Lmq8KYNbQjokPG3Hw4xfOh1zCj3O5pppQ:',
    '_shopify_s': '51bacfc7-9B5A-4EE4-517D-7895310ED976',
    '_ga_F1H7VLWCB9': 'GS2.1.s1758009373$o1$g1$t1758012825$j54$l0$h1709076340',
    '_ga_RCEF0MS1T5': 'GS2.1.s1758012822$o2$g1$t1758012825$j57$l0$h0',
    '_ga': 'GA1.1.1623927627.1758009374',
    'keep_alive': 'eyJ2IjoyLCJ0cyI6MTc1ODAxMjg2MDQyOCwiZW52Ijp7IndkIjowLCJ1YSI6MSwiY3YiOjEsImJyIjoxfSwiYmh2Ijp7Im1hIjo3NSwiY2EiOjAsImthIjowLCJzYSI6MzYsImtiYSI6MCwidGEiOjAsInQiOjM1LCJubSI6MSwibXMiOjAuMzgsIm1qIjowLjU4LCJtc3AiOjAuMzcsInZjIjowLCJjcCI6MCwicmMiOjAsImtqIjowLCJraSI6MCwic3MiOjAuNDYsInNqIjowLjYzLCJzc20iOjAuOTQsInNwIjozLCJ0cyI6MCwidGoiOjAsInRwIjowLCJ0c20iOjB9LCJzZXMiOnsicCI6NywicyI6MTc1ODAwOTM3MjU0MSwiZCI6MzQ1N319',
}

headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'en-US,en;q=0.9',
    'cache-control': 'max-age=0',
    'if-none-match': '"cacheable:52431619284a6e73e531847549209fc4"',
    'priority': 'u=0, i',
    'sec-ch-ua': '"Chromium";v="140", "Not=A?Brand";v="24", "Google Chrome";v="140"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'none',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36',
}

class PetexpPlSpider(PricemateBaseSpider):
    name = "petexp_pl"

    def __init__(self, retailer, region, *args, **kwargs):
        super().__init__(retailer=retailer, region=region, *args, **kwargs)

    def start_requests(self):
        docs = self.category_input.find({
            "retailer": self.retailer,
            "region": self.region,
            "Status": "Pending"
        })
        for doc in docs:
            url = doc["url"]
            hash_id = doc.get("_id")
            slug = url.split("collections/")[-1].split("/")[0]
            meta = {
                "proxy": "http://21ed11ef5c872bc7727680a52233027db4578a0e:@api.zenrows.com:8001",
                "url": url,
                "_id": hash_id,
                "slug":slug,
                "page": 1,
                "filename": f"{slug}_page.html",
                "should_be": ["product-item__info-inner"]
            }
            yield scrapy.Request(
                url,
                cookies=cookies,
                headers=headers,
                callback=self.parse_pl,
                meta=meta,
                dont_filter=True
            )

    def parse_pl(self, response):
        meta = response.meta
        doc_id = meta.get("_id")
        slug = meta.get("slug")
        page = int(meta.get("page", 1))
        links = response.xpath('//div[@class="product-item__info-inner"]/a[@class="product-item__title text--strong link"]/@href').getall()

        for link in links:
            pdp_url = f'https://www.petexpress.com.ph{link}'
            product_hash = self.generate_hash_id(pdp_url, self.retailer, self.region)
            item = {
                "_id": product_hash,
                "ProductURL": pdp_url,
                "Status": "Pending",
                "retailer": self.retailer,
                "region": self.region,
            }
            self.save_product(item)
            print("✅ Inserted")

        next_page = response.xpath('//a[contains(@class,"pagination__next")]/@href').get()
        if next_page:
            next_page_num = page + 1
            next_page_url = f'https://www.petexpress.com.ph{next_page}'
            yield response.follow(next_page_url, callback=self.parse_pl, meta={
                "url": next_page_url,
                "_id": doc_id,
                "page": next_page_num,
                "filename": f"{slug}_{page}page.html",
                "should_be": ["product-item__info-inner"]
            })
            self.category_input.update_one(
                {"_id": doc_id},
                {"$set": {"Status": "Done"}}
            )
            self.logger.info(f"Product URL: {pdp_url}")

    def close(self, reason):
        self.mongo_client.close()

if __name__ == '__main__':
    from scrapy.cmdline import execute
    execute("scrapy crawl petexp_pl -a retailer=petexpress-ph -a region=ph -a Type=eshop -a RetailerCode=petexpress_ph".split())