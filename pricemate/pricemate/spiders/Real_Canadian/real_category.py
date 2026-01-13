# import re
# from typing import Iterable, Any
# from lxml import etree
# import scrapy
# import time
# from urllib.parse import urljoin
# import os, sys
#
# from scrapy.http import JsonRequest
#
# sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# from PriceMate_Master.spiders.base_spider import PricemateBaseSpider
#
# cookies = {
#     "NEXT_LOCALE": "en",
#     "lcl_lang_pref": "en",
#     "banner": "superstore",
#     "banner-client": "superstore"
# }
#
# headers = {
#     "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
#     "Accept-Language": "en-US,en;q=0.9",
#     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36",
# }
#
# class RealCateSpider(PricemateBaseSpider):
#     name = "real_cate"
#
#     def __init__(self, retailer, region, *args, **kwargs):
#         super().__init__(retailer=retailer, region=region, *args, **kwargs)
#
#     def start_requests(self):
#         urls = ["https://www.realcanadiansuperstore.ca/en/sitemap.xml"]
#
#         for url in urls:
#             yield scrapy.Request(
#                 url=url,
#                 headers=headers,
#                 callback=self.parse,
#                 meta={
#                     "filename": f"PL_{self.generate_hash_id(url)}.html",
#                     # "should_be": ["cascader-menu-4983-0-0"]
#                 }
#
#             )
#     def parse(self, response):
#
#         namespaces = {'ns': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
#         root = etree.fromstring(response.body)
#
#         loc_elements = root.xpath('//ns:loc', namespaces=namespaces)
#
#         for loc in loc_elements:
#             url = loc.text.strip()
#             hash_id = self.generate_hash_id(url, self.retailer, self.region)
#             self.category_input.update_one(
#                 {"_id": hash_id},
#                 {"$set": {"url": url, "Status": "Pending", "retailer": self.retailer, "region": self.region}},
#                 upsert=True
#             )
#             print(f"inserted: {url}")
#
#             # Start crawling this category
#             yield scrapy.Request(
#                 url,
#                 headers=headers,
#                 cookies=cookies,
#                 callback=self.parse_category_page,
#                 meta={
#                     "category_url": url,
#                     "category_id": hash_id,
#                     "page": 1,
#                     "filename": f"PL_{hash_id}_page_1.html",
#                     # "should_be": ["card "]
#                 }
#             )
#
#         self.logger.info(f"Found {len(url)} category URLs")
#
#     def parse_category_page(self, response):
#         meta = response.meta
#         category_url = meta["category_url"]
#         cate_id = category_url.split("?")[0].split("/")[-1]
#         category_id = meta["category_id"]
#         page = meta["page"]
#
#         pdp_url = response.xpath('//div[@class="css-qoklea"]//a[@class="chakra-linkbox__overlay css-1hnz6hu"]/@href').get()
#         if not pdp_url:
#             self.logger.info(f"No more products on page {page} for {category_url}")
#             self.update_category_status(category_id, "Done")
#             return
#         for pdp_urls in pdp_url:
#             product_hash = self.generate_hash_id(pdp_urls, self.retailer, self.region)
#
#             item = {
#             "_id": product_hash,
#             "ProductURL": f'https://www.realcanadiansuperstore.ca{pdp_url}',
#             "Parent_id": cate_id,
#             "Status": "Pending",
#             "retailer": self.retailer,
#             "region": self.region,
#             "category_url": category_url
#             }
#             self.save_product(item)
#         self.logger.info(f"Page {page}: Collected {len(pdp_url)} product URLs from {category_url}")
#
#         next_page = response.xpath('//div[@aria-label="Pagination"]//a[contains(text(), "Next")]/@href').get()
#
#         if next_page:
#             yield scrapy.Request(
#                 url=urljoin(response.url, next_page),
#                 callback=self.parse_category_page,
#                 meta={
#                     "category_url": category_url,
#                     "category_id": category_id,
#                     "page": page + 1
#                 }
#             )
#         else:
#             self.update_category_status(category_id, "Done")
#
#     def close(self, reason):
#         self.mongo_client.close()
#
#
# if __name__ == '__main__':
#     from scrapy.cmdline import execute
#     execute("scrapy crawl real_cate -a retailer=realcanadian -a region=ca".split())

import re
from typing import Iterable, Any
from lxml import etree
import scrapy
from urllib.parse import urljoin, urlsplit, urlunsplit
import os, sys

from scrapy.http import JsonRequest

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from pricemate.spiders.base_spider import PricemateBaseSpider


cookies = {
    "NEXT_LOCALE": "en",
    "lcl_lang_pref": "en",
    "banner": "superstore",
    "banner-client": "superstore",
    # if you rely on store selection, add it here, e.g.:
    # "auto_store_selected": "1530",
}

headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36",
}

CATEGORY_RE = re.compile(
    r"^https://www\.realcanadiansuperstore\.ca/en/(?:.+/c/\d+|collection/[^/?#]+)(?:\?.*)?$"
)

class RealCateSpider(PricemateBaseSpider):
    name = "real_cate"

    def __init__(self, retailer, region, *args, **kwargs):
        super().__init__(retailer=retailer, region=region, *args, **kwargs)

    # ---------- helpers ----------
    def to_en(self, url: str) -> str:
        # normalize any /fr/ path to /en/
        return url.replace("://www.realcanadiansuperstore.ca/fr/", "://www.realcanadiansuperstore.ca/en/")

    def is_category_url(self, url: str) -> bool:
        return bool(CATEGORY_RE.match(url))

    def _cate_id_from_url(self, url: str) -> str:
        # works for .../c/28223 and for .../collection/grilling
        path = urlsplit(url).path.rstrip("/")
        last = path.split("/")[-1]
        return last

    # ---------- spider ----------
    def start_requests(self):
        start = "https://www.realcanadiansuperstore.ca/en/sitemap.xml"
        yield scrapy.Request(
            url=start,
            headers=headers,
            cookies=cookies,
            callback=self.parse_sitemap,
            meta={"depth": 0, "filename": f"PL_{self.generate_hash_id(start)}.html",
                "should_be": ["loc"]},
        )

    def parse_sitemap(self, response):
        """
        Handles both <sitemapindex> and <urlset>. Recurses into nested .xml sitemaps.
        Filters to EN category/collection pages only before scheduling.
        """
        ns = {'ns': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
        try:
            root = etree.fromstring(response.body)
        except Exception as e:
            self.logger.warning(f"Failed to parse sitemap XML at {response.url}: {e}")
            return

        locs = [t.strip() for t in root.xpath('//ns:loc/text()', namespaces=ns)]
        scheduled = 0

        for loc in locs:
            loc = self.to_en(loc)

            if loc.endswith(".xml"):
                # recurse into child sitemap
                yield scrapy.Request(
                    url=loc,
                    headers=headers,
                    cookies=cookies,
                    callback=self.parse_sitemap,
                    meta={"depth": response.meta.get("depth", 0) + 1,"filename": f"PL_{self.generate_hash_id(loc)}.html",
                "should_be": ["loc"]},
                )
                continue

            if not self.is_category_url(loc):
                # skip non-category URLs (legal pages, homepage, store locators, etc.)
                continue

            hash_id = self.generate_hash_id(loc, self.retailer, self.region)
            self.category_input.update_one(
                {"_id": hash_id},
                {"$set": {"url": loc, "Status": "Pending", "retailer": self.retailer, "region": self.region}},
                upsert=True,
            )

            yield scrapy.Request(
                url=loc,
                headers=headers,
                cookies=cookies,
                callback=self.parse_category_page,
                meta={
                    "category_url": loc,
                    "category_id": hash_id,
                    "page": 1,
                    "filename": f"PL_{self.generate_hash_id(loc)}.html",
                    "should_be": ["loc"]
                },
            )
            scheduled += 1

        self.logger.info(f"[sitemap] {response.url} → scheduled {scheduled} category URLs")

    def parse_category_page(self, response):
        meta = response.meta
        category_url = meta["category_url"]
        cate_id = category_url.split("?")[0].split("/")[-1]
        category_id = meta["category_id"]
        page = meta["page"]

        pdp_urls = response.xpath(
            '//div[@class="css-qoklea"]//a[@class="chakra-linkbox__overlay css-1hnz6hu"]/@href'
        ).getall()

        if not pdp_urls:
            self.logger.info(f"No more products on page {page} for {category_url}")
            self.update_category_status(category_id, "Done")
            return

        unique_urls = set(pdp_urls)  # remove duplicates

        for pdp_url in unique_urls:
            product_hash = self.generate_hash_id(pdp_url, self.retailer, self.region)

            item = {
                "_id": product_hash,
                "ProductURL": f'https://www.realcanadiansuperstore.ca{pdp_url}',
                "ParentCode": cate_id,
                "Status": "Pending",
                "retailer": self.retailer,
                "region": self.region,
                "category_url": category_url
            }
            self.save_product(item)

        self.logger.info(f"Page {page}: Collected {len(unique_urls)} unique product URLs from {category_url}")

        next_page = response.xpath('//div[@aria-label="Pagination"]//a[contains(text(), "Next")]/@href').get()
        if next_page:
            yield scrapy.Request(
                url=urljoin(response.url, next_page),
                callback=self.parse_category_page,
                meta={
                    "category_url": category_url,
                    "category_id": category_id,
                    "page": page + 1,
                    "filename": f"{cate_id}_{next_page}_page.html",
                    "should_be": ["data"]
                }
            )
        else:
            self.update_category_status(category_id, "Done")

    def close(self, reason):
        self.mongo_client.close()


if __name__ == '__main__':
    from scrapy.cmdline import execute
    execute("scrapy crawl real_cate -a retailer=realcanadian-ca -a region=ca -a Type=eshop -a RetailerCode=REALCANADIAN-CA".split())
