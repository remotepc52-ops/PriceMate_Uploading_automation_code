import json
import math
import re, unicodedata
import time
from parsel import Selector
from urllib.parse import quote
import scrapy
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from pricemate.spiders.spider_lazada import PricemateBaseSpider

cookies = {
    '__wpkreporterwid_': '59107cab-a338-4bf3-17da-1548aa59d727',
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
    'xlly_s': '1',
    '_uetvid': '640c2b50c9be11f0b4b82d0a3e174b6e',
    '_ga_6VT623WX3F': 'GS2.3.s1765368848$o3$g1$t1765368860$j48$l0$h0',
    'cto_bundle': 'Flo9vV95Slh0RjIxdTdLVVNWbEJJVGZOQzVoSUhTZHZtZnhwZWV6N05rWFRNRFlVbjdYSUo3S0JNU3klMkJLJTJCR2JJNiUyQm9jNmRqZ3ZoSDV3dFZ1THZsR0dhb3JtNzdGcVdoWjFXM2ZJY0hzbDJmd3ExbU9CaW9WYWEwR2Z4a3FNOCUyRkF2b2cxU1gya3UyYmV4MkduTVBXeTIxRW1uQSUzRCUzRA',
    'isg': 'BObmTCr9s0hIwWfwPH9vxNOGN1xoxyqBBTA2YdCP0onkU4ZtOFd6kcwiq1dfeyKZ',
    'lzd_sid': '15a8c79907eb26a302ee75959885d3ac',
    '_tb_token_': 'e3bd385b97e33',
    'undefined_click_time': '1765513716656',
    '_m_h5_tk': '5697397d4e5ae1e172e68c7f9daad666_1765523438117',
    '_m_h5_tk_enc': '5911b15f2a782fe2484b88d299f6cde3',
    'x5sec': '7b22617365727665722d6c617a6164613b33223a22617c4350697a37736b474550476c724f76342f2f2f2f2f77456943584a6c5932467764474e6f5954436334636579413070714d44597759575a6d4d4441774d4441774d4441774d4441774e4441774d4441774d4441784d4441774d4441774d4441774d4441774e446b794e4459775a5445314d44566b4e44566c4d445533595463335a575130595441774d4441774d4441774d444530596d4e6c4e4759305a5445354e5445314d5751314d4467775954526c5957566a4e6a41334e47526d4e513d3d222c22733b32223a2261363264373863663166366361626334227d',
    't_sid': '78VVmbZITtcmrJlCK9aoRviuQFPnRsBV',
    'utm_channel': 'NA',
    'tfstk': 'f3ftg0sN0kqgfZVtUtw3mCAw7aUhW1QN9G7SinxihMIdPaoMhi2ahIIPDK1MsNXdMNxEiP5M1xNAYMaNjP7sDKsC0OYD1sBEMa7VsPR07C7wgIZuqSIA7NRqne4LysdBOET0ixG65l1KK4Euq7Vh5npriubif_gZIE-B5f9jGynB7FOX5AtbJHTvzxi1cITSrrzxlql61sL_iUQXE14kgFp9DAxIMWzD7dKN5HE7c6F6B3_69jE13WRMDH57xJQFoOsM8iF8vQ6PvspWM5nyW9_JOhA7evdO-G5J1_EtseAHjL6XpPN1JCK9hFJ8ilROhG5vQO34zwO1YT-yCJreJ1fkH3JKAl_hJh9RHg5dZ_p070xJoAaLJxk2Ce8somok4TUqHeKu-TDq3pbeJ34LJxk2Ce8pqyAo3xJh8',
    'epssw': '11*mmLkIm5GErUDfmma3uAk4z8YrQ9T5hEhxQpYKlIpM_7WKH0rM1k1RP85jzoZzr60PUJ6GRhmwqinvjeiart2Ltv0xBmHQOAZLweU7pbE_kovTOGvLOAmOTmiHHC75k6l3gGWIBavXBLKvUxCujIKlzAZ3eAxarA-gYV7nxx_QqD3meZ7ueVClo7nS2AXrgrVP7rHiqFoLAFqyxeEBCSdumJHRtuDmoWxOt6nuuuu2_pq0lK9cxUFF07CZun_mmm0EmQYsgpTBeaENZb3EREYNx2nXjZu0_aEEmEYNjaNXjSlGmBeuukmUtCzcDNYsHAYxSvBDpFrgVSJurmiEBe.',
    'lwrtk': 'AAIEaTzJszmrBS6YNJ0Cs7Y9IlboTc84qS3Zw6okY5qRAIst5af0TYc=',
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
    'x-csrf-token': 'e3bd385b97e33',
    # 'cookie': '__wpkreporterwid_=59107cab-a338-4bf3-17da-1548aa59d727; t_fv=1764323729914; t_uid=hEQZBLfPlbOS7CLCfRWMKlmObjvnhzwO; lwrid=AgGan%2Fc36WmdiDZV%2BOCTX39uI5Qx; hng=MY|en-MY|MYR|458; hng.sig=3PRPmcBmKLS4UwrxxIzxYKE2BjFcClNbRbYGSaUai_0; lzd_cid=b15e9aab-add0-403b-8209-41360905fa98; _bl_uid=gvm31i5Fi6zrhmf0n5kR28h15Cgs; _gcl_au=1.1.983622923.1764921604; cna=ZiqsIbfYC18CAS2FBBQqxhQD; _ga=GA1.3.1754007218.1764921606; _fbp=fb.2.1764921605952.606715168461176159; AMCV_126E248D54200F960A4C98C6%40AdobeOrg=-1124106680%7CMCIDTS%7C20432%7CMCMID%7C34947093032700580204267579038899530150%7CMCAAMLH-1765863295%7C12%7CMCAAMB-1765863295%7CRKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y%7CMCOPTOUT-1765265695s%7CNONE%7CvVersion%7C5.2.0; xlly_s=1; _uetvid=640c2b50c9be11f0b4b82d0a3e174b6e; _ga_6VT623WX3F=GS2.3.s1765368848$o3$g1$t1765368860$j48$l0$h0; cto_bundle=Flo9vV95Slh0RjIxdTdLVVNWbEJJVGZOQzVoSUhTZHZtZnhwZWV6N05rWFRNRFlVbjdYSUo3S0JNU3klMkJLJTJCR2JJNiUyQm9jNmRqZ3ZoSDV3dFZ1THZsR0dhb3JtNzdGcVdoWjFXM2ZJY0hzbDJmd3ExbU9CaW9WYWEwR2Z4a3FNOCUyRkF2b2cxU1gya3UyYmV4MkduTVBXeTIxRW1uQSUzRCUzRA; isg=BObmTCr9s0hIwWfwPH9vxNOGN1xoxyqBBTA2YdCP0onkU4ZtOFd6kcwiq1dfeyKZ; lzd_sid=15a8c79907eb26a302ee75959885d3ac; _tb_token_=e3bd385b97e33; undefined_click_time=1765513716656; _m_h5_tk=5697397d4e5ae1e172e68c7f9daad666_1765523438117; _m_h5_tk_enc=5911b15f2a782fe2484b88d299f6cde3; x5sec=7b22617365727665722d6c617a6164613b33223a22617c4350697a37736b474550476c724f76342f2f2f2f2f77456943584a6c5932467764474e6f5954436334636579413070714d44597759575a6d4d4441774d4441774d4441774d4441774e4441774d4441774d4441784d4441774d4441774d4441774d4441774e446b794e4459775a5445314d44566b4e44566c4d445533595463335a575130595441774d4441774d4441774d444530596d4e6c4e4759305a5445354e5445314d5751314d4467775954526c5957566a4e6a41334e47526d4e513d3d222c22733b32223a2261363264373863663166366361626334227d; t_sid=78VVmbZITtcmrJlCK9aoRviuQFPnRsBV; utm_channel=NA; tfstk=f3ftg0sN0kqgfZVtUtw3mCAw7aUhW1QN9G7SinxihMIdPaoMhi2ahIIPDK1MsNXdMNxEiP5M1xNAYMaNjP7sDKsC0OYD1sBEMa7VsPR07C7wgIZuqSIA7NRqne4LysdBOET0ixG65l1KK4Euq7Vh5npriubif_gZIE-B5f9jGynB7FOX5AtbJHTvzxi1cITSrrzxlql61sL_iUQXE14kgFp9DAxIMWzD7dKN5HE7c6F6B3_69jE13WRMDH57xJQFoOsM8iF8vQ6PvspWM5nyW9_JOhA7evdO-G5J1_EtseAHjL6XpPN1JCK9hFJ8ilROhG5vQO34zwO1YT-yCJreJ1fkH3JKAl_hJh9RHg5dZ_p070xJoAaLJxk2Ce8somok4TUqHeKu-TDq3pbeJ34LJxk2Ce8pqyAo3xJh8; epssw=11*mmLkIm5GErUDfmma3uAk4z8YrQ9T5hEhxQpYKlIpM_7WKH0rM1k1RP85jzoZzr60PUJ6GRhmwqinvjeiart2Ltv0xBmHQOAZLweU7pbE_kovTOGvLOAmOTmiHHC75k6l3gGWIBavXBLKvUxCujIKlzAZ3eAxarA-gYV7nxx_QqD3meZ7ueVClo7nS2AXrgrVP7rHiqFoLAFqyxeEBCSdumJHRtuDmoWxOt6nuuuu2_pq0lK9cxUFF07CZun_mmm0EmQYsgpTBeaENZb3EREYNx2nXjZu0_aEEmEYNjaNXjSlGmBeuukmUtCzcDNYsHAYxSvBDpFrgVSJurmiEBe.; lwrtk=AAIEaTzJszmrBS6YNJ0Cs7Y9IlboTc84qS3Zw6okY5qRAIst5af0TYc=',
}

class PetsmoreSpider(PricemateBaseSpider):
    name = "petsmore_main"

    def __init__(self, retailer, region, *args, **kwargs):
        super().__init__(retailer=retailer, region=region, *args, **kwargs)

    def start_requests(self):
        url = 'https://www.lazada.com.my/petsmore/?ajax=true&from=wangpu&isFirstRequest=true&langFlag=en&page=1&pageTypeId=2&q=All-Products'
        # url = 'https://www.lazada.com.my/aeon/?ajax=true&from=wangpu&isFirstRequest=true&langFlag=en&page=1&pageTypeId=2&q=All-Products'
        # url = 'https://www.lazada.com.my/tag/village-grocer/?ajax=true&catalog_redirect_tag=true&isFirstRequest=true&page=1&q=village%20grocer&spm=a2o4k.homepage.search.d_go'
        docs = self.category_input.find({
            # "retailer": self.retailer,
            # "region": self.region,
            "Status": "Pending"
        })
        for doc in docs:
            # url = doc["url"]
            hash_id = doc.get("_id")
            source_id = doc.get("source_id")
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
                # "hash_id": hash_id,
                # "source_id": source_id,
                "filename": f"PDP_{self.generate_hash_id(url)}.html",
                "page": 1,
                "should_be": ["mainInfo"]
            }

        )
    def parse_pdp(self, response):
        meta = response.meta
        hash_id = meta.get("hash_id")
        source_id = meta.get("source_id")

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
                # "Hash_id": hash_id,
                # "source_id": "f80e8d48-a5ec-4176-acd6-919cab558c32", #pets
                # "source_id": "4c01210a-f471-4d01-b263-24e3c9357d9b", #aeon
                "source_id": "dd646d39-7faa-446e-9575-9daa4a816f57", #village
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
                "retailer_name" : "lazada_petsmore_my",
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
            next_url = f'https://www.lazada.com.my/petsmore/?ajax=true&from=wangpu&isFirstRequest=true&langFlag=en&page={next_page}&pageTypeId=2&q=All-Products'
            # next_url = f'https://www.lazada.com.my/aeon/?ajax=true&from=wangpu&isFirstRequest=true&langFlag=en&page={next_page}&pageTypeId=2&q=All-Products'
            # next_url = f'https://www.lazada.com.my/tag/village-grocer/?ajax=true&catalog_redirect_tag=true&isFirstRequest=true&page={next_page}&q=village%20grocer&spm=a2o4k.homepage.search.d_go'
            print(f"Going to next page...{next_url}✅")
            meta = {
                "page": next_page,
                "source_id":source_id,
                "filename": f"PDP_{self.generate_hash_id(next_url)}_{next_page}.html",
                "should_be": ["mainInfo"]
            }

            yield scrapy.Request(url=next_url,
                                 callback=self.parse_pdp,
                                 meta=meta,
                                 )

            print(f"Product URL Inserted !")

    def close(self, reason):
        # import subprocess
        # cmd = [
        #     "python",
        #     "upload_to_s3_direct.py",
        #     "--domain", "lazada.com.my/petsmore"
        # ]
        # subprocess.run(cmd, cwd=r"E:\pricemate_service")
        self.mongo_client.close()

if __name__ == '__main__':
    from scrapy.cmdline import execute
    execute("scrapy crawl petsmore_main -a retailer=lazada_petsmore_my -a region=my -a Type=marketplace -a RetailerCode=lazada_petsmore_my".split())
    # execute("scrapy crawl petsmore_main -a retailer=lazada_my -a region=my -a Type=marketplace -a RetailerCode=lazada_aeon_my".split())
    # execute("scrapy crawl petsmore_main -a retailer=lazada_my -a region=my -a Type=marketplace -a RetailerCode=lazada_villagegrocer_my".split())