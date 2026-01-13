import json
import re
import time
from parsel import Selector
from urllib.parse import quote
import scrapy
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from pricemate.spiders.bs_spider import PricemateBaseSpider

headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
    'priority': 'u=1, i',
    'referer': 'https://tiki.vn/new-arrivals-giay-sneaker-nam-dincox-dc42-matcha-phong-cach-nang-dong-chat-lieu-canvas-cao-cap-p277250739.html?spid=277250743',
    'sec-ch-ua': '"Google Chrome";v="143", "Chromium";v="143", "Not A(Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36',
    'x-guest-token': 'yckNibgTaOo490GfjdxR8ZYe7lwXVFtK',
    'cookie': '_trackity=1e80fe0f-8359-4b5d-ffac-86483cf899ac; TOKENS={%22access_token%22:%22yckNibgTaOo490GfjdxR8ZYe7lwXVFtK%22}',
}

class TikiPdpSpider(PricemateBaseSpider):
    name = "tiki_pdp"

    def __init__(self, retailer, region, *args, **kwargs):
        super().__init__(retailer=retailer, region=region, *args, **kwargs)

    def start_requests(self):
        docs = self.product_url.find({
            "retailer": self.retailer,
            "region": self.region,
            "Status": "Pending"
        })
        for doc in docs:
            url = doc["ProductURL"]
            hash_id = doc.get("_id")
            slug_id = doc.get("slug_id")
            spid = doc.get("spid")
            slug = "p" + url.split("-p")[-1].split(".")[0]


            meta = {
                "proxy": "http://21ed11ef5c872bc7727680a52233027db4578a0e:@api.zenrows.com:8001",
                "url": url,
                "_id": hash_id,
                "slug": slug,
                "filename": f"{slug}_page.json",
                "should_be": ["data"],
                "direct_request": True,
            }
            yield scrapy.Request(
                url=f'https://tiki.vn/api/v2/products/{slug_id}?platform=web&spid={spid}&version=3',
                headers=headers,
                callback=self.parse_pdp,
                meta=meta
            )

    def parse_pdp(self, response):
        meta = response.meta
        prod_url = meta.get("url")
        doc_id = meta.get('_id')

        try:
            product = response.json()
        except Exception as e:
            self.logger.error(f"JSON failed : {e}")
            return

        # 1. Extract Global Data (Parent Level)
        # These fields are the same for all sizes
        parent_id = product.get("id")
        brand = product.get("brand", {}).get("name", "")

        crumbs_list = product.get("breadcrumbs") or []
        breadcrumb = " > ".join([c.get("name") for c in crumbs_list if c.get("name")])

        # 2. Get Variants (Children)
        # If 'configurable_products' is empty, we treat the main product as the only variant
        variants = product.get("configurable_products", [])
        if not variants:
            variants = [product]

        # 3. Loop through each variant to insert separately
        for v in variants:
            # --- UNIQUE IDENTIFIERS ---
            # Use the Child ID as the ProductCode
            v_id = v.get("id")

            # GENERATE HASH USING THE VARIANT ID
            # This ensures every size gets its own unique row in the database
            product_hash = self.generate_hash_id(str(v_id), self.retailer, self.region)

            # --- SPECIFIC VARIANT DATA ---
            v_sku = v.get("sku")  # Barcode specific to this size
            v_name = v.get("name")  # Name usually includes size (e.g. "... - 41")

            # Size is usually in 'option1' based on your JSON
            pack_size = v.get("option1", "")

            # Prices
            raw_price = v.get("price")
            raw_was = v.get("original_price")

            # Convert to float and divide by 1000 immediately
            price = float(raw_price) / 1000 if raw_price is not None else None
            was_price = float(raw_was) / 1000 if raw_was is not None else None

            # Logic: If current price is missing, use original price.
            if was_price is None:
                rrp = price
                was_price = ""  # Set to empty string if no discount logic applies
            else:
                rrp = was_price

            # Discount
            discount_rate = v.get("discount_rate", 0)
            promo = f"{discount_rate}%" if discount_rate > 0 else ""
            discount = f"-{discount_rate}% off" if discount_rate > 0 else ""

            # Images (Specific to this variant/color)
            images_list = v.get("images") or []
            img_urls = [img.get("large_url") for img in images_list if img.get("large_url")]
            img = " | ".join(img_urls)

            # Stock
            in_stock_status = v.get("inventory_status")
            in_stock = True if in_stock_status == "available" else False

            # --- BUILD ITEM ---
            item = {
                "_id": product_hash,  # Unique Hash based on Variant ID
                "ProductCode": v_id,  # Unique ID (e.g., 277250745)
                "ParentCode": parent_id,  # ID of the main group (e.g., 277250739)
                "Name": v_name,
                "Pack_size": pack_size,  # The Size (e.g., "41")
                "Barcode": "",
                "Price": price,
                "WasPrice": was_price,
                "RRP": rrp,
                "Promo_Type": "",
                "Offer_info": discount,
                "Images": img,
                "ProductURL": prod_url,  # URL remains the same for all
                "is_available": in_stock,
                "Status": "Done",
                "retailer_name": "tiki-vn",
                "Category_Hierarchy": breadcrumb,
                "Brand": brand,
                "per_unit_price": ""
            }

            try:
                self.save_product(item)
                print(f"✓ Saved Variant: {pack_size} (Code: {v_id})")
                self.product_url.update_one(
                    {"_id": doc_id},
                    {"$set": {"Status": "Done"}}
                )
            except Exception as e:
                # If duplicate hash exists, this might error, but since we use v_id, it should be fine
                print(f"Error saving variant {v_id}: {e}")



    def close(self, reason):

        self.mongo_client.close()

if __name__ == '__main__':
    from scrapy.cmdline import execute
    execute("scrapy crawl tiki_pdp -a retailer=tiki-vn -a region=vn -a Type=eshop -a RetailerCode=tiki_vn".split())