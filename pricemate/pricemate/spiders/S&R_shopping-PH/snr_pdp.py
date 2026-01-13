import json
import re
import time
import html as html_lib
from urllib.parse import quote
import scrapy
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from pricemate.spiders.base_spider import PricemateBaseSpider

cookies = {
    '_fbp': 'fb.1.1759835619244.418966476792689519',
    'useOfCookieNotice': 'true',
    'remember_member_59ba36addc2b2f9401580f014c7f58ea4e30989d': 'eyJpdiI6Im5pNXlvWVRRdDVyVGRVelg2THIrOUE9PSIsInZhbHVlIjoiKzBXV2p0XC9mMHprSEYzZjExdVhicUsxU1hGUUhMVkN1bkJcLzJcLzRzdmI1NEVWVlI5MkFwZFJ3d1wvU3BDVlhsS2JFUG1QRmEySHFEYTJ4OGJibCs3QnJCYWtRajYxNXJ0RTZ2SjB2XC9TZ0RKcDJpWnkrSHIxUHl1NE0rY1V4QW1cL1h0M1wvdnB0Y0IyamFEZlwvaExUOXNxS254SEdSenVDSGlZYVhCRFFOWFJLZ2VYbWd2UXFKYUNpMVJhXC9QZEdLVjNUIiwibWFjIjoiMWZlZjQ3NGQ5NzJmMzM4MWYxYzRkM2YxNzQ0MDM0ZTA3NTk3Mjc0YzRkNDgwMmY4YzM5MDJjMjBhYWNhMDM0NCJ9',
    'XSRF-TOKEN': 'eyJpdiI6IlwvbDQ0MDNPdENEWHkrYVwvakdtWHQ4Zz09IiwidmFsdWUiOiJ3VXErZDE1MVRyQjF1aFVqUTBEclwvaUNmZXE1bGlhMDQwaHA5Ums1bXY5QzhyUFBWZ1FSVHArdWdLT1NMZit2VyIsIm1hYyI6ImIxNDU5NzcyMTJlOThiNWMzMWNmYjExMmJhNWVhYmFhM2U4YThkZjg2MTI1YzRmYmMxYTUyOWJiMWQ5MjdmYzEifQ%3D%3D',
    'laravel_session': 'eyJpdiI6IkQrM2tSUk1DYWVvS1MzUFhETVBMT2c9PSIsInZhbHVlIjoiQVBURjJjM3pjRWNpRjNCc0xsU3NuTEk2QjRqUG5JQytPaVc4bTBPR3lCZlJMd1dTVitlNDEwVnZsdUdBV2pESSIsIm1hYyI6IjA5ZGU5MGZiYjg1ZTAzZDQ4YTU3NDFlMGVjYmRmNzVkMWQ2NzUwZjhkOWNkZmU4NDRjMTUzNDliOTUyNWMzMzYifQ%3D%3D',
}

headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
    'cache-control': 'max-age=0',
    'priority': 'u=0, i',
    'referer': 'https://www.snrshopping.com/',
    'sec-ch-ua': '"Chromium";v="142", "Google Chrome";v="142", "Not_A Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36',
    # 'cookie': '_fbp=fb.1.1759835619244.418966476792689519; useOfCookieNotice=true; remember_member_59ba36addc2b2f9401580f014c7f58ea4e30989d=eyJpdiI6Im5pNXlvWVRRdDVyVGRVelg2THIrOUE9PSIsInZhbHVlIjoiKzBXV2p0XC9mMHprSEYzZjExdVhicUsxU1hGUUhMVkN1bkJcLzJcLzRzdmI1NEVWVlI5MkFwZFJ3d1wvU3BDVlhsS2JFUG1QRmEySHFEYTJ4OGJibCs3QnJCYWtRajYxNXJ0RTZ2SjB2XC9TZ0RKcDJpWnkrSHIxUHl1NE0rY1V4QW1cL1h0M1wvdnB0Y0IyamFEZlwvaExUOXNxS254SEdSenVDSGlZYVhCRFFOWFJLZ2VYbWd2UXFKYUNpMVJhXC9QZEdLVjNUIiwibWFjIjoiMWZlZjQ3NGQ5NzJmMzM4MWYxYzRkM2YxNzQ0MDM0ZTA3NTk3Mjc0YzRkNDgwMmY4YzM5MDJjMjBhYWNhMDM0NCJ9; XSRF-TOKEN=eyJpdiI6IlwvbDQ0MDNPdENEWHkrYVwvakdtWHQ4Zz09IiwidmFsdWUiOiJ3VXErZDE1MVRyQjF1aFVqUTBEclwvaUNmZXE1bGlhMDQwaHA5Ums1bXY5QzhyUFBWZ1FSVHArdWdLT1NMZit2VyIsIm1hYyI6ImIxNDU5NzcyMTJlOThiNWMzMWNmYjExMmJhNWVhYmFhM2U4YThkZjg2MTI1YzRmYmMxYTUyOWJiMWQ5MjdmYzEifQ%3D%3D; laravel_session=eyJpdiI6IkQrM2tSUk1DYWVvS1MzUFhETVBMT2c9PSIsInZhbHVlIjoiQVBURjJjM3pjRWNpRjNCc0xsU3NuTEk2QjRqUG5JQytPaVc4bTBPR3lCZlJMd1dTVitlNDEwVnZsdUdBV2pESSIsIm1hYyI6IjA5ZGU5MGZiYjg1ZTAzZDQ4YTU3NDFlMGVjYmRmNzVkMWQ2NzUwZjhkOWNkZmU4NDRjMTUzNDliOTUyNWMzMzYifQ%3D%3D',
}



class SnrPdpSpider(PricemateBaseSpider):
    name = "snr_pdp"

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
            pattern2 = r'([\d.]+)\s*(ml|mL|l|L|g|kg|oz|lb|pcs|qt|oz|Pieces|in|pc|Set|s|packs?|pack|tablets?|capsules?)'
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
            slug = url.split("/")[-1].split("/")[0]
            meta = {
                "url": url,
                "_id": hash_id,
                "slug": slug,
                "filename": f"PDP_{slug}_page.html",
                "should_be": ["html"]
            }
            yield scrapy.Request(
                url,
                cookies=cookies,
                headers=headers,
                callback=self.parse_pdp,
                meta=meta,
                dont_filter=True
            )

    def parse_pdp(self, response):
        meta = response.meta
        pro_url = meta.get("url")
        doc_id = meta.get("_id")
        slug = meta.get("slug")

        scripts = response.xpath('//script[contains(., "view_item")]/text()').getall()

        product_code = None

        # Strategy A: Try to get the SKU from the Data Layer (Most Accurate)
        # This exists in Page 1 but is missing/empty in Page 2
        try:
            scripts = response.xpath('//script[contains(., "view_item")]/text()').getall()
            for script in scripts:
                # Clean up script to avoid matching commented out lines
                clean_script = "\n".join([line for line in script.split('\n') if not line.strip().startswith('//')])
                # Match "id": "12345" or "id": 12345
                match = re.search(r'[\'"]id[\'"]\s*:\s*[\'"]?(\d+)[\'"]?', clean_script)
                if match:
                    product_code = match.group(1)
                    break
        except Exception:
            pass

        # Strategy B: Fallback to Wishlist Data ID (Web ID)
        # Found in both Page 1 (14266) and Page 2 (6282)
        if not product_code:
            product_code = response.xpath('//button[contains(@class, "add-to-list")]/@data-id').get()

        # Strategy C: Fallback to Hidden Input #pid (Internal DB ID)
        # Found in both Page 1 (1990313) and Page 2 (789639)
        if not product_code:
            product_code = response.xpath('//input[@id="pid"]/@value').get()

        if not product_code:
            print(f"❌ No product ID found for {pro_url}")
            self.product_table.update_one({"_id": doc_id}, {"$set": {"Status": "Not Found"}})
            return  # Stop processing if no ID

        print(f"✓ Extracted Product ID: {product_code}")
        # --- Extract product fields ---
        #product_code = product_data.get("id") or product_data.get("item_id")
        # Name
        name = response.xpath("//meta[@property='og:title']/@content").get()
        if not name:
            name = response.xpath("//h2/text()").get()

        product_url = response.url
        title = response.xpath("//meta[@property='og:title']/@content").get()
        words = title.split()

        if words[0].endswith('.'):
            brand = " ".join(words[:2])
        elif words[0].isdigit():
            brand = " ".join(words[:2])
        else:
            brand = words[0]

        raw_price = response.xpath("//div//span[contains(@class, 'font-weight-normal')]/text()").get()
        if not raw_price:
            raw_price = response.xpath("//div[@class='p-1 oo-p']/h2/text()").get()
        price = re.sub(r'[^\d.]', '', raw_price)
        raw_was = response.xpath("//div//span[contains(@class, 'original-online-price')]/text()").get()

        if not raw_was:
            was_price = ""
            rrp = price
        else:
            was_price = re.sub(r'[^\d.]', '', raw_was)
            rrp = was_price
        image_urls = response.xpath("//meta[@property='og:image']/@content").getall()
        images = " | ".join(image_urls)
        raw_info = response.xpath("//div//p[contains(@class, 'saved-price')]/text()").get() or ""
        offer = " ".join(raw_info.split())
        offer_info = offer.replace("â‚±", "₱")
        promo_type = response.xpath("normalize-space(//div[contains(@class, 'camp-name')]/text())").get()
        items = response.xpath("//nav[@aria-label='breadcrumb']//li//text()").getall()
        items = [i.strip() for i in items if i.strip()]

        # Remove first two items and last item
        middle = items[2:-1]

        breadcrumb = " > ".join(middle)
        stock = response.xpath("//*[contains(text(),'Out of stock') or contains(text(),'Sold Out')]")
        is_available = False if stock else True

        pack_size = self.extract_size(name)
        # if not name or not price or not product_code:
        #     self.category_input.update_one({"_id": doc_id}, {"$set": {"Status": "Not Found"}})
        #     raise ValueError(
        #         f"❌ Missing critical field(s) on product page: {product_url} "
        #         f"[Name='{name}', Price='{price}', ProductCode='{product_code}']"
        #     )
        product_hash = self.generate_hash_id(product_url, self.retailer, self.region)
        item = {
            "_id": product_hash,
            "ProductCode": product_code,
            "ParentCode": "",
            "ProductURL": product_url,
            "Name": name,
            "Brand": brand,
            "Pack_size": pack_size,
            "Price": price,
            "WasPrice": was_price,
            "Category_Hierarchy": breadcrumb,
            "is_available": is_available,
            "Status": "Done",
            "Images": images,
            "RRP": rrp,
            "Offer_info": offer_info,
            "Promo_Type": promo_type,
            "per_unit_price": "",
            "Barcode": "",
            "retailer_name": "snrshopping-ph",
        }
        try:
            self.save_product(item)
            print(f"✓ Successfully inserted {product_url}")

            # self.product_table.update_one(
            #     {"_id": doc_id},
            #     {"$set": {"Status": "Done"}}
            # )
        except Exception as e:
            print(e)


    def close(self, reason):
        import subprocess
        cmd = [
            "python",
            "upload_to_s3_direct.py",
            "--domain", "snrshopping.com"
        ]
        subprocess.run(cmd, cwd=r"E:\pricemate_service")
        self.mongo_client.close()

if __name__ == '__main__':
    from scrapy.cmdline import execute
    execute("scrapy crawl snr_pdp -a retailer=snrshopping-ph -a region=ph -a Type=eshop -a RetailerCode=snrshopping_ph".split())