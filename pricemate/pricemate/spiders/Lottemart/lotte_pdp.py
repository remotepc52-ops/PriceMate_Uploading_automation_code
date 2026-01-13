import json
import re
import time
from parsel import Selector
from urllib.parse import quote
import scrapy
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from pricemate.spiders.base_spider import PricemateBaseSpider

cookies = {
    'cookiesession1': '678ADA7B61A1B1FFD8629D98D150F1D0',
    '_ga': 'GA1.1.253009876.1756469297',
    '_ga_W3RDM1W0G3': 'GS2.1.s1757571957$o4$g1$t1757575965$j45$l0$h0',
}

headers = {
    'Accept': 'text/x-component',
    'Accept-Language': 'en-US,en;q=0.9',
    'Connection': 'keep-alive',
    'Content-Type': 'text/plain;charset=UTF-8',
    'Next-Action': 'c436285e51e8b479f062b9ff0094831e5f7d7a21',
    'Next-Router-State-Tree': '%5B%22%22%2C%7B%22children%22%3A%5B%22product%22%2C%7B%22children%22%3A%5B%5B%22prodNm%22%2C%22super-bubur-single-ayam-pack-45gr%22%2C%22d%22%5D%2C%7B%22children%22%3A%5B%5B%22store%22%2C%22lotte-grosir-banjarmasin%22%2C%22d%22%5D%2C%7B%22children%22%3A%5B%22__PAGE__%22%2C%7B%7D%2C%22%2Fproduct%2Fsuper-bubur-single-ayam-pack-45gr%2Flotte-grosir-banjarmasin%22%2C%22refresh%22%5D%7D%5D%7D%5D%7D%5D%7D%2Cnull%2Cnull%2Ctrue%5D',
    'Origin': 'https://order.lottemart.co.id',
    'Referer': 'https://order.lottemart.co.id/',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36',
    'sec-ch-ua': '"Chromium";v="140", "Not=A?Brand";v="24", "Google Chrome";v="140"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
}

class LottePdpSpider(PricemateBaseSpider):
    name = "lotte_pdp"

    def __init__(self, retailer, region, *args, **kwargs):
        super().__init__(retailer=retailer, region=region, *args, **kwargs)
    @staticmethod
    def extract_size(size_string):
        try:
            size_string = size_string.strip()

            # 1️⃣ Look for patterns like "Size: 200ml" or "Pack Size: 2kg"
            pattern1 = r'(?:Size|Pack Size)[:\s]*([\d.]+)\s*(ml|mL|l|L|g|kg|oz|lb|packs?|pack|tablets?|capsules?)'
            match = re.search(pattern1, size_string, re.IGNORECASE)
            if match:
                size_value = match.group(1)
                size_unit = match.group(2)
                return f"{size_value} {size_unit}"

            # 2️⃣ Look for things like "200ml", "2kg", "90g", etc.
            pattern2 = r'([\d.]+)\s*(ml|mL|l|L|g|kg|oz|lb|packs?|pack|tablets?|capsules?)'
            match = re.search(pattern2, size_string, re.IGNORECASE)
            if match:
                size_value = match.group(1)
                size_unit = match.group(2)
                return f"{size_value} {size_unit}"

            # 3️⃣ Look for patterns like "90g×2" or "200ml x 3"
            pattern3 = r'([\d.]+)\s*(ml|mL|l|L|g|kg|oz|lb)\s*[×xX]\s*(\d+)'
            match = re.search(pattern3, size_string, re.IGNORECASE)
            if match:
                size = f"{match.group(1)} {match.group(2)}"
                quantity = match.group(3)
                return f"{size} x {quantity}"

            # 4️⃣ Look for just quantity (like "24本入り" or "2個")
            pattern4 = r'(\d+)\s*(個|本入り|袋|本)'
            match = re.search(pattern4, size_string, re.IGNORECASE)
            if match:
                quantity = f"{match.group(1)} {match.group(2)}"
                return quantity

            # If nothing matched
            return ""

        except Exception as e:
            print(f"Error extracting size: {e}")
            return ""
    def start_requests(self):
        docs = self.product_table.find({
            "retailer": self.retailer,
            "region": self.region,
            "Status": "Pending"
        })

        for doc in docs:
            url = doc["ProductURL"]
            hash_id = doc.get("_id")
            slug = url.rstrip("/").split("/product/")[-1].split("/")[0]
            data = json.dumps([{"storeSlug": "lotte-grosir-alam-sutera", "prodSlug": slug, "custGrade": "undefined"}])

            # current_proxy = '2c6ea6e6d8c14216a62781b8f850cd5b'
            # proxy_host = "api.zyte.com"
            # proxy_port = "8011"
            # proxy_auth = f"{current_proxy}:"
            #
            # proxy_url = f"https://{proxy_auth}@{proxy_host}:{proxy_port}"

            meta = {
                # "proxy": "http://21ed11ef5c872bc7727680a52233027db4578a0e:@api.zenrows.com:8001",
                # "proxy": proxy_url,
                "url": url,
                "_id": hash_id,
                "slug": slug,
                "filename": f"{slug}_page.html",
                "should_be": ["data"]
            }

            yield scrapy.Request(
                url,
                method="POST",
                body=data.encode("utf-8"),
                headers=headers,
                cookies=cookies,
                callback=self.parse_pdp,
                meta=meta
            )


    def parse_pdp(self, response):
        meta = response.meta
        doc_id = meta.get('_id')
        prod_url = meta.get('url')
        text = response.text
        match = re.search(r'(?<=1:)\{[\s\S]*}', text)
        if not match:
            self.logger.warning(f"JSON part not found in {response.url}")
            return
        json_text = match.group()
        data = json.loads(json_text)
        prod_data = data.get("data", {})

        prod_code = prod_data.get('prod_cd')
        name = prod_data.get('prod_nm')
        price = float(prod_data.get('sale_prc'))
        # price = prod_data.get('sale_prc')
        was_price = float(prod_data.get('normal_prc'))
        if price == was_price:
            was_price = ""
            rrp = price
        else:
            was_price = was_price
            rrp= was_price
        img = prod_data.get('image')
        offer = prod_data.get("offer", {})

        if isinstance(offer, dict):
            offer_info = offer.get("offerNm", "")
        elif isinstance(offer, list) and len(offer) > 0 and isinstance(offer[0], dict):
            offer_info = offer[0].get("offerNm", "")
        else:
            offer_info = ""
        l1 = prod_data.get('l1_nm') #.replace('/','>')
        l4 = prod_data.get('l4_nm')
        bread= f'{l1}>{l4}'
        size = prod_data.get('weight')
        stock= True if int(prod_data.get("stk_qty", 0)) > 0 else False
        # stock = prod_data.get("stk_qty")
        # if stock:
        #     stock = True
        # else:
        #     stock = False
        barcode = (prod_data.get('nie') or "").split()[1] if (prod_data.get('nie') and len(prod_data.get('nie').split()) > 1) else (prod_data.get('nie') or "")
        product_hash = self.generate_hash_id(prod_url, self.retailer, self.region)

        if price == 0:
            self.product_table.update_one({"_id": doc_id}, {'$set': {'Status': "Not found"}})
            print("price Not Found...")
            return

        item = {
            "_id": product_hash,
            "Name": name,
            "Promo_Type": "",
            "Price": price,
            "per_unit_price": "",
            "WasPrice": was_price,
            "Offer_info": offer_info,
            "Pack_size": size,
            "Barcode": barcode,
            "is_available": stock,
            "Images": img,
            "ProductURL": prod_url,
            "Status": "Done",
            "ParentCode": "",
            "ProductCode": prod_code,
            "retailer_name": "lottemart-id",
            "Category_Hierarchy": bread,
            "Brand": "",
            "RRP": rrp,
        }
        try:
            _id = item.pop("_id")
            self.product_table.update_one(
                {
                    "ProductURL": prod_url,
                    "retailer": self.retailer
                },
                {"$set": item},
                upsert=True
            )
            print(f"✓ Successfully inserted {prod_url}")
            if doc_id:
                self.category_input.update_one(
                    {"_id": doc_id},
                    {"$set": {"Status": "Done"}}
                )
        except Exception as e:
            print(e)

    def close(self, reason):
        import subprocess
        cmd = [
            "python",
            "upload_to_s3_direct.py",
            "--domain", "lottemart.co.id"
        ]
        subprocess.run(cmd, cwd=r"E:\pricemate_service")
        self.mongo_client.close()

if __name__ == '__main__':
    from scrapy.cmdline import execute
    execute("scrapy crawl lotte_pdp -a retailer=lottemartgrosir-id -a region=id -a Type=eshop -a RetailerCode=lottemartgrosir_id".split())
