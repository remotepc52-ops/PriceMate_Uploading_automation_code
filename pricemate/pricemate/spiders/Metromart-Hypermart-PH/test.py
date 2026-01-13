# # import json
# # import re
# #
# # import requests
# #
# # cookies = {
# #     '__Host-authjs.csrf-token': 'dd755a40bfc15904486e46871fdc1f98986acb530599b8b89a44ae2a40d1a7d8%7Caa782220112e9316cc8e223ea3ba1de33b52554e3140b6fb825e700804f47a22',
# #     '__Secure-next-auth.callback-url': 'https%3A%2F%2Fwww.metromart.com',
# #     'token': 'eyJhbGciOiJIUzI1NiJ9.eyJpZCI6MTU0NDM4NDcsInR5cGUiOiJndWVzdCIsInNob3AtaWQiOjIxMjQsImlhdCI6MTc2MzYyMzc1NH0.oVwYJlDGmzwqC4gkkgrGhiObs_GxDdfqHSWnKWWo1S0',
# #     'addressObject': '%7B%22kind%22%3A%22home%22%2C%22label%22%3A%22Novaliches%20Proper%22%2C%22address1%22%3A%22Quezon%20City%2C%20Metro%20Manila%2C%20Philippines%22%2C%22latitude%22%3A%2214.720093%22%2C%22longitude%22%3A%22121.03781%22%2C%22areaId%22%3A124%2C%22userId%22%3A15443847%2C%22id%22%3A2670252%2C%22address2%22%3Anull%2C%22city%22%3A%22Quezon%20City%22%2C%22landmark%22%3Anull%2C%22postCode%22%3Anull%7D',
# #     'areaId': '124',
# #     'hasUserAddress': 'true',
# #     'shopId': '2110',
# #     'shopSlug': 'sm-hypermarket-north-edsa',
# # }
# #
# # headers = {
# #     'accept': 'text/x-component',
# #     'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
# #     'baggage': 'sentry-environment=vercel-production,sentry-release=9f9b3653118c77a7cf726703b187f16c709b86c7,sentry-public_key=3e10e277c451ec42dec7fe16c0175b3f,sentry-trace_id=47a0eda228b84fd9a88112e904321c22,sentry-sampled=false,sentry-sample_rand=0.14269384233665605,sentry-sample_rate=0.02',
# #     'content-type': 'text/plain;charset=UTF-8',
# #     'next-action': '962196e6b9607b28f29e729546253e0725c3e87d',
# #     'next-router-state-tree': '%5B%22%22%2C%7B%22children%22%3A%5B%22shops%22%2C%7B%22children%22%3A%5B%5B%22slug%22%2C%22sm-hypermarket-north-edsa%22%2C%22d%22%5D%2C%7B%22children%22%3A%5B%22departments%22%2C%7B%22children%22%3A%5B%5B%22department-id%22%2C%2243777%22%2C%22d%22%5D%2C%7B%22children%22%3A%5B%22__PAGE__%22%2C%7B%7D%2C%22%2Fshops%2Fsm-hypermarket-north-edsa%2Fdepartments%2F43777%22%2C%22refresh%22%5D%7D%2Cnull%2Cnull%2Ctrue%5D%7D%2Cnull%2Cnull%5D%7D%2Cnull%2Cnull%5D%7D%2Cnull%2Cnull%5D%7D%2Cnull%2Cnull%2Ctrue%5D',
# #     'origin': 'https://www.metromart.com',
# #     'priority': 'u=1, i',
# #     'referer': 'https://www.metromart.com/shops/sm-hypermarket-north-edsa/departments/43777',
# #     'sec-ch-ua': '"Chromium";v="142", "Google Chrome";v="142", "Not_A Brand";v="99"',
# #     'sec-ch-ua-mobile': '?0',
# #     'sec-ch-ua-platform': '"Windows"',
# #     'sec-fetch-dest': 'empty',
# #     'sec-fetch-mode': 'cors',
# #     'sec-fetch-site': 'same-origin',
# #     'sentry-trace': '47a0eda228b84fd9a88112e904321c22-91015cc08c440b98-0',
# #     'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36',
# #     'x-deployment-id': 'dpl_HUA5TzdbAUs9pVRDa9UzJ3Z8dRJ7',
# #     # 'cookie': '__Host-authjs.csrf-token=dd755a40bfc15904486e46871fdc1f98986acb530599b8b89a44ae2a40d1a7d8%7Caa782220112e9316cc8e223ea3ba1de33b52554e3140b6fb825e700804f47a22; __Secure-next-auth.callback-url=https%3A%2F%2Fwww.metromart.com; token=eyJhbGciOiJIUzI1NiJ9.eyJpZCI6MTU0NDM4NDcsInR5cGUiOiJndWVzdCIsInNob3AtaWQiOjIxMjQsImlhdCI6MTc2MzYyMzc1NH0.oVwYJlDGmzwqC4gkkgrGhiObs_GxDdfqHSWnKWWo1S0; addressObject=%7B%22kind%22%3A%22home%22%2C%22label%22%3A%22Novaliches%20Proper%22%2C%22address1%22%3A%22Quezon%20City%2C%20Metro%20Manila%2C%20Philippines%22%2C%22latitude%22%3A%2214.720093%22%2C%22longitude%22%3A%22121.03781%22%2C%22areaId%22%3A124%2C%22userId%22%3A15443847%2C%22id%22%3A2670252%2C%22address2%22%3Anull%2C%22city%22%3A%22Quezon%20City%22%2C%22landmark%22%3Anull%2C%22postCode%22%3Anull%7D; areaId=124; hasUserAddress=true; shopId=2110; shopSlug=sm-hypermarket-north-edsa',
# # }
# #
# # data = '[{"page":2,"query":"include=weights,take-y-weight,take-y-products,favorites,fmcg-campaign,fmcg-campaign.fmcg-campaign-vouchers,dhz-campaign-brand,department&fields[products]=alcoholic,amount-in-cents,base-amount-in-cents,business-max-items-count,buy-x,buy-x-take-y,bulk,bulk-quantity-threshold,delicate,description,dhz-campaign-brand,dhz-campaign-brand-priority,image-url,image-740x740,max-items-count,name,percent-off,priority,require-legal-age,sari-sari-max-items-count,size,sold-as,status,take-y,weight-metric,weight-multiplier,weighted,weighted-disclaimer,fmcg-campaign,fmcg-campaign.fmcg-campaign-vouchers,department,aisle,shop,buy-x-weight,take-y-products,take-y-weight,weights&fields[fmcg-campaigns]=kind,status,fmcg-campaign-vouchers&fields[weights]=value,default&filter[aisle.id]=174795,174794,181861,181862,181863,181864&filter[sub-aisle.id]=&filter[brand.id]=&fields[fmcg-campaign-vouchers]=discount-in-cents,minimum-spend-in-cents&filter[shop.id]=2110&filter[status]=available&page[size]=30&sort=fmcg-campaign.status=[active],fmcg-campaign.kind=[free-delivery,peso-discount,free-shopping-fee,display-only],-monthly-popular-score,-updated-at","v2":true,"resource":"products"}]'
# #
# # response = requests.post(
# #     'https://www.metromart.com/shops/sm-hypermarket-north-edsa/departments/43777',
# #     cookies=cookies,
# #     headers=headers,
# #     data=data,
# # )
# # print(response.text)
# # try:
# #     text = response.text
# #     match = re.search(r'1:\s*(\{[\s\S]*\})', text)
# #     if not match:
# #         print("Could not extract JSON from response")
# #
# #     clean_json_text = match.group(1)
# #     data = json.loads(clean_json_text)
# #     products = data.get('data', [])
# #     print(products)
# #     for product in products:
# #         product_id = product.get('id')
# #         print(product_id)
# #     print(response.status_code)
# #     print(data)
# # except Exception as e:
# #     print(f"❌ Failed to parse JSON : {e}")
# #
# import scrapy
#
# class MetroMartTestSpider(scrapy.Spider):
#     name = "metromart_test"
#
#     custom_settings = {
#         "COOKIES_ENABLED": True,
#         "REDIRECT_ENABLED": False,
#         "COMPRESSION_ENABLED": False,
#         "DOWNLOAD_FAIL_ON_DATALOSS": False,
#         "RETRY_ENABLED": False,
#         "LOG_LEVEL": "DEBUG",
#     }
#
#     cookies = {
#         '__Host-authjs.csrf-token': 'dd755a40bfc15904486e46871fdc1f98986acb530599b8b89a44ae2a40d1a7d8%7Caa782220112e9316cc8e223ea3ba1de33b52554e3140b6fb825e700804f47a22',
#         '__Secure-next-auth.callback-url': 'https%3A%2F%2Fwww.metromart.com',
#         'token': 'eyJhbGciOiJIUzI1NiJ9.eyJpZCI6MTU0NDM4NDcsInR5cGUiOiJndWVzdCIsInNob3AtaWQiOjIxMjQsImlhdCI6MTc2MzYyMzc1NH0.oVwYJlDGmzwqC4gkkgrGhiObs_GxDdfqHSWnKWWo1S0',
#         'addressObject': '%7B%22kind%22%3A%22home%22%2C%22label%22%3A%22Novaliches%20Proper%22%2C%22address1%22%3A%22Quezon%20City%2C%20Metro%20Manila%2C%20Philippines%22%2C%22latitude%22%3A%2214.720093%22%2C%22longitude%22%3A%22121.03781%22%2C%22areaId%22%3A124%2C%22userId%22%3A15443847%2C%22id%22%3A2670252%2C%22address2%22%3Anull%2C%22city%22%3A%22Quezon%20City%22%2C%22landmark%22%3Anull%2C%22postCode%22%3Anull%7D',
#         'areaId': '124',
#         'hasUserAddress': 'true',
#         'shopId': '2110',
#         'shopSlug': 'sm-hypermarket-north-edsa',
#     }
#
#     headers = {
#         'accept': 'text/x-component',
#         'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
#         'content-type': 'text/plain;charset=UTF-8',
#         'next-action': '962196e6b9607b28f29e729546253e0725c3e87d',
#         'next-router-state-tree': '%5B%22%22%2C%7B%22children%22%3A%5B%22shops%22%2C%7B%22children%22%3A%5B%5B%22slug%22%2C%22sm-hypermarket-north-edsa%22%2C%22d%22%5D%2C%7B%22children%22%3A%5B%22departments%22%2C%7B%22children%22%3A%5B%5B%22department-id%22%2C%2243777%22%2C%22d%22%5D%2C%7B%22children%22%3A%5B%22__PAGE__%22%2C%7B%7D%2C%22%2Fshops%2Fsm-hypermarket-north-edsa%2Fdepartments%2F43777%22%2C%22refresh%22%5D%7D%2Cnull%2Cnull%2Ctrue%5D%7D%2Cnull%2Cnull%5D%7D%2Cnull%2Cnull%5D%7D%2Cnull%2Cnull%5D%7D%2Cnull%2Cnull%2Ctrue%5D',
#         'referer': 'https://www.metromart.com/shops/sm-hypermarket-north-edsa/departments/43777',
#         'origin': 'https://www.metromart.com',
#         'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36',
#         'sec-fetch-site': 'same-origin',
#         'sec-fetch-mode': 'cors',
#     }
#
#     data = '[{"page":1,"query":"include=weights,take-y-weight,take-y-products,favorites,fmcg-campaign,fmcg-campaign.fmcg-campaign-vouchers,dhz-campaign-brand,department&fields[products]=alcoholic,amount-in-cents,base-amount-in-cents,business-max-items-count,buy-x,buy-x-take-y,bulk,bulk-quantity-threshold,delicate,description,dhz-campaign-brand,dhz-campaign-brand-priority,image-url,image-740x740,max-items-count,name,percent-off,priority,require-legal-age,sari-sari-max-items-count,size,sold-as,status,take-y,weight-metric,weight-multiplier,weighted,weighted-disclaimer,fmcg-campaign,fmcg-campaign.fmcg-campaign-vouchers,department,aisle,shop,buy-x-weight,take-y-products,take-y-weight,weights&filter[shop.id]=2110&filter[status]=available&page[size]=30","v2":true,"resource":"products"}]'
#
#     def start_requests(self):
#
#         yield scrapy.Request(
#             url="https://www.metromart.com/shops/sm-hypermarket-north-edsa/departments/43777",
#             method="POST",
#             body=self.data,
#             headers=self.headers,
#             cookies=self.cookies,
#             callback=self.parse_test,
#             meta={
#                 "dont_redirect": True,
#                 "handle_httpstatus_all": True,
#                 "http2": True,
#                 "filename": f"test_page.html",
#                 "should_be": ['data']
#             },
#             dont_filter=True
#         )
#
#     def parse_test(self, response):
#         self.logger.info("STATUS = %s", response.status)
#         self.logger.info("CONTENT-TYPE = %s", response.headers.get("Content-Type"))
#         self.logger.info("FIRST 2000 CHARS:\n%s", response.text[:2000])
#
# if __name__ == '__main__':
#     from scrapy.cmdline import execute
#     execute("scrapy crawl metromart_test".split())