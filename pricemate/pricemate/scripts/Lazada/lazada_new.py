import json
import math
import urllib.parse
import os, sys
import urllib3
import requests
import time
import hashlib
import logging
import argparse
from datetime import datetime
from pymongo import MongoClient
from concurrent.futures import ThreadPoolExecutor, as_completed
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# Disable SSL warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# ==============================================================================
# 1. CONFIGURATION & LOGGING
# ==============================================================================
LOG_FILENAME = f"lazada_spider_{datetime.now().strftime('%Y%m%d')}.log"
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILENAME),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# YOUR EXACT HEADERS
lazada_headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36',
}

lazada_domains = {
    "ID": "https://lazada.co.id", "MY": "https://lazada.com.my",
    "PH": "https://lazada.com.ph", "SG": "https://lazada.sg",
    "TH": "https://lazada.co.th", "VN": "https://lazada.vn",
}

PROXY_TOKEN = "2192d06a19b74b23884d257fcffee6f696674f8e128"


# ==============================================================================
# 2. BASE CLASS
# ==============================================================================
class PricemateBaseSpider:
    def __init__(self, retailer, region, Type, RetailerCode, start=0, end=100000, lazada_pdp=False):
        self.retailer = retailer.lower()
        self.Type = Type
        self.RetailerCode = RetailerCode
        self.lazada_pdp = lazada_pdp
        self.region = region.lower()
        self.start_index = int(start)
        self.end = int(end)
        self.today = datetime.today().strftime("%Y_%m_%d")

        # Database Connection
        mongo_uri = "mongodb://localhost:27017"
        self.mongo_client = MongoClient(mongo_uri)
        self.db = self.mongo_client[f"pricemate_{self.Type}_{self.RetailerCode}"]

        self.product_table = self.db[f"Product_Data_{self.today}"]
        self.category_input = self.db[f"input_data_table"]

        # Ensure 'Status: Pending' exists if collection is new
        collection_names = self.db.list_collection_names()
        if f"Product_Data_{self.today}" not in collection_names:
            self.category_input.update_many({}, {'$set': {"Status": "Pending"}})

        # Create Indexes
        self.product_table.create_index("ProductURL", unique=True)
        self.product_table.create_index("retailer")
        self.product_table.create_index("region")
        self.product_table.create_index("Status")
        self.category_input.create_index("Status")

    def generate_hash_id(self, *args):
        hash_input = "|".join(str(a) for a in args)
        return hashlib.md5(hash_input.encode('utf-8')).hexdigest()

    def save_product(self, item):
        if not item: return

        if "_id" not in item:
            hash_id = self.generate_hash_id(item["ProductCode"], self.retailer, self.region)
        else:
            hash_id = item["_id"]

        required_keys = {"_id": hash_id, "retailer": self.retailer, "region": self.region}
        item.update(required_keys)

        if "Status" not in item:
            item["Status"] = "Pending"

        try:
            self.product_table.update_one({"_id": hash_id}, {"$set": item}, upsert=True)
        except Exception as e:
            logger.error(f"DB Error: {e}")

    def close(self):
        self.mongo_client.close()


# ==============================================================================
# 3. LAZADA SPIDER (Fixed Math Error + JSON Saving)
# ==============================================================================
class LazadaSpider(PricemateBaseSpider):
    def __init__(self, retailer, region, Type, RetailerCode):
        super().__init__(retailer, region, Type, RetailerCode)
        self.domain = lazada_domains.get(self.region.upper(), "https://lazada.com.my")
        self.headers = lazada_headers
        self.proxy_name = 'scrape_do'

        # Setup Local Directory for Saving JSONs
        # Path: ~/lazada_my/2025_12_10
        self.save_directory = fr"E:\\Data\\Crawl_Data_Collection\\{self.today}\\Lazada\\{self.region}"
        # self.save_directory = os.path.join(os.path.expanduser("~"), self.retailer, self.today)
        if not os.path.exists(self.save_directory):
            try:
                os.makedirs(self.save_directory)
                logger.info(f" Created folder: {self.save_directory}")
            except OSError as e:
                logger.error(f"Failed to create folder: {e}")

        # Session with Retries
        self.session = requests.Session()
        retries = Retry(total=5, backoff_factor=1, status_forcelist=[500, 502, 503, 504])
        self.session.mount('http://', HTTPAdapter(max_retries=retries))
        self.session.mount('https://', HTTPAdapter(max_retries=retries))

    def _get_proxy_url(self, target_url):
        encoded_url = urllib.parse.quote(target_url)
        return f'http://api.scrape.do?token={PROXY_TOKEN}&url={encoded_url}&super=true'

    def fetch_url(self, url):
        proxy_url = self._get_proxy_url(url)
        try:
            response = self.session.get(proxy_url, headers=self.headers, verify=False, timeout=60)

            if response.status_code != 200:
                logger.warning(f"Status {response.status_code} for {url}")
                return None

            try:
                return response.json()
            except json.JSONDecodeError:
                logger.warning(f"Blocked (Not JSON) for {url}")
                return None
        except Exception as e:
            logger.error(f"Request Error for {url}: {e}")
            return None

    def process_shop(self, doc):
        url = doc["url"]
        hash_id = doc.get("_id")
        source_id = doc.get("source_id")

        logger.info(f"Starting Shop: {url}")

        # 1. Formatting URL
        try:
            if '/shop/' in url:
                shop_id = url.split('/shop/shop/')[-1].split('/shop/')[-1].split('/')[0]
                filter_query = 'All-Products'
                base_url = f'{self.domain}/{shop_id}/?q={filter_query}&from=wangpu&langFlag=en&pageTypeId=2&sort=pricedesc'
            else:
                shop_id = url.split(f"{self.domain[10:]}/")[-1].split('/')[0]
                filter_query = 'All-Products'
                base_url = f'{self.domain}/{shop_id}/?q={filter_query}&from=wangpu&langFlag=en&pageTypeId=2&sort=pricedesc'
        except Exception as e:
            logger.error(f"URL Parse Error for {url}: {e}")
            return

        # Validation Variables
        is_fully_completed = True
        total_items_scraped = 0
        expected_total_items = 0
        current_page = 1

        # 2. Page Loop
        while True:
            if "?" in base_url:
                ajax_url = f"{base_url}&ajax=true&page={current_page}".replace('www.', '')
            else:
                ajax_url = f"{base_url}?ajax=true&page={current_page}".replace('www.', '')

            # Fetch Data
            data = self.fetch_url(ajax_url)

            if not data:
                logger.error(f" Failed to fetch Page {current_page} for Shop {shop_id}. Marking incomplete.")
                is_fully_completed = False
                break

            try:
                # --- SAVE JSON TO FILE START ---
                try:
                    # Construct Filename (Cleaned up)
                    domain_clean = self.domain.split("//")[-1]
                    shop_clean = shop_id.replace("-", "_")
                    filename = f'{domain_clean}_{shop_clean}_page_{current_page}.json'

                    full_path = os.path.join(self.save_directory, filename)

                    with open(full_path, 'w', encoding='utf-8') as f:
                        json.dump(data, f, ensure_ascii=False, indent=4)
                    # logger.info(f"💾 Saved JSON: {filename}")
                except Exception as file_error:
                    logger.error(f"Failed to save JSON file: {file_error}")
                # --- SAVE JSON TO FILE END ---

                main_info = data.get('mainInfo', {})
                # FIX: Force int() conversion immediately
                total_results = int(main_info.get('totalResults', 0))
                page_size = int(main_info.get('pageSize', 40))

                # Lazada 4080 Limit Logic
                if total_results == 4080:
                    # FIX: Handle string values in filteredQuatity
                    raw_filtered = data.get('mods', {}).get('filter', {}).get('filteredQuatity', 4080)
                    total_results = int(raw_filtered)  # Force int conversion here too

                expected_total_items = total_results

                product_list = data.get('mods', {}).get('listItems', [])

                if product_list:
                    items_on_page = len(product_list)
                    total_items_scraped += items_on_page

                    for pdp_data in product_list:
                        self.extract_and_save(pdp_data, base_url, hash_id, source_id)

                    logger.info(f"Shop {shop_id} | Page {current_page} Scraped: {items_on_page} items.")
                else:
                    if current_page == 1 and total_results > 0:
                        logger.warning(f" Shop {shop_id} has results but Page 1 is empty.")
                        is_fully_completed = False
                    break

                    # Pagination Check
                # FIX: total_results is now guaranteed to be int, so / works fine
                total_pages = math.ceil(total_results / page_size)

                if current_page >= total_pages:
                    break

                current_page += 1
                time.sleep(1)

            except Exception as e:
                # Log detailed error with variable types to debug if it happens again
                logger.error(f" Parse Error on page {current_page} shop {shop_id}: {e}")
                is_fully_completed = False
                break

        # 3. Status Update
        logger.info(f" Verification {shop_id}: Scraped {total_items_scraped} / Expected ~{expected_total_items}")

        if is_fully_completed:
            self.category_input.update_one({"_id": hash_id}, {'$set': {'Status': "Done"}})
            logger.info(f"  Shop {shop_id} Status Updated to 'Done'.")
        else:
            logger.warning(f"  Shop {shop_id} incomplete. Retrying in next cycle...")

    def extract_and_save(self, pdp_data, url, hash_id, source_id):
        try:
            Parent_Id = pdp_data.get('itemId')
            Product_Name = pdp_data.get('name')
            img = pdp_data.get('image')

            raw_url = pdp_data.get('itemUrl') or pdp_data.get('productUrl')
            if not raw_url: return

            product_url = raw_url.split("?")[0]
            if not product_url.startswith("https"):
                product_url = f"https:{product_url}"

            try:
                discount = pdp_data.get('discount', "")
                pack_size = pdp_data.get('packageInfo', "")
            except:
                discount = ""
                pack_size = ""

            try:
                originalPrice = float(pdp_data.get('originalPrice', 0))
            except:
                originalPrice = ""

            try:
                salePrice = float(pdp_data.get('price', 0))
            except:
                if originalPrice == salePrice:
                    originalPrice = ""
                else:
                    return

            try:
                isOos = not pdp_data.get('inStock', False)
            except:
                isOos = False

            skuId = pdp_data.get('skuId')
            brand = pdp_data.get('brandName')

            rrp = originalPrice
            if originalPrice is None or originalPrice == "":
                rrp = salePrice

            breadcrumb_items = pdp_data.get('breadcrumb', [])
            bread = ""

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
                "is_available": not isOos,
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
        except Exception as e:
            pass

    def run(self, max_threads=5):
        """Multithreaded Execution with Retry Loop"""
        while True:
            docs = list(self.category_input.find({"Status": "Pending"}))
            remaining = len(docs)

            if remaining == 0:
                logger.info(" All shops are DONE! Exiting Spider.")
                break

            logger.info(f" Starting Cycle with {remaining} pending shops...")

            with ThreadPoolExecutor(max_workers=max_threads) as executor:
                futures = [executor.submit(self.process_shop, doc) for doc in docs]
                for future in as_completed(futures):
                    try:
                        future.result()
                    except Exception as e:
                        logger.error(f"Thread Error: {e}")

            logger.info("Cycle finished. Checking for any remaining pending items...")
            time.sleep(5)


# ==============================================================================
# 4. EASY EXECUTION
# ==============================================================================
def start_spider(retailer, region, Type, code, workers=5):
    print(f"--- Starting Spider: {code} ({region}) ---")
    spider = LazadaSpider(
        retailer=retailer,
        region=region,
        Type=Type,
        RetailerCode=code
    )
    try:
        spider.run(max_threads=workers)
    except KeyboardInterrupt:
        print("Stopping...")
    finally:
        spider.close()
        print("Finished.")


if __name__ == '__main__':
    # ==========================================================================
    # INSTRUCTIONS: Uncomment the line you want to run (Remove the '#')
    # ==========================================================================

    # --- MALAYSIA ---
    # start_spider(retailer="lazada_my", region="my", Type="marketplace", code="lazada_my", workers=5)
    # start_spider(retailer="lazada_my", region="my", Type="marketplace", code="lazada_bigpharmacy_my", workers=5)
    # start_spider(retailer="lazada_my", region="my", Type="marketplace", code="lazada_guardian_my", workers=5)
    # start_spider(retailer="lazada_my", region="my", Type="marketplace", code="lazada_petsmore_my", workers=5)
    # start_spider(retailer="lazada_my", region="my", Type="marketplace", code="lazada_mydin_my", workers=25)
    # start_spider(retailer="lazada_my", region="my", Type="marketplace", code="lazada_watsons_my", workers=5)
    # start_spider(retailer="lazada_my", region="my", Type="marketplace", code="lazada_caring_my", workers=50)

    # --- INDONESIA ---
    # start_spider(retailer="lazada_id", region="id", Type="marketplace", code="lazada_id", workers=5)
    # start_spider(retailer="lazada_id", region="id", Type="eshop", code="lazada_watsons_id", workers=5)

    # start_spider(retailer="lazada_ph", region="ph", Type="marketplace", code="lazada_watsons_ph", workers=15)
    start_spider(retailer="lazada_ph", region="ph", Type="marketplace", code="lazada_ph", workers=5)