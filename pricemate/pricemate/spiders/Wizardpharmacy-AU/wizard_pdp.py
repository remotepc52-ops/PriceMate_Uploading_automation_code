import re
import scrapy
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from pricemate.spiders.base_spider_me import PricemateBaseSpider

cookies = {
    '_fbp': 'fb.2.1763873361984.424601933995042391',
    'SSESS511a7bcc5c76b391214fee9f12fa0d7b': 'EKpt9sHYJZeEqMEUVl9sZ721J9y8sl21cGV2i7BnyXc',
    'prism_799653711': '0743f156-d3ce-4b7a-9d0c-5f3825cc5fcf',
}

headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
    'cache-control': 'max-age=0',
    'priority': 'u=0, i',
    'sec-ch-ua': '"Google Chrome";v="143", "Chromium";v="143", "Not A(Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'cross-site',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36',
    # 'cookie': '_fbp=fb.2.1763873361984.424601933995042391; SSESS511a7bcc5c76b391214fee9f12fa0d7b=EKpt9sHYJZeEqMEUVl9sZ721J9y8sl21cGV2i7BnyXc; prism_799653711=0743f156-d3ce-4b7a-9d0c-5f3825cc5fcf',
}

class WizardPdpSpider(PricemateBaseSpider):
    name = "wizard_pdp"

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

        docs = self.product_url.find({
            "retailer": self.retailer,
            "region": self.region,
            "Status": "Pending"
        })
        for doc in docs:
            url = doc.get("ProductURL")
            hash_id = doc.get("_id")
            slug = url.split("/")[-1]

            region = "au"

            zenrows_res_proxies = {
                'http': f'http://3dbxcTLYpHGv:YF67LxHnCPRwc57_country-{region.lower()}@superproxy.zenrows.com:1337',
                'https': f'http://3dbxcTLYpHGv:YF67LxHnCPRwc57_country-{region.lower()}@superproxy.zenrows.com:1337',
            }

            current_proxy = '2c6ea6e6d8c14216a62781b8f850cd5b'

            proxy_host = "api.zyte.com"
            proxy_port = "8011"
            proxy_auth = f"{current_proxy}:"

            proxy_url = f"https://{proxy_auth}@{proxy_host}:{proxy_port}"
            # proxy_url = f'http://3dbxcTLYpHGv:YF67LxHnCPRwc57_country-{region.lower()}@superproxy.zenrows.com:1337'

            meta = {
                'proxy':proxy_url,
                "url": url,
                "_id": hash_id,
                "slug": slug,
                "filename": f"{slug}_page.html",
                "should_be": ['id="skip-link"']
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

        #Prod_Details
        # --- Product Name ---
        name = response.xpath(
            "string(//div[contains(@class, 'tw:text-4xl') and contains(@class, 'tw:font-bold')])"
        ).get()
        name = name.strip() if name else ""

        # --- Price (more precise) ---l
        price = response.xpath(
            "normalize-space(//div[contains(@class, 'tw:text-lg') and contains(@class, 'tw:font-bold')]/text())"
        ).get()

        if not price:
            price = response.xpath(
                "normalize-space(//div[contains(@class, 'tw:font-bold tw:text-4xl tw:text-wizard-deep-purple') and contains(text(), '$')]/text())"
            ).get()

        # Clean and convert price
        if price:
            price = price.strip().replace('$', '').replace(',', '')
            try:
                price = float(price)
            except ValueError:
                price = 0.0
        else:
            price = 0.0

        # ✅ Skip product if price is 0
        if price == 0.0:
            print(f"⏭️ Skipping product with $0 price: {prod_url}")
            self.category_input.update_one({"_id": doc_id}, {"$set": {"Status": "Not Found"}})
            return

        # --- Was Price ---
        was_price_raw = response.xpath(
            "normalize-space(//div[contains(@class, 'tw:font-normal') and contains(text(), 'Was')]/text())"
        ).get()

        if was_price_raw:
            was_price = was_price_raw.replace('Was $', '').replace(',', '').strip()
            try:
                was_price = float(was_price)
            except ValueError:
                was_price = ""
        else:
            was_price = ""

        # --- Images ---
        images = response.xpath("//img[@id='zoom_01']/@src").getall()
        images = [img.strip() for img in images if img.strip()]

        fixed_images = []

        for img in images:
            # Make relative URLs absolute
            if not img.startswith("https://"):
                img = f"https://www.wizardpharmacy.com.au{img}"

            # Change w-200 → w-1200 in ImageKit resize parameter
            img = img.replace("w-200", "w-1200")

            fixed_images.append(img)

        image_str = "|".join(fixed_images)

        # --- Product Code (try multiple locations) ---
        sku = response.xpath('//span[@class="sku"]/text()').get()
        if not sku:
            sku = response.xpath('//form[contains(@class,"cart")]/@data-product_sku').get()

        # fallback to JSON if still missing
        if not sku:
            script_text = " ".join(response.xpath('//script[contains(text(),"dataLayer")]/text()').getall())
            if script_text:
                import re
                match = re.search(r'"item_id"\s*:\s*"(\d+)"', script_text)
                if match:
                    sku = match.group(1)
        sku = sku.strip() if sku else ""

        # --- Brand ---
        brand = response.xpath("//a[contains(@href, '/brand/')]/text()").get() or ""

        # --- Breadcrumb Hierarchy ---
        breadcrumbs = response.xpath("//section[@class='breadcrumb-container']//ol[@class='breadcrumb']//li/a/text()").getall()
        breadcrumbs = [b.strip() for b in breadcrumbs if b.strip()]
        breadcrumb_str = " > ".join(breadcrumbs) if breadcrumbs else ""

        # --- Pack size ---
        size = self.extract_size(name)

        # --- Availability ---
        stock_text = response.xpath('//p[contains(@class,"stock")]/text()').get()
        is_available = not (stock_text and "out" in stock_text.lower())

        # --- RRP ---
        rrp = was_price or price

        # ✅ --- Validation (Critical Fields) ---
        if not name or not price or not sku:
            self.category_input.update_one({"_id": doc_id}, {"$set": {"Status": "Not Found"}})
            raise ValueError(
                f"❌ Missing critical field(s) on product page: {prod_url} "
                f"[Name='{name}', Price='{price}', ProductCode='{sku}']"
            )


        # --- Build Final Product Data ---
        product_hash = self.generate_hash_id(sku, self.retailer, self.region)
        item = {
            "_id": product_hash,
            "Name": name,
            "Promo_Type": "",
            "Price": price,
            "per_unit_price": "",
            "WasPrice": was_price,
            "Offer_info": "",
            "Pack_size": size,
            "Barcode": "",
            "Images": image_str,
            "ProductURL": prod_url,
            "is_available": is_available,
            "Status": "Done",
            "ParentCode": "",
            "ProductCode": sku,
            "retailer": self.retailer,
            "retailer_name": "wizardpharmacy_au",
            "Category_Hierarchy": breadcrumb_str,
            "Brand": brand,
            "RRP": rrp,
        }

        # --- Save Product ---
        self.product_table.update_one(
            {"ProductURL": item["ProductURL"], "retailer": item["retailer"]},
            {"$set": item},
            upsert=True
        )
        print(f"✓ Inserted product SKU {sku}: {name}")

        self.product_url.update_one({"_id": doc_id}, {"$set": {"Status": "Done"}})

    def close(self, reason):
        # import subprocess
        # cmd = [
        #     "python",
        #     "upload_to_s3_direct.py",
        #     "--domain", "wizardpharmacy.com"
        # ]
        # subprocess.run(cmd, cwd=r"E:\pricemate_service")
        self.mongo_client.close()

if __name__ == '__main__':
    from scrapy.cmdline import execute
    execute("scrapy crawl wizard_pdp -a retailer=wizardpharmacy-au -a region=au -a Type=eshop -a RetailerCode=wizardpharmacy_au".split())