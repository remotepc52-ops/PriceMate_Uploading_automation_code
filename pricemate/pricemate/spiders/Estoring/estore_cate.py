import json
import time
from lxml import etree
from urllib.parse import quote
import scrapy
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from pricemate.spiders.base_spider import PricemateBaseSpider

cookies = {
    'secure_customer_sig': '',
    'localization': 'MY',
    'cart_currency': 'MYR',
    '_shopify_y': '56AE7C9E-ba43-419A-abe9-6b08d456e1b8',
    '_tracking_consent': '%7B%22con%22%3A%7B%22CMP%22%3A%7B%22a%22%3A%22%22%2C%22m%22%3A%22%22%2C%22p%22%3A%22%22%2C%22s%22%3A%22%22%7D%7D%2C%22v%22%3A%222.1%22%2C%22region%22%3A%22TWTPE%22%2C%22reg%22%3A%22%22%2C%22purposes%22%3A%7B%22a%22%3Atrue%2C%22p%22%3Atrue%2C%22m%22%3Atrue%2C%22t%22%3Atrue%7D%2C%22display_banner%22%3Afalse%2C%22sale_of_data_region%22%3Afalse%2C%22consent_id%22%3A%229AAE9B75-3306-469C-9c1f-9d660de26966%22%7D',
    '_orig_referrer': '',
    '_landing_page': '%2F',
    '_shopify_sa_p': '',
    'WISHLIST_TOTAL': '0',
    'bb_page-9560cac402cb492cb4836e0a_token': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VySWQiOiJiYi1PSHhBRWNHQjhIaWlXZjBJYl9FREkiLCJwYWdlSWQiOiJwYWdlLTk1NjBjYWM0MDJjYjQ5MmNiNDgzNmUwYSIsImJvdElkIjoiYm90LU9WU25Qa3BLdiIsImlhdCI6MTc0ODU5Nzc2NSwiaXNzIjoiYm90Ym9ubmllX3dlYmNoYXQifQ.iZ2_yRGo85NEAxLr5oeUXt4cziXkomJBHCyxczjz8xs',
    'bb_page-9560cac402cb492cb4836e0a_uuid': 'bb-OHxAEcGB8HiiWf0Ib_EDI',
    '_ga': 'GA1.1.1928736646.1748597766',
    '_ttp': '01JWG8RXSJKS8DWNRX467PQYK2_.tt.0',
    'WISHLIST_PRODUCTS_IDS': '{}',
    'WISHLIST_PRODUCTS_IDS_SET': '1',
    'WISHLIST_UUID': 'null',
    'WISHLIST_IP_ADDRESS': '192.253.210.19',
    '_fbp': 'fb.1.1748597766424.536586331276264203',
    '_shopify_s': '9AC45B22-55b3-46EB-b7ee-f108c321afad',
    '_shopify_sa_t': '2025-05-30T09%3A36%3A16.108Z',
    'ttcsid_D0LFVTBC77U3MP4V0FT0': '1748597765944::N7kcwwQhR3uYDtFXpCxZ.1.1748597778163',
    'ttcsid': '1748597765945::c2BRbeDF5VpgNz1_sXVm.1.1748597778225',
    'keep_alive': 'eyJ2IjoyLCJ0cyI6MTc0ODU5Nzc4ODA5NCwiZW52Ijp7IndkIjowLCJ1YSI6MSwiY3YiOjEsImJyIjoxfSwiYmh2Ijp7Im1hIjo1LCJjYSI6MCwia2EiOjAsInNhIjowLCJ0YSI6MCwia2JhIjowLCJ0IjoxMSwibm0iOjEsIm1zIjowLCJtaiI6MC4zMSwibXNwIjowLjcyLCJ2YyI6MCwiY3AiOjAsInJjIjowLCJraiI6MCwia2kiOjAsInNzIjowLCJzaiI6MCwic3NtIjowLCJzcCI6MCwidHMiOjAsInRqIjowLCJ0cCI6MCwidHNtIjowfSwic2VzIjp7InAiOjIsInMiOjE3NDg1OTc3NjQ2NTgsImQiOjIyfX0%3D',
    '_ga_H9K4E9PVHJ': 'GS2.1.s1748597765$o1$g1$t1748597789$j36$l0$h0',
    '_ga_VECPQBDPS0': 'GS2.1.s1748597765$o1$g1$t1748597789$j36$l0$h0',
    'mp_d7f79c10b89f9fa3026f2fb08d3cf36d_mixpanel': '%7B%22distinct_id%22%3A%20%22%24device%3A197208c73bc17bc-080f90da6e3ab7-26011f51-144000-197208c73bc17bc%22%2C%22%24device_id%22%3A%20%22197208c73bc17bc-080f90da6e3ab7-26011f51-144000-197208c73bc17bc%22%2C%22%24initial_referrer%22%3A%20%22%24direct%22%2C%22%24initial_referring_domain%22%3A%20%22%24direct%22%7D',
}

headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8,hi;q=0.7',
    'cache-control': 'max-age=0',
    'if-none-match': '"cacheable:a2809b4af32dea40ba9eea1c4b638007"',
    'priority': 'u=0, i',
    'sec-ch-ua': '"Chromium";v="136", "Google Chrome";v="136", "Not.A/Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'none',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36',
}


class EstoreCateSpider(PricemateBaseSpider):
    name = "estore_cate"

    def __init__(self, retailer, region, *args, **kwargs):
        super().__init__(retailer=retailer, region=region, *args, **kwargs)

    def start_requests(self):
        sitemaps = [
            'https://estore.caring2u.com/sitemap_products_1.xml?from=9787108098368&to=9787970945344',
            'https://estore.caring2u.com/sitemap_products_2.xml?from=9787970978112&to=9788851257664',
            'https://estore.caring2u.com/sitemap_products_3.xml?from=9788851421504&to=9794274001216'
        ]
        for url in sitemaps:
            current_proxy = '2c6ea6e6d8c14216a62781b8f850cd5b'

            proxy_host = "api.zyte.com"
            proxy_port = "8011"
            proxy_auth = f"{current_proxy}:"

            proxy_url = f"https://{proxy_auth}@{proxy_host}:{proxy_port}"

            yield scrapy.Request(
                url=url,
                cookies=cookies,
                headers=headers,
                callback=self.parse,
                meta={
                    "proxy": proxy_url,
                    'sitemap_url': url,
                    "filename": f"PL_{self.generate_hash_id(url)}.html",
                    "should_be": ["/products"]
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
    execute("scrapy crawl estore_cate -a retailer=caring-my -a region=my -a Type=eshop -a RetailerCode=caring_my".split())