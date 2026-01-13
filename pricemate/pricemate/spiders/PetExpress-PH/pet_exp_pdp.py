import json
import re
import time
from lxml import etree
from urllib.parse import quote
import scrapy
import os, sys

from pandas.io.clipboard import is_available

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from pricemate.spiders.base_spider import PricemateBaseSpider
cookies = {
    'localization': 'PH',
    '_shopify_y': '53a3fc3a-a773-4921-ad8c-d474acb20ab6',
    '_tracking_consent': '3.AMPS_IDJK_f_f_fBEIQ6JmTKelFYg9jDU6kg',
    '_orig_referrer': '',
    '_landing_page': '%2F',
    'WISHLIST_TOTAL': '0',
    'WISHLIST_PRODUCTS_IDS': '{}',
    'WISHLIST_PRODUCTS_IDS_SET': '1',
    'WISHLIST_UUID': 'null',
    'WISHLIST_IP_ADDRESS': '45.8.25.32',
    '_fbp': 'fb.2.1758009374874.955357043559420247',
    '_gid': 'GA1.3.557831823.1758009375',
    '_shopify_s': 'fe4ae1ad-6403-46a8-890f-4bf3e7341ac6',
    '_ga_F1H7VLWCB9': 'GS2.1.s1758009373$o1$g1$t1758018750$j47$l0$h1709076340',
    '_ga_RCEF0MS1T5': 'GS2.1.s1758017021$o3$g1$t1758018750$j47$l0$h0',
    '_ga': 'GA1.3.1623927627.1758009374',
    '_shopify_essential': ':AZlRhj1oAAEAfDxNj_J2_iroc-TCyqakDO5ZbsCfyCVUHVdy5pLjKjKfCnmqnDYKOTZLcvSaRgxIDQ-CgB_zVcjCFBb9KZyBdFAau9_U0RBb6YxDaQ0B7f5AS4aUP6zwZBiUFqdTkk7QDEZVS-QJk4muRghCl-TaY77v3t2dObKlgzH0IDNmxCzZ_6RUurOK_EENyw:',
    'keep_alive': 'eyJ2IjoyLCJ0cyI6MTc1ODAxOTE1MjMxMiwiZW52Ijp7IndkIjowLCJ1YSI6MSwiY3YiOjEsImJyIjoxfSwiYmh2Ijp7Im1hIjoyOCwiY2EiOjAsImthIjowLCJzYSI6MSwia2JhIjowLCJ0YSI6MCwidCI6NDAyLCJubSI6MSwibXMiOjAuMTMsIm1qIjowLjk1LCJtc3AiOjAuNjgsInZjIjowLCJjcCI6MCwicmMiOjAsImtqIjowLCJraSI6MCwic3MiOjAsInNqIjowLCJzc20iOjAsInNwIjowLCJ0cyI6MCwidGoiOjAsInRwIjowLCJ0c20iOjB9LCJzZXMiOnsicCI6MTUsInMiOjE3NTgwMDkzNzI1NDEsImQiOjk1NDB9fQ%3D%3D',
}

headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'en-US,en;q=0.9',
    'cache-control': 'max-age=0',
    'if-none-match': '"cacheable:64f48f4be925a7e976faa988fc4c6ac6"',
    'priority': 'u=0, i',
    'referer': 'https://www.petexpress.com.ph/collections/skin-and-coat-treatment/muddy-paws',
    'sec-ch-ua': '"Chromium";v="140", "Not=A?Brand";v="24", "Google Chrome";v="140"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36',
}
class PetexpPdpSpider(PricemateBaseSpider):
    name = "petexp_pdp"

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
            url = doc.get("ProductURL")
            hash_id = doc.get("_id")
            slug = url.split("products/")[-1].split("/")[0]

            meta = {
                "url": url,
                "_id": hash_id,
                "filename": f"PDP_{slug}_page.html",
                "should_be": ["data-product-json"]
            }
            yield scrapy.Request(
                url,
                cookies=cookies,
                headers=headers,
                callback=self.process_category,
                meta=meta
            )
    def process_category(self, response):
        meta = response.meta
        prod_url = meta.get("url")
        doc_id = meta.get("_id")

        raw_json = response.xpath('//script[@type="application/json" and @data-product-json]/text()').get()
        product_json = json.loads(raw_json)
        product = product_json.get("product", {})
        inventories = product_json.get("inventories", {})

        name = product.get("title")
        brand = product.get("vendor")
        price = float(product.get("price", 0)) / 100
        compare_at_price = product.get("compare_at_price")
        was_price = float(compare_at_price) / 100 if compare_at_price else 0

        # Logic for was_price and rrp
        if not was_price or was_price == price:  # was_price is 0 or None
            was_price = ""
            rrp = price
        else:
            rrp = was_price
        sku = response.xpath('//div[@class="product-meta__reference"]/span[@class="product-meta__sku"]/span[@class="product-meta__sku-number"]/text()').get()
        if sku:
            sku = sku.strip()
        else:
            sku = ""
        images = product.get("images", [])
        images_full = ["https:" + img if img.startswith("//") else img for img in images]
        img = "|".join(images_full)
        barcode = product.get("id")
        stock_text = response.xpath('//div[@class="product-form__info-item"]/span[text()="Stock:"]/following-sibling::div//span[contains(@class,"inventory")]/text()').get()

        in_stock = True if stock_text and "in stock" in stock_text.lower() else False
        pack_size = self.extract_size(name)
        offer = response.xpath('//div[@class="product-meta__label-list"]/span[contains(@class,"product-label--on-sale")]/text()').get()
        if offer:
            offer = offer.strip()
        else:
            offer = ""
        breadcrumb_parts = response.xpath('//div[@class="page__sub-header"]//ol[@class="breadcrumb__list"]/li/a/text() | //div[@class="page__sub-header"]//ol[@class="breadcrumb__list"]/li/span/text()').getall()
        breadcrumb = " > ".join([part.strip() for part in breadcrumb_parts])
        product_hash = self.generate_hash_id(prod_url, self.retailer, self.region)
        item = {"_id": product_hash, "Name": name, "Promo_Type": "", "Price": price, "per_unit_price": "",
                "WasPrice": was_price,
                "Offer_info": offer, "Pack_size": pack_size, "Barcode": barcode,
                "Images": img,
                "ProductURL": prod_url, "is_available": in_stock,
                "Status": "Done", "ParentCode": "", "ProductCode": sku,
                "retailer_name": "petexpress",
                "Category_Hierarchy": breadcrumb, "Brand": brand, "RRP": rrp}
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
            "--domain", "petexpress.com.ph"
        ]
        subprocess.run(cmd, cwd=r"E:\pricemate_service")
        self.mongo_client.close()

if __name__ == '__main__':
    from scrapy.cmdline import execute
    execute("scrapy crawl petexp_pdp -a retailer=petexpress-ph -a region=ph -a Type=eshop -a RetailerCode=petexpress_ph".split())
