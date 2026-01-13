# import json
# import time
# from lxml import etree
# from urllib.parse import quote
# import scrapy
# import os, sys
# sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# from pricemate.spiders.base_spider import PricemateBaseSpider
#
# cookies = {
#     'SF-CSRF-TOKEN': 'c947a7b1-5681-4e71-aecd-144fa942af43',
#     'fornax_anonymousId': '157f2d86-3cf3-4898-a2e3-eb3c068ee12e',
#     'SHOP_SESSION_TOKEN': '39c26e5e-c265-4505-baec-258536533acb',
#     '_shg_user_id': '06a669e4-6eca-4658-8a81-a13fe99549ce',
#     'lantern': '85bb5da5-0fee-4b35-a6d1-1e4b942afd3d',
#     'STORE_VISITOR': '1',
#     'XSRF-TOKEN': 'b91d40cc992f92408f24a9902bb127f07b9429bcc8dbec4a47e4ed4a976383f0',
#     '_fbp': 'fb.2.1762776350457.48384813880456306',
#     'viewPosts[limit]': '12',
#     '__cf_bm': 'yAZJ2pS7F.1ZqFi20denAd6cur5s36jg0F.kqxa2OYs-1762845612-1.0.1.1-sUhuV_Qj6GUnW.xOvdQiPqTWwOnOB.Rjcf3bBdMsvNAV1_33AzcboP3nyENmxC_7EjUbAdOL9t4ijmFKpC1o5K10xJ68H_JSbuL.X32wuME',
#     'athena_short_visit_id': '3e2071c6-0129-4891-94d3-ce764102ac85:1762845613',
#     '_shg_session_id': '2fc38c13-d3c1-44b7-9e1b-5b2e18a388e6',
#     'lastVisitedCategory': '2163',
#     'ssUserId': 'c2a0a14c-00bd-43d4-b6eb-08f1d28802b7',
#     'ssSessionId': 'f03240bb-8700-42cd-8648-9dc67d48f85a',
#     'Shopper-Pref': '6FCFA1D9FB8C9CE005241C0DAD12F3A47D65C5D6-1763450658064-x%7B%22cur%22%3A%22SGD%22%2C%22funcConsent%22%3Atrue%7D',
# }
#
# headers = {
#     'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
#     'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
#     'cache-control': 'max-age=0',
#     'priority': 'u=0, i',
#     'sec-ch-ua': '"Chromium";v="142", "Google Chrome";v="142", "Not_A Brand";v="99"',
#     'sec-ch-ua-mobile': '?0',
#     'sec-ch-ua-platform': '"Windows"',
#     'sec-fetch-dest': 'document',
#     'sec-fetch-mode': 'navigate',
#     'sec-fetch-site': 'none',
#     'sec-fetch-user': '?1',
#     'upgrade-insecure-requests': '1',
#     'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36',
#     # 'cookie': 'SF-CSRF-TOKEN=c947a7b1-5681-4e71-aecd-144fa942af43; fornax_anonymousId=157f2d86-3cf3-4898-a2e3-eb3c068ee12e; SHOP_SESSION_TOKEN=39c26e5e-c265-4505-baec-258536533acb; _shg_user_id=06a669e4-6eca-4658-8a81-a13fe99549ce; lantern=85bb5da5-0fee-4b35-a6d1-1e4b942afd3d; STORE_VISITOR=1; XSRF-TOKEN=b91d40cc992f92408f24a9902bb127f07b9429bcc8dbec4a47e4ed4a976383f0; _fbp=fb.2.1762776350457.48384813880456306; viewPosts[limit]=12; __cf_bm=yAZJ2pS7F.1ZqFi20denAd6cur5s36jg0F.kqxa2OYs-1762845612-1.0.1.1-sUhuV_Qj6GUnW.xOvdQiPqTWwOnOB.Rjcf3bBdMsvNAV1_33AzcboP3nyENmxC_7EjUbAdOL9t4ijmFKpC1o5K10xJ68H_JSbuL.X32wuME; athena_short_visit_id=3e2071c6-0129-4891-94d3-ce764102ac85:1762845613; _shg_session_id=2fc38c13-d3c1-44b7-9e1b-5b2e18a388e6; lastVisitedCategory=2163; ssUserId=c2a0a14c-00bd-43d4-b6eb-08f1d28802b7; ssSessionId=f03240bb-8700-42cd-8648-9dc67d48f85a; Shopper-Pref=6FCFA1D9FB8C9CE005241C0DAD12F3A47D65C5D6-1763450658064-x%7B%22cur%22%3A%22SGD%22%2C%22funcConsent%22%3Atrue%7D',
# }
#
# class HealthCateSpider(PricemateBaseSpider):
#     name = "health_cate"
#
#     def __init__(self, retailer, region, *args, **kwargs):
#         super().__init__(retailer=retailer, region=region, *args, **kwargs)
#
#     def start_requests(self):
#         url = "https://www.healthpost.co.nz/xmlsitemap.php?type=categories&page=1"
#
#         current_proxy = '2c6ea6e6d8c14216a62781b8f850cd5b'
#
#         proxy_host = "api.zyte.com"
#         proxy_port = "8011"
#         proxy_auth = f"{current_proxy}:"
#
#         proxy_url = f"https://{proxy_auth}@{proxy_host}:{proxy_port}"
#
#         yield scrapy.Request(
#             url=url,
#             cookies=cookies,
#             headers=headers,
#             callback=self.parse,
#             meta={
#                 "proxy": proxy_url,
#                 'sitemap_url': url,
#                 "filename": f"Cate_{self.generate_hash_id(url)}.html",
#                 "should_be": ["loc"]
#             }
#
#         )
#
#     def parse(self, response):
#         sitemap_url = response.meta['sitemap_url']
#         namespaces = {'ns': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
#         try:
#             root = etree.fromstring(response.body)
#
#             loc_elements = root.xpath('//ns:loc', namespaces=namespaces)
#
#             for loc in loc_elements:
#                 cate_url = loc.text.strip()
#                 hash_id = self.generate_hash_id(cate_url, self.retailer, self.region)
#                 self.category_input.update_one(
#                     {"_id": hash_id},
#                     {"$set": {"url": cate_url, "Status": "Pending", "retailer": self.retailer, "region": self.region}},
#                     upsert=True
#                 )
#                 print(f"inserted: {cate_url}")
#
#         except Exception as e:
#             print(f"Failed to fetch sitemap {sitemap_url}:{e}")
#
#
#
#     def close(self, reason):
#         self.mongo_client.close()
#
# if __name__ == '__main__':
#     from scrapy.cmdline import execute
#     execute("scrapy crawl health_cate -a retailer=healthpost-nz -a region=nz -a Type=eshop -a RetailerCode=healthpost_nz".split())