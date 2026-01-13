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
    '_shopify_s': '916ff1ea-28c0-43e7-a5ca-16b5b29d6f83',
    '_ga_F1H7VLWCB9': 'GS2.1.s1758009373$o1$g1$t1758009734$j58$l0$h1709076340',
    '_ga_RCEF0MS1T5': 'GS2.1.s1758009374$o1$g1$t1758009734$j58$l0$h0',
    '_ga': 'GA1.3.1623927627.1758009374',
    '_shopify_essential': ':AZlRhj1oAAEA-Zw_80VP6FT0MgdGADci9PptBaZfxWThW4hIY74cJQQGcvjFfcVDd1nPwMsDop9KIAc-38CA7nwQG5PniSXdPKdRzU_0MavCNZ-YJ5ARsDUg5Ee6ej9eYFNWCnt0iw_XZSJQ07lfnQi7tc7_1NDf7zTqFn1ErHhueFMlcEqKJPrTxjCeez9yYOM:',
    'keep_alive': 'eyJ2IjoyLCJ0cyI6MTc1ODAxMDMwNDQ3OSwiZW52Ijp7IndkIjowLCJ1YSI6MSwiY3YiOjEsImJyIjoxfSwiYmh2Ijp7Im1hIjoxMywiY2EiOjAsImthIjowLCJzYSI6NCwia2JhIjowLCJ0YSI6MCwidCI6NTY5LCJubSI6MSwibXMiOjAuMzgsIm1qIjowLjk5LCJtc3AiOjAuNzYsInZjIjowLCJjcCI6MCwicmMiOjAsImtqIjowLCJraSI6MCwic3MiOjAuNDMsInNqIjowLjM5LCJzc20iOjAuNzUsInNwIjoxLCJ0cyI6MCwidGoiOjAsInRwIjowLCJ0c20iOjB9LCJzZXMiOnsicCI6NSwicyI6MTc1ODAwOTM3MjU0MSwiZCI6OTAzfX0%3D',
}

headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'en-US,en;q=0.9',
    'cache-control': 'max-age=0',
    'if-none-match': '"cacheable:8c755e57f132103a2d9d21a9050404f8"',
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
    # 'cookie': 'localization=PH; _shopify_y=53a3fc3a-a773-4921-ad8c-d474acb20ab6; _tracking_consent=3.AMPS_IDJK_f_f_fBEIQ6JmTKelFYg9jDU6kg; _orig_referrer=; _landing_page=%2F; WISHLIST_TOTAL=0; WISHLIST_PRODUCTS_IDS={}; WISHLIST_PRODUCTS_IDS_SET=1; WISHLIST_UUID=null; WISHLIST_IP_ADDRESS=45.8.25.32; _fbp=fb.2.1758009374874.955357043559420247; _gid=GA1.3.557831823.1758009375; _shopify_s=916ff1ea-28c0-43e7-a5ca-16b5b29d6f83; _ga_F1H7VLWCB9=GS2.1.s1758009373$o1$g1$t1758009734$j58$l0$h1709076340; _ga_RCEF0MS1T5=GS2.1.s1758009374$o1$g1$t1758009734$j58$l0$h0; _ga=GA1.3.1623927627.1758009374; _shopify_essential=:AZlRhj1oAAEA-Zw_80VP6FT0MgdGADci9PptBaZfxWThW4hIY74cJQQGcvjFfcVDd1nPwMsDop9KIAc-38CA7nwQG5PniSXdPKdRzU_0MavCNZ-YJ5ARsDUg5Ee6ej9eYFNWCnt0iw_XZSJQ07lfnQi7tc7_1NDf7zTqFn1ErHhueFMlcEqKJPrTxjCeez9yYOM:; keep_alive=eyJ2IjoyLCJ0cyI6MTc1ODAxMDMwNDQ3OSwiZW52Ijp7IndkIjowLCJ1YSI6MSwiY3YiOjEsImJyIjoxfSwiYmh2Ijp7Im1hIjoxMywiY2EiOjAsImthIjowLCJzYSI6NCwia2JhIjowLCJ0YSI6MCwidCI6NTY5LCJubSI6MSwibXMiOjAuMzgsIm1qIjowLjk5LCJtc3AiOjAuNzYsInZjIjowLCJjcCI6MCwicmMiOjAsImtqIjowLCJraSI6MCwic3MiOjAuNDMsInNqIjowLjM5LCJzc20iOjAuNzUsInNwIjoxLCJ0cyI6MCwidGoiOjAsInRwIjowLCJ0c20iOjB9LCJzZXMiOnsicCI6NSwicyI6MTc1ODAwOTM3MjU0MSwiZCI6OTAzfX0%3D',
}

class PetexpCateSpider(PricemateBaseSpider):
    name = "petexp_cate"

    def __init__(self, retailer, region, *args, **kwargs):
        super().__init__(retailer=retailer, region=region, *args, **kwargs)

    def start_requests(self):
        sitemaps = 'https://www.petexpress.com.ph/sitemap_collections_1.xml?from=183408492675&to=434540839043'

        yield scrapy.Request(
            url=sitemaps,
            cookies=cookies,
            headers=headers,
            callback=self.parse,
            meta={
                'sitemap_url': sitemaps,
                "filename": f"PL_{self.generate_hash_id(sitemaps)}.html",
                "should_be": ["/collections"]
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
    execute("scrapy crawl petexp_cate -a retailer=petexpress-ph -a region=ph -a Type=eshop -a RetailerCode=petexpress_ph".split())