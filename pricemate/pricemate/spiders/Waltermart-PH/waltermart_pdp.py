import json
import re
import scrapy
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from pricemate.spiders.base_spider import PricemateBaseSpider

headers = {
    'accept': 'application/json, text/javascript, */*; q=0.01',
    'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
    'origin': 'https://www.waltermartdelivery.com.ph',
    'priority': 'u=1, i',
    'referer': 'https://www.waltermartdelivery.com.ph/shop/similac_milk_tummicare_hw_one_2_8kg/p/1764405684715632028',
    'sec-ch-ua': '"Google Chrome";v="141", "Not?A_Brand";v="8", "Chromium";v="141"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'cross-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36',
}

class WaltermartPdpSpider(PricemateBaseSpider):
    name = "walter_pdp"

    def __init__(self, retailer, region, *args, **kwargs):
        super().__init__(retailer=retailer, region=region, *args, **kwargs)

    @staticmethod
    def extract_size(size_string):
        try:
            size_string = size_string.strip()

            # 1️⃣ Look for patterns like "Size: 200ml" or "Pack Size: 2kg"
            pattern1 = r'(?:Size|Pack Size)[:\s]*([\d.]+)\s*(mg|mcg|ml|mL|l|L|g|kg|oz|lb|packs?|pack|tablets?|capsules?)'
            match = re.search(pattern1, size_string, re.IGNORECASE)
            if match:
                size_value = match.group(1)
                size_unit = match.group(2)
                return f"{size_value} {size_unit}"

            # 2️⃣ Look for things like "200ml", "2kg", "90g", etc.
            pattern2 = r'([\d.]+)\s*(mg|mcg|ml|mL|l|L|g|kg|oz|lb|packs?|pack|tablets?|capsules?)'
            match = re.search(pattern2, size_string, re.IGNORECASE)
            if match:
                size_value = match.group(1)
                size_unit = match.group(2)
                return f"{size_value} {size_unit}"

            # 3️⃣ Look for patterns like "90g×2" or "200ml x 3"
            pattern3 = r'([\d.]+)\s*(mg|mcg|ml|mL|l|L|g|kg|oz|lb)\s*[×xX]\s*(\d+)'
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

            # 5️⃣ Pharma shorthand like "30s"
            pattern5 = r'(\d+)[sS]\b'
            match = re.search(pattern5, size_string, re.IGNORECASE)
            if match:
                return f"{match.group(1)} pcs"

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
            slug = url.split("/")[-1]

            meta = {
                "url": url,
                "_id": hash_id,
                "filename": f"PDP_{slug}_page.html",
                "should_be": ["product"]
            }
            yield scrapy.Request(
                url= f"https://api.freshop.ncrcloud.com/1/products/{slug}?app_key=walter_mart&include_flavors=true&include_other_sizes=true&render_id=1763976135951&store_id=6483&token=c0fd243769fa2b504f7794a6437efda4",
                # cookies=cookies,
                headers=headers,
                callback=self.process_category,
                meta=meta
            )

    def process_category(self, response):
        meta = response.meta
        prod_url = meta.get("url")
        doc_id = meta.get("_id")

        data = json.loads(response.text)

        name = data.get("name")
        price = data.get("offer_unit_price")
        was_price = data.get("unit_price")
        if not price:
            price = was_price
            was_price = ""

        try:
            rrp = max(float(was_price or 0), float(price or 0))
        except (ValueError, TypeError):
            rrp = price or was_price or ""

        brand = data.get("brand") or ""
        images = data.get("images", [])
        image_urls = [
            f"https://ip.prod.freshop.retail.ncrcloud.com/resize?url=https://images.freshop.ncrcloud.com/{img['identifier']}_large.png&width=512&type=webp&quality=90"
            for img in images if 'identifier' in img
        ]
        image = "|".join(image_urls)
        prod_code = data.get("like_code")
        size = self.extract_size(name)
        barcode = data.get("barcode")
        offer = data.get("offer_unit_saving")
        if not offer:
            offer = ""
        promotion = " | ".join(data.get("displayable_offers", []))
        stoke = data.get("status")
        if stoke == "available":
            stoke = True
        else:
            stoke = False

        breadcrumb = ' > '.join(response.meta['url'].split('/')[3:5]) if '/shop/' in response.meta['url'] else ' > '.join(response.meta['url'].split('/')[4].split('-') + [response.meta['url'].split('/')[5]])

        product_hash = self.generate_hash_id(prod_url, self.retailer, self.region)
        item = {"_id": product_hash, "Name": name, "Promo_Type": promotion, "Price": price, "per_unit_price": "",
                "WasPrice": was_price,
                "Offer_info": offer, "Pack_size": size, "Barcode": barcode,
                "Images": image,
                "ProductURL": prod_url, "is_available": stoke,
                "Status": "Done", "ParentCode": "", "ProductCode": prod_code,
                "retailer_name": "waltermart_ph",
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
            "--domain", "waltermartdelivery.com.ph"
        ]
        subprocess.run(cmd, cwd=r"E:\pricemate_service")
        self.mongo_client.close()

if __name__ == '__main__':
    from scrapy.cmdline import execute
    execute("scrapy crawl walter_pdp -a retailer=waltermart-ph -a region=ph -a Type=eshop -a RetailerCode=waltermart_ph".split())