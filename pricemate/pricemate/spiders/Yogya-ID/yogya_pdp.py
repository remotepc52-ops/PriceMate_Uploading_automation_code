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
    '_fbp': 'fb.2.1767934457215.828576790597856419',
    'callbell_uid': '4a67c230-ed17-11f0-8b3d-b7c10dda08f4',
    'lastPopupTime': '1767938137162',
    'TS6ef1c577077': '08328b1ebeab2800e04f113dfccd271df8a4ed19438d4987f5b4faf9aa93de6e6bb39a5f2a50250ec0fc292af6d77f9d08b9dbe1d1172000943a1be45a75e66f6714880fe41603ba376446d8dfcd8900862aaafec5117102',
    'XSRF-TOKEN': 'eyJpdiI6IlM5c1pkcitJUTVxQVFlaXRoK2N0OWc9PSIsInZhbHVlIjoiVmVmbExmb1ZIWVRndkpMazdSVEs0NjR5MnJcL2tWN2Y2RCtNQU9NaFcrV3JlYUk4SmU0dGdYZ21McU5cL2pOMWxaIiwibWFjIjoiZjY5MWI3ZGM3ZTYyODA4MWYwNjgyM2MwMGY0NWM0Y2NlNGVkOWEyNjBiOWUyMDE5MjI2MGVlMWQ5ZjY0NDgxMSJ9',
    'yogya_online_session': 'eyJpdiI6IjhaN3pPXC9uUlZqQ0Q0U2RBZDNPV3BnPT0iLCJ2YWx1ZSI6IitPUUY1aWt0aERZZGJHUFhoemhCTDJWSHFNUjFITjJ0V1piSVlxSjZtQkZMS0UwZHBJXC9ZTjNKZURkSUN5SHdkIiwibWFjIjoiYzMzYTU3NWJiZjYxYTI1YzliODM0YzM5ZDgwMmI2YzM5OGNjMTNkZDYwOWEyNzNhYWVjYmFhN2U3MWUzMDQzNCJ9',
    'TS131d75c5027': '08328b1ebeab2000e7f61f6966be2e2aef17dc1d5fb39db2b0d0b3691f3a15ff2568df3cdb79114108e2c8406411300003ad4c07fa3d84480fb700cfdcb7f5014b879ea35af771f1fbf79e85d9f4e72aa148f6c4b558d03e961d2eeaabffd545',
}

headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
    'priority': 'u=1, i',
    'referer': 'https://supermarket.yogyaonline.co.id/supermarket/detail/biokul/biokul-yoghurt-drink-blueberry-150ml/01587746',
    'sec-ch-ua': '"Google Chrome";v="143", "Chromium";v="143", "Not A(Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36',
    'x-csrf-token': '',
    'x-requested-with': 'XMLHttpRequest',
    'x-xsrf-token': 'eyJpdiI6IlM5c1pkcitJUTVxQVFlaXRoK2N0OWc9PSIsInZhbHVlIjoiVmVmbExmb1ZIWVRndkpMazdSVEs0NjR5MnJcL2tWN2Y2RCtNQU9NaFcrV3JlYUk4SmU0dGdYZ21McU5cL2pOMWxaIiwibWFjIjoiZjY5MWI3ZGM3ZTYyODA4MWYwNjgyM2MwMGY0NWM0Y2NlNGVkOWEyNjBiOWUyMDE5MjI2MGVlMWQ5ZjY0NDgxMSJ9',
    # 'cookie': '_fbp=fb.2.1767934457215.828576790597856419; callbell_uid=4a67c230-ed17-11f0-8b3d-b7c10dda08f4; lastPopupTime=1767938137162; TS6ef1c577077=08328b1ebeab2800e04f113dfccd271df8a4ed19438d4987f5b4faf9aa93de6e6bb39a5f2a50250ec0fc292af6d77f9d08b9dbe1d1172000943a1be45a75e66f6714880fe41603ba376446d8dfcd8900862aaafec5117102; XSRF-TOKEN=eyJpdiI6IlM5c1pkcitJUTVxQVFlaXRoK2N0OWc9PSIsInZhbHVlIjoiVmVmbExmb1ZIWVRndkpMazdSVEs0NjR5MnJcL2tWN2Y2RCtNQU9NaFcrV3JlYUk4SmU0dGdYZ21McU5cL2pOMWxaIiwibWFjIjoiZjY5MWI3ZGM3ZTYyODA4MWYwNjgyM2MwMGY0NWM0Y2NlNGVkOWEyNjBiOWUyMDE5MjI2MGVlMWQ5ZjY0NDgxMSJ9; yogya_online_session=eyJpdiI6IjhaN3pPXC9uUlZqQ0Q0U2RBZDNPV3BnPT0iLCJ2YWx1ZSI6IitPUUY1aWt0aERZZGJHUFhoemhCTDJWSHFNUjFITjJ0V1piSVlxSjZtQkZMS0UwZHBJXC9ZTjNKZURkSUN5SHdkIiwibWFjIjoiYzMzYTU3NWJiZjYxYTI1YzliODM0YzM5ZDgwMmI2YzM5OGNjMTNkZDYwOWEyNzNhYWVjYmFhN2U3MWUzMDQzNCJ9; TS131d75c5027=08328b1ebeab2000e7f61f6966be2e2aef17dc1d5fb39db2b0d0b3691f3a15ff2568df3cdb79114108e2c8406411300003ad4c07fa3d84480fb700cfdcb7f5014b879ea35af771f1fbf79e85d9f4e72aa148f6c4b558d03e961d2eeaabffd545',
}

class YogyaPdpSpider(PricemateBaseSpider):
    name = "yogya_pdp"

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
            sku = url.rstrip("/").split("/")[-1]

            api_url = f'https://supermarket.yogyaonline.co.id/supermarket/product/detail/{sku}/load'
            current_proxy = '2c6ea6e6d8c14216a62781b8f850cd5b'
            proxy_host = "api.zyte.com"
            proxy_port = "8011"
            proxy_auth = f"{current_proxy}:"

            proxy_url = f"https://{proxy_auth}@{proxy_host}:{proxy_port}"

            meta = {
                # "proxy": proxy_url,
                "url": api_url,
                "Prod_url": url,
                "_id": hash_id,
                "sku": sku,
                "filename": f"{sku}_page.html",
                "should_be": ["data"]
            }

            yield scrapy.Request(
                url=api_url,
                cookies=cookies,
                headers=headers,
                callback=self.parse_pdp,
                meta=meta,
            )

    def parse_pdp(self, response):
        meta = response.meta
        sku = meta.get("sku")
        prod_url = meta.get("Prod_url")
        doc_id = meta.get('_id')

        try:
            data = json.loads(response.text)
        except Exception as e:
            self.logger.error(f"JSON decode failed: {e}")
            return

        html_content = data.get("html", "")
        if not html_content:
            self.logger.error("No HTML found in response JSON")
            return

        sel = Selector(text=html_content)

        p_name = data.get("productName")
        brand = data.get("brandName")
        stock_text = sel.xpath("normalize-space(//*[contains(text(),'Stok')])").get(default="").strip()
        if "Habis" in stock_text:
            is_available = False
        else:
            is_available = True
        was_price_str = sel.xpath("normalize-space(//del/text())").get(default="").replace("Rp", "").replace(".","").replace(",",".").strip()
        was_price = float(was_price_str) if was_price_str else ""
        price_str = sel.xpath("normalize-space((//div[contains(@class,'product-price')])[last()]/text())").get(
            default="").replace("Rp", "").replace(".", "").replace(",", ".").strip()
        price = int(price_str) if price_str else 0.0
        price = float(price) if price else 0.0
        rrp = was_price if was_price != "" else price
        pack_size = self.extract_size(p_name)
        offer_info = sel.xpath('normalize-space(//div[@class="product-promo d-flex flex-column w-fit"]//span[contains(@class,"badge")]/text())').get()
        bread = f'Home>Supermarket>{brand}>{p_name}'

        product_hash = self.generate_hash_id(prod_url, self.retailer, self.region)
        item = {"_id": product_hash, "Name": p_name, "Promo_Type": "", "Price": price, "per_unit_price": "",
                "WasPrice": was_price,
                "Offer_info": offer_info, "Pack_size": pack_size, "Barcode": "",
                "Images": "",
                "ProductURL": prod_url, "is_available": is_available,
                "Status": "Done", "ParentCode": "", "ProductCode": sku,
                "retailer_name": "yogya-online",
                "Category_Hierarchy": bread, "Brand": brand, "RRP": rrp}
        headers["Referer"] = prod_url
        media_url = f"https://supermarket.yogyaonline.co.id/supermarket/product/media/{sku}/load"
        yield scrapy.Request(
            url=media_url,
            cookies=cookies,
            headers=headers,
            callback=self.parse_media,
            meta={"item": item, "doc_id": doc_id, "sku": sku, "prod_url": prod_url,"filename": f"{sku}_img_page.html","should_be": ["swiper-container"]}
        )

    def parse_media(self, response):
        meta = response.meta
        item = meta["item"]
        doc_id = meta["doc_id"]
        sku = meta["sku"]
        prod_url = meta["prod_url"]

        try:
            data1 = json.loads(response.text)
        except Exception as e:
            self.logger.error(f"JSON decode failed for media: {e}")
            return

        html_content = data1.get("html", "")
        sel = Selector(text=html_content)

        # Extract all image URLs from swiper slides
        images = sel.xpath('//div[@id="bannerSliderImage"]//div[@class="swiper-slide"]/img/@src').getall()
        # Join them with | as in your style
        item["Images"] = "|".join(images)

        try:
                self.save_product(item)
                print(f"✓ Successfully inserted {prod_url}")
                if doc_id:
                    self.product_table.update_one(
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
            "--domain", "yogyaonline.co.id"
        ]
        subprocess.run(cmd, cwd=r"E:\pricemate_service")
        self.mongo_client.close()


if __name__ == '__main__':
    from scrapy.cmdline import execute
    execute("scrapy crawl yogya_pdp -a retailer=yogya-id -a region=id -a Type=eshop -a RetailerCode=yogya_id".split())