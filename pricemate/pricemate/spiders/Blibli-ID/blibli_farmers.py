import json
import re, unicodedata
import time
from parsel import Selector
from urllib.parse import quote
import scrapy
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from pricemate.spiders.spider_lazada import PricemateBaseSpider

cookies = {
    'Blibli-Device-Id': 'U.4d836901-f297-4225-811a-9be7e80cd5e0',
    'Blibli-Device-Id-Signature': '0bf8744622cac44b0cc744d63eb1189ee684696d',
    'blibli-location': '-6.1792189,106.8189094',
    '_gcl_au': '1.1.1579204044.1764157954',
    '__bwa_user_id': '1764157954.e42ce694-e5ef-4058-9c35-5c9e44167191',
    '_fbp': 'fb.1.1764157954561.296307953373334781',
    '_tt_enable_cookie': '1',
    '_ttp': '01KB0046J2A52H5ECET2CDNZ92_.tt.1',
    'afUserId': '31b650c1-7e98-42f6-8b74-f4c2ffc877d2-p',
    '_ga': 'GA1.2.172126548.1764157954',
    'ttcsid': '1764157954630::8hzNaiEM4Ych90YJdSxz.1.1764157956731.0',
    'ttcsid_C38OU43TAIRUEDS4L1L0': '1764157954629::serSJLYmohoBeYeSOa_x.1.1764157956731.0',
    'moe_uuid': '6fef390b-27a3-4d1d-bafe-60d855ffbc02',
    '_ce.s': 'v~92a670856ea4195a27f6fc7ecf27df9a548c3b10~lcw~1764157956905~vir~new~lva~1764157956757~vpv~0~v11.cs~295312~v11.s~66fdee40-cabe-11f0-9985-8b003ee6ee03~v11.vs~92a670856ea4195a27f6fc7ecf27df9a548c3b10~v11.fsvd~eyJ1cmwiOiJibGlibGkuY29tL3AvKi8qIiwicmVmIjoiIiwidXRtIjpbXX0%3D~v11.sla~1764157956902~v11.ss~1764157956905~v11ls~66fdee40-cabe-11f0-9985-8b003ee6ee03~lcw~1764157956909',
    '_ga_G3ZP2F3MW9': 'GS2.1.s1764157954$o1$g1$t1764157957$j57$l0$h1403243900',
    'Blibli-User-Id': '48ed88c4-4d3b-4a38-810d-7843ec9ac033',
    'Blibli-Is-Member': 'false',
    'Blibli-Is-Remember': 'false',
    'Blibli-Session-Id': 'e3ac74b0-3eb4-4ef8-b363-f50154795cc3',
    'Blibli-Signature': 'ee0275d893fd79fff71d973cd1e34f2cea9a0819',
    '__bwa_session_id': '1767675682.041c3c67-c909-415c-a101-c370d7cc58ad',
    '__cf_bm': 'ImxNPXqWp04.pfkokdhwMSGCsTDqykeZ.ExgjWW3pGQ-1767675838-1.0.1.1-QD6mTfiSWjPeo2KoSOcsjsGa0cxEWv79pv.3XuVXAoY0jNNy0NwRPwZSNAPxuRW2tyHwDi7GSj1gI3tQE.UjnFkcmyGkdVHxqTquHEA44Xg',
    '_cfuvid': 'f_GKvntL0AlnBeY_mtJDXj9aBIXHQKeo.WtMZoKK.xc-1767675838370-0.0.1.1-604800000',
    'cf_clearance': 'RA97GT1JDRpf0KpmtVcbDJ9lViSZfKO2ZV5mR3XVS7Y-1767675903-1.2.1.1-P00YqWr5bS4LcW.4aoh5ZelUEcFgE48MJqvHoeDQHtdt8YHVOJsX3SRarVEq8ICCry6o19LqNyOkvMerW3mWj86dDQwq6HWbkqJ2Ei.L38kznCmVj9_t4H7vT2tzkdsaeU4OdUUn7JVE6vS49ZoioN_xnuQun2fW22Zb64H7w1tNiFEOPw8li50yDtGrg5eCOic7aKysxuYYtDvtdbWuJn4rasizekGXERYy774FJFg',
    'g_state': '{"i_l":0,"i_ll":1767676057078,"i_b":"wD6Xv1+Rd2FOQsryQAq/lRBKBoDGJJDOEtNw1Hn4KIE","i_e":{"enable_itp_optimization":0}}',
    'Blibli-dv-token': 'JT_1mtlJkEYGrb2Y9vq7OKAbDynyOeCaX82UVlJlXuoUhC',
    'forterToken': 'fd13a7cc1f2f49c49cab5b6013fdd6ff_1767676057111__UDF43-m4_25ck_',
}

headers = {
    'Accept': 'application/json, text/plain, */*',
    # 'Accept-Encoding': 'gzip, deflate, br, zstd',
    'Accept-Language': 'en-US,en;q=0.9',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    # 'Cookie': '__cf_bm=Y7NIy3lF5I0va5bZDisIGgEIhfMfjHlhbxBFtV5lYkI-1759128822-1.0.1.1-MhAW37OvgTCBbzoWrY7FjK.lF2B_Db75au2ypUG5hjXrixTmrkYaMIuh7k0XDz.yWyrt1TV2hUT.hJUCbxs6tECGvIZ5r6e1lDvkfVZx.RA; _cfuvid=43ysba7IRvIVEQjehUAxkvv0hxXYCnQRfJZCiJFAHLU-1759128822635-0.0.1.1-604800000; cf_clearance=SYcs.aM94MYZQE7zmy9WQV5LL9nsgzNnzrLKSyR4n7Q-1759128824-1.2.1.1-EKrKSr8R9nJVfkOkqIK6MlgMr8En_EhzgROVJ52D9SWqZJ9.ABsHQOTKrdHr_urKWjbchQqYoUKZK8peXf3zQfTfGHzamq9Icn9tlEDaGkNC1JtXE3wdCVpCeTKWbOYxP7KFotiaTNeOn3.HZp0ZTlmx17irE1qmq1JbJmRlL2cnEJw04ScSco409KT_Gs_APDrTsfXsOFrxhcPvZyIWf.1_Vo6WtTF4ZEqKyKw0mOg; Blibli-Additional-Parameter-Signature=; Blibli-Is-Member=false; Blibli-Is-Remember=false; Blibli-Device-Id=U.275ab4e2-57e1-405f-8314-f0a11526aaf6; Blibli-Device-Id-Signature=9c89794dcd7998f2270ee4a5733d66911fba3290; Blibli-Session-Id=0e000973-9e65-479e-bbe3-2e78589b6ca8; Blibli-Signature=52130cf66a218adde225f20f3a9dab229b7af5c1; Blibli-User-Id=0e000973-9e65-479e-bbe3-2e78589b6ca8; Blibli-Unm-Signature=5b9bfc34dd973697f7325e006da1d60b3bafa34d; Blibli-Unm-Id=0e000973-9e65-479e-bbe3-2e78589b6ca8; Blibli-dv-token=JT_0ruW5SgdVerJLk36zqg6w2idjNwfX8FW3RgHETi5Gv_; forterToken=73a8483943384833b4d2a7c8dc580f70_1759129202012__UDF43-m4_25ck_',
    'Host': 'www.blibli.com',
    'Referer': 'https://www.blibli.com/',
    'sec-ch-ua': '"Chromium";v="140", "Not=A?Brand";v="24", "Google Chrome";v="140"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36',
}

class BlibliShopSpider(PricemateBaseSpider):
    name = "blibli_farmers"

    def __init__(self, retailer, region, *args, **kwargs):
        super().__init__(retailer=retailer, region=region, *args, **kwargs)

    @staticmethod
    def extract_size(size_string):
        try:
            if not size_string:
                return ""
            size_string = size_string.strip()

            # 1️⃣ Size: 200ml / Pack Size: 2kg
            pattern1 = r'(?:Size|Pack Size)[:\s]*([\d.,]+)\s*(ml|mL|l|L|g|kg|oz|lb|packs?|pack|tablets?|capsules?|pcs?|butir)'
            match = re.search(pattern1, size_string, re.IGNORECASE)
            if match:
                return f"{match.group(1)} {match.group(2)}"

            # 2️⃣ Simple number + unit (200ml, 2kg, 10pcs, 15 butir, 500 gr)
            pattern2 = r'([\d.,]+)\s*(ml|mL|l|L|g|gr|kg|oz|lb|pcs?|butir|biji|tablet|capsule|pack|packs?)'
            match = re.search(pattern2, size_string, re.IGNORECASE)
            if match:
                return f"{match.group(1)} {match.group(2)}"

            # 3️⃣ Multi-pack like "90g×2" or "200 ml x 3" or "10pcs x 2"
            pattern3 = r'([\d.,]+)\s*(ml|mL|l|L|g|gr|kg|oz|lb|pcs?|butir)\s*[×xX]\s*(\d+)'
            match = re.search(pattern3, size_string, re.IGNORECASE)
            if match:
                return f"{match.group(1)} {match.group(2)} x {match.group(3)}"

            # 4️⃣ Just quantity like "isi 10", "10 pcs", "15 butir"
            pattern4 = r'(?:isi\s*)?(\d+)\s*(pcs?|butir|biji|pack|packs?|tablet|capsule)?'
            match = re.search(pattern4, size_string, re.IGNORECASE)
            if match:
                qty = match.group(1)
                unit = match.group(2) if match.group(2) else ""
                return f"{qty} {unit}".strip()

            # 5️⃣ Composite like "2x10pcs" or "3x200ml"
            pattern5 = r'(\d+)\s*[×xX]\s*([\d.,]+)\s*(ml|mL|l|L|g|gr|kg|pcs?|butir)'
            match = re.search(pattern5, size_string, re.IGNORECASE)
            if match:
                return f"{match.group(1)} x {match.group(2)} {match.group(3)}"

            # fallback → return raw text if it looks like size
            if any(u in size_string.lower() for u in ["ml", "g", "kg", "pcs", "butir", "isi", "pack"]):
                return size_string

            return ""

        except Exception as e:
            print(f"Error extracting size: {e}")
            return ""
    def start_requests(self):
        # docs = self.category_input.find({
        #     "Platform": self.retailer,
        #     "Country": self.region,
        #     "Status": "Pending"
        # })
        # url = 'https://www.blibli.com/merchant/farmers-market-flagship-store/FAM-70080?pickupPointCode=PP-3536528&fbbActivated=false&promoTab=false&excludeProductList=false'
        # for doc in docs:
        #     url = doc["url"]
        #     hash_id = doc.get("_id")
        slug = "farmers-market-flagship-store"

        meta = {
            "page":1,
            "filename": f"{slug}_page.json",
            "should_be": ["data"]
        }
        yield scrapy.Request(
            url=f'https://www.blibli.com/backend/search/merchant/FAM-70080?excludeProductList=false&promoTab=false&pickupPointCode=PP-3536528&fbbActivated=false&page=1&start=40&sort=7&multiCategory=true&merchantSearch=false&pickupPointLatLong=&defaultPickupPoint=true&showFacet=false',
            headers=headers,
            callback=self.parse_pdp,
            meta=meta
        )

    def parse_pdp(self, response):
        meta = response.meta
        current_page = meta.get("page", 1)

        try:
            main_data = response.json()
        except Exception as e:
            self.logger.error(f"JSON failed : {e}")
            return
        products = main_data.get("data", {}).get("products", [])
        if not products:
            self.logger.info(f"No products found on page {current_page}, stopping pagination.")
            return

        page_size = 40  # Blibli usually returns 40 items per page

        for idx, data in enumerate(products, start=1):
            # global rank = ((page-1) * page_size) + index_on_page
            rank = ((current_page - 1) * page_size) + idx
            name = data.get("name")
            parent_code = data.get("itemSku")
            prod_code = data.get("sku")
            brand = data.get("brand")
            # if brand == "no brand":
            #     brand = ""
            product_url = data.get("url")
            bread = " > ".join(data.get("categoryNameHierarchy", []))
            img = " | ".join(data.get("images", []))

            price_list = data.get("price", {})
            discount = price_list.get("discount")
            if discount == 0:
                discount = ""
            else:
                discount = f'{discount} %'
            original_price = price_list.get("salePrice")
            was_price = price_list.get("listPrice")
            if was_price == original_price:
                rrp = original_price
                was_price = ""
            else:
                rrp = was_price

            pack_size = self.extract_size(name)
            review = data.get("review",{})
            count = review.get("count")
            avg_rating = review.get("sellerRating")
            item_sold = data.get("soldCountTotal")
            stock = data.get("status")
            if stock == "AVAILABLE":
                stock = True
            else:
                stock = False
            # barcode = data.get("level0Id")
            ads_tags = [tag.lower() for tag in data.get("productLabelTags", [])]
            if "sponsored" in ads_tags or "ads" in ads_tags:
                traffic_type = "Paid"
            else:
                traffic_type = "Organic"
            #store details
            store_name = data.get("merchantName")
            seller_id = data.get("merchantCode")
            store_slug = re.sub(r'[\s_]+', '-',re.sub(r"[^\w\s-]", '', unicodedata.normalize('NFKD', store_name or '').lower())).strip('-')
            sell_id = f"ID.BLB.{seller_id}"
            store_url = f"https://www.blibli.com/merchant/{store_slug}/{seller_id}"
            promo_type = "|".join(data.get("productLabelTags", []))
            product_hash = self.generate_hash_id(product_url, self.retailer, self.region)

            item = {
                "_id": product_hash,
                "source_id" : "0708122b-c59e-4270-a346-dd38e41dd76f",
                # "Keyword": "",
                # "Organic/Paid": traffic_type,
                # "Ranking": rank,
                # "Store name": store_name,
                # "Store URL": store_url,
                "Name": name,
                "Promo_Type": promo_type,
                # "Currency":"Rp",
                # "Seller ID": sell_id,
                "Price": original_price,
                "per_unit_price": "",
                "WasPrice": was_price,
                "Offer_info": discount,
                # "Monthly Item Sold": "",
                "Pack_size": pack_size,
                "Barcode": "",
                "is_available": stock,
                "Images": img,
                "ProductURL": f'https://www.blibli.com{product_url}',
                "Status": "Done",
                "ParentCode": "",
                "ProductCode": prod_code,
                "retailer_name": "farmersmarket_id",
                "Category_Hierarchy": bread,
                "Brand": brand,
                "RRP": rrp,
                # "Avg Rating": avg_rating,
                # "Total Review": count,
                # "Historical Item Sold": item_sold,
                # "Country":"ID",
                # "Platform":"Blibli",
            }

            try:
                self.save_product(item)
                print(f"✓ Successfully inserted {product_url}")
            except Exception as e:
                print(e)

        next_page = current_page + 1
        slug = "farmers-market-flagship-store"

        next_url = (
            f'https://www.blibli.com/backend/search/merchant/FAM-70080?excludeProductList=false&promoTab=false&pickupPointCode=PP-3536528&fbbActivated=false&page={next_page}&start={(next_page - 1) * page_size}&sort=7&multiCategory=true&merchantSearch=false&pickupPointLatLong=&defaultPickupPoint=true&showFacet=false'
        )

        meta = {
            "url": next_url,
            "slug": slug,
            "page": next_page,
            "filename": f"{slug}_{next_page}_page.json",
            "should_be": ["data"]
        }

        yield scrapy.Request(
            url=next_url,
            headers=headers,
            callback=self.parse_pdp,
            meta=meta
        )

    def close(self, reason):
        # import subprocess
        #
        # cmd = [
        #     "python",
        #     "upload_to_s3_direct.py",
        #     "--domain", "blibli.com"
        # ]
        #
        # subprocess.run(cmd, cwd=r"E:\pricemate_service")
        self.mongo_client.close()

if __name__ == '__main__':
    from scrapy.cmdline import execute
    execute( "scrapy crawl blibli_farmers -a retailer=farmersmarket_id -a region=id -a Type=marketplace -a RetailerCode=farmersmarket_id".split())