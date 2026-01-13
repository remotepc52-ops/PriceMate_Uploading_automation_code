import json
import math
import re, unicodedata
import time
from parsel import Selector
from urllib.parse import quote
import scrapy
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from pricemate.spiders.base_spider import PricemateBaseSpider

cookies = {
    '__wpkreporterwid_': '5edfe027-7583-4c23-b5f9-4fb27370b315',
    'lzd_cid': 'e0b16b1f-193a-4f86-bc2a-d8f2284418a2',
    'lzd_sid': '123d654913cf5d29a8021f1150fdf3ce',
    '_tb_token_': 'f84b1e6e837a9',
    'lwrid': 'AgGaoAn5MPOVmPOuO9EAX39uI5Qx',
    'hng': 'TH|en|THB|764',
    'userLanguageML': 'en',
    'undefined_click_time': '1763621600521',
    '_bl_uid': '02m1bibh7Os2X6raXkICl6jjyb80',
    'lwrtk': 'AAIEaR8rYAYZ1t69oWRVXTovHzpto4jevR3HHQo84j3AF8Ti3O08jq8=',
    '_m_h5_tk': 'd3fc75e7bb92178845818821b2b6a81b_1763629882083',
    '_m_h5_tk_enc': 'e54792b12dac461a3446d84344d01fd6',
    't_fv': '1763621604412',
    't_uid': 'SgUS5yBEvRLf4yAbh2xnqRK1zP7lyp4i',
    't_sid': 'TmO9sDRiCuL8jbFxZC7HgdB96nR7IW6W',
    'utm_channel': 'NA',
    'x5sectag': '727739',
    'bx-cookie-test': '1',
    'x5sec': '7b22617365727665722d6c617a6164613b33223a22617c434c53412b386747454d61716770634449676c795a574e686348526a614745776e4f484873674e4b616a41324d446c6d5a6a41774d4441774d4441774d4441774d4441774d4441774d4441774d4441774d4441774d4441774d4441774d4451354d6a51324d4755784f4759354d3249324f4467304e575a695a6a55304d6a63774d4441774d4441774d4441784e6a49315a4451774f5759354e6a4a6d4e44557a4f44566c4f47566c59574e6c4d446b315a5746694f57593d222c22733b32223a2239613464316233396130323536333234227d',
    'tfstk': 'fSfXodODsmmbPDvxLNUrdW6VKCd6hiNUhVTO-NhqWIdxXcQp4CzmQ-Y613sM0dKN_giObwh20N-VVqf5Afl4m-bt1CRTYkPUTaaDsCEFn7Gb8nYGyhIOPTrFoCAT4L5FRb_c0LrdjFOTPQL97cd9Hnh8PF8wXCKvB0HJJ3K9yzELBVuCzqcjMv2Xtm700TB5NE98TZK-qdCWle-dksGt6zLXhHBv2oan-x9RSd1iSfOFk9jMJinYfhf5ysBdvuk2D9T18O_YMbdViZBpB6EiBZR2cQCAdVhOPIt5x1IocutdiaCHwLPLRaCl0Zf57VF9zM-Rosd_9yAXMnd54cceA8soC49n1UtUPzMiIcOddl-Cs4u9HUYuUzaSKE9vrUtUPzMiIKLkruz7PvYf.',
    'epssw': '11*mmLg2moAHsZ3gmAz3ubkTTOF70FhYFA_GWU6NrieNnKsYi1rIuGypGcpqkc2olZvcdtN7tEUa9CLlhemaOtXtEAZEOyZa7FBLOAZnYRhHHzgPEGHmTVcJR8ltWw9TbIkhsiKlRmmarf-xSDYneis1zRmXiQmMXXeuEGprDzpP3p_mWut27Oo1mHJmmamD0CxmYK6u0NCkM__oBEC1u0xucFn_nLjtjmImmmeu6BmmH-uuXDiN_oamcuFf0ImmeaElx6FmmBeBjaYNZgau000cM8BfDjeEmBmTjeaJEfUNYehLGNm5PNEBmj.',
}

headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
    'priority': 'u=1, i',
    'referer': 'https://www.lazada.co.th/',
    'sec-ch-ua': '"Chromium";v="142", "Google Chrome";v="142", "Not_A Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36',
    'x-csrf-token': 'f84b1e6e837a9',
    # 'cookie': '__wpkreporterwid_=5edfe027-7583-4c23-b5f9-4fb27370b315; lzd_cid=e0b16b1f-193a-4f86-bc2a-d8f2284418a2; lzd_sid=123d654913cf5d29a8021f1150fdf3ce; _tb_token_=f84b1e6e837a9; lwrid=AgGaoAn5MPOVmPOuO9EAX39uI5Qx; hng=TH|en|THB|764; userLanguageML=en; undefined_click_time=1763621600521; _bl_uid=02m1bibh7Os2X6raXkICl6jjyb80; lwrtk=AAIEaR8rYAYZ1t69oWRVXTovHzpto4jevR3HHQo84j3AF8Ti3O08jq8=; _m_h5_tk=d3fc75e7bb92178845818821b2b6a81b_1763629882083; _m_h5_tk_enc=e54792b12dac461a3446d84344d01fd6; t_fv=1763621604412; t_uid=SgUS5yBEvRLf4yAbh2xnqRK1zP7lyp4i; t_sid=TmO9sDRiCuL8jbFxZC7HgdB96nR7IW6W; utm_channel=NA; x5sectag=727739; bx-cookie-test=1; x5sec=7b22617365727665722d6c617a6164613b33223a22617c434c53412b386747454d61716770634449676c795a574e686348526a614745776e4f484873674e4b616a41324d446c6d5a6a41774d4441774d4441774d4441774d4441774d4441774d4441774d4441774d4441774d4441774d4441774d4451354d6a51324d4755784f4759354d3249324f4467304e575a695a6a55304d6a63774d4441774d4441774d4441784e6a49315a4451774f5759354e6a4a6d4e44557a4f44566c4f47566c59574e6c4d446b315a5746694f57593d222c22733b32223a2239613464316233396130323536333234227d; tfstk=fSfXodODsmmbPDvxLNUrdW6VKCd6hiNUhVTO-NhqWIdxXcQp4CzmQ-Y613sM0dKN_giObwh20N-VVqf5Afl4m-bt1CRTYkPUTaaDsCEFn7Gb8nYGyhIOPTrFoCAT4L5FRb_c0LrdjFOTPQL97cd9Hnh8PF8wXCKvB0HJJ3K9yzELBVuCzqcjMv2Xtm700TB5NE98TZK-qdCWle-dksGt6zLXhHBv2oan-x9RSd1iSfOFk9jMJinYfhf5ysBdvuk2D9T18O_YMbdViZBpB6EiBZR2cQCAdVhOPIt5x1IocutdiaCHwLPLRaCl0Zf57VF9zM-Rosd_9yAXMnd54cceA8soC49n1UtUPzMiIcOddl-Cs4u9HUYuUzaSKE9vrUtUPzMiIKLkruz7PvYf.; epssw=11*mmLg2moAHsZ3gmAz3ubkTTOF70FhYFA_GWU6NrieNnKsYi1rIuGypGcpqkc2olZvcdtN7tEUa9CLlhemaOtXtEAZEOyZa7FBLOAZnYRhHHzgPEGHmTVcJR8ltWw9TbIkhsiKlRmmarf-xSDYneis1zRmXiQmMXXeuEGprDzpP3p_mWut27Oo1mHJmmamD0CxmYK6u0NCkM__oBEC1u0xucFn_nLjtjmImmmeu6BmmH-uuXDiN_oamcuFf0ImmeaElx6FmmBeBjaYNZgau000cM8BfDjeEmBmTjeaJEfUNYehLGNm5PNEBmj.',
}

class WatsonsThSpider(PricemateBaseSpider):
    name = "watsons_thi"

    def __init__(self, retailer, region, *args, **kwargs):
        super().__init__(retailer=retailer, region=region, *args, **kwargs)

    def start_requests(self):
        url = 'https://www.lazada.co.th/watsons/?ajax=true&from=wangpu&isFirstRequest=true&langFlag=en&page=1&pageTypeId=2&q=All-Products'

        # current_proxy = '2c6ea6e6d8c14216a62781b8f850cd5b'
        # current_proxy = '7d12e8dc87c84c9b9fccc23416cbdc40'

        # proxy_host = "api.zyte.com"
        # proxy_port = "8011"
        # proxy_auth = f"{current_proxy}:"

        # proxies1 = "http://{}@{}:{}/".format(proxy_auth, proxy_host, proxy_port)


        yield scrapy.Request(
            url=url,
            cookies=cookies,
            headers=headers,
            callback=self.parse_pdp,
            meta={
                # "proxy" : proxies1,
                "url": url,
                "filename": f"PDP_{self.generate_hash_id(url)}.html",
                "page": 1,
                "should_be": ["mainInfo"]
            }

        )
    def parse_pdp(self, response):
        meta = response.meta

        loaded_json = json.loads(response.text)

        totalResults = loaded_json['mainInfo']['totalResults']
        if int(totalResults) == 4080:
            totalResults = loaded_json['mods']['filter']['filteredQuatity']
            print("Max Page Limitation...", totalResults)

        product_list = loaded_json['mods']['listItems']

        if product_list:
            # process_thread(product_list)

            for pdp_data in product_list:

                Parent_Id = pdp_data['itemId']
                Product_Name = pdp_data['name']
                itemid = pdp_data['skuId']
                img = pdp_data['image']
                try:
                    product_url = pdp_data['itemUrl'].split("?")[0]
                except:
                    product_url = pdp_data['productUrl'].split("?")[0]

                if not str(product_url).startswith("https"):
                    product_url = f"https:{product_url}"

                seller_name = pdp_data['sellerName']
                # seller_url = f"{domain}/{seller_name.lower().replace(' ', '-')}/?q=All-Products&from=wangpu&langFlag=en&pageTypeId=2"
                try:
                    discount = pdp_data['discount']
                    pack_size = pdp_data['packageInfo']
                except:
                    discount = ""
                    pack_size = ""
                try:
                    originalPrice = float(pdp_data['originalPrice'])
                except:
                    originalPrice = ""

                try:
                    salePrice = float(pdp_data['price'])
                except:
                    if originalPrice == salePrice:
                        # salePrice = originalPrice
                        originalPrice = ""

                    else:

                        print("Sale Price is required,,,,,", itemid)
                        return None

                try:
                    stock_count = pdp_data['inStock']
                    if not stock_count:
                        isOos = True
                    else:
                        isOos = False
                except:
                    isOos = False

                item_sold = pdp_data.get('querystring', "") or pdp_data.get('productUrl', "")
                if item_sold:
                    item_sold = int(item_sold.split("&sale=")[-1].split("&")[0])

                ratingScore = pdp_data['ratingScore']
                if ratingScore:
                    ratingScore = round(float(ratingScore), 1)

                review = pdp_data['review']
                if review:
                    review = int(review)

                brand = pdp_data['brandName']
                skuId = pdp_data['skuId']

                currency = loaded_json['mainInfo']['currency']

                sellerId = pdp_data['sellerId']
                rrp = originalPrice
                if originalPrice is None or originalPrice == "":
                    rrp = salePrice

                breadcrumb_items = loaded_json.get('mods', {}).get('breadcrumb', [])
                breadcrumb_titles = [crumb.get('title') for crumb in breadcrumb_items]
                bread = ' > '.join(breadcrumb_titles)

                product_hash = self.generate_hash_id(product_url, self.retailer, self.region)
                item = {
                "_id": product_hash,
                "ProductCode": skuId,
                "ParentCode": Parent_Id,
                "ProductURL": product_url,
                "Name": Product_Name,
                "Brand": brand,
                "Pack_size": pack_size,
                "Price": salePrice,
                "WasPrice": originalPrice,
                "Category_Hierarchy":bread,
                "is_available": True if not isOos else False,
                "Status": "Done",
                "Images": img,
                "RRP": rrp,
                "Offer_info": discount,
                "Promo_Type": "",
                "per_unit_price": "",
                "Barcode": "",
                "retailer": self.retailer,
                "region": self.region,
                "retailer_name" : "lazada_watsons_th",
            }
                self.save_product(item)
                print(f"Product URL Inserted !")

        main_info = loaded_json.get('mainInfo', {})
        total_results = int(main_info.get('totalResults'))
        page_size = int(main_info.get('pageSize', 40))
        current_page = int(main_info.get('page', 1))

        total_pages = math.ceil(total_results / page_size)

        if current_page < total_pages:
            next_page = current_page + 1
            next_url = f'https://www.lazada.co.th/watsons/?ajax=true&from=wangpu&isFirstRequest=true&langFlag=en&page={next_page}&pageTypeId=2&q=All-Products'
            print(f"Going to next page...{next_url}✅")
            meta = {
                "page": next_page,
                "filename": f"PDP_{self.generate_hash_id(next_url)}_{next_page}.html",
                "should_be": ["mainInfo"]
            }

            yield scrapy.Request(url=next_url,
                                 callback=self.parse_pdp,
                                 meta=meta,
                                 )

            print(f"Product URL Inserted !")

    def close(self, reason):
        self.mongo_client.close()

if __name__ == '__main__':
    from scrapy.cmdline import execute
    execute("scrapy crawl watsons_thi -a retailer=lazada_watsons_th -a region=th -a Type=marketplace -a RetailerCode=lazada_watsons_th".split())