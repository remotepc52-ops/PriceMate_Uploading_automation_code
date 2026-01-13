import json
import math
from fileinput import filename

import scrapy
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from pricemate.spiders.spider_lazada import PricemateBaseSpider

cookies = {
    '__wpkreporterwid_': '1a790a1f-cacc-49b1-9635-4c164d5fa8d7',
    't_fv': '1764323729914',
    't_uid': 'hEQZBLfPlbOS7CLCfRWMKlmObjvnhzwO',
    'lwrid': 'AgGan%2Fc36WmdiDZV%2BOCTX39uI5Qx',
    'hng': 'MY|en-MY|MYR|458',
    'hng.sig': '3PRPmcBmKLS4UwrxxIzxYKE2BjFcClNbRbYGSaUai_0',
    'lzd_cid': 'b15e9aab-add0-403b-8209-41360905fa98',
    '_bl_uid': 'gvm31i5Fi6zrhmf0n5kR28h15Cgs',
    '_gcl_au': '1.1.983622923.1764921604',
    'cna': 'ZiqsIbfYC18CAS2FBBQqxhQD',
    '_ga': 'GA1.3.1754007218.1764921606',
    '_fbp': 'fb.2.1764921605952.606715168461176159',
    'AMCV_126E248D54200F960A4C98C6%40AdobeOrg': '-1124106680%7CMCIDTS%7C20432%7CMCMID%7C34947093032700580204267579038899530150%7CMCAAMLH-1765863295%7C12%7CMCAAMB-1765863295%7CRKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y%7CMCOPTOUT-1765265695s%7CNONE%7CvVersion%7C5.2.0',
    '_uetvid': '640c2b50c9be11f0b4b82d0a3e174b6e',
    '_ga_6VT623WX3F': 'GS2.3.s1765368848$o3$g1$t1765368860$j48$l0$h0',
    'cto_bundle': 'Flo9vV95Slh0RjIxdTdLVVNWbEJJVGZOQzVoSUhTZHZtZnhwZWV6N05rWFRNRFlVbjdYSUo3S0JNU3klMkJLJTJCR2JJNiUyQm9jNmRqZ3ZoSDV3dFZ1THZsR0dhb3JtNzdGcVdoWjFXM2ZJY0hzbDJmd3ExbU9CaW9WYWEwR2Z4a3FNOCUyRkF2b2cxU1gya3UyYmV4MkduTVBXeTIxRW1uQSUzRCUzRA',
    'isg': 'BObmTCr9s0hIwWfwPH9vxNOGN1xoxyqBBTA2YdCP0onkU4ZtOFd6kcwiq1dfeyKZ',
    '__itrace_wid': '0294eb84-6481-4505-234e-9a3c0e13171b',
    'lzd_sid': '1e4c60fb0d5b2fa9368bdfc00a1cd220',
    '_tb_token_': '3b16e5b0e1d68',
    'undefined_click_time': '1765826959737',
    '_m_h5_tk': '52eaf646fcc685909b64ddea4f49929d_1765837402389',
    '_m_h5_tk_enc': '014d91a45d56f9d3bb3b84ca93dbf5f3',
    'x5sec': '7b22617365727665722d6c617a6164613b33223a22617c434a6a4467636f47454a695675746f4249676c795a574e686348526a614745776e4f484873674e4b616a41324d47466d5a6a41774d4441774d4441774d4441774d4451774d4441774d4441774d5441774d4441774d4441774d4441774d4451324e7a5a6a5a54646c595441315a4451315a5441314e3245334e32566b4e4745774d4441774d4441774d4441784d6a56695957453159545669597a59304d54497a4d7a4d7859545934597a6c6a596a55304e5459325a444d3d222c22733b32223a2230333231643061666433313432303162227d',
    'epssw': '11*mmLS5m90VrPjgmAzEN0dYlH3y01qlPVyXFPI4M45Zw9dZLBeSpFat10nHZN3vdujXODIeRhm_D2gOuZKEOyl4imm3tevQRTiLOAvHSB-0kLSZ0oo3gix6jH6gL54v8ErujIKQOAZmTE-xSDYkcBqJ1jmNtV31Au7zhxC_8U5PxfZVo9RZ2zwt-pC1ucFNREE5gfEmmmmmTyU1_UJ2JK71lpC1RXmkBmmqZge7D6q1BjTEmNV8_Emuu3RzFn0BjPEBtuuuu3eeCymLuxuuRBeEmmLBBjyaYU3VS4G5eERdZgeui..',
    'tfstk': 'gkZi0tfCdPuslnAFqIo17js3gx_K5cijeSKxMmhV8XlB6CKT3tm0ISqAC-5_ioc3tdhZ6oF03XPYWmFA5oj43X4xDNZtgKVT3V-tMc32mcZLWnhO1m24wmfRwgI8CRiI0_CRMWOIZmkVDj7K745Nd21RwgIdVvRVL_eO0PdQLxGEQxkq09cEFX-20SlZ8Bkohml4gSoETxkjgIl2b2SEOxoqgSoVKDlInml4gmW3LbM20bq4Ak5xB9a4Cry3xA0iaRjB0nqH2VczQXxVakDG0byZtn-qab1IFJ2Os3wKfuVoe5Iej724Fru3mB5oGk2UbryBs9ouKyU-SyfwmXEt94ZZqKSaKccizkPpQOFzK-z--kBPVcmZ_rn_HLfTKlVTCk2v3eoiXy0uj0SW_jULEoD0css3Z-y7u2qDsgrD8U8gNnMFHkYXlVkIKbBaTtYJY9bJb9XHPNgZdACRK9YXlVkIKbBhKUOs7vMOw',
    'lwrtk': 'AAIEaUIH57T/P3da93o+b52fVq7cH0eTH0R4wmbOhWijVmCH23qSEc8=',
    't_sid': 'ufiYYotXjOsV8oSWRsbIvfUN1adP9vAr',
    'utm_channel': 'NA',
}

headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
    'priority': 'u=1, i',
    'referer': 'https://www.lazada.com.my/',
    'sec-ch-ua': '"Google Chrome";v="143", "Chromium";v="143", "Not A(Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36',
    'x-csrf-token': '3b16e5b0e1d68',
    # 'cookie': '__wpkreporterwid_=1a790a1f-cacc-49b1-9635-4c164d5fa8d7; t_fv=1764323729914; t_uid=hEQZBLfPlbOS7CLCfRWMKlmObjvnhzwO; lwrid=AgGan%2Fc36WmdiDZV%2BOCTX39uI5Qx; hng=MY|en-MY|MYR|458; hng.sig=3PRPmcBmKLS4UwrxxIzxYKE2BjFcClNbRbYGSaUai_0; lzd_cid=b15e9aab-add0-403b-8209-41360905fa98; _bl_uid=gvm31i5Fi6zrhmf0n5kR28h15Cgs; _gcl_au=1.1.983622923.1764921604; cna=ZiqsIbfYC18CAS2FBBQqxhQD; _ga=GA1.3.1754007218.1764921606; _fbp=fb.2.1764921605952.606715168461176159; AMCV_126E248D54200F960A4C98C6%40AdobeOrg=-1124106680%7CMCIDTS%7C20432%7CMCMID%7C34947093032700580204267579038899530150%7CMCAAMLH-1765863295%7C12%7CMCAAMB-1765863295%7CRKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y%7CMCOPTOUT-1765265695s%7CNONE%7CvVersion%7C5.2.0; _uetvid=640c2b50c9be11f0b4b82d0a3e174b6e; _ga_6VT623WX3F=GS2.3.s1765368848$o3$g1$t1765368860$j48$l0$h0; cto_bundle=Flo9vV95Slh0RjIxdTdLVVNWbEJJVGZOQzVoSUhTZHZtZnhwZWV6N05rWFRNRFlVbjdYSUo3S0JNU3klMkJLJTJCR2JJNiUyQm9jNmRqZ3ZoSDV3dFZ1THZsR0dhb3JtNzdGcVdoWjFXM2ZJY0hzbDJmd3ExbU9CaW9WYWEwR2Z4a3FNOCUyRkF2b2cxU1gya3UyYmV4MkduTVBXeTIxRW1uQSUzRCUzRA; isg=BObmTCr9s0hIwWfwPH9vxNOGN1xoxyqBBTA2YdCP0onkU4ZtOFd6kcwiq1dfeyKZ; __itrace_wid=0294eb84-6481-4505-234e-9a3c0e13171b; lzd_sid=1e4c60fb0d5b2fa9368bdfc00a1cd220; _tb_token_=3b16e5b0e1d68; undefined_click_time=1765826959737; _m_h5_tk=52eaf646fcc685909b64ddea4f49929d_1765837402389; _m_h5_tk_enc=014d91a45d56f9d3bb3b84ca93dbf5f3; x5sec=7b22617365727665722d6c617a6164613b33223a22617c434a6a4467636f47454a695675746f4249676c795a574e686348526a614745776e4f484873674e4b616a41324d47466d5a6a41774d4441774d4441774d4441774d4451774d4441774d4441774d5441774d4441774d4441774d4441774d4451324e7a5a6a5a54646c595441315a4451315a5441314e3245334e32566b4e4745774d4441774d4441774d4441784d6a56695957453159545669597a59304d54497a4d7a4d7859545934597a6c6a596a55304e5459325a444d3d222c22733b32223a2230333231643061666433313432303162227d; epssw=11*mmLS5m90VrPjgmAzEN0dYlH3y01qlPVyXFPI4M45Zw9dZLBeSpFat10nHZN3vdujXODIeRhm_D2gOuZKEOyl4imm3tevQRTiLOAvHSB-0kLSZ0oo3gix6jH6gL54v8ErujIKQOAZmTE-xSDYkcBqJ1jmNtV31Au7zhxC_8U5PxfZVo9RZ2zwt-pC1ucFNREE5gfEmmmmmTyU1_UJ2JK71lpC1RXmkBmmqZge7D6q1BjTEmNV8_Emuu3RzFn0BjPEBtuuuu3eeCymLuxuuRBeEmmLBBjyaYU3VS4G5eERdZgeui..; tfstk=gkZi0tfCdPuslnAFqIo17js3gx_K5cijeSKxMmhV8XlB6CKT3tm0ISqAC-5_ioc3tdhZ6oF03XPYWmFA5oj43X4xDNZtgKVT3V-tMc32mcZLWnhO1m24wmfRwgI8CRiI0_CRMWOIZmkVDj7K745Nd21RwgIdVvRVL_eO0PdQLxGEQxkq09cEFX-20SlZ8Bkohml4gSoETxkjgIl2b2SEOxoqgSoVKDlInml4gmW3LbM20bq4Ak5xB9a4Cry3xA0iaRjB0nqH2VczQXxVakDG0byZtn-qab1IFJ2Os3wKfuVoe5Iej724Fru3mB5oGk2UbryBs9ouKyU-SyfwmXEt94ZZqKSaKccizkPpQOFzK-z--kBPVcmZ_rn_HLfTKlVTCk2v3eoiXy0uj0SW_jULEoD0css3Z-y7u2qDsgrD8U8gNnMFHkYXlVkIKbBaTtYJY9bJb9XHPNgZdACRK9YXlVkIKbBhKUOs7vMOw; lwrtk=AAIEaUIH57T/P3da93o+b52fVq7cH0eTH0R4wmbOhWijVmCH23qSEc8=; t_sid=ufiYYotXjOsV8oSWRsbIvfUN1adP9vAr; utm_channel=NA',
}

lazada_domains = {
    "ID": "https://lazada.co.id",  # Indonesia
    "MY": "https://lazada.com.my",  # Malaysia
    "PH": "https://lazada.com.ph",  # Philippines
    "SG": "https://lazada.sg",  # Singapore
    "TH": "https://lazada.co.th",  # Thailand
    "VN": "https://lazada.vn",  # Vietnam
}

class WatsonsSpider(PricemateBaseSpider):
    name = "watsons_main"

    def __init__(self, retailer, region, *args, **kwargs):
        super().__init__(retailer=retailer, region=region, *args, **kwargs)
        self.domain = lazada_domains[self.region.upper()]
        # self.cookies = lazada_cookies[f"cookies_{self.region.lower()}"]
        # self.headers = lazada_cookies[f"headers_{self.region.lower()}"]
        # self.proxy_name = 'scrape_do'
        self.proxy_name = None

    def start_requests(self):
        # urls = 'https://www.lazada.com.my/watsons/?ajax=true&from=wangpu&isFirstRequest=true&langFlag=id&page=100&pageTypeId=2&q=All-Products'
        # source_id = "7d893f92-10e6-41b5-9891-3c7948096f5a"
        # urls = 'https://www.lazada.com.ph/watsons/?ajax=true&from=wangpu&isFirstRequest=true&langFlag=en&page=1&pageTypeId=2&q=All-Products'
        # source_id = "75f4b4a1-d756-4882-8886-7754a99e00fb"
        # urls = 'https://www.lazada.co.id/watsons/?ajax=true&from=wangpu&isFirstRequest=true&langFlag=id&page=1&pageTypeId=2&q=All-Products'
        # source_id = "05d7b80d-dfb7-4d5d-ac2c-db18dc3f3fab"
        # urls = 'https://www.lazada.com.my/big-pharmacy/?ajax=true&from=wangpu&isFirstRequest=true&langFlag=en&page=1&pageTypeId=2&q=All-Products'
        # source_id = "578c8122-dfb2-4df0-acea-5b9348abf083"
        # urls = 'https://www.lazada.com.my/guardian/?ajax=true&from=wangpu&isFirstRequest=true&langFlag=en&page=1&pageTypeId=2&q=All-Products'
        # source_id = "7e62eeb2-4807-4767-8945-237aeeec2837"
        # urls = 'https://www.lazada.com.my/mydin-malaysia/?ajax=true&from=wangpu&isFirstRequest=true&langFlag=en&page=99&pageTypeId=2&q=All-Products'
        # source_id = "a0487e29-015a-4422-abac-013f733db5b9"
        # urls = 'https://www.lazada.com.my/caring-estore/?ajax=true&from=wangpu&isFirstRequest=true&langFlag=en&page=65&pageTypeId=2&q=All-Products'
        # source_id = "27b99842-0a8e-4b3e-b814-4e126720094b"
        urls = 'https://www.lazada.com.my/bellamys-flagship-store/?ajax=true&from=wangpu&isFirstRequest=true&langFlag=en&page=1&pageTypeId=2&q=All-Products'
        source_id = "d739d579-e1b9-4bc6-8b8e-b246ff569f7e"
        # urls = 'https://www.lazada.co.id/beautyhaul-indonesia/?q=All-Products&from=wangpu&langFlag=en&pageTypeId=2&ajax=true&page=95'
        # source_id = "609a9a00-7c01-4084-904b-2cba14890c03"
        # urls = 'https://www.lazada.com.ph/zest-o-official-store/?ajax=true&from=wangpu&isFirstRequest=true&langFlag=en&page=1&pageTypeId=2&q=All-Products'
        # source_id = "585ef44d-c16f-4b8a-a612-e3a03a0b8826"

        # current_proxy = '2c6ea6e6d8c14216a62781b8f850cd5b'
        # current_proxy = '7d12e8dc87c84c9b9fccc23416cbdc40'

        # proxy_host = "api.zyte.com"
        # proxy_port = "8011"
        # proxy_auth = f"{current_proxy}:"

        # proxies1 = "http://{}@{}:{}/".format(proxy_auth, proxy_host, proxy_port)
        docs = self.category_input.find({
            # "retailer": self.retailer,
            # "region": self.region,
            "Status": "Pending"
        })

        for doc in docs:
            ur = doc["url"]
            hash_id = doc.get("_id")
            # source_id = doc.get("source_id")
            if '/shop/' in ur:
                shop_id = ur.split('/shop/shop/')[-1].split('/shop/')[-1].split('/')[0]

            else:
                shop_id = ur.split(f"{self.domain[10:]}/")[-1].split('/')[0]
            page = 1
            filename = f'{self.domain.split("//")[-1]}_{shop_id.replace("-", "_")}_page_{page}.json'

            yield scrapy.Request(
            url=urls,
            cookies=cookies,
            headers=headers,
            callback=self.parse_pdp,
            meta={
                # "proxy" : proxies1,
                "url": urls,
                "source_id": source_id,
                "page": page,
                "shop_id": shop_id,
                "hash_id": hash_id,
                "filename": f"PDP_{self.generate_hash_id(urls)}_{page}.html",
                "should_be": ["mainInfo"]
            }

        )
    def parse_pdp(self, response):
        meta = response.meta
        hash_id = meta.get("hash_id")
        filename = meta.get("filename")
        source_id = meta.get("source_id")
        ur = meta.get("ur")
        # page = meta.get("page")
        page = meta.get("page")
        shop_id = meta.get("shop_id")

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
                "hash_id": hash_id,
                "CategoryURL": ur,
                "source_id": source_id,
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
                "retailer_name" : self.retailer,
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
            # next_url = f'https://www.lazada.com.my/watsons/?ajax=true&from=wangpu&isFirstRequest=true&langFlag=id&page={next_page}&pageTypeId=2&q=All-Products'
            # next_url = f'https://www.lazada.com.ph/watsons/?ajax=true&from=wangpu&isFirstRequest=true&langFlag=id&page={next_page}&pageTypeId=2&q=All-Products'
            # next_url = f'https://www.lazada.co.id/watsons/?ajax=true&from=wangpu&isFirstRequest=true&langFlag=id&page={next_page}&pageTypeId=2&q=All-Products'
            # next_url = f'https://www.lazada.com.my/big-pharmacy/?ajax=true&from=wangpu&isFirstRequest=true&langFlag=en&page={next_page}&pageTypeId=2&q=All-Products'
            # next_url = f'https://www.lazada.com.my/guardian/?ajax=true&from=wangpu&isFirstRequest=true&langFlag=en&page={next_page}&pageTypeId=2&q=All-Products'
            # next_url = f'https://www.lazada.com.my/mydin-malaysia/?ajax=true&from=wangpu&isFirstRequest=true&langFlag=en&page={next_page}&pageTypeId=2&q=All-Products'
            # next_url = f'https://www.lazada.com.my/caring-estore/?ajax=true&from=wangpu&isFirstRequest=true&langFlag=en&page={next_page}&pageTypeId=2&q=All-Products'
            next_url = f' https://www.lazada.com.my/bellamys-flagship-store/?q=All-Products&from=wangpu&langFlag=en&pageTypeId=2'
            # next_url = f' https://www.lazada.co.id/beautyhaul-indonesia/?q=All-Products&from=wangpu&langFlag=en&pageTypeId=2&ajax=true&page={next_page}'
            # next_url = f'https://www.lazada.com.ph/zest-o-official-store/?ajax=true&from=wangpu&isFirstRequest=true&langFlag=en&page=1&pageTypeId=2&q=All-Products'
            print(f"Going to next page...{next_url}✅")
            meta = {
                "page": next_page,
                "source_id": source_id,
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
    # execute("scrapy crawl watsons_main -a retailer=lazada_my -a region=my -a Type=marketplace -a RetailerCode=lazada_watsons_my".split())
    # execute("scrapy crawl watsons_main -a retailer=lazada_ph -a region=ph -a Type=marketplace -a RetailerCode=lazada_watsons_ph".split())
    # execute("scrapy crawl watsons_main -a retailer=lazada_id -a region=id -a Type=eshop -a RetailerCode=lazada_watsons_id".split())
    # execute("scrapy crawl watsons_main -a retailer=lazada_my -a region=my -a Type=marketplace -a RetailerCode=lazada_bigpharmacy_my".split())
    # execute("scrapy crawl watsons_main -a retailer=lazada_my -a region=my -a Type=marketplace -a RetailerCode=lazada_guardian_my".split())
    # execute("scrapy crawl watsons_main -a retailer=lazada_my -a region=my -a Type=marketplace -a RetailerCode=lazada_mydin_my".split())
    # execute("scrapy crawl watsons_main -a retailer=lazada_my -a region=my -a Type=marketplace -a RetailerCode=lazada_caring_my".split())
    execute("scrapy crawl watsons_main -a retailer=lazada_my -a region=my -a Type=marketplace -a RetailerCode=lazada_my".split())
    # execute("scrapy crawl watsons_main -a retailer=lazada_id -a region=id -a Type=marketplace -a RetailerCode=lazada_id".split())
    # execute("scrapy crawl watsons_main -a retailer=lazada_ph -a region=ph -a Type=marketplace -a RetailerCode=lazada_ph".split())