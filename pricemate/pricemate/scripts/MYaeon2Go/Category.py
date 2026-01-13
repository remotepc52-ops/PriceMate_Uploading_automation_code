# import sys
#
# from config import *
#
#
# def data_extraction(url = None, page = 1, total_page = 0):
#     try:
#         if not url:
#             url = 'https://myaeon2go.com/products/category/545234/aeon/pages/1-5'
#
#         if '/pages/' not in url:
#             url = f"{url}/pages/1-5"  # 100 pages means almost 6k products in first page....
#             # url = f"{url}/pages/1-2"
#
#         print(url)
#
#         hashid = generate_hashId(url)
#         filename = f'MYAEON2GO_PL_{hashid}_page_{page}.html'
#         filepath = os.path.join(html_path, filename)
#         path = filepath.replace("\\", "/")
#
#         headers = {
#             'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
#             'accept-language': 'en-US,en;q=0.9,hi;q=0.8',
#             'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36',
#             'cookie': 'deviceId=b76f4490-9ccf-4976-85ff-f8fb7eb3522b; i18next=en-GB; _ga=GA1.1.417556377.1749711924; locationCaptured=true; crumb=c2P_VjYYgfPv7UpxdxbPzM_xEugFxlcDBWFwKN2XGb9; selectedPostalCode=55100; mp_d7f79c10b89f9fa3026f2fb08d3cf36d_mixpanel=%7B%22distinct_id%22%3A%20%22%24device%3A19762f52a235b1-05d7e416a36d24-26011e51-144000-19762f52a235b1%22%2C%22%24device_id%22%3A%20%2219762f52a235b1-05d7e416a36d24-26011e51-144000-19762f52a235b1%22%2C%22%24initial_referrer%22%3A%20%22%24direct%22%2C%22%24initial_referring_domain%22%3A%20%22%24direct%22%7D; locationIdentifierIds=63b70a81277ca7244135741e,63b70a81277ca724413572f2; aeon-malaysia-prodnxweb.sid=Fe26.2**ae0ca13be3a22369774591793a16426a0808f963224feaa90d47cd57b01f23f7*lLDuYy-UHQgaFM0GCSPGgA*nqSKDlxMsG0h8-gc3FG1_ZMn4ZEEX7fhnT4gk8BVuZSojB1QcEakrBzqyKbNWAGb**4989fe498b2f9a847576cf6539619f77fd4defa28108c394ceafc0b39e4b54c8*XicOK5sVvRe1oGGicwJ_CPHPBsrH-DmmhffE3Wthg_0; datadome=U~nRSXbfoO~QL63fW1zvoJzFpSLI91NPZEv2HO0YcCxap09WybKXk8NSTQywcBpHt98aaSJSM9OaTJqTk2oLOPzgsh812_59d7YwRDv_FYNSQyrGnzcVqX2i7IAJuDLI; _ga_JGW88X53V2=GS2.1.s1756292597$o9$g1$t1756292601$j56$l0$h0; _dd_s=rum=0&expire=1756293500532; superSession={%22id%22:%22b76f4490-9ccf-4976-85ff-f8fb7eb3522b-1756292597570%22%2C%22expiry%22:1756294404179}',
#         }
#
#         proxy = "http://21ed11ef5c872bc7727680a52233027db4578a0e:@api.zenrows.com:8001"
#
#         proxies = {"http": proxy, "https": proxy}
#
#         response = obj.to_requests(url=url, headers=headers, proxies=proxies,
#                                    should_be=['id="page-content"'], html_path=path)
#
#         if not response:
#             print("Getting none in MYAEON2GO response....")
#             return None
#
#         elif 'Result Not Found' in response:
#             print("Url is not found...")
#
#         else:
#             print("Getting Correct Response of MYAEON2GO...")
#             res_selector = Selector(text=response)
#             try:
#                 product_list = res_selector.xpath('//ul[contains(@class,"g-product-list")]//li[@data-bx="ple"]')
#                 if product_list:
#                     for product in product_list:
#
#                         pro_url = product.xpath('.//a/@href').get()
#                         if 'http' not in pro_url:
#                             pro_url = f"https://myaeon2go.com{pro_url}"
#
#                         itemid = pro_url.split("/product/")[-1].split("/")[0].split("?")[0]
#
#                         # name = product.xpath('.//div[@data-bx="ple-wrap"]/a/@title').get()
#                         # if not name:
#                         name = c_replace(" ".join(product.xpath(
#                             './/div[@data-bx="ple-wrap"]//div[@class="hlfuLGCmHPsi1uwgI5FR"]//text()').getall()))
#                         Product_Size = extract_size(name)
#                         if not Product_Size:
#                             Product_Size = ""
#
#                         activePrice = product.xpath(
#                             './/div[@data-bx="ple-wrap"]//span[contains(@class,"EgZI6WlRYJ4ErOBeOctF")]//span[@class="g-sr-only"]//text()').get()
#                         if not activePrice:
#                             continue
#
#                         else:
#                             try:
#                                 activePrice = activePrice.split("RM ")[-1].replace(",", "")
#                                 Price = float(activePrice.strip())
#                             except:
#                                 activePrice = product.xpath(
#                                     './/div[@data-bx="ple-wrap"]//span[contains(@class,"EgZI6WlRYJ4ErOBeOctF")]//span[@class="LU7OiYInCEvMB1aSOO6j"][1]//text()').get()
#
#                                 activePrice = activePrice.split("RM ")[-1].replace(",", "")
#                                 Price = float(activePrice.strip())
#
#                         try:
#                             original_price = product.xpath(
#                                 './/span[contains(text(), "original price")]//text()').get() or None
#                             if original_price:
#                                 WasPrice = float(original_price.split("RM ")[-1]).replace(",", "")
#                             else:
#                                 WasPrice = None
#                         except:
#                             WasPrice = None
#
#                         if WasPrice and not Price or Price == WasPrice:
#                             Price = WasPrice
#                             WasPrice = None
#
#                         offer_info = product.xpath('.//div[@data-bx="ple-wrap"]/a//strong[contains(@class, "QaatOuE6YHqLVCeOpesn")]//text()').get()
#                         if offer_info:
#                             offer_info = offer_info.strip()
#
#
#                         # if not isOos:
#                         # isOos = product.xpath('.//div[@data-bx="ple-btn-add"]')
#                         # if isOos:
#                         #     is_available = True
#                         # else:
#                         #     is_available = False
#
#                         items = {}
#                         items["full_path"] = path
#                         items["ProductURL"] = pro_url
#                         items["ProductCode"] = itemid
#                         items["Name"] = name
#                         items["Price"] = activePrice
#                         items["WasPrice"] = WasPrice
#                         items["RRP"] = WasPrice if WasPrice else Price
#                         items["per_unit_price"] = ""
#                         items["Offer_info"] = offer_info
#                         items["Pack_size"] = Product_Size
#                         items["Barcode"] = ""
#                         items["retailer_name"] = "myaeon2go"
#                         # items["Category_Hierarchy"] = breadcrumbs
#                         # items["Brand"] = brand
#                         # items["Promo_Type"] = promo_type
#                         # items["Images"] = product_images
#                         # items["is_available"] = is_available
#                         items["Status"] = "Done"
#
#                         try:
#                             product_data.insert_one(items)
#                             print("Product Data Inserted...")
#
#                         except Exception as e:
#                             if 'duplicate key error' not in str(e):
#                                 print(e)
#
#                 else:
#                     print("Product List Not Found,,,,", page)
#
#             except Exception as e:
#                 print("Error in Myaeon2Go...", e)
#                 exc_type, exc_obj, exc_tb = sys.exc_info()
#                 fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
#                 print(exc_type, fname, exc_tb.tb_lineno)
#
#             if 'LOAD MORE' in response:
#                 page    += 5
#                 page_range = page + 4
#                 print("Going To Next Page...", page)
#
#                 next_url = url.split("/pages/")[0] + f"/pages/{page}-{page_range}"
#                 data_extraction(next_url, total_page=total_page, page=page)
#
#             else:
#                 print("else.....")
#
#     except Exception as e:
#         print(f"Error in Main Data Extraction function ",e)
#         exc_type,exc_obj,exc_tb = sys.exc_info()
#         fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
#         print(exc_type,fname,exc_tb.tb_lineno)
#
#
# if __name__ == '__main__':
#
#     data_extraction()
#     exit()
