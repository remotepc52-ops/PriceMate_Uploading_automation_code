import json
import re, unicodedata
import time
from parsel import Selector
from urllib.parse import quote
import scrapy
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from pricemate.spiders.base_spider import PricemateBaseSpider

cookies = {
    '__cf_bm': 'Y7NIy3lF5I0va5bZDisIGgEIhfMfjHlhbxBFtV5lYkI-1759128822-1.0.1.1-MhAW37OvgTCBbzoWrY7FjK.lF2B_Db75au2ypUG5hjXrixTmrkYaMIuh7k0XDz.yWyrt1TV2hUT.hJUCbxs6tECGvIZ5r6e1lDvkfVZx.RA',
    '_cfuvid': '43ysba7IRvIVEQjehUAxkvv0hxXYCnQRfJZCiJFAHLU-1759128822635-0.0.1.1-604800000',
    'cf_clearance': 'SYcs.aM94MYZQE7zmy9WQV5LL9nsgzNnzrLKSyR4n7Q-1759128824-1.2.1.1-EKrKSr8R9nJVfkOkqIK6MlgMr8En_EhzgROVJ52D9SWqZJ9.ABsHQOTKrdHr_urKWjbchQqYoUKZK8peXf3zQfTfGHzamq9Icn9tlEDaGkNC1JtXE3wdCVpCeTKWbOYxP7KFotiaTNeOn3.HZp0ZTlmx17irE1qmq1JbJmRlL2cnEJw04ScSco409KT_Gs_APDrTsfXsOFrxhcPvZyIWf.1_Vo6WtTF4ZEqKyKw0mOg',
    'Blibli-Additional-Parameter-Signature': '',
    'Blibli-Is-Member': 'false',
    'Blibli-Is-Remember': 'false',
    'Blibli-Device-Id': 'U.275ab4e2-57e1-405f-8314-f0a11526aaf6',
    'Blibli-Device-Id-Signature': '9c89794dcd7998f2270ee4a5733d66911fba3290',
    'Blibli-Session-Id': '0e000973-9e65-479e-bbe3-2e78589b6ca8',
    'Blibli-Signature': '52130cf66a218adde225f20f3a9dab229b7af5c1',
    'Blibli-User-Id': '0e000973-9e65-479e-bbe3-2e78589b6ca8',
    'Blibli-Unm-Signature': '5b9bfc34dd973697f7325e006da1d60b3bafa34d',
    'Blibli-Unm-Id': '0e000973-9e65-479e-bbe3-2e78589b6ca8',
    'Blibli-dv-token': 'JT_0ruW5SgdVerJLk36zqg6w2idjNwfX8FW3RgHETi5Gv_',
    'forterToken': '73a8483943384833b4d2a7c8dc580f70_1759129202012__UDF43-m4_25ck_',
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

class BlibliPdpSpider(PricemateBaseSpider):
    name = "blibli_pdp"

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
        docs = self.category_input.find({
            "Platform": self.retailer,
            "Country": self.region,
            "Status": "Pending"
        })

        for doc in docs:
            url = doc["url"]
            hash_id = doc.get("_id")
            slug = url.split("/")[-1]
            cat_num = url.split("/")[3].replace("c",'')

            meta = {
                "cat_url": url,
                "_id": hash_id,
                "slug": slug,
                "cat_num": cat_num,
                "page":1,
                "filename": f"{slug}_page.html",
                "should_be": ["data"]
            }
            yield scrapy.Request(
                url=f'https://www.blibli.com/backend/search/products?categoryLevel={cat_num}&category={slug}&page=1&start=0&sort=7&channelId=web&isMobileBCA=false&showFacet=false',
                headers=headers,
                callback=self.parse_pdp,
                meta=meta
            )

    def parse_pdp(self, response):
        meta = response.meta
        doc_id = meta.get('_id')
        cate_url = meta.get('cat_url')
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
                stock = "In Stock"
            else:
                stock = "Out of Stock"
            barcode = data.get("level0Id")
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
                "Keyword": "",
                "Organic/Paid": traffic_type,
                "Ranking": rank,
                "Store name": store_name,
                "Store URL": store_url,
                "Product Name": name,
                # "Promo_Type": promo_type,
                "Currency":"Rp",
                "Seller ID": sell_id,
                "Selling Price": original_price,
                # "per_unit_price": "",
                "Retail Price": was_price,
                # "Offer_info": discount,
                "Monthly Item Sold": "",
                # "Pack_size": pack_size,
                # "Barcode": barcode,
                "Stock Status": stock,
                # "Images": img,
                "ProductURL": f'https://www.blibli.com{product_url}',
                "Status": "Done",
                # "ParentCode": parent_code,
                "Product ID": prod_code,
                # "retailer_name": "blibli-id",
                "Category": bread,
                "Category URL": cate_url,
                "Brand": brand,
                # "RRP": rrp,
                "Avg Rating": avg_rating,
                "Total Review": count,
                "Historical Item Sold": item_sold,
                "Country":"ID",
                "Platform":"Blibli",
            }

            try:
                self.save_product(item)
                print(f"✓ Successfully inserted {product_url}")
                if doc_id:
                    self.category_input.update_one(
                        {"_id": doc_id},
                        {"$set": {"Status": "Done"}}
                    )
            except Exception as e:
                print(e)

        next_page = current_page + 1
        slug = meta["slug"]
        cat_num = meta["cat_num"]

        next_url = (
            f'https://www.blibli.com/backend/search/products?categoryLevel={cat_num}'
            f'&category={slug}&page={next_page}&start={(next_page - 1) * page_size}&sort=7'
            f'&channelId=web&isMobileBCA=false&showFacet=false'
        )

        meta = {
            "url": next_url,
            "slug": slug,
            "cat_num": cat_num,
            "page": next_page,
            "filename": f"{slug}_{next_page}_page.html",
            "should_be": ["data"]
        }

        yield scrapy.Request(
            url=next_url,
            headers=headers,
            callback=self.parse_pdp,
            meta=meta
        )

    def close(self, reason):
        self.mongo_client.close()

if __name__ == '__main__':
    from scrapy.cmdline import execute
    execute( "scrapy crawl blibli_pdp -a retailer=Blibli -a region=id -a Type=eshop -a RetailerCode=blibli_id".split())