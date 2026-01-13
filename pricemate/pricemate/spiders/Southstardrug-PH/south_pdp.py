import json
import re
import scrapy
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from pricemate.spiders.base_spider import PricemateBaseSpider
cookies = {
    'localization': 'PH',
    '_shopify_y': '794087fa-8ee5-4e01-9b7e-6a8a05617d2b',
    '_tracking_consent': '3.AMPS_AUWA_f_f_7AUxuHq8TwWPRARDwt06mw',
    '_shopify_analytics': ':AZnDo_lHAAEAyjgraiEIWjqyLm3AJM5zK8iheTo7GvecDngxOjZXOPHfHpjclA:',
    'WISHLIST_TOTAL': '0',
    'WISHLIST_PRODUCTS_IDS': '{}',
    'WISHLIST_PRODUCTS_IDS_SET': '1',
    'WISHLIST_UUID': 'null',
    'WISHLIST_IP_ADDRESS': '103.108.231.19',
    '_fbp': 'fb.2.1759923940325.201946050156262699',
    '_shopify_s': '7be1b684-b1c2-4f2d-a9ae-500a3e4ff3de',
    'epb_previous_pathname': '/products/cardiclear-fish-oil-1000-mg-softgel-capsule-10s-600-in-house-trade-account',
    'fsb_previous_pathname': '/products/cardiclear-fish-oil-1000-mg-softgel-capsule-10s-600-in-house-trade-account',
    '_shopify_essential': ':AZnDo_krAAEASUDJz2AhrYHquvOGlbw5qX8LJwkSmOalh_N8PMA9Me5E9CUvmmVjzD62ZRxCA0weyM6V2ntHjFCOKTJbQ-ObmX-0a8WDa9wF8ISoCinGe3nM2bbpbAZE5CFeiU7UbZm-27eON4bFr7B8TFCyfeyWf_SpGfAoYDiln4EfYvZXJI-cukpOoVldrgsl1EX6hgYCjpJ9d_dFhdRuksJSrgNdwKzATP0UsdKr_brOQqHXwbLrq7Rlc1UnaFXPNrtzo_XNjszWfJOUvo7VyLXVFi27MyvMCAoH5D9gITY01xqvAxook5XOVbbFD01cAKI:',
    'keep_alive': 'eyJ2IjoyLCJ0cyI6MTc1OTk4NDk5OTUwNiwiZW52Ijp7IndkIjowLCJ1YSI6MSwiY3YiOjEsImJyIjoxfSwiYmh2Ijp7Im1hIjo4MSwiY2EiOjIsImthIjoyLCJzYSI6MTcsImtiYSI6MCwidGEiOjAsInQiOjc1LCJubSI6MSwibXMiOjAuNSwibWoiOjAuNTUsIm1zcCI6MC40NSwidmMiOjEsImNwIjowLjkzLCJyYyI6MCwia2oiOjAsImtpIjowLCJzcyI6MC4yNiwic2oiOjAuMzksInNzbSI6MC44OCwic3AiOjQsInRzIjowLCJ0aiI6MCwidHAiOjAsInRzbSI6MH0sInNlcyI6eyJwIjoxMSwicyI6MTc1OTkyMzkzMzMxNywiZCI6NjA0NzN9fQ%3D%3D',
}

headers = {
    'accept': '*/*',
    'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
    'content-type': 'application/json',
    'if-none-match': '"cacheable:9e7eb213edc8d3489468ee3dee894386"',
    'priority': 'u=1, i',
    'referer': 'https://southstardrug.com.ph/products/cardiclear-fish-oil-1000-mg-softgel-capsule-10s-600-in-house-trade-account',
    'sec-ch-ua': '"Google Chrome";v="141", "Not?A_Brand";v="8", "Chromium";v="141"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36',
    # 'cookie': 'localization=PH; _shopify_y=794087fa-8ee5-4e01-9b7e-6a8a05617d2b; _tracking_consent=3.AMPS_AUWA_f_f_7AUxuHq8TwWPRARDwt06mw; _shopify_analytics=:AZnDo_lHAAEAyjgraiEIWjqyLm3AJM5zK8iheTo7GvecDngxOjZXOPHfHpjclA:; WISHLIST_TOTAL=0; WISHLIST_PRODUCTS_IDS={}; WISHLIST_PRODUCTS_IDS_SET=1; WISHLIST_UUID=null; WISHLIST_IP_ADDRESS=103.108.231.19; _fbp=fb.2.1759923940325.201946050156262699; _shopify_s=7be1b684-b1c2-4f2d-a9ae-500a3e4ff3de; epb_previous_pathname=/products/cardiclear-fish-oil-1000-mg-softgel-capsule-10s-600-in-house-trade-account; fsb_previous_pathname=/products/cardiclear-fish-oil-1000-mg-softgel-capsule-10s-600-in-house-trade-account; _shopify_essential=:AZnDo_krAAEASUDJz2AhrYHquvOGlbw5qX8LJwkSmOalh_N8PMA9Me5E9CUvmmVjzD62ZRxCA0weyM6V2ntHjFCOKTJbQ-ObmX-0a8WDa9wF8ISoCinGe3nM2bbpbAZE5CFeiU7UbZm-27eON4bFr7B8TFCyfeyWf_SpGfAoYDiln4EfYvZXJI-cukpOoVldrgsl1EX6hgYCjpJ9d_dFhdRuksJSrgNdwKzATP0UsdKr_brOQqHXwbLrq7Rlc1UnaFXPNrtzo_XNjszWfJOUvo7VyLXVFi27MyvMCAoH5D9gITY01xqvAxook5XOVbbFD01cAKI:; keep_alive=eyJ2IjoyLCJ0cyI6MTc1OTk4NDk5OTUwNiwiZW52Ijp7IndkIjowLCJ1YSI6MSwiY3YiOjEsImJyIjoxfSwiYmh2Ijp7Im1hIjo4MSwiY2EiOjIsImthIjoyLCJzYSI6MTcsImtiYSI6MCwidGEiOjAsInQiOjc1LCJubSI6MSwibXMiOjAuNSwibWoiOjAuNTUsIm1zcCI6MC40NSwidmMiOjEsImNwIjowLjkzLCJyYyI6MCwia2oiOjAsImtpIjowLCJzcyI6MC4yNiwic2oiOjAuMzksInNzbSI6MC44OCwic3AiOjQsInRzIjowLCJ0aiI6MCwidHAiOjAsInRzbSI6MH0sInNlcyI6eyJwIjoxMSwicyI6MTc1OTkyMzkzMzMxNywiZCI6NjA0NzN9fQ%3D%3D',
}


class SouthPdpSpider(PricemateBaseSpider):
    name = "south_pdp"

    def __init__(self, retailer, region, *args, **kwargs):
        super().__init__(retailer=retailer, region=region, *args, **kwargs)
        # self.stock_status_dict = {}  <-- Removed: Not needed anymore

    @staticmethod
    def extract_size(size_string):
        # ... (Keep your existing extract_size logic here) ...
        try:
            size_string = size_string.strip()
            pattern1 = r'(?:Size|Pack Size)[:\s]*([\d.]+)\s*(mg|mcg|ml|mL|l|L|g|kg|oz|lb|packs?|pack|tablets?|capsules?)'
            match = re.search(pattern1, size_string, re.IGNORECASE)
            if match: return f"{match.group(1)} {match.group(2)}"

            pattern2 = r'([\d.]+)\s*(mg|mcg|ml|mL|l|L|g|kg|oz|lb|packs?|pack|tablets?|capsules?)'
            match = re.search(pattern2, size_string, re.IGNORECASE)
            if match: return f"{match.group(1)} {match.group(2)}"

            pattern3 = r'([\d.]+)\s*(mg|mcg|ml|mL|l|L|g|kg|oz|lb)\s*[×xX]\s*(\d+)'
            match = re.search(pattern3, size_string, re.IGNORECASE)
            if match: return f"{match.group(1)} {match.group(2)} x {match.group(3)}"

            pattern4 = r'(\d+)\s*(個|本入り|袋|本)'
            match = re.search(pattern4, size_string, re.IGNORECASE)
            if match: return f"{match.group(1)} {match.group(2)}"

            pattern5 = r'(\d+)[sS]\b'
            match = re.search(pattern5, size_string, re.IGNORECASE)
            if match: return f"{match.group(1)} pcs"

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

            # We only create ONE meta object initially for the first request (HTML)
            # We include data needed for the FUTURE request (JSON) here too
            meta = {
                "proxy": "http://21ed11ef5c872bc7727680a52233027db4578a0e:@api.zenrows.com:8001",
                "url": url,
                "_id": hash_id,
                "slug": slug,  # Store slug to reconstruct filename later
                "filename": f"size_{slug}_page.html",
                "should_be": ["ProductSubmitButton"]
            }

            # Step 1: Request the HTML Page to check stock
            yield scrapy.Request(
                url=url,
                cookies=cookies,
                headers=headers,
                callback=self.parse_html_stock,
                meta=meta,
                dont_filter=True
            )

    def parse_html_stock(self, response):
        meta = response.meta

        # --- Logic Step 1: Check Availability ---
        is_available = True  # default
        try:
            button_text = response.xpath(
                '//div[@class="product-form__buttons"]//button[@type="submit"]//span/text()'
            ).get()

            if button_text and button_text.strip() == "Available Soon":
                is_available = False
        except Exception as e:
            self.logger.error(f"Error checking stock for {response.url}: {e}")

        # --- Logic Step 2: Prepare for Next Request (JSON) ---

        # Update meta with the availability we just found
        meta['is_available'] = is_available

        # Update meta fields for the JSON request (ZenRows config)
        slug = meta.get('slug', 'product')
        meta['filename'] = f"PDP_{slug}_page.html"
        meta['should_be'] = ["product"]

        # Yield the chained request
        yield scrapy.Request(
            url=f"{response.url}.json",
            cookies=cookies,
            headers=headers,
            callback=self.process_category,
            meta=meta
        )

    def process_category(self, response):
        meta = response.meta
        prod_url = meta.get("url")
        doc_id = meta.get("_id")

        # Retrieve the availability passed from the previous function
        is_available = meta.get("is_available")

        product_json = json.loads(response.text)
        product = product_json.get("product", {})
        name = product.get("title")
        brand = product.get("vendor")

        variants = product.get("variants", [])
        variant = variants[0] if variants else {}
        product_id = variant.get("product_id")
        price = float(variant.get("price", "0") or 0)
        was_price = float(variant.get("compare_at_price", "0") or 0)

        if not was_price or was_price == price:
            was_price = ""
            rrp = price
        else:
            rrp = was_price

        images_list = product.get("images", [])
        if images_list:
            image_urls = [image.get("src") for image in images_list if image.get("src")]
            images_combined = " | ".join(image_urls)
        else:
            images_combined = ""

        barcode = variant.get("barcode")
        pack_size = self.extract_size(name)

        breadcrumb = f"Home > {name}"
        product_hash = self.generate_hash_id(prod_url, self.retailer, self.region)

        item = {
            "_id": product_hash,
            "Name": name,
            "Promo_Type": "",
            "Price": price,
            "per_unit_price": "",
            "WasPrice": was_price,
            "Offer_info": "",
            "Pack_size": pack_size,
            "Barcode": barcode,
            "Images": images_combined,
            "ProductURL": prod_url,
            "is_available": is_available,  # This will now be populated correctly
            "Status": "Done",
            "ParentCode": "",
            "ProductCode": product_id,
            "retailer_name": "southstardrug-ph",
            "Category_Hierarchy": breadcrumb,
            "Brand": brand,
            "RRP": rrp
        }

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
        # import subprocess
        # cmd = [
        #     "python",
        #     "upload_to_s3_direct.py",
        #     "--domain", "southstardrug.com.ph"
        # ]
        # subprocess.run(cmd, cwd=r"E:\pricemate_service")
        self.mongo_client.close()

if __name__ == '__main__':
    from scrapy.cmdline import execute
    execute("scrapy crawl south_pdp -a retailer=southstardrug-ph -a region=ph -a Type=eshop -a RetailerCode=southstardrug_ph".split())
