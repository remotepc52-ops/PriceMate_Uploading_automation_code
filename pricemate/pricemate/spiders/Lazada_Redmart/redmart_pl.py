import json
import math
import scrapy
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from pricemate.spiders.base_spider import PricemateBaseSpider

cookies = {
    '__wpkreporterwid_': '1f3ec99f-9ef5-4a00-26ad-418af9157910',
    'hng': 'SG|en-SG|SGD|702',
    'hng.sig': 'ryBKXOqZIsp9xOQ3YsZRgD7f-p0UaGB2pZ4BbZM8uEc',
    'lzd_cid': '6a3e0b1f-2649-4387-8eb9-068f8ba2d7d5',
    't_fv': '1759833970174',
    't_uid': 'IiZlFPb28kS76EuTzddB9lVXXVR3hjpi',
    'lwrid': 'AgGZvkdWsHwo2%2F2J6HE1X38RnKx3',
    'x5sec': '7b22617365727665722d6c617a6164613b33223a22307c434e4c6167636747454f544a75737a382f2f2f2f2f774577783853592b2f6e2f2f2f2f2f41513d3d222c22733b32223a2263663331613937616538376430316362227d',
    'lzd_sid': '1f1ed7a03988d726f0c433268e34adbf',
    '_tb_token_': '735f5ebb58716',
    't_sid': 'uwdbnXcTyT1hhjnJw1u3N5pU8uB43lVb',
    'utm_channel': 'NA',
    '_m_h5_tk': 'b7246f56154c0d8a54b9c24b58dec9ce_1761645137806',
    '_m_h5_tk_enc': 'd7607d9321b1c8997959562bc59bc914',
    'lwrtk': 'AAIEaQDeQXfPn1aH9pTHHoFwJGwk4l0XsJsHk0lc9hXWj0QcgLMq2wA=',
    'isg': 'BKamGQ0z8zGB96ZxL8bERwp39xwoh-pBR7VFNZBPmUmkE0Yt-RSUU1Poaxefu-JZ',
    'tfstk': 'fLLHrqDs1HSBp0yhGcbIx9bVg2oOJJ_5nLUReaBrbOW1wHHW9ajyGOQ-OunCZaXMNpBFpUpkaOpRpJpRpdVBSK48JviBazbRzxHxkqdiOa_rHt8HcFBCNCWPKSGo-B_5zAI9kI4MOpQPvZ1lzfbNa_ePzy5y_ffRtT7PLgyabsWNUUi3p4XuZeFhmt2Rudr9wqAl3BWeeLTNw-B2Ttazz9fhxmAFIzyy73SH-OWEc5B5J991tLgbRwSk4eQw8AuPun9Mri7m2XseZhv5JFlzYt-ppgTCjJrFiwXh0eSnPX_14hYGJek7cCdGLib9XcMd2wvHctsEfA9ks9py-Gyh4mZa06zgP1lJ7uZ5Y11GHECE_Ls-ySiisfq4RM51OKL-suruhzz8Yfcg0GsF169R.',
    'epssw': '10*9iyss6YtX00Z_s3sbRFeOIrRoRPgAqsGA8cDbjlYsshssRX9UNsus7MAICiQOND0UNdssR32UsUjx1iVojCCs3vpwtNwkr1dcTCyssFOt123zFsfkaDsmbelOsRtOObazRO7qGbJULq5rhaR4rFJ-OtNOehr689THdBmaq6LeSiPFsKIiSnKhsopUbthQCCRT7zP-Ob_uCpnKQKxvxaipdXGyVw7O-JZnMjPssFbORFeshuL36FtbsOOs7e4t_DC9fNoy_uKg7URO3KQlTylTZy7ATNfaFSU4uVeEqjUr-HA4cofZvCf8KBsGpZnss..',
}

headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'en-US,en;q=0.9,en-IN;q=0.8',
    'priority': 'u=1, i',
    'referer': 'https://redmart.lazada.sg/',
    'sec-ch-ua': '"Microsoft Edge";v="141", "Not?A_Brand";v="8", "Chromium";v="141"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36 Edg/141.0.0.0',
    # 'cookie': '__wpkreporterwid_=1f3ec99f-9ef5-4a00-26ad-418af9157910; hng=SG|en-SG|SGD|702; hng.sig=ryBKXOqZIsp9xOQ3YsZRgD7f-p0UaGB2pZ4BbZM8uEc; lzd_cid=6a3e0b1f-2649-4387-8eb9-068f8ba2d7d5; t_fv=1759833970174; t_uid=IiZlFPb28kS76EuTzddB9lVXXVR3hjpi; lwrid=AgGZvkdWsHwo2%2F2J6HE1X38RnKx3; x5sec=7b22617365727665722d6c617a6164613b33223a22307c434e4c6167636747454f544a75737a382f2f2f2f2f774577783853592b2f6e2f2f2f2f2f41513d3d222c22733b32223a2263663331613937616538376430316362227d; lzd_sid=1f1ed7a03988d726f0c433268e34adbf; _tb_token_=735f5ebb58716; t_sid=uwdbnXcTyT1hhjnJw1u3N5pU8uB43lVb; utm_channel=NA; _m_h5_tk=b7246f56154c0d8a54b9c24b58dec9ce_1761645137806; _m_h5_tk_enc=d7607d9321b1c8997959562bc59bc914; lwrtk=AAIEaQDeQXfPn1aH9pTHHoFwJGwk4l0XsJsHk0lc9hXWj0QcgLMq2wA=; isg=BKamGQ0z8zGB96ZxL8bERwp39xwoh-pBR7VFNZBPmUmkE0Yt-RSUU1Poaxefu-JZ; tfstk=fLLHrqDs1HSBp0yhGcbIx9bVg2oOJJ_5nLUReaBrbOW1wHHW9ajyGOQ-OunCZaXMNpBFpUpkaOpRpJpRpdVBSK48JviBazbRzxHxkqdiOa_rHt8HcFBCNCWPKSGo-B_5zAI9kI4MOpQPvZ1lzfbNa_ePzy5y_ffRtT7PLgyabsWNUUi3p4XuZeFhmt2Rudr9wqAl3BWeeLTNw-B2Ttazz9fhxmAFIzyy73SH-OWEc5B5J991tLgbRwSk4eQw8AuPun9Mri7m2XseZhv5JFlzYt-ppgTCjJrFiwXh0eSnPX_14hYGJek7cCdGLib9XcMd2wvHctsEfA9ks9py-Gyh4mZa06zgP1lJ7uZ5Y11GHECE_Ls-ySiisfq4RM51OKL-suruhzz8Yfcg0GsF169R.; epssw=10*9iyss6YtX00Z_s3sbRFeOIrRoRPgAqsGA8cDbjlYsshssRX9UNsus7MAICiQOND0UNdssR32UsUjx1iVojCCs3vpwtNwkr1dcTCyssFOt123zFsfkaDsmbelOsRtOObazRO7qGbJULq5rhaR4rFJ-OtNOehr689THdBmaq6LeSiPFsKIiSnKhsopUbthQCCRT7zP-Ob_uCpnKQKxvxaipdXGyVw7O-JZnMjPssFbORFeshuL36FtbsOOs7e4t_DC9fNoy_uKg7URO3KQlTylTZy7ATNfaFSU4uVeEqjUr-HA4cofZvCf8KBsGpZnss..',
}

class RedmartPlSpider(PricemateBaseSpider):
    name = "redmart_pl"

    def __init__(self, retailer, region, *args, **kwargs):
        super().__init__(retailer=retailer, region=region, *args, **kwargs)
        self.api_key = "21ed11ef5c872bc7727680a52233027db4578a0e"
        self.zenrows_url = "https://api.zenrows.com/v1/"

    def start_requests(self):
        docs = self.category_input.find({
            "retailer": self.retailer,
            "region": self.region,
            "Status": "Pending"
        })

        for doc in docs:
            url = doc["url"]
            hash_id = doc.get("_id")
            slug = url.split("/")[-2]

            meta = {
                "proxy": "http://21ed11ef5c872bc7727680a52233027db4578a0e:@api.zenrows.com:8001",
                "cat_url": url,
                "_id": hash_id,
                "slug": slug,
                "page":1,
                "filename": f"{slug}_page.html",
                "should_be": ["mods"]
            }
            yield scrapy.Request(
                url=f'https://redmart.lazada.sg/{slug}/?ajax=true&m=redmart&page=1',
                cookies=cookies,
                headers=headers,
                callback=self.parse_pdp,
                meta=meta
            )

    def parse_pdp(self, response):
        meta = response.meta
        doc_id = meta.get('_id')
        slug = meta.get('slug')
        current_page = meta.get("page", 1)

        # try:
        #     data = json.loads(response.text)
        # except Exception as e:
        #     self.logger.error(f"JSON failed : {e}")
        #     return
        # list_items = data.get('mods', {}).get('listItems', [])
        # for item in list_items:
        #     prod_code = item.get('itemId')
        #     name = item.get('name')
        #     pdp_url = item.get('productUrl')
        #     brand = item.get('brandName')
        #     price = item.get('priceShow').replace('$', '').replace(',', '')
        #     was_price = item.get('originalPriceShow').replace('$', '').replace(',', '')
        #     if not was_price:
        #         rrp = price
        #         was_price = ""
        #     else:
        #         was_price = was_price
        #         rrp = was_price
        #
        #
        #     breadcrumb_items = data.get('mods', {}).get('breadcrumb', [])
        #     breadcrumb_titles = [crumb.get('title') for crumb in breadcrumb_items]
        #     bread = ' > '.join(breadcrumb_titles)
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
                    discount = pdp_data['discount']
                    pack_size = pdp_data['packageInfo']
                except:
                    discount = ""
                    pack_size = ""
                try:
                    product_url = pdp_data['itemUrl'].split("?")[0]
                except:
                    product_url = pdp_data['productUrl'].split("?")[0]

                if not str(product_url).startswith("https"):
                    product_url = f"https:{product_url}"

                seller_name = pdp_data['sellerName']
                # seller_url = f"{domain}/{seller_name.lower().replace(' ', '-')}/?q=All-Products&from=wangpu&langFlag=en&pageTypeId=2"

                try:
                    originalPrice = float(pdp_data['originalPrice'])
                    unit_price = pdp_data['unitPrice']
                except:
                    originalPrice = ""
                    unit_price = ""

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
                "source_id": "816ea913-47a2-4c0b-83dc-c46e7c786613",
                "ProductCode": skuId,
                "ParentCode": Parent_Id,
                "ProductURL": product_url,
                "Name": Product_Name,
                "Brand": brand,
                "Price": salePrice,
                "WasPrice": originalPrice,
                "Category_Hierarchy":bread,
                "is_available": True if not isOos else False,
                "Status": "Done",
                "Images": img,
                "Pack_size": pack_size,
                "RRP": rrp,
                "Offer_info": discount,
                "Promo_Type": "",
                "per_unit_price": unit_price,
                "Barcode": "",
                "retailer": self.retailer,
                "region": self.region,
                "retailer_name" : "lazada_redmart_sg",
            }
                self.save_product(item)
                print(f"Product URL Inserted !")

        main_info = loaded_json.get('mainInfo', {})
        total_results = int(main_info.get('totalResults', 0))
        page_size = int(main_info.get('pageSize', 40))
        current_page = int(main_info.get('page', 1))

        total_pages = math.ceil(total_results / page_size)

        if current_page < total_pages:
            next_page = current_page + 1
            next_url = f'https://redmart.lazada.sg/{slug}/?ajax=true&m=redmart&page={next_page}'

            meta = {
                "_id": doc_id,
                "slug": slug,
                "page": next_page,
                "filename": f"{slug}_{next_page}_page.html",
                "should_be": ["mods"]
            }

            yield scrapy.Request(url=next_url,
                                 callback=self.parse_pdp,
                                 meta=meta,
                                 )
            self.category_input.update_one(
                {"_id": doc_id},
                {"$set": {"Status": "Done"}}
            )
            print(f"Product URL Inserted !")

    def close(self, reason):
        import subprocess
        cmd = [
            "python",
            "upload_to_s3_direct.py",
            "--domain", "redmart.lazada.sg"
        ]
        subprocess.run(cmd, cwd=r"E:\pricemate_service")
        self.mongo_client.close()

if __name__ == '__main__':
    from scrapy.cmdline import execute
    execute("scrapy crawl redmart_pl -a retailer=lazada_redmart_sg -a region=sg -a Type=eshop -a RetailerCode=lazada_redmart_sg".split())