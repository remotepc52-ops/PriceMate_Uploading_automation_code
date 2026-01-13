import json
import math
import urllib.parse
import os, sys
import urllib3
import requests
import time
import hashlib
from datetime import datetime
from pymongo import MongoClient

# Disable SSL warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


# ==============================================================================
# 1. Base Class (Mocked for standalone use, same as your previous requests)
# ==============================================================================
class PricemateBaseSpider:
    custom_settings = {
        'RETRY_TIMES': 5,
        'DOWNLOAD_TIMEOUT': 51
    }

    def __init__(self, retailer, region, Type, RetailerCode, start=0, end=100000, lazada_pdp=False, *args, **kwargs):
        self.retailer = retailer.lower()
        self.Type = Type
        self.RetailerCode = RetailerCode
        self.lazada_pdp = lazada_pdp
        self.region = region.lower()
        self.start_index = int(start)
        self.end = int(end)
        self.today = datetime.today().strftime("%Y_%m_%d")

        # Database Configuration
        mongo_uri = "mongodb://localhost:27017"
        self.mongo_client = MongoClient(mongo_uri)
        self.db = self.mongo_client[f"pricemate_{self.Type}_{self.RetailerCode}"]

        self.product_table = self.db[f"Product_Data_{self.today}"]
        # self.product_table = self.db[f"Product_Data_2025_12_12"]
        self.category_input = self.db[f"input_data_table"]
        collection_names = self.db.list_collection_names()

        if f"Product_Data_{self.today}" not in collection_names:
            self.category_input.update_many({}, {'$set': {"Status": "Pending"}})

        # Create Index
        self.category_input.create_index("Status")

    def generate_hash_id(self, *args):
        hash_input = "|".join(str(a) for a in args)
        return hashlib.md5(hash_input.encode('utf-8')).hexdigest()

    def save_product(self, item):
        if not item:
            return
        if "_id" not in item:
            hash_id = self.generate_hash_id(item["ProductCode"], self.retailer, self.region)
        else:
            hash_id = item["_id"]

        required_keys = {"_id": hash_id, "retailer": self.retailer, "region": self.region}
        item.update(required_keys)
        if "Status" not in item:
            item["Status"] = "Pending"

        self.product_table.update_one({"_id": hash_id}, {"$set": item}, upsert=True)
        print(f"Saved product: {item.get('ProductCode')}")

    def close(self, reason):
        self.mongo_client.close()


# ==============================================================================
# 2. Configuration & Headers
# ==============================================================================
lazada_headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36',
}

lazada_domains = {
    "ID": "https://lazada.co.id",  # Indonesia
    "MY": "https://lazada.com.my",  # Malaysia
    "PH": "https://lazada.com.ph",  # Philippines
    "SG": "https://lazada.sg",  # Singapore
    "TH": "https://lazada.co.th",  # Thailand
    "VN": "https://lazada.vn",  # Vietnam
}


# ==============================================================================
# 3. Main Spider Class (Fixed with Proxy Logic)
# ==============================================================================
class LazadaSpider(PricemateBaseSpider):
    name = "lazada_shop"

    def __init__(self, retailer, region, *args, **kwargs):
        super().__init__(retailer=retailer, region=region, *args, **kwargs)
        self.domain = lazada_domains[self.region.upper()]
        self.headers = lazada_headers
        self.proxy_name = 'scrape_do'
        self.save_directory = fr"E:\\Data\\Crawl_Data_Collection\\{self.today}\\Lazada\\{self.region}"
        if not os.path.exists(self.save_directory):
            try:
                os.makedirs(self.save_directory)
                print(f" Created folder: {self.save_directory}")
            except OSError as e:
                print(f"Failed to create folder: {e}")
        # Extracted token from your original file
        self.proxy_token = "2192d06a19b74b23884d257fcffee6f696674f8e128"

        # Initialize Requests Session
        self.session = requests.Session()

    def _get_proxy_url(self, target_url):
        """Helper to wrap the target URL with the Scrape.do proxy"""
        encoded_url = urllib.parse.quote(target_url)
        return f'http://api.scrape.do?token={self.proxy_token}&url={encoded_url}&super=true'

    def _make_request(self, url, headers, callback, meta):
        """
        Handles the request using the proxy to avoid blocking.
        Includes retry logic for failed connections or non-JSON responses.
        """
        # Always use the proxy URL
        proxy_url = self._get_proxy_url(url)

        retries = 5
        for attempt in range(retries):
            try:
                # print(f"Fetching ({attempt+1}/{retries}): {url}")
                response = self.session.get(proxy_url, headers=headers, verify=False, timeout=60)

                if response.status_code == 200:
                    # Validate JSON content immediately
                    try:
                        json.loads(response.text)

                        # If successful, attach meta and call callback
                        response.meta = meta
                        callback(response)
                        return
                    except json.JSONDecodeError:
                        print(f"Blocked (Response was HTML, not JSON) - Retrying {url}...")
                else:
                    print(f"Status {response.status_code} for {url}. Retrying...")

                time.sleep(2)  # Wait before retry
            except Exception as e:
                print(f"Connection Error: {e}. Retrying...")
                time.sleep(2)

        print(f"Failed to fetch {url} after {retries} attempts.")

    def start_requests(self):
        docs = self.category_input.find({
            "Status": "Pending"
        })

        for doc in docs:
            url = doc["url"]
            hash_id = doc.get("_id")
            source_id = doc.get("source_id")
            print(f"source_id value: {source_id}")

            if source_id is None:
                print(f"Warning: source_id is None for document {hash_id}")

            # URL parsing logic preserved from original
            if '/shop/' in url:
                try:
                    shop_id = url.split('/shop/shop/')[-1].split('/shop/')[-1].split('/')[0]
                except:
                    # Fallback if URL structure differs slightly
                    shop_id = url.split("lazada")[1].split("/")[1]
                filter_query = 'All-Products'
                url = f'{self.domain}/{shop_id}/?q={filter_query}&from=wangpu&langFlag=en&pageTypeId=2&sort=pricedesc'
            else:
                shop_id = url.split(f"{self.domain[10:]}/")[-1].split('/')[0]
                filter_query = 'All-Products'
                url = f'{self.domain}/{shop_id}/?q={filter_query}&from=wangpu&langFlag=en&pageTypeId=2&sort=pricedesc'
                print(f"Formatted URL: {url}")

            page = 1
            if "?" in url:
                ajax_url = f"{url}&ajax=true&page={page}".replace('www.', '')
            else:
                ajax_url = f"{url}?ajax=true&page={page}".replace('www.', '')

            filename = f'{self.domain.split("//")[-1]}_{shop_id.replace("-", "_")}_page_{page}.json'
            try:
                # Construct Filename (Cleaned up)
                domain_clean = self.domain.split("//")[-1]
                shop_clean = shop_id.replace("-", "_")
                filename = f'{domain_clean}_{shop_clean}_page_{page}.json'

                full_path = os.path.join(self.save_directory, filename)

                with open(full_path, 'w', encoding='utf-8') as f:
                    json.dump( f, ensure_ascii=False, indent=4)
                # logger.info(f"💾 Saved JSON: {filename}")
            except Exception as file_error:
                print(f"Failed to save JSON file: {file_error}")
            # Initiate request
            self._make_request(
                url=ajax_url,
                headers=self.headers,
                callback=self.parse_pdp,
                meta={
                    "proxy_name": self.proxy_name,
                    "main_url": url,
                    "hash_id": hash_id,
                    "source_id": source_id,
                    "ajax_url": ajax_url,
                    "shop_id": shop_id,
                    "filename": filename,
                    "page": page,
                    "should_be": ["mainInfo"]
                }
            )

    def parse_pdp(self, response):
        try:
            meta = response.meta
            url = meta.get('main_url')
            hash_id = meta.get('hash_id')
            source_id = meta.get('source_id')
            shop_id = meta.get('shop_id')
            page = meta.get('page')

            # This will succeed now because _make_request ensures it is JSON
            loaded_json = json.loads(response.text)

            totalResults = loaded_json['mainInfo']['totalResults']
            # Specific Lazada logic from original code
            if int(totalResults) == 4080:
                totalResults = loaded_json['mods']['filter']['filteredQuatity']
                print("Max Page Limitation...", totalResults)

            product_list = loaded_json['mods']['listItems']

            if product_list:
                for pdp_data in product_list:
                    # Extraction logic strictly preserved
                    Parent_Id = pdp_data['itemId']
                    Product_Name = pdp_data['name']
                    # itemid = pdp_data['skuId'] # Unused variable in original logic flow?
                    img = pdp_data['image']
                    try:
                        product_url = pdp_data['itemUrl'].split("?")[0]
                    except:
                        product_url = pdp_data['productUrl'].split("?")[0]

                    if not str(product_url).startswith("https"):
                        product_url = f"https:{product_url}"

                    # seller_name = pdp_data['sellerName']
                    try:
                        discount = pdp_data['discount']
                        pack_size = pdp_data['packageInfo']
                    except:
                        discount = ""
                        pack_size = ""
                    try:
                        originalPrice = float(pdp_data['originalPrice'])
                    except:
                        originalPrice = ""

                    try:
                        salePrice = float(pdp_data['price'])
                    except:
                        if originalPrice == salePrice:
                            originalPrice = ""
                        else:
                            print("Sale Price is required,,,,,", pdp_data.get('skuId'))
                            continue  # Skip this item

                    try:
                        stock_count = pdp_data['inStock']
                        if not stock_count:
                            isOos = True
                        else:
                            isOos = False
                    except:
                        isOos = False

                    # item_sold logic
                    item_sold = pdp_data.get('querystring', "") or pdp_data.get('productUrl', "")
                    if item_sold:
                        try:
                            item_sold = int(item_sold.split("&sale=")[-1].split("&")[0])
                        except:
                            item_sold = 0  # Fallback

                    ratingScore = pdp_data.get('ratingScore')
                    if ratingScore:
                        ratingScore = round(float(ratingScore), 1)

                    review = pdp_data.get('review')
                    if review:
                        review = int(review)

                    brand = pdp_data.get('brandName')
                    skuId = pdp_data.get('skuId')

                    sellerId = pdp_data.get('sellerId')
                    rrp = originalPrice
                    if originalPrice is None or originalPrice == "":
                        rrp = salePrice

                    breadcrumb_items = loaded_json.get('mods', {}).get('breadcrumb', [])
                    breadcrumb_titles = [crumb.get('title') for crumb in breadcrumb_items]
                    bread = ' > '.join(breadcrumb_titles)

                    product_hash = self.generate_hash_id(product_url, self.retailer, self.region)
                    item = {
                        "_id": product_hash,
                        "CategoryURL": url,
                        "HashID": hash_id,
                        "source_id": source_id,
                        "ProductCode": skuId,
                        "ParentCode": Parent_Id,
                        "ProductURL": product_url,
                        "Name": Product_Name,
                        "Brand": brand,
                        "Pack_size": pack_size,
                        "Price": salePrice,
                        "WasPrice": originalPrice,
                        "Category_Hierarchy": bread,
                        "is_available": True if not isOos else False,
                        "Status": "Done",
                        "Images": img,
                        "RRP": rrp,
                        "Offer_info": discount,
                        "Promo_Type": "",
                        "per_unit_price": "",
                        "Barcode": "",
                        "retailer": self.retailer,
                        "region": self.region,
                        "retailer_name": self.RetailerCode,
                    }
                    self.save_product(item)

            # Pagination Logic
            main_info = loaded_json.get('mainInfo', {})
            total_results = int(main_info.get('totalResults', 0))
            page_size = int(main_info.get('pageSize', 40))

            total_pages = math.ceil(total_results / page_size)

            if page < total_pages:
                page = page + 1
                print(f"Going for next page.. {page}, Total pages: {total_pages}")

                if "?" in url:
                    next_ajax_url = f"{url}&ajax=true&page={page}".replace('www.', '')
                else:
                    next_ajax_url = f"{url}?ajax=true&page={page}".replace('www.', '')

                filename = f'{self.domain.split("//")[-1]}_{shop_id.replace("-", "_")}_page_{page}.json'

                # Request next page using proxy
                self._make_request(
                    url=next_ajax_url,
                    headers=self.headers,
                    callback=self.parse_pdp,
                    meta={
                        "proxy_name": self.proxy_name,
                        "main_url": url,
                        "hash_id": hash_id,
                        "source_id": source_id,
                        "ajax_url": next_ajax_url,
                        "shop_id": shop_id,
                        "filename": filename,
                        "page": page,
                        "should_be": ["mainInfo"]
                    }
                )
            else:
                self.category_input.update_one({"_id": hash_id}, {'$set': {'Status': "Done"}})
                print("Status Updated !")
                return None

        except Exception as e:
            print(f"Error parsing PDP: {e}")
            return None


# ==============================================================================
# 4. Execution
# ==============================================================================
if __name__ == '__main__':
    # Configuration - Change these as needed
    spider = LazadaSpider(retailer='lazada_my', region='my', Type='marketplace', RetailerCode='lazada_my')
    # spider = LazadaSpider(retailer='lazada_ph', region='ph', Type='marketplace', RetailerCode='lazada_ph')
    # spider = LazadaSpider(retailer='lazada_id', region='id', Type='marketplace', RetailerCode='lazada_id')
    # spider = LazadaSpider(retailer='lazada_my', region='my', Type='marketplace', RetailerCode='lazada_caring_my')
    # spider = LazadaSpider(retailer='lazada_ph', region='ph', Type='marketplace', RetailerCode='lazada_watsons_ph')


    try:
        spider.start_requests()
    except KeyboardInterrupt:
        print("Stopping spider...")
    finally:
        spider.close("Finished")