# import json
# import re
# import time
#
# from lxml import etree
# from parsel import Selector
# from urllib.parse import quote
# import scrapy
# import os, sys
# sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# from PriceMate_Master.spiders.base_spider import PricemateBaseSpider
#
# headers = {
#     'Accept': 'application/json, text/plain, */*',
#     'Accept-Language': 'en',
#     'Business-User-Agent': 'PCXWEB',
#     'Connection': 'keep-alive',
#     'Content-Type': 'application/json',
#     'Origin': 'https://www.loblaws.ca',
#     'Referer': 'https://www.loblaws.ca/',
#     'Sec-Fetch-Dest': 'empty',
#     'Sec-Fetch-Mode': 'cors',
#     'Sec-Fetch-Site': 'cross-site',
#     'Site-Banner': 'loblaw',
#     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36',
#     'baseSiteId': 'loblaw',
#     'is-helios-account': 'false',
#     'is-iceberg-enabled': 'true',
#     'sec-ch-ua': '"Not)A;Brand";v="8", "Chromium";v="138", "Google Chrome";v="138"',
#     'sec-ch-ua-mobile': '?0',
#     'sec-ch-ua-platform': '"Windows"',
#     'x-apikey': 'C1xujSegT5j3ap3yexJjqhOfELwGKYvz',
#     'x-application-type': 'web',
#     'x-channel': 'web',
#     'x-loblaw-tenant-id': 'ONLINE_GROCERIES',
#     'x-preview': 'false',
# }
#
#
#
# class loblawsPlSpider(PricemateBaseSpider):
#     name = "loblaws_pl"
#
#     def start_requests(self):
#
#         def __init__(self, retailer, region, *args, **kwargs):
#             super().__init__(retailer=retailer, region=region, *args, **kwargs)
#
#         def start_requests(self):
#             docs = self.category_input.find({
#                 "retailer": self.retailer,
#                 "region": self.region,
#                 "Status": "Pending"
#             })
#
#             for doc in docs:
#                 url = doc["url"]
#                 hash_id = doc.get("_id")
#
#                 match = re.search(r"/supermarket/([^/]+)/category", url)
#
#                 slug = match.group(1)
#
#                 meta = {
#                 "url": url,
#                 "_id": hash_id,
#                 "slug": slug,
#                 "filename": f"{slug}_page.html",
#                 "should_be": ["row mt-3"]
#             }
#             yield scrapy.Request(
#                 url,
#                 cookies=cookies,
#                 headers=headers,
#                 callback=self.parse_pl,
#                 meta=meta
#             )
#
#
#     def process_category(self, response):
#         referer_url = response.meta["url"]
#         doc_id = response.meta["doc_id"]
#         category_id = referer_url.split("?")[0].split("/")[-1]
#         navdid = referer_url.split("?")[-1].split("=")[-1]
#         page = response.meta.get("page")
#         next_page = response.meta["page"] + 1
#         new_url = f'https://api.pcexpress.ca/pcx-bff/api/v2/listingPage/{category_id}'
#
#         json_data = {
#             'cart': {
#                 'cartId': 'c6830696-9148-4f22-b581-403589e510d1',
#             },
#             'userData': {
#                 'domainUserId': 'd00c7890-8ba7-4235-938c-7810ae9cf84c',
#                 'sessionId': '7d436375-eebc-481e-aaa9-d2b16b54f4a7',
#             },
#             'fulfillmentInfo': {
#                 'offerType': 'OG',
#                 'storeId': '7309',
#                 'pickupType': 'STORE',
#                 'date': '18082025',
#                 'timeSlot': None,
#             },
#             'banner': 'loblaw',
#             'listingInfo': {
#                 'filters': {
#                     'navid': [
#                         f'{navdid}',
#                     ],
#                 },
#                 'sort': {},
#                 'pagination': {
#                     'from': next_page,
#                 },
#                 'includeFiltersInResponse': True,
#             },
#             'device': {
#                 'screenSize': 1366,
#             },
#         }
#
#         try:
#             yield JsonRequest(
#                 url=new_url,
#                 callback=self.parse_json,
#                 headers=headers,
#                 data = json_data,
#                 meta={
#                 "doc_id": doc_id,
#                 "category_id": category_id,
#                 "page": page,
#                 "referer_url": referer_url
#             }
#             )
#         except Exception as e:
#             print(f"Data not Found {e}")
#     def parse_json(self, response):
#         cate_id = response.meta["category_id"]
#         doc_id = response.meta["doc_id"]
#         page = response.meta["page"]
#         data = response.json()
#         products = []
#         for comp in data.get("layout", {}).get("sections", {}).get("mainContentCollection", {}).get("components", []):
#             comp_data = comp.get("data", {})
#             if "productTiles" in comp_data:
#                 products.extend(comp_data["productTiles"])
#         if not products:
#             self.logger.warning(f"No products found in {response.url}")
#             return
#         for product in products:
#             product_urls = product.get("link")
#             product_id = product.get("productId")
#
#             Items = {"ProductUrl": f'https://www.loblaws.ca{product_urls}', "ParentCode": cate_id, "ProductCode": product_id,
#                      }
#
#
#             try:
#                 main_data_url.insert_one(Items)
#                 search_data.update_one(
#                     {"_id": doc_id},
#                     {"$set": {"Status": "Done"}}
#                 )
#                 print(f"Upserted: {product_urls}")
#             except Exception as e:
#                 print(f"Failed to upsert {product_urls}: {e}")
#
#
# if __name__ == '__main__':
#     from scrapy.cmdline import execute
#     execute("scrapy crawl loblaws_pl -a retailer=loblaws -a region=ca".split())