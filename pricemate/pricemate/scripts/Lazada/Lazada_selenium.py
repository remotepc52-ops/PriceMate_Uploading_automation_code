import os
import json
import time
import asyncio
import logging
import random
# import winsound  <-- REMOVED
from datetime import datetime
from pymongo import MongoClient
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

# ==============================================================================
# CONFIGURATION
# ==============================================================================
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

lazada_domains = {
    "ID": "https://www.lazada.co.id", "MY": "https://www.lazada.com.my",
    "PH": "https://www.lazada.com.ph", "SG": "https://www.lazada.sg",
    "TH": "https://www.lazada.co.th", "VN": "https://www.lazada.vn",
}


class LazadaNetworkSaverSelenium:
    def __init__(self, region, retailer_code, type_code):
        self.region = region.upper()
        self.retailer = f"lazada_{region.lower()}"
        self.retailer_code = retailer_code
        self.type = type_code
        self.domain = lazada_domains.get(self.region, "https://www.lazada.com.my")
        self.today = datetime.today().strftime("%Y_%m_%d")

        # Database
        self.mongo_client = MongoClient("mongodb://localhost:27017")
        self.db = self.mongo_client[f"pricemate_{self.type}_{self.retailer_code}"]
        self.input_table = self.db[f"input_data_table"]
        self.product_table = self.db[f"Product_Data_{self.today}"]

        # Save Path
        self.pdp_html_path = fr"E:\Data\crawl_data_collection\Lazada\{self.retailer}\{self.today}"
        self.ensure_directory(self.pdp_html_path)
        self.driver = None

    def ensure_directory(self, path):
        if not os.path.exists(path):
            os.makedirs(path)
            logger.info(f"📁 Directory Created: {path}")

    # ==============================================================================
    # 1. CONNECT TO CHROME
    # ==============================================================================
    def connect_driver(self):
        logger.info("🔌 Connecting to Chrome (Port 9222)...")
        try:
            chrome_options = Options()
            chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
            driver = webdriver.Chrome(options=chrome_options)

            # Enable Network Domain (Crucial for JSON capture)
            try:
                driver.execute_cdp_cmd('Network.enable', {})
                logger.info("📡 Network Domain Enabled")
            except:
                logger.warning("Network domain check passed.")

            return driver
        except Exception as e:
            logger.error(f"❌ Connection Failed: {e}")
            logger.warning(
                "👉 Run this in CMD: chrome.exe --remote-debugging-port=9222 --user-data-dir='C:\\selenium_chrome_profile'")
            return None

    # ==============================================================================
    # 2. CAPTCHA (NO SOUND) & NETWORK
    # ==============================================================================
    def detect_and_wait_captcha(self):
        try:
            if "challenge" in self.driver.current_url or "security check" in self.driver.title.lower():
                logger.warning("\n" + "!" * 40)
                logger.warning("⛔ CAPTCHA DETECTED! Script Paused.")
                logger.warning("👉 Please solve it manually in the browser.")
                logger.warning("!" * 40 + "\n")

                # Loop until solved (No Sound)
                while True:
                    if "challenge" not in self.driver.current_url and "security check" not in self.driver.title.lower():
                        logger.info("✅ CAPTCHA Solved! Resuming...")
                        time.sleep(2)
                        return True
                    time.sleep(2)
            return False
        except:
            return False

    def capture_ajax_requests(self, page_num):
        """Captures JSON from Performance Logs"""
        try:
            logs = self.driver.get_log("performance")

            for log in logs:
                try:
                    message = json.loads(log["message"])
                    log_data = message.get("message", {})

                    if log_data.get("method") == "Network.responseReceived":
                        url = log_data.get("params", {}).get("response", {}).get("url", "")
                        req_id = log_data.get("params", {}).get("requestId")

                        if url and "ajax=true" in url and "lazada" in url:
                            try:
                                res = self.driver.execute_cdp_cmd("Network.getResponseBody", {"requestId": req_id})
                                body = res.get("body", "")
                                data = json.loads(body)

                                if data.get('mods', {}).get('listItems'):
                                    logger.info(
                                        f"🎯 [PAGE {page_num}] Captured Valid JSON ({len(data['mods']['listItems'])} items)")
                                    return data
                            except Exception:
                                continue
                except:
                    continue
            return None
        except Exception as e:
            logger.error(f"Log Error: {e}")
            return None

    def click_next_page(self):
        try:
            xpath = '//li[contains(@class, "ant-pagination-next")]//button[not(@disabled)]'
            btn = self.driver.find_element(By.XPATH, xpath)
            self.driver.execute_script("arguments[0].scrollIntoView(true);", btn)
            time.sleep(1)
            btn.click()
            return True
        except:
            return False

    # ==============================================================================
    # 3. PROCESS STORE
    # ==============================================================================
    async def process_store(self, store_item, max_pages=102):
        mongo_id = store_item['_id']
        store_url = store_item['url']
        store_name = store_item.get('source_id', 'Unknown')

        try:
            if '/shop/' in store_url:
                shop_id = store_url.split('/shop/shop/')[-1].split('/shop/')[-1].split('/')[0]
            else:
                shop_id = store_url.split('/')[-1]
        except:
            shop_id = store_name

        logger.info(f"🚀 Processing: {store_name} | {shop_id}")

        db_filter = store_item.get('Brand to filter', 'No filter')
        if isinstance(db_filter, float): db_filter = 'No filter'
        filters = [f.strip() for f in db_filter.split(",")] if db_filter != 'No filter' else ['No filter']

        total_files_saved = 0

        for f_query in filters:
            if f_query == 'No filter':
                url = f"{self.domain}/{shop_id}/?q=All-Products&from=wangpu&langFlag=en&pageTypeId=2&sort=priceasc"
                clean_filter = "All"
            else:
                url = f"{store_url}?q={f_query}&from=wangpu&langFlag=en&pageTypeId=2&sort=priceasc"
                clean_filter = f_query.replace(" ", "")

            self.driver.get(url)
            time.sleep(random.uniform(5, 7))
            self.detect_and_wait_captcha()

            page_num = 1
            while page_num <= max_pages:
                json_data = self.capture_ajax_requests(page_num)

                if json_data:
                    filename = f'{self.domain.split("//")[-1]}_{shop_id}_{clean_filter}_page_{page_num}.json'
                    save_path = os.path.join(self.pdp_html_path, filename)

                    try:
                        with open(save_path, 'w', encoding='utf-8') as f:
                            json.dump(json_data, f, indent=4)
                        logger.info(f"💾 [SAVED] {filename}")
                        total_files_saved += 1
                    except Exception as e:
                        logger.error(f"File Save Error: {e}")
                else:
                    logger.warning(f"⚠️ [PAGE {page_num}] No JSON Data. Filter ended or Captcha blocked.")
                    break

                if not self.click_next_page():
                    logger.info("⏹️ Pagination Ended")
                    break

                time.sleep(random.uniform(4, 6))
                self.detect_and_wait_captcha()
                page_num += 1

        if total_files_saved > 0:
            self.input_table.update_one({"_id": mongo_id}, {'$set': {'Status': "Done"}})
            logger.info(f"✅ Store {store_name} Done. (Saved {total_files_saved} files)")
        else:
            logger.error(f"❌ Store {store_name} Failed (0 files). Check manually.")

    async def run(self):
        self.driver = self.connect_driver()
        if not self.driver: return

        stores = list(self.input_table.find({"Status": "Pending"}))
        logger.info(f"📋 Found {len(stores)} Pending Stores")

        for i, store in enumerate(stores, 1):
            logger.info(f"\n--- Store {i}/{len(stores)} ---")
            await self.process_store(store)
            time.sleep(3)


if __name__ == '__main__':
    bot = LazadaNetworkSaverSelenium("MY", "lazada_my", "marketplace")
    asyncio.run(bot.run())