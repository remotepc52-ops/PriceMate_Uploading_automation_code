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
    '__wpkreporterwid_': '4711bc54-1bde-479b-099a-c656f6d01225',
    't_fv': '1764323729914',
    't_uid': 'hEQZBLfPlbOS7CLCfRWMKlmObjvnhzwO',
    'lwrid': 'AgGan%2Fc36WmdiDZV%2BOCTX39uI5Qx',
    'hng': 'MY|en-MY|MYR|458',
    'hng.sig': '3PRPmcBmKLS4UwrxxIzxYKE2BjFcClNbRbYGSaUai_0',
    'lzd_cid': 'b15e9aab-add0-403b-8209-41360905fa98',
    '_bl_uid': 'gvm31i5Fi6zrhmf0n5kR28h15Cgs',
    '_m_h5_tk': '40c056f24ca5300da01b22819c1c57d9_1764768324431',
    '_m_h5_tk_enc': 'c91bf1342734b2fcf5f4ce43fb7e301d',
    't_sid': 'x6t0LgekcQAsv28PGg3DgT4p7fpdgTQ5',
    'utm_channel': 'NA',
    'lwrtk': 'AAIEaTOJii9O5myQX6drZDwxoWqVJ/5KqtO9KO4C3flBy4lj2Qh79CQ=',
    'epssw': '11*mmLZsmdTdrWohmma3uflWvGrTtc4fYe0IvEGL3E4xdnLED8PPCWgEjTFCr4p9gLJmS3aoBhEu19_7BmmmmH-9uvOaOAZaOfvE4yZQ-ehOpDjEudsmTKWUqg35-pXgwrkzSxHR_AZEMV3aRAhgYV7nxx_emw3meSmBWx-TH7nSkLhrgO3Aq1ZiqnNsDRm4imEBWTHzRCJz_7smvFqQXemuu3m9ImmiIcqqJUFZK7CZ_wemmmpuuw_qsR6uc7YBZb2ucpYNx2nc6pYBBBmuu7EBBBBc6FA_tV7EmNEBjR5fYDiHRLGQXd_BmoDuuwe',
    'tfstk': 'gT-qJVtDqmn2gcVScQIaL_aPwWSAXGlIsh11IdvGhsf0coNMzQdaCxhtkU5wZQ7GlrscsOA6CAUjMI1M4CAJ5FMxH3Swp_R1GKMvaQTkyjhA1K6wNUY-MjKwBlWMICHA1x3WHKIOjXGB_D9vH6xinSc5jAvlfOrqbaT2HKITeVP3a3JxbOb4g1jMsgblptSGnsAGrafRBOVcIoDyE_Cln-bcnz2lKOw0oCjiULfRIGfMsZDyE_BGj1cSBNQnA9bmF2HhWvmXtZ5Hn_re93Wc-rpcaury4U7Vtj5zjlxP3dXbVTZE56YdGw1HZ0ZVbLXwawTqToRwIpLGzhPmhBAk7CXJyfzNTFvXJ3Q7Irvybs7HmaynppJAICbwyXrC3iTP8n8xB7vDOs8hDdwEGL7ezwBlrRzcce9BXwxm0WC5JORPRElU0BjPd5Blzyx9u54GoTBPOYkzl4viHSlhR-4TWZFlU6MvIPUOoTBPOYkzWPQxrT5IHdf..',
    'x5sec': '7b22617365727665722d6c617a6164613b33223a22617c43492b5078386b47454a6d34376f66392f2f2f2f2f77456943584a6c5932467764474e6f5954436334636579413070714d4459774f575a6d4d4441774d4441774d4441774d4441774d4441774d4441774d4441774d4441774d4441774d4441774d4441774e4459334e6d4e6c4e3255325a6a6b7a596a59344f445133595463335a575130595441774d4441774d4441774d4445304e7a566a4e7a63354e324d314d574a6c5a6d55324e6a41335957493459546c6a4d6d466a4e6d52684e773d3d222c22733b32223a2265356236653838383766323631623361227d',
}

headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
    'cache-control': 'max-age=0',
    'priority': 'u=0, i',
    'referer': 'https://www.lazada.com.my//starbucks-coffee-at-home//_____tmd_____/punish?x5secdata=xfVMATGLiLBlqA3SCPIarM5qP-_8Yts5zP8uERMRHW8AYqNRRt2VF36rTF3V8gPzM0mAiLFrmA4YxxfWHB38ck6szcMhWFFGtE0TdB3Lv_zT_gnQ7RIz6upkgtG_IszLwC4IxdtaBbz-i4Iq8PF8ZGhUkZVPJgs7pcnp0GcQ8TUeX5Xl03_wN2SZM_IGYgFn0SO1v-1h2cwn8W7UNTqeqofKNZZ0VWT9ufJwbC3uCP15m8x7awcuOcvcV4izuoWzNeKKkGictdewcallW9F07ASiFD_OmdvnGjDR9FCy4lScKVDkUWQ55sX19HQOGJAk1i1JXIP3MXU5zG4BBJhCbgoXh9AE_0aJeDSpYbgHyPww8v_oZK6mA3DrCOU8mTel9Cyc6w_2PViDu99asuqI0hNnPeiuRMT77hqFPtpKbBrZdCVBpMxs1qdo38FthBo1zGAOzxHhlSoaN7IPDD9v8LFu9YscGzA5qszhHVm69d8BeL-ZxqWuUQLzIKfTSTYCQioQ62A9J33FBdwCyd9dItryUUfRfe9jmDK4ycLIkwaaMopL8gNWozldDgSoBhmN-wRshZHCdmsvHqolMuy07z58Asfo5OcWzh4pyN_hCpyjFnRQ6nSZP6yuCXam4fsTGIZYOryRnaze3AC3kCr2KrHPunOznQK74YOgIOlgFVYLji0OIB4SYabgi4r6VKa0iF8SEYSj4cqwzHJJalIvHYTQ__bx__www.lazada.com.my%2fstarbucks-coffee-at-home%2f&x5step=1',
    'sec-ch-ua': '"Chromium";v="142", "Google Chrome";v="142", "Not_A Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36',
    # 'cookie': '__wpkreporterwid_=4711bc54-1bde-479b-099a-c656f6d01225; t_fv=1764323729914; t_uid=hEQZBLfPlbOS7CLCfRWMKlmObjvnhzwO; lwrid=AgGan%2Fc36WmdiDZV%2BOCTX39uI5Qx; hng=MY|en-MY|MYR|458; hng.sig=3PRPmcBmKLS4UwrxxIzxYKE2BjFcClNbRbYGSaUai_0; lzd_cid=b15e9aab-add0-403b-8209-41360905fa98; _bl_uid=gvm31i5Fi6zrhmf0n5kR28h15Cgs; _m_h5_tk=40c056f24ca5300da01b22819c1c57d9_1764768324431; _m_h5_tk_enc=c91bf1342734b2fcf5f4ce43fb7e301d; t_sid=x6t0LgekcQAsv28PGg3DgT4p7fpdgTQ5; utm_channel=NA; lwrtk=AAIEaTOJii9O5myQX6drZDwxoWqVJ/5KqtO9KO4C3flBy4lj2Qh79CQ=; epssw=11*mmLZsmdTdrWohmma3uflWvGrTtc4fYe0IvEGL3E4xdnLED8PPCWgEjTFCr4p9gLJmS3aoBhEu19_7BmmmmH-9uvOaOAZaOfvE4yZQ-ehOpDjEudsmTKWUqg35-pXgwrkzSxHR_AZEMV3aRAhgYV7nxx_emw3meSmBWx-TH7nSkLhrgO3Aq1ZiqnNsDRm4imEBWTHzRCJz_7smvFqQXemuu3m9ImmiIcqqJUFZK7CZ_wemmmpuuw_qsR6uc7YBZb2ucpYNx2nc6pYBBBmuu7EBBBBc6FA_tV7EmNEBjR5fYDiHRLGQXd_BmoDuuwe; tfstk=gT-qJVtDqmn2gcVScQIaL_aPwWSAXGlIsh11IdvGhsf0coNMzQdaCxhtkU5wZQ7GlrscsOA6CAUjMI1M4CAJ5FMxH3Swp_R1GKMvaQTkyjhA1K6wNUY-MjKwBlWMICHA1x3WHKIOjXGB_D9vH6xinSc5jAvlfOrqbaT2HKITeVP3a3JxbOb4g1jMsgblptSGnsAGrafRBOVcIoDyE_Cln-bcnz2lKOw0oCjiULfRIGfMsZDyE_BGj1cSBNQnA9bmF2HhWvmXtZ5Hn_re93Wc-rpcaury4U7Vtj5zjlxP3dXbVTZE56YdGw1HZ0ZVbLXwawTqToRwIpLGzhPmhBAk7CXJyfzNTFvXJ3Q7Irvybs7HmaynppJAICbwyXrC3iTP8n8xB7vDOs8hDdwEGL7ezwBlrRzcce9BXwxm0WC5JORPRElU0BjPd5Blzyx9u54GoTBPOYkzl4viHSlhR-4TWZFlU6MvIPUOoTBPOYkzWPQxrT5IHdf..; x5sec=7b22617365727665722d6c617a6164613b33223a22617c43492b5078386b47454a6d34376f66392f2f2f2f2f77456943584a6c5932467764474e6f5954436334636579413070714d4459774f575a6d4d4441774d4441774d4441774d4441774d4441774d4441774d4441774d4441774d4441774d4441774d4441774e4459334e6d4e6c4e3255325a6a6b7a596a59344f445133595463335a575130595441774d4441774d4441774d4445304e7a566a4e7a63354e324d314d574a6c5a6d55324e6a41335957493459546c6a4d6d466a4e6d52684e773d3d222c22733b32223a2265356236653838383766323631623361227d',
}

class StarbucksSpider(PricemateBaseSpider):
    name = "starbucks_main"

    def __init__(self, retailer, region, *args, **kwargs):
        super().__init__(retailer=retailer, region=region, *args, **kwargs)

    def start_requests(self):
        url = 'https://www.lazada.com.my/starbucks-coffee-at-home/?ajax=true&from=wangpu&langFlag=en&page=1&pageTypeId=2&q=All-Products'

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
                "retailer_name" : "lazada_starbucks_my",
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
            next_url = f'https://www.lazada.com.my/starbucks-coffee-at-home/?ajax=true&from=wangpu&langFlag=en&page={next_page}&pageTypeId=2&q=All-Products'
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
    execute("scrapy crawl starbucks_main -a retailer=lazada_my -a region=my -a Type=marketplace -a RetailerCode=lazada_my".split())