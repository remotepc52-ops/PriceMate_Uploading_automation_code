import json
import re
import time
from parsel import Selector
from urllib.parse import quote
import scrapy
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from pricemate.spiders.base_spider_me import PricemateBaseSpider

cookies = {
    '_I_': '79d867b6c9cbec73a70ebe4d9ab3a9833986e6bf54fcdd0aeaad36507c39b183-1763873352',
    'SSESS511a7bcc5c76b391214fee9f12fa0d7b': 'jZmstdAA-CdHhiv27uccP-tLNOUEwldSqpVJsZI-MTc',
    '_fbp': 'fb.2.1763873361984.424601933995042391',
    'prism_799653711': '0743f156-d3ce-4b7a-9d0c-5f3825cc5fcf',
}

headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
    'cache-control': 'max-age=0',
    'priority': 'u=0, i',
    'referer': 'https://www.wizardpharmacy.com.au/products-category/category/hair-accessories',
    'sec-ch-ua': '"Chromium";v="142", "Google Chrome";v="142", "Not_A Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36',
    # 'cookie': '_I_=79d867b6c9cbec73a70ebe4d9ab3a9833986e6bf54fcdd0aeaad36507c39b183-1763873352; SSESS511a7bcc5c76b391214fee9f12fa0d7b=jZmstdAA-CdHhiv27uccP-tLNOUEwldSqpVJsZI-MTc; _fbp=fb.2.1763873361984.424601933995042391; prism_799653711=0743f156-d3ce-4b7a-9d0c-5f3825cc5fcf',
}

class MainPlSpider(PricemateBaseSpider):
    name = "wiz_pl"

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
            slug = url.split("/")[-1]

            current_proxy = '2c6ea6e6d8c14216a62781b8f850cd5b'

            proxy_host = "api.zyte.com"
            proxy_port = "8011"
            proxy_auth = f"{current_proxy}:"

            proxy_url = f"https://{proxy_auth}@{proxy_host}:{proxy_port}"

            meta = {
                "proxy": proxy_url,
                "url": url,
                "_id": hash_id,
                "slug": slug,
                "page": 0,
                "filename": f"PL_{slug}_page.html",
                "should_be": ["description"]
            }
            yield scrapy.Request(
                url,
                cookies=cookies,
                headers=headers,
                callback=self.parse_pl,
                meta=meta
            )


    def parse_pl(self, response):
        meta = response.meta
        doc_id = meta.get("_id")
        slug = meta.get("slug")

        href = response.xpath('//div[@class="product-name"]/a/@href').getall()
        for link in href:
            pdp_url = f"https://www.wizardpharmacy.com.au{link}"
            product_hash = self.generate_hash_id(pdp_url, self.retailer, self.region)

            item = {
                "_id": product_hash,
                "ProductURL": pdp_url,
                "Status": "Pending",
                "retailer": self.retailer,
                "region": self.region,
            }
            # self.save_product(item)
            self.save_url(item)
            print("Inserted : ", pdp_url)
        current_page = int(response.xpath('//ul[@class="pagination"]/li[@class="active"]/span/text()').get(default='1'))
        last_page_href = response.xpath('//ul[@class="pagination"]/li[@class="pager-last"]/a/@href').get()

        if last_page_href:
            match = re.search(r'page=(\d+)', last_page_href)
            if match:
                last_page_num = int(match.group(1))

                if current_page < last_page_num:
                    next_page = current_page + 1
                    next_url = re.sub(r'page=\d+', f'page={next_page}', response.url)

                    # Handle URL if there's no page param on first page
                    if 'page=' not in response.url:
                        if '?' in response.url:
                            next_url = response.url + f"&page={next_page}"
                        else:
                            next_url = response.url + f"?page={next_page}"
                    current_proxy = '2c6ea6e6d8c14216a62781b8f850cd5b'

                    proxy_host = "api.zyte.com"
                    proxy_port = "8011"
                    proxy_auth = f"{current_proxy}:"

                    proxy_url = f"https://{proxy_auth}@{proxy_host}:{proxy_port}"

                    meta = {
                        "url": next_url,
                        "page": next_page,
                        "slug": slug,
                        "proxy": proxy_url,
                        "filename": f"PL_{slug}_{next_page}_page.html",
                        "should_be": ["product-name"]
                    }
                    yield scrapy.Request(
                        url=next_url,
                        cookies=cookies,
                        headers=headers,
                        callback=self.parse_pl,
                        meta=meta
                    )
        self.category_input.update_one(
                        {"_id": doc_id},
                        {"$set": {"Status": "Done"}}
                    )



    def close(self, reason):
        self.mongo_client.close()

if __name__ == '__main__':
    from scrapy.cmdline import execute
    execute("scrapy crawl wiz_pl -a retailer=wizardpharmacy-au -a region=au -a Type=eshop -a RetailerCode=wizardpharmacy_au".split())