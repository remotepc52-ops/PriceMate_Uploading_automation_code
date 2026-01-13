from Common_Modual.common_functionality import *
import pymongo
import os
from datetime import datetime


Today1 = datetime.today().date()

obj = RequestsManager()

website = "bigc_th_backup"
today = Today1.strftime("%Y_%m_%d")
# today = Today1.strftime("2025_10_29")

# conn = pymongo.MongoClient("mongodb://192.168.1.52:27017/")
conn = pymongo.MongoClient("mongodb://localhost:27017/")
db = conn[f"pricemate_eshop_bigc_th1"]

search_data = db[f'Search_Data']
product_data = db[f'Product_Data_{today}']

search_data.create_index("url", unique=True)

product_data.create_index(["ProductCode", "retailer"], unique=True)
product_data.create_index("ProductCode")
product_data.create_index("retailer")
product_data.create_index("region")
product_data.create_index("Status")

base_path = f"~\\Crawl_Data_Collection\\Master PriceMate\\{today}\\{website}"

html_path = os.path.join(base_path,"HTMLs")

os.makedirs(html_path, exist_ok=True)

print(f"HTML files path: {html_path}")

current_proxy = "21ed11ef5c872bc7727680a52233027db4578a0e"

proxy_host = "api.zenrows.com"
proxy_port = "8001"
proxy_auth = f"{current_proxy}:"

proxies = {
    "http": f"http://{proxy_auth}@{proxy_host}:{proxy_port}",
    "https": f"http://{proxy_auth}@{proxy_host}:{proxy_port}",  # <-- IMPORTANT
}

# current_proxy = '7d12e8dc87c84c9b9fccc23416cbdc40'
current_proxy = '2c6ea6e6d8c14216a62781b8f850cd5b'

proxy_host = "api.zyte.com"
proxy_port = "8011"
proxy_auth = f"{current_proxy}:"


proxies1 = {
    "http": "https://{}@{}:{}/".format(proxy_auth, proxy_host, proxy_port),
    "https": "http://{}@{}:{}/".format(proxy_auth, proxy_host, proxy_port)
}


# scraper_api_key = "f8f2ef6134be4c604d89eb084196f7bd"


def generate_hash_id(*args):
    hash_input = "|".join(str(a) for a in args)
    return hashlib.md5(hash_input.encode('utf-8')).hexdigest()