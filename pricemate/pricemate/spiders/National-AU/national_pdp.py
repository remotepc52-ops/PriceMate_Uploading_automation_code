import json
import re
import scrapy
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from pricemate.spiders.bs_spider import PricemateBaseSpider

cookies = {
    'sbjs_migrations': '1418474375998%3D1',
    'sbjs_current_add': 'fd%3D2025-10-14%2004%3A25%3A35%7C%7C%7Cep%3Dhttps%3A%2F%2Fwww.nationalpharmacies.com.au%2F%7C%7C%7Crf%3D%28none%29',
    'sbjs_first_add': 'fd%3D2025-10-14%2004%3A25%3A35%7C%7C%7Cep%3Dhttps%3A%2F%2Fwww.nationalpharmacies.com.au%2F%7C%7C%7Crf%3D%28none%29',
    'sbjs_current': 'typ%3Dtypein%7C%7C%7Csrc%3D%28direct%29%7C%7C%7Cmdm%3D%28none%29%7C%7C%7Ccmp%3D%28none%29%7C%7C%7Ccnt%3D%28none%29%7C%7C%7Ctrm%3D%28none%29%7C%7C%7Cid%3D%28none%29%7C%7C%7Cplt%3D%28none%29%7C%7C%7Cfmt%3D%28none%29%7C%7C%7Ctct%3D%28none%29',
    'sbjs_first': 'typ%3Dtypein%7C%7C%7Csrc%3D%28direct%29%7C%7C%7Cmdm%3D%28none%29%7C%7C%7Ccmp%3D%28none%29%7C%7C%7Ccnt%3D%28none%29%7C%7C%7Ctrm%3D%28none%29%7C%7C%7Cid%3D%28none%29%7C%7C%7Cplt%3D%28none%29%7C%7C%7Cfmt%3D%28none%29%7C%7C%7Ctct%3D%28none%29',
    'sbjs_udata': 'vst%3D3%7C%7C%7Cuip%3D%28none%29%7C%7C%7Cuag%3DMozilla%2F5.0%20%28Windows%20NT%2010.0%3B%20Win64%3B%20x64%29%20AppleWebKit%2F537.36%20%28KHTML%2C%20like%20Gecko%29%20Chrome%2F141.0.0.0%20Safari%2F537.36',
    'sbjs_session': 'pgs%3D2%7C%7C%7Ccpg%3Dhttps%3A%2F%2Fwww.nationalpharmacies.com.au%2Fproduct%2Fpalm-beach-sparkling-lychee-200ml-fragrance-diffuser%2F',
}

headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
    'cache-control': 'max-age=0',
    'if-modified-since': 'Tue, 14 Oct 2025 10:57:58 GMT',
    'priority': 'u=0, i',
    'referer': 'https://www.nationalpharmacies.com.au/product-sitemap3.xml',
    'sec-ch-ua': '"Google Chrome";v="141", "Not?A_Brand";v="8", "Chromium";v="141"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36',
    # 'cookie': 'sbjs_migrations=1418474375998%3D1; sbjs_current_add=fd%3D2025-10-14%2004%3A25%3A35%7C%7C%7Cep%3Dhttps%3A%2F%2Fwww.nationalpharmacies.com.au%2F%7C%7C%7Crf%3D%28none%29; sbjs_first_add=fd%3D2025-10-14%2004%3A25%3A35%7C%7C%7Cep%3Dhttps%3A%2F%2Fwww.nationalpharmacies.com.au%2F%7C%7C%7Crf%3D%28none%29; sbjs_current=typ%3Dtypein%7C%7C%7Csrc%3D%28direct%29%7C%7C%7Cmdm%3D%28none%29%7C%7C%7Ccmp%3D%28none%29%7C%7C%7Ccnt%3D%28none%29%7C%7C%7Ctrm%3D%28none%29%7C%7C%7Cid%3D%28none%29%7C%7C%7Cplt%3D%28none%29%7C%7C%7Cfmt%3D%28none%29%7C%7C%7Ctct%3D%28none%29; sbjs_first=typ%3Dtypein%7C%7C%7Csrc%3D%28direct%29%7C%7C%7Cmdm%3D%28none%29%7C%7C%7Ccmp%3D%28none%29%7C%7C%7Ccnt%3D%28none%29%7C%7C%7Ctrm%3D%28none%29%7C%7C%7Cid%3D%28none%29%7C%7C%7Cplt%3D%28none%29%7C%7C%7Cfmt%3D%28none%29%7C%7C%7Ctct%3D%28none%29; sbjs_udata=vst%3D3%7C%7C%7Cuip%3D%28none%29%7C%7C%7Cuag%3DMozilla%2F5.0%20%28Windows%20NT%2010.0%3B%20Win64%3B%20x64%29%20AppleWebKit%2F537.36%20%28KHTML%2C%20like%20Gecko%29%20Chrome%2F141.0.0.0%20Safari%2F537.36; sbjs_session=pgs%3D2%7C%7C%7Ccpg%3Dhttps%3A%2F%2Fwww.nationalpharmacies.com.au%2Fproduct%2Fpalm-beach-sparkling-lychee-200ml-fragrance-diffuser%2F',
}

class NationalPdpSpider(PricemateBaseSpider):
    name = "national_pdp"

    def __init__(self, retailer, region, *args, **kwargs):
        super().__init__(retailer=retailer, region=region, *args, **kwargs)

        self.api_key = "21ed11ef5c872bc7727680a52233027db4578a0e"  # same as category spider
        self.zenrows_url = "https://api.zenrows.com/v1/"

    @staticmethod
    def extract_size(size_string):
        try:
            size_string = size_string.strip()

            units = r'ml|mL|l|L|g|kg|oz|lb|m|cm|meter|meters|packs?|pack|tablets?|capsules?'

            # 1️⃣ Size or Pack Size with single value
            pattern1 = rf'(?:Size|Pack Size)[:\s]*([\d.]+)\s*({units})'
            match = re.search(pattern1, size_string, re.IGNORECASE)
            if match:
                return f"{match.group(1)} {match.group(2)}"

            # 2️⃣ Simple number + unit
            pattern2 = rf'([\d.]+)\s*({units})'
            match = re.search(pattern2, size_string, re.IGNORECASE)
            if match:
                return f"{match.group(1)} {match.group(2)}"

            # 3️⃣ Pattern for dimensions with unit after second number, e.g. "180 x 90cm"
            pattern3 = rf'([\d.]+)\s*[×xX]\s*([\d.]+)\s*({units})'
            match = re.search(pattern3, size_string, re.IGNORECASE)
            if match:
                return f"{match.group(1)} x {match.group(2)} {match.group(3)}"

            # 4️⃣ Quantity with Japanese units
            pattern4 = r'(\d+)\s*(個|本入り|袋|本)'
            match = re.search(pattern4, size_string, re.IGNORECASE)
            if match:
                return f"{match.group(1)} {match.group(2)}"

            # 5️⃣ Pack size "Pk250", "Pack10"
            pattern5 = r'\b(Pk|Pack)(\d+)\b'
            match = re.search(pattern5, size_string, re.IGNORECASE)
            if match:
                return f"{match.group(1)}{match.group(2)}"

            return ""

        except Exception as e:
            return ""

    def start_requests(self):

        docs = self.category_input.find({
            "retailer": self.retailer,
            "region": self.region,
            "Status": "Pending"
        })
        for doc in docs:
            url = doc.get("url")
            hash_id = doc.get("_id")
            slug = url.split("/")[-2]
            params = {
                "apikey": self.api_key,
                "url": url,
                "js_render": "true",
                "premium_proxy": "true"
            }
            query = "&".join([f"{k}={v}" for k, v in params.items()])
            full_url = f"{self.zenrows_url}?{query}"

            meta = {
                "url": url,
                "_id": hash_id,
                "filename": f"Pdp_{slug}_page.html",
                "should_be": ["content-area"]
            }
            yield scrapy.Request(
                url=full_url,
                cookies=cookies,
                headers=headers,
                callback=self.process_category,
                meta=meta
            )
    def process_category(self, response):
        meta = response.meta
        prod_url = meta.get("url")
        doc_id = meta.get("_id")
        # # raw_json = response.xpath('//script[@type="application/ld+json"]/text()').get()
        # # product_json = json.loads(raw_json)
        #
        # name = response.xpath("//meta[@property='og:title']/@content").get()
        # brand = response.xpath("//h2[@class='product_title entry-title']/a/text()").get()
        # if not brand:
        #     brand = ""
        # price = response.xpath('//div[@class="member-price"]//div[@class="current-price"]//bdi/text()').get()
        # if price:
        #     price = price.strip().replace("$", "").replace(",", "")
        # was_price = response.xpath('//div[@class="member-price"]//div[@class="full-price"]//bdi/text()').get()
        # if was_price:
        #     rrp = was_price
        #     was_price = was_price.strip().replace("$", "").replace(",", "")
        # else:
        #     rrp = price
        #     was_price = ""
        #
        # # offer = response.xpath("offer")
        # sku = response.xpath('//div[@class="summary entry-summary"]//span[@class="sku"]/text()').get()
        # if not sku:
        #     sku = response.xpath('//div[@class="summary entry-summary"]/span[@class="sku"]/text()').get()
        # # barcode = response.xpath("barcode")
        # images = response.xpath('//figure//img/@src').getall()
        # if not images:
        #     images = response.xpath('//div[contains(@class,"woocommerce-product-gallery")]//img/@src').getall()
        # if images:
        #     images = [i.strip() for i in images if i.strip()]
        #     image_str = "|".join(images)
        # else:
        #     image_str = ""
        # size = self.extract_size(name)
        # stock_text = response.xpath('//p[contains(@class,"stock")]/text()').get()
        # if stock_text:
        #     stock_text = stock_text.strip()
        # is_available = False if stock_text and "out" in stock_text.lower() else True
        # breadcrumbs = response.xpath('//nav[contains(@class,"woocommerce-breadcrumb")]/a/text()').getall()
        # if breadcrumbs:
        #     breadcrumbs = [b.strip() for b in breadcrumbs if b.strip()]
        #     breadcrumb_str = " > ".join(breadcrumbs)
        # else:
        #     breadcrumb_str = ""
        #
        # product_hash = self.generate_hash_id(prod_url, self.retailer, self.region)
        # item = {"_id": product_hash, "Name": name, "Promo_Type": "", "Price": price, "per_unit_price": "",
        #         "WasPrice": was_price,
        #         "Offer_info": "", "Pack_size": size, "Barcode": "",
        #         "Images": image_str,
        #         "ProductURL": prod_url, "is_available": is_available,
        #         "Status": "Done", "ParentCode": "", "ProductCode": sku,
        #         "retailer_name": "nationalpharmacies_au",
        #         "Category_Hierarchy": breadcrumb_str, "Brand": brand, "RRP": rrp}
        #
        # try:
        #     self.save_product(item)
        #     print(f"✓ Successfully inserted {prod_url}")
        #     if doc_id:
        #         self.category_input.update_one(
        #             {"_id": doc_id},
        #             {"$set": {"Status": "Done"}}
        #         )
        # except Exception as e:
        #     print(e)

        name = response.xpath("//meta[@property='og:title']/@content").get()
        brand = response.xpath("//h2[@class='product_title entry-title']/a/text()").get() or ""

        # --- Prices ---
        price = response.xpath('//div[@class="member-price"]//div[@class="current-price"]//bdi/text()').get()
        price = price.strip().replace("$", "").replace(",", "") if price else ""

        was_price = response.xpath('//div[@class="member-price"]//div[@class="full-price"]//bdi/text()').get()
        was_price = was_price.strip().replace("$", "").replace(",", "") if was_price else ""
        rrp = was_price or price

        # --- Images ---
        images = response.xpath('//figure//img/@src').getall() or \
                 response.xpath('//div[contains(@class,"woocommerce-product-gallery")]//img/@src').getall()
        images = [i.strip() for i in images if i.strip()]
        image_str = "|".join(images) if images else ""

        # --- Breadcrumbs ---
        breadcrumbs = response.xpath('//nav[contains(@class,"woocommerce-breadcrumb")]/a/text()').getall()
        breadcrumb_str = " > ".join([b.strip() for b in breadcrumbs if b.strip()])

        # --- Try to detect variations ---
        variations_json = response.xpath('//form[contains(@class,"variations_form")]/@data-product_variations').get()

        if variations_json:
            try:
                variations = json.loads(variations_json)

                # Try to find parent product code (if mentioned anywhere)
                parent_sku = response.xpath('//span[@class="sku"]/text()').get()
                if parent_sku:
                    parent_sku = parent_sku.strip()

                for var in variations:
                    sku = str(var.get("sku") or "").strip()
                    if not sku:
                        raise ValueError(f"❌ Missing ProductCode (SKU) for product {prod_url}")

                    var_price = str(var.get("display_price") or price)
                    var_rrp = str(var.get("display_regular_price") or rrp)
                    is_available = bool(var.get("is_in_stock", True))

                    # Extract attribute(s) like size, color etc.
                    attrs = var.get("attributes", {})
                    size = next(iter(attrs.values()), "")
                    size = self.extract_size(size) or self.extract_size(name)

                    # Variation image
                    var_image = ""
                    if var.get("image") and var["image"].get("url"):
                        var_image = var["image"]["url"]
                    image_final = var_image or image_str

                    product_hash = self.generate_hash_id(sku, self.retailer, self.region)
                    item = {
                        "_id": product_hash,
                        "Name": name,
                        "Promo_Type": "",
                        "Price": var_price,
                        "per_unit_price": "",
                        "WasPrice": was_price,
                        "Offer_info": "",
                        "Pack_size": size,
                        "Barcode": "",
                        "Images": image_final,
                        "ProductURL": prod_url,
                        "is_available": is_available,
                        "Status": "Done",
                        "ParentCode": parent_sku or "",  # ✅ parent product code linkage
                        "ProductCode": sku,  # ✅ use SKU (e.g. 137839)
                        "retailer_name": "nationalpharmacies_au",
                        "Category_Hierarchy": breadcrumb_str,
                        "Brand": brand,
                        "RRP": var_rrp,
                    }

                    self.save_product(item)
                    print(f"✓ Inserted variation SKU {sku}")

            except Exception as e:
                print(f"⚠️ Variation parsing error: {e}")

        else:
            # --- Non-variation product ---
            sku = response.xpath('//span[@class="sku"]/text()').get()
            sku = str(sku).strip() if sku else ""
            if not sku:
                raise ValueError(f"❌ Missing ProductCode (SKU) for product {prod_url}")
            stock_text = response.xpath('//p[contains(@class,"stock")]/text()').get()
            is_available = not (stock_text and "out" in stock_text.lower())

            size = self.extract_size(name)
            product_hash = self.generate_hash_id(sku or prod_url, self.retailer, self.region)

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
                "retailer_name": "nationalpharmacies_au",
                "Category_Hierarchy": breadcrumb_str,
                "Brand": brand,
                "RRP": rrp,
            }

            self.save_product(item)
            print(f"✓ Inserted single product SKU {sku}")
        if doc_id:
            self.category_input.update_one({"_id": doc_id}, {"$set": {"Status": "Done"}})

    def close(self, reason):
        import subprocess
        cmd = [
            "python",
            "upload_to_s3_direct.py",
            "--domain", "nationalpharmacies.com.au"
        ]
        subprocess.run(cmd, cwd=r"E:\pricemate_service")
        self.mongo_client.close()

if __name__ == '__main__':
    from scrapy.cmdline import execute
    execute(
        "scrapy crawl national_pdp -a retailer=nationalpharmacies-au -a region=au -a Type=eshop -a RetailerCode=nationalpharmacies_au".split())