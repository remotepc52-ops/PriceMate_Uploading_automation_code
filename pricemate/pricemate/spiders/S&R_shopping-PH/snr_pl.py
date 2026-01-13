import json
import time
from lxml import etree
from urllib.parse import quote
import scrapy
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from pricemate.spiders.base_spider import PricemateBaseSpider

cookies = {
    '_fbp': 'fb.1.1759835619244.418966476792689519',
    'useOfCookieNotice': 'true',
    'XSRF-TOKEN': 'eyJpdiI6IlFFRVBYaXdcL1wvamFVaXRGUE8xRk1JZz09IiwidmFsdWUiOiJCdXA2VlwvVjZoTnhzNllJUkhwNUlrYUdwOW1EdUQwTVgyTjN4NUpxT204ZFQ2REhPaGFkMTh0YU1sUzRzVmVabSIsIm1hYyI6IjBmZjBiZmQyNzcwNDZjNTgxNTVjYTZlNmI2OTY0ZjdiZTg0NDZlNDk1Y2QzYzFkZTc5NDg4M2ZjYTQxNmMwODAifQ%3D%3D',
    'laravel_session': 'eyJpdiI6ImZOSXRSdGc4YmlBWWRCaU5LcUtKOGc9PSIsInZhbHVlIjoiRDhseTQ0N3hidldjbU96a2JFVkJHRmE4ZG1yeUE2UU1uSG1Vc1hrTUNzXC9BM2NPeFhYNWl6THdremtUZmZTelEiLCJtYWMiOiI1OTU2MjUxNGJkYmJhNDBiYzA5OTYwYTMzODMxYWI1ODlmYmUzMDA2ZjUwZjM3Njc5OTg5MGRiOWNmZDFmOGVhIn0%3D',
}

headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
    'cache-control': 'max-age=0',
    'priority': 'u=0, i',
    'referer': 'https://www.snrshopping.com/category/shop-all-categories/wines-liquor-1/beer-1',
    'sec-ch-ua': '"Chromium";v="140", "Not=A?Brand";v="24", "Google Chrome";v="140"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36',
    # 'cookie': '_fbp=fb.1.1759835619244.418966476792689519; useOfCookieNotice=true; XSRF-TOKEN=eyJpdiI6IlFFRVBYaXdcL1wvamFVaXRGUE8xRk1JZz09IiwidmFsdWUiOiJCdXA2VlwvVjZoTnhzNllJUkhwNUlrYUdwOW1EdUQwTVgyTjN4NUpxT204ZFQ2REhPaGFkMTh0YU1sUzRzVmVabSIsIm1hYyI6IjBmZjBiZmQyNzcwNDZjNTgxNTVjYTZlNmI2OTY0ZjdiZTg0NDZlNDk1Y2QzYzFkZTc5NDg4M2ZjYTQxNmMwODAifQ%3D%3D; laravel_session=eyJpdiI6ImZOSXRSdGc4YmlBWWRCaU5LcUtKOGc9PSIsInZhbHVlIjoiRDhseTQ0N3hidldjbU96a2JFVkJHRmE4ZG1yeUE2UU1uSG1Vc1hrTUNzXC9BM2NPeFhYNWl6THdremtUZmZTelEiLCJtYWMiOiI1OTU2MjUxNGJkYmJhNDBiYzA5OTYwYTMzODMxYWI1ODlmYmUzMDA2ZjUwZjM3Njc5OTg5MGRiOWNmZDFmOGVhIn0%3D',
}


class SnrPlSpider(PricemateBaseSpider):
    name = "snr_pl"

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
            slug = url.split("/")[-1].split("/")[0]
            current_proxy = '2c6ea6e6d8c14216a62781b8f850cd5b'

            proxy_host = "api.zyte.com"
            proxy_port = "8011"
            proxy_auth = f"{current_proxy}:"

            proxy_url = f"https://{proxy_auth}@{proxy_host}:{proxy_port}"

            meta = {
                'proxy': proxy_url,
                "url": url,
                "_id": hash_id,
                "slug": slug,
                "page": 1,
                "filename": f"{slug}_page.html",
                "should_be": ["img-event"]
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
        cate_url = meta.get("url")
        doc_id = meta.get("_id")
        slug = meta.get("slug")
        page = int(meta.get("page", 1))
        links = response.xpath('//div[@class="img-event"]/a/@href').getall()

        for link in links:
            pdp_url = f'https://www.snrshopping.com{link}'
            product_hash = self.generate_hash_id(pdp_url, self.retailer, self.region)
            item = {
                "_id": product_hash,
                "ProductURL": pdp_url,
                "Status": "Pending",
                "retailer": self.retailer,
                "region": self.region,
            }
            self.save_product(item)
            print("✅ Inserted -> ", pdp_url)
        next_page_url = response.xpath('//a[@rel="next"]/@href').get()

        if next_page_url:
            parsed_url = next_page_url.split('page=')[-1]
            next_page_num = int(parsed_url) if parsed_url.isdigit() else page + 1

            yield response.follow(next_page_url, callback=self.parse_pl, meta={
                "url": response.urljoin(next_page_url),
                "_id": doc_id,
                "page": next_page_num,
                "filename": f"{slug}_{next_page_num}page.html",
                "should_be": ["img-event"]
            })
        self.category_input.update_one(
            {"_id": doc_id},
            {"$set": {"Status": "Done"}}
        )
        print("Going to next page...")

    def close(self, reason):
        self.mongo_client.close()

if __name__ == '__main__':
    from scrapy.cmdline import execute
    execute("scrapy crawl snr_pl -a retailer=snrshopping-ph -a region=ph -a Type=eshop -a RetailerCode=snrshopping_ph".split())