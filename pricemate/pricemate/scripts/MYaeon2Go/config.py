import datetime
import json

import pymongo
import os
from Common_Modual.common_functionality import *
from dateutil.relativedelta import relativedelta, MO
from datetime import datetime
from dateutil.relativedelta import relativedelta, TU
from dateutil.relativedelta import relativedelta, MO
# next_tuesday = (datetime.today() + relativedelta(weekday=TU(0))).date()
# Today1 = (datetime.today() + relativedelta(weekday=MO(1))).date()
Today1 = datetime.today()
# first_monday_date = (datetime.datetime.today() + relativedelta(weekday=MO(0))).date()
# Today1 = (datetime.today() + relativedelta(weekday=MO(1))).date()

obj = RequestsManager()

website = "MYAeon2Go"
today = Today1.strftime("%Y_%m_%d")


conn = pymongo.MongoClient("mongodb://localhost:27017/")
db = conn[f"pricemate_eshop_aeon_my"]

category_input = db[f'Category_Input_{today}']
coll_list = db.list_collection_names()


print(f'Product_Data_{today}' not in coll_list)
if f'Product_Data_{today}' not in coll_list:
    category_input.update_many({}, {"$set": {"Status":"Pending"}})

product_data = db[f'Product_Data_{today}']

category_input.create_index("UrlFriendlyName",unique = True)
product_data.create_index("ProductCode",unique = True)


# Base path
base_path = f"E:\Data\Crawl_Data_Collection\\{website}\\{today}"

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
apikey = '21ed11ef5c872bc7727680a52233027db4578a0e'

scraper_api_key = "f8f2ef6134be4c604d89eb084196f7bd"



