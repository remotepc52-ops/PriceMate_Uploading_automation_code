import datetime
from Common_Modual.common_functionality import *
import pymongo
import os
from dateutil.relativedelta import relativedelta, MO
from colorama import Fore, Back, Style, init
from bson.objectid import ObjectId
first_monday_date = (datetime.datetime.today() + relativedelta(weekday=MO(0))).date()

obj = RequestsManager()

# website = "shopee_supermarket"
# website = "shopee_petsmore"
# website = "shopee_bigpharmacy"
# website = "shopee_guardian"
# website = "shopee_caringpharmacyn"
# website = "shopee"
# website = "shopee_watson"

# type = "eshop"
# type = "marketplace"

# region = "my"
today = datetime.datetime.today().strftime("%Y_%m_%d")
# today = "2025_12_06"

# def get_configration(*args):
#     conn = pymongo.MongoClient("mongodb://localhost:27017/")
#     db = conn[f"pricemate_{type}_{website}_{region}"]
#
#     category_input = db[f'Category_Input_{today}']
#     coll_list = db.list_collections()
#     if f'Product_Data_{today}' not in coll_list:
#         category_input.update_many({}, {"$set": {"Status":"Pending"}})
#
#     product_data = db[f'Product_Data_{today}']
#
#     product_data.create_index("ProductCode", unique = True)
#
#     # Base path
#     base_path = f"E:\\Data\\Crawl_Data_Collection\\PriceMate\\{website}\\{today}"
#
#     # Define paths for different file types
#     html_path = os.path.join(base_path, "HTML_Files")
#     # excel_path = os.path.join(base_path, "Excel_Files")
#
#     # Create directories
#     os.makedirs(html_path, exist_ok=True)
#     # os.makedirs(excel_path, exist_ok=True)
#
#     print(f"HTML files path: {html_path}")
#     # print(f"Excel files path: {excel_path}")

init()
red = Fore.RED + Style.BRIGHT
green = Fore.GREEN + Style.BRIGHT
blue = Fore.BLUE + Style.BRIGHT
yellow = Fore.YELLOW + Style.BRIGHT
highlight = Fore.LIGHTRED_EX + Style.BRIGHT + Back.LIGHTWHITE_EX
reset = Style.RESET_ALL

def rprint(*args):
    print(red, ' '.join(map(str, args)), reset)

def gprint(*args):
    print(green, ' '.join(map(str, args)), reset)

def yprint(*args):
    print(yellow, ' '.join(map(str, args)), reset)

def bprint(*args):
    print(blue, ' '.join(map(str, args)), reset)

def hprint(*args):
    print(highlight, ' '.join(map(str, args)), reset)
def get_configration(*args):
    conn = pymongo.MongoClient("mongodb://192.168.1.52:27017/")

    # Unpack arguments
    db_name = args[0]  # Assuming only one argument is passed
    db = conn[db_name]

    category_input = db[f'input_data_table']
    coll_list = db.list_collection_names()  # Fixed: should use list_collection_names()
    if f'Product_Data_{today}' not in coll_list:
        category_input.update_many({}, {"$set": {"Status": "Pending"}})

    product_data = db[f'Product_Data_{today}']
    product_data.create_index("ProductCode", unique=True)

    # Base path
    # base_path = f"E:\\Data\\Crawl_Data_Collection\\PriceMate\\{website}\\{today}"
    base_path = f"\\\\192.168.1.52\\E\\Data\\Crawl_Data_Collection\\PriceMate\\shopee\\{today}"
    # base_path = f"E:\\Data\\Crawl_Data_Collection\\PriceMate\\shopee\\2026_01_11\\HTML_Files"
    # base_path = f"C:\\Users\\admin\\Downloads\\Shopee_URLs_23_11_2025.zip\\Shopee_URLs_23_11_2025"
    # "E:\Data\Crawl_Data_Collection\PriceMate\shopee\2025_10_27\HTML_Files\shopee.sg_supermarket_page_0.json"
    # E: / Data / Crawl_Data_Collection / PriceMate / shopee_supermarket / 2025_10_27 / HTML_Files / shopee.sg_supermarket_page_0.json

    html_path = os.path.join(base_path, "HTML_Files")

    # excel_path = os.path.join(base_path, "Excel_Files")

    os.makedirs(html_path, exist_ok=True)
    # os.makedirs(excel_path, exist_ok=True)

    print(f"HTML files path: {html_path}")

    return {
        'html_path': html_path,
        'Input_Table': category_input,
        'search_data': product_data,
        # 'excel': excel_path,  # if needed
    }

region_mapping = {
    'tw': ('shopee.tw', 'NT$', 'Taiwan'),
    'my': ('shopee.com.my', 'RM', 'Malaysia'),
    'br': ('shopee.com.br', 'R$', 'Brazil'),
    'cl': ('shopee.cl', 'CLP$', 'Chile'),
    'id': ('shopee.co.id', 'Rp', 'Indonesia'),
    'th': ('shopee.co.th', '฿', 'Thailand'),
    'co': ('shopee.com.co', 'COP$', 'Colombia'),
    'ph': ('shopee.ph', '₱', 'Philippines'),
    'sg': ('shopee.sg', '$', 'Singapore'),
    'vn': ('shopee.vn', '₫', 'Vietnam'),
    'mx': ('shopee.com.mx', 'MX$', 'Mexico')
}


def format_shopee_price(price):
    # Convert price to float and divide by 100000
    formatted_price = price / 100000

    # if str(formatted_price).endswith('.0'):
    #     r = int(formatted_price)
    # else:
    # Format the price with two decimal places and replace the decimal point with a comma
    r = f"{formatted_price:,.2f}".replace('.', ',')
    if r.endswith(',00'):
        r = r[:-3]
    return r.replace(",", "")

def format_indonesian_price(price):
    # Convert price to float and divide (same logic as your other functions)
    formatted_price = price / 100000

    # Format with 2 decimals using English locale (comma thousands, dot decimals)
    temp = f"{formatted_price:,.2f}"

    # Convert to Indonesian format: dot for thousands, comma for decimals
    result = temp.replace(',', 'X').replace('.', ',').replace('X', '.')

    # Remove trailing ",00"
    if result.endswith(',00'):
        result = result[:-3]

    return result

def format_vietnamese_price(price):
    # Convert price to float and divide by 1000
    formatted_price = price / 100000
    # Format the price with two decimal places, replace the decimal point with a comma,
    # and use dot as the thousand separator
    return f"{formatted_price:,.2f}".replace(',', '.')  #.replace(',', 'X').replace('.', ',').replace('X', '.')

def price_raw_from_shopee(shopee_price_value, divisor=100000):
    """
    Convert the integer price value returned by Shopee API into a float number.
    Shopee often returns prices as integers that need to be divided (100000 in your code).
    - shopee_price_value: int or numeric-like (or None)
    - divisor: default 100000 (matches your format_* functions)
    Returns float (0.0 on error / None input).
    """
    try:
        if shopee_price_value is None or shopee_price_value == "":
            return 0.0
        return round(float(shopee_price_value) / float(divisor), 2)
    except Exception:
        return 0.0

def check_video_url(url):
    try:
        response = requests.head(url, allow_redirects=True, timeout=5)
        # Check if the status code is 200 and the content type is a video
        if response.status_code == 200 and 'video' in response.headers.get('Content-Type', ''):
            return True
        else:
            return False
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return False
def generate_hashId(string):
    hash_utf8_b = f'{string}'.encode('utf8')
    hash_id = int(hashlib.md5(hash_utf8_b).hexdigest(),16) % (10 ** 10)
    return hash_id


def insert_record(collection,item):
    try:
        collection.insert_one(dict(item))
        gprint("Data Inserted Successfully...")
        return True

    except Exception as e:
        if 'duplicate' not in str(e).lower():
            rprint(f"Error in Inserting Data Query: {e}")
            return None


def update_record(collection,item: dict,_id: ObjectId):
    try:
        d = collection.update_one({'_id':ObjectId(_id)},{'$set':item})
        if not d.modified_count:
            print("Records is not updated...",_id)
        else:
            gprint("Data Updated Successfully...")

        return True

    except Exception as e:
        if 'duplicate' not in str(e).lower():
            rprint(f"Error in Inserting Data Query: {e}")
            return None

# Base path
# base_path = f"E:\\Data\\Crawl_Data_Collection\\PriceMate\\{website}\\{today}"
#
# # Define paths for different file types
# html_path = os.path.join(base_path, "HTML_Files")
# # excel_path = os.path.join(base_path, "Excel_Files")
#
# # Create directories
# os.makedirs(html_path, exist_ok=True)
# # os.makedirs(excel_path, exist_ok=True)
#
# print(f"HTML files path: {html_path}")
# # print(f"Excel files path: {excel_path}")