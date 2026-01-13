import json
import re
from urllib.parse import urljoin
import scrapy
import os
import sys

# Ensure project path is in sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from pricemate.spiders.bs_spider import PricemateBaseSpider

cookies = {
    'fornax_anonymousId': 'e336ab3d-c3c9-4c70-839e-d0375074061a',
    'SHOP_SESSION_TOKEN': 'ce0320a5-5755-4724-bc46-cbfa35564c23',
    '_shg_user_id': '2282d256-e45a-42e7-ad53-28966e9b2c2a',
    'lantern': 'a972cd83-8c20-4265-b996-30fc8b76b1e2',
    '_fbp': 'fb.2.1764745571590.353855508197657284',
    'STORE_VISITOR': '1',
    'SF-CSRF-TOKEN': '41781fca-27cb-4116-b5dd-d19baf4b4788',
    'athena_short_visit_id': 'da9c380a-7052-45ea-93ec-082ef21f59ec:1765263746',
    'XSRF-TOKEN': '2b7527c6da0fb438122712132451e06a5c132135e56dbead22e123c1373b18c5',
    '__cf_bm': 'F0uC4qpEHnJ2orntCITq_r5bQ.CHdvIdJlDFm7c_Ycw-1765263746-1.0.1.1-5pbFHlxyDFLvEaRvC8NfwY6QzpiDodgXyesNaktPExqDfOW0quC2loMfVnMVvnfLguTwt14IdWADYm3eWWIxnKL8se98EVIxBORXybCPG1E',
    '_vwo_uuid_v2': 'D8A7E74D2D5B81A0D7ECCE120DDC59C0C|e3aa349a350e816a375e9ec1befc6c37',
    '_shg_session_id': 'd6d64f0c-12f9-4897-8cde-a2f3704d2c19',
    '_gcl_au': '1.1.315626057.1765263748',
    '__kla_id': 'eyJjaWQiOiJaRE00WW1Rd1l6RXROVGszWWkwMFlqQTNMVGszTXprdFptRXhZemRsWlRJNU5qYzEifQ==',
    '_clck': 'q5yr68%5E2%5Eg1p%5E0%5E2169',
    'sa-user-id': 's%253A0-b2e3ad93-ec10-5b45-5cf5-0cd911fa67a6.pGGSFqRk9r2km%252BQNHtDpAR2o%252BgBd9HS3ZRftx9kMos0',
    'sa-user-id-v2': 's%253AsuOtk-wQW0Vc9QzZEfpnpg5ga4s.N1gQyb0hoLTqTb20tQ0D4o2XYODjr5LTsu5ydk184LI',
    'sa-user-id-v3': 's%253AAQAKIF-QE2OTq0kQOy9O_VCmVl00Mm5IoNFULPi-U1ADDDCDEAEYAyD4z8nJBjABOgTXE9rbQgRnxab8.ColZzY1B6b3O8F1pC%252BakyRzQBqiv24tdYGmZwA97RZc',
    'yotpo_pixel': '847b40ed-3233-4901-ad43-12600fda8fc6',
    '_sp_ses.655f': '*',
    '_pin_unauth': 'dWlkPVpUZzBZVEptWVRFdE1ETmhZaTAwTXpnMUxXRmhNbUV0TjJNMFpXRTJORGt3TUdJNQ',
    '_tt_enable_cookie': '1',
    '_ttp': '01KC0YPCJ9NMDNK7PX03ZXT5S6_.tt.2',
    '_gid': 'GA1.3.1317817617.1765263750',
    '_vid_t': 'KzUrHFTG9gO5RNnINX8nGxlKMNoh6U0Cs3TFQHiFrl7s7LSmBaLvsXEYTL1+J/+j9Aqnn2P30nEwVA==',
    'viewPosts[limit]': '12',
    'dicbo_id': '%7B%22dicbo_fetch%22%3A1765264312127%7D',
    'lastVisitedCategory': '1351',
    '_dc_gtm_UA-292047-1': '1',
    'ssViewedProducts': 'GYGLU-P%2CCEOCWR%2CLNES%2CSGPOT%2CHLLD-P',
    'ssUserId': 'e28326cd-8a65-446c-a7ab-60a39c0fd6ba',
    'ssSessionId': '8f15780f-6b5b-4186-8ff6-6940403d4d15',
    '_uetsid': '0682a560d4cd11f0bbe9f113328e6ea7',
    '_uetvid': '0682d6c0d4cd11f08aeb857ee0e13687',
    '_clsk': 'epz9bd%5E1765264423245%5E10%5E1%5Ei.clarity.ms%2Fcollect',
    '_ga_FDT06VXH78': 'GS2.1.s1765263748$o1$g1$t1765264423$j6$l0$h0',
    '_ga_9SH1YV1CB5': 'GS2.1.s1765263748$o1$g1$t1765264423$j5$l0$h0',
    '_ga': 'GA1.3.975374210.1765263748',
    'ttcsid': '1765263749709::6j6u1wSRD8YHtsq1-sVE.1.1765264424737.0',
    'ttcsid_CID5P93C77U4TTM9NL0G': '1765264308039::1O_HusgI5ozLyve5yUMe.1.1765264424738.1',
    'cto_bundle': 'EQsUrl9oQkdzQ1dXaEF3eENCOG1Jc08wT1VnTkFXYm5MQzhBemRoc0VWOUh0N0UzblBiJTJCZ1Y0UmFCNERPQnRwSUJ4Z3JNcmZWQjRQJTJGa0pYWlFHREVjRnp4RWFybWlJRWoxNSUyQjI2N1cyTEVUcUtJWnZJN1lBV2FkdFBNcXd4WnQ0MFNqN1Q5dmhCV3FzcWhnNmZDN3JFJTJCTkFIWHdQcDVaS015QWZIR0tBRXU4ZjhoVSUzRA',
    'Shopper-Pref': 'E136FAADD016E6975B6F0FC159AA7E1779104AB0-1765869228697-x%7B%22cur%22%3A%22NZD%22%2C%22funcConsent%22%3Atrue%7D',
    '_sp_id.655f': '31a52e4b61d90539.1765263749.1.1765264443.1765263749',
}

headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
    'cache-control': 'max-age=0',
    'priority': 'u=0, i',
    'referer': 'https://www.healthpost.co.nz/health-concerns/?view=products&page=2',
    'sec-ch-ua': '"Chromium";v="142", "Google Chrome";v="142", "Not_A Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36',
    # 'cookie': 'fornax_anonymousId=e336ab3d-c3c9-4c70-839e-d0375074061a; SHOP_SESSION_TOKEN=ce0320a5-5755-4724-bc46-cbfa35564c23; _shg_user_id=2282d256-e45a-42e7-ad53-28966e9b2c2a; lantern=a972cd83-8c20-4265-b996-30fc8b76b1e2; _fbp=fb.2.1764745571590.353855508197657284; STORE_VISITOR=1; SF-CSRF-TOKEN=41781fca-27cb-4116-b5dd-d19baf4b4788; athena_short_visit_id=da9c380a-7052-45ea-93ec-082ef21f59ec:1765263746; XSRF-TOKEN=2b7527c6da0fb438122712132451e06a5c132135e56dbead22e123c1373b18c5; __cf_bm=F0uC4qpEHnJ2orntCITq_r5bQ.CHdvIdJlDFm7c_Ycw-1765263746-1.0.1.1-5pbFHlxyDFLvEaRvC8NfwY6QzpiDodgXyesNaktPExqDfOW0quC2loMfVnMVvnfLguTwt14IdWADYm3eWWIxnKL8se98EVIxBORXybCPG1E; _vwo_uuid_v2=D8A7E74D2D5B81A0D7ECCE120DDC59C0C|e3aa349a350e816a375e9ec1befc6c37; _shg_session_id=d6d64f0c-12f9-4897-8cde-a2f3704d2c19; _gcl_au=1.1.315626057.1765263748; __kla_id=eyJjaWQiOiJaRE00WW1Rd1l6RXROVGszWWkwMFlqQTNMVGszTXprdFptRXhZemRsWlRJNU5qYzEifQ==; _clck=q5yr68%5E2%5Eg1p%5E0%5E2169; sa-user-id=s%253A0-b2e3ad93-ec10-5b45-5cf5-0cd911fa67a6.pGGSFqRk9r2km%252BQNHtDpAR2o%252BgBd9HS3ZRftx9kMos0; sa-user-id-v2=s%253AsuOtk-wQW0Vc9QzZEfpnpg5ga4s.N1gQyb0hoLTqTb20tQ0D4o2XYODjr5LTsu5ydk184LI; sa-user-id-v3=s%253AAQAKIF-QE2OTq0kQOy9O_VCmVl00Mm5IoNFULPi-U1ADDDCDEAEYAyD4z8nJBjABOgTXE9rbQgRnxab8.ColZzY1B6b3O8F1pC%252BakyRzQBqiv24tdYGmZwA97RZc; yotpo_pixel=847b40ed-3233-4901-ad43-12600fda8fc6; _sp_ses.655f=*; _pin_unauth=dWlkPVpUZzBZVEptWVRFdE1ETmhZaTAwTXpnMUxXRmhNbUV0TjJNMFpXRTJORGt3TUdJNQ; _tt_enable_cookie=1; _ttp=01KC0YPCJ9NMDNK7PX03ZXT5S6_.tt.2; _gid=GA1.3.1317817617.1765263750; _vid_t=KzUrHFTG9gO5RNnINX8nGxlKMNoh6U0Cs3TFQHiFrl7s7LSmBaLvsXEYTL1+J/+j9Aqnn2P30nEwVA==; viewPosts[limit]=12; dicbo_id=%7B%22dicbo_fetch%22%3A1765264312127%7D; lastVisitedCategory=1351; _dc_gtm_UA-292047-1=1; ssViewedProducts=GYGLU-P%2CCEOCWR%2CLNES%2CSGPOT%2CHLLD-P; ssUserId=e28326cd-8a65-446c-a7ab-60a39c0fd6ba; ssSessionId=8f15780f-6b5b-4186-8ff6-6940403d4d15; _uetsid=0682a560d4cd11f0bbe9f113328e6ea7; _uetvid=0682d6c0d4cd11f08aeb857ee0e13687; _clsk=epz9bd%5E1765264423245%5E10%5E1%5Ei.clarity.ms%2Fcollect; _ga_FDT06VXH78=GS2.1.s1765263748$o1$g1$t1765264423$j6$l0$h0; _ga_9SH1YV1CB5=GS2.1.s1765263748$o1$g1$t1765264423$j5$l0$h0; _ga=GA1.3.975374210.1765263748; ttcsid=1765263749709::6j6u1wSRD8YHtsq1-sVE.1.1765264424737.0; ttcsid_CID5P93C77U4TTM9NL0G=1765264308039::1O_HusgI5ozLyve5yUMe.1.1765264424738.1; cto_bundle=EQsUrl9oQkdzQ1dXaEF3eENCOG1Jc08wT1VnTkFXYm5MQzhBemRoc0VWOUh0N0UzblBiJTJCZ1Y0UmFCNERPQnRwSUJ4Z3JNcmZWQjRQJTJGa0pYWlFHREVjRnp4RWFybWlJRWoxNSUyQjI2N1cyTEVUcUtJWnZJN1lBV2FkdFBNcXd4WnQ0MFNqN1Q5dmhCV3FzcWhnNmZDN3JFJTJCTkFIWHdQcDVaS015QWZIR0tBRXU4ZjhoVSUzRA; Shopper-Pref=E136FAADD016E6975B6F0FC159AA7E1779104AB0-1765869228697-x%7B%22cur%22%3A%22NZD%22%2C%22funcConsent%22%3Atrue%7D; _sp_id.655f=31a52e4b61d90539.1765263749.1.1765264443.1765263749',
}


class HealthPostSpider(PricemateBaseSpider):
    name = "healthpost_pdp"

    custom_settings = {
        # 'CONCURRENT_REQUESTS': 1,
        # 'DOWNLOAD_DELAY': 2,
        'RETRY_TIMES': 3,
    }

    def __init__(self, retailer, region, *args, **kwargs):
        super().__init__(retailer=retailer, region=region, *args, **kwargs)
        self.logger.info(f"Spider initialized for {retailer} in {region}")

    @staticmethod
    def extract_size(text):
        """Extract size/pack information from product name"""
        if not text: return ""
        try:
            text = text.strip()
            pattern1 = r'(\d+)\s*(tablets?|capsules?|vcaps?|softgels?|ml|mL|g|kg|oz|lb|l|L)\b'
            match = re.search(pattern1, text, re.IGNORECASE)
            if match: return f"{match.group(1)} {match.group(2)}"

            pattern2 = r'(?:size|pack\s*size)[:\s]+(\d+)\s*(ml|mL|l|L|g|kg|oz|lb)'
            match = re.search(pattern2, text, re.IGNORECASE)
            if match: return f"{match.group(1)} {match.group(2)}"
            return ""
        except Exception:
            return ""

    def start_requests(self):
        try:
            if not hasattr(self, 'product_url'):
                self.logger.warning("Local Mode: No product_url collection found.")
                urls = ["https://www.healthpost.co.nz/go-healthy-go-glucosamine-1-a-day-gyglu-p"]
                for url in urls:
                    yield scrapy.Request(url, callback=self.parse_product, headers=headers, cookies=cookies)
                return

            docs = self.product_url.find({
                "retailer": self.retailer,
                "region": self.region,
                "Status": "Pending"
            })

            for doc in docs:
                url = doc.get("ProductURL")
                hash_id = doc.get("_id")
                slug = url.split("/")[-1]
                if not url: continue

                meta = {
                    'url': url,
                    '_id': hash_id,
                    "filename": f"{slug}_page.html",
                    "should_be": ['no-js pages-product'],
                    'dont_redirect': True
                }
                yield scrapy.Request(
                    url, callback=self.parse_product, meta=meta,
                    headers=headers, cookies=cookies,
                    errback=self.errback_httpbin, dont_filter=True
                )

        except Exception as e:
            self.logger.error(f"Error in start_requests: {e}")

    def errback_httpbin(self, failure):
        self.logger.error(f"Request failed: {failure.request.url}")
        if failure.request.meta.get('_id') and hasattr(self, 'product_url'):
            self.product_url.update_one(
                {"_id": failure.request.meta['_id']},
                {"$set": {"Status": "Failed", "Error": str(failure.value)}}
            )

    def parse_product(self, response):
        meta = response.meta
        prod_url = meta.get("url", response.url)
        doc_id = meta.get("_id")

        try:
            # --- 1. Master Template ---
            template_item = {
                "_id": "", "Barcode": "", "Brand": "", "Category_Hierarchy": "",
                "Images": "", "Name": "", "Offer_info": "", "Pack_size": "", "ParentCode": "",
                "Price": "", "ProductCode": "", "ProductURL": prod_url, "Promo_Type": "",
                "RRP": "", "Status": "Done", "WasPrice": "", "is_available": True,
                "per_unit_price": "", "retailer": self.retailer, "retailer_name": self.retailer
            }

            # --- 2. Extract JSON Data ---
            custom_data = None
            json_pattern = r'<script id="custom-product-price"[^>]*>(.*?)</script>'
            match = re.search(json_pattern, response.text, re.DOTALL)
            if match:
                try:
                    custom_data = json.loads(match.group(1))
                except json.JSONDecodeError:
                    pass

            # --- 3. Base Attributes ---
            name = ""
            sku = ""
            price = 0.0
            source_rrp = 0.0
            brand = ""
            parent_id = None
            barcode = ""
            saved_value = 0.0  # From JSON 'saved'

            if custom_data:
                name = custom_data.get('title', '').strip()
                sku = custom_data.get('sku', '').strip()
                parent_id = custom_data.get('id')

                # Barcode / UPC
                if custom_data.get('upc'):
                    barcode = str(custom_data.get('upc')).strip()
                if not barcode and custom_data.get('gtin'):
                    barcode = str(custom_data.get('gtin')).strip()

                # Price & RRP & Saved
                if custom_data.get('price'):
                    p_data = custom_data['price']
                    if isinstance(p_data, dict):
                        if p_data.get('without_tax'):
                            price = float(p_data['without_tax'].get('value', 0))
                        if p_data.get('rrp_without_tax'):
                            val = p_data['rrp_without_tax'].get('value')
                            if val: source_rrp = float(val)
                        # Check for 'saved' object in price
                        if p_data.get('saved'):
                            val = p_data['saved'].get('value')
                            if val: saved_value = float(val)

                # Check top-level 'saved' object if not in price
                if not saved_value and custom_data.get('saved'):
                    val = custom_data['saved'].get('value')
                    if val: saved_value = float(val)

                if custom_data.get('brand'):
                    brand = custom_data['brand'].get('name') if isinstance(custom_data['brand'], dict) else str(
                        custom_data['brand'])

            # Fallbacks
            if not name: name = response.xpath('//h1/text()').get(default='').strip()
            if not sku: sku = response.xpath('//span[@itemprop="sku"]/text()').get(default='').strip()
            if not parent_id:
                pid_val = response.xpath('//input[@name="product_id"]/@value').get()
                if pid_val and pid_val.isdigit():
                    parent_id = int(pid_val)

            if not parent_id:
                raise ValueError("No Parent ID found to use as ProductCode")

            # Images
            img_urls = response.css('.productView-image--default::attr(src)').getall()
            if not img_urls: img_urls = response.css('.productView-thumbnail-link::attr(href)').getall()
            images_str = "|".join([u.replace('{:size}', '1280x1280') for u in set(img_urls)])

            # Breadcrumbs
            # breadcrumbs = response.css('.breadcrumbs .breadcrumb-label::text').getall()
            # breadcrumb_str = " > ".join([b.strip() for b in breadcrumbs if b.strip()])

            breadcrumbs = response.css(
                'ul.breadcrumbs.desktopOnly .breadcrumb-label::text'
            ).getall()

            breadcrumb_str = " > ".join(b.strip() for b in breadcrumbs if b.strip())


            # Helper for Price & Offer Logic
            def calculate_prices_and_offer(current_price, raw_rrp_val, raw_saved_val):
                """
                Returns final_rrp, final_was, offer_string
                Logic:
                - RRP/WasPrice set by comparison.
                - Offer_info calculated if savings exist.
                """
                was_p = ""
                # Determine WasPrice/RRP
                if raw_rrp_val and raw_rrp_val > current_price:
                    was_p = raw_rrp_val

                final_rrp = 0.0
                if was_p and current_price < was_p:
                    final_rrp = was_p
                else:
                    final_rrp = current_price
                    was_p = ""

                # Calculate Offer Info
                offer_str = ""

                # Method 1: Use raw_saved_val from JSON if available
                savings = 0.0
                if raw_saved_val and raw_saved_val > 0:
                    savings = raw_saved_val
                # Method 2: Calculate from RRP - Price
                elif final_rrp > current_price:
                    savings = final_rrp - current_price

                if savings > 0 and final_rrp > 0:
                    pct = int((savings / final_rrp) * 100)
                    # Format: Savings off RRP: NZ$61.39 (43%)
                    offer_str = f"Savings off RRP: NZ${savings:.2f} ({pct}%)"

                return final_rrp, was_p, offer_str

            # --- 4. Variation Loop ---
            variations = []
            if custom_data and 'options' in custom_data:
                for opt in custom_data['options']:
                    if 'values' in opt and isinstance(opt['values'], list):
                        for val in opt['values']:
                            v_id = val.get('id')
                            v_label = val.get('label')

                            if v_id and v_label:
                                v_available = True
                                # Stock Check
                                label_sel = response.xpath(f'//label[@data-variant="{v_label}"]')
                                if label_sel:
                                    stock_text = label_sel.xpath('.//span[contains(@class, "stock")]/text()').get()
                                    stock_style = label_sel.xpath(
                                        './/span[contains(@class, "stock")]/@style').get() or ""
                                    if stock_text and 'out of stock' in stock_text.lower() and 'none' not in stock_style:
                                        v_available = False

                                variations.append({
                                    'ProductCode': int(v_id),
                                    'VariantName': v_label,
                                    'Size': self.extract_size(v_label) or v_label,
                                    'Price': price,
                                    'Available': v_available,
                                    'Images': images_str
                                })

            # --- 5. Yield Results ---

            if variations:
                for var in variations:
                    if not var['Price'] or var['Price'] <= 0: continue

                    final_rrp, final_was, offer_txt = calculate_prices_and_offer(var['Price'], source_rrp, saved_value)

                    item = template_item.copy()
                    item["Name"] = f"{name}"
                    item["Brand"] = brand
                    item["Category_Hierarchy"] = breadcrumb_str
                    item["Images"] = var['Images']
                    item["Pack_size"] = var['Size']
                    item["ParentCode"] = int(parent_id)
                    item["Price"] = var['Price']
                    item["ProductCode"] = int(var['ProductCode'])
                    item["RRP"] = final_rrp
                    item["WasPrice"] = final_was
                    item["Offer_info"] = offer_txt  # Set Offer Info
                    item["is_available"] = var['Available']
                    item["Barcode"] = barcode

                    hash_key = self.generate_hash_id(str(item["ProductCode"]), self.retailer, self.region)
                    item["_id"] = hash_key
                    self.save_product(item, doc_id)

            else:
                # Main Product Fallback
                if price and price > 0:
                    final_rrp, final_was, offer_txt = calculate_prices_and_offer(price, source_rrp, saved_value)

                    item = template_item.copy()
                    item["Name"] = name
                    item["Brand"] = brand
                    item["Category_Hierarchy"] = breadcrumb_str
                    item["Images"] = images_str
                    item["Pack_size"] = self.extract_size(name)
                    item["ParentCode"] = int(parent_id)
                    item["Price"] = price
                    item["ProductCode"] = int(parent_id)
                    item["RRP"] = final_rrp
                    item["WasPrice"] = final_was
                    item["Offer_info"] = offer_txt  # Set Offer Info
                    item["Barcode"] = barcode

                    main_avail = True
                    og_avail = response.xpath('//meta[@property="og:availability"]/@content').get()
                    if og_avail and 'out of stock' in og_avail:
                        main_avail = False
                    item["is_available"] = main_avail

                    hash_key = self.generate_hash_id(str(item["ProductCode"]), self.retailer, self.region)
                    item["_id"] = hash_key
                    self.save_product(item, doc_id)
                else:
                    self.logger.warning(f"Skipping product with invalid price: {price}")

        except Exception as e:
            self.logger.error(f"Error parsing {prod_url}: {e}", exc_info=True)
            if doc_id and hasattr(self, 'product_url'):
                self.product_url.update_one({"_id": doc_id}, {"$set": {"Status": "Failed", "Error": str(e)}})

    def save_product(self, item, doc_id):
        if hasattr(self, 'product_table'):
            try:
                self.product_table.update_one(
                    {"_id": item["_id"]},
                    {"$set": item},
                    upsert=True
                )
                self.logger.info(f"✓ Saved: {item['Name']} | Code: {item['ProductCode']}")
                if doc_id:
                    self.product_url.update_one({"_id": doc_id}, {"$set": {"Status": "Done"}})
            except Exception as e:
                self.logger.error(f"DB Error: {e}")
        else:
            print(json.dumps(item, indent=4, default=str))

    def close(self, reason):
        try:
            if hasattr(self, 'mongo_client'):
                self.mongo_client.close()
                self.logger.info("MongoDB connection closed")
        except Exception as e:
            self.logger.error(f"Error closing MongoDB: {e}")

if __name__ == '__main__':
    from scrapy.cmdline import execute

    execute(
        "scrapy crawl healthpost_pdp -a retailer=healthpost-nz -a region=nz -a Type=eshop -a RetailerCode=healthpost_nz".split())