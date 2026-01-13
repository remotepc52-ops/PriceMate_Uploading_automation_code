import datetime

from Common_Modual.common_functionality import *
import pymongo
import os
import re
from dateutil.relativedelta import relativedelta, MO

first_monday_date = (datetime.datetime.today() + relativedelta(weekday=MO(0))).date()

obj = RequestsManager()
from datetime import datetime

# Parameters
website = "Amazon_sg_main"  # Replace with the actual website name or variable
today = datetime.today().strftime("%Y_%m_%d")

conn = pymongo.MongoClient("mongodb://localhost:27017/")
db = conn[f"pricemate_eshop_amazon_sg"]

search_data = db[f'Search_Data_{today}']
main_data  = db[f'Product_Url_{today}']
product_data = db[f'Product_Data_{today}']
raw_url = db[f'raw_urls_{today}']
# another = db[f'another_urls_{today}']


# Use url or another identifier instead of ProductCode
search_data.create_index("url", unique=True)
main_data.create_index("ProductCode", unique=True)
product_data.create_index("ProductCode", unique=True)
raw_url.create_index("url", unique=True)
# another.create_index("url", unique=True)





# Base path
base_path = f"E:\\Data\\Crawl_Data_Collection\\{today}\\{website}"

# Define paths for different file types
html_path = os.path.join(base_path, "Data_Files", "HTML_Files")
excel_path = os.path.join(base_path, "Data_Files", "Excel_Files")

# Create directories
os.makedirs(html_path, exist_ok=True)
os.makedirs(excel_path, exist_ok=True)

print(f"HTML files path: {html_path}")
print(f"Excel files path: {excel_path}")


# current_proxy = '7d12e8dc87c84c9b9fccc23416cbdc40'
current_proxy = '2c6ea6e6d8c14216a62781b8f850cd5b'

proxy_host = "api.zyte.com"
proxy_port = "8011"
proxy_auth = f"{current_proxy}:"


proxies = {
    "http": "https://{}@{}:{}/".format(proxy_auth, proxy_host, proxy_port),
    "https": "http://{}@{}:{}/".format(proxy_auth, proxy_host, proxy_port)
}

scraper_api_key = "f8f2ef6134be4c604d89eb084196f7bd"
