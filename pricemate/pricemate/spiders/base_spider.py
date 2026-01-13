import logging
import hashlib
from datetime import datetime
from scrapy import Spider
from pymongo import MongoClient

logging.getLogger("pymongo").setLevel(logging.WARNING)

# next_tuesday = (datetime.today() + relativedelta(weekday=MO(0))).date()
# Today1 = (datetime.today() + relativedelta(weekday=MO(2))).date()
# Today1 = (datetime.today() + relativedelta(weekday=MO(1))).date()
# today_date = datetime.date.today()
# day = today_date.strftime("%A").lower()
# if day == 'monday':
#     days = 2
# else:
#     days = 1
today = datetime.today()

class PricemateBaseSpider(Spider):
    custom_settings = {
        'RETRY_TIMES': 5,
        'DOWNLOAD_TIMEOUT': 51
    }

    def __init__(self, retailer, region, Type, RetailerCode, start=0, end=100000, lazada_pdp=False, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.retailer = retailer.lower()
        self.Type = Type
        self.RetailerCode = RetailerCode
        self.lazada_pdp = lazada_pdp
        self.region = region.lower()
        self.start_index = int(start)
        self.end = int(end)
        self.today = today.strftime("%Y_%m_%d")
        mongo_uri = "mongodb://localhost:27017"
        # mongo_uri = "mongodb://192.168.1.129:27017"
        self.mongo_client = MongoClient(mongo_uri)
        # self.db = self.mongo_client[f"pricemate_master_{self.region}"]
        self.db = self.mongo_client[f"pricemate_{self.Type}_{self.RetailerCode}"]
        self.product_table = self.db[f"Product_Data_{self.today}"]
        # self.product_url = self.db[f"Product_Url_{self.today}"]
        self.category_input = self.db[f"category_urls"]
        # self.category_input = self.db[f"input_data_table"]

        # self.product_url = self.db[f"Product_Url_2025_10_20"]
        # self.product_table = self.db[f"Product_Data_2025_11_06"]
        # self.category_input = self.db["category_urls_2025_11_06"]


        self.product_table.create_index(["ProductURL", "retailer"], unique = True)
        # self.product_table.create_index(["ProductCode", "retailer"], unique = True)
        # self.product_url.create_index(["ProductURL", "retailer"], unique = True)
        # self.product_table.create_index("ProductCode")
        self.product_table.create_index("retailer")
        self.product_table.create_index("region")
        self.product_table.create_index("Status")

        self.price_logs = self.db["Product_Data_Main"]
        # self.price_logs.create_index("ProductCode")
        # self.price_logs.create_index("retailer")
        # self.price_logs.create_index("region")
        # self.price_logs.create_index("Status")


        self.category_input.create_index("retailer")
        self.category_input.create_index("region")
        self.category_input.create_index("Status")


        if self.lazada_pdp:
            self.base_path =  f"E:\\Data\\Crawl_Data_Collection\\PriceMate\\{self.today}\\Lazada\\HTMLs"
        elif 'shopee' in self.retailer:
            self.base_path =  f"E:\\Data\\Crawl_Data_Collection\\PriceMate\\{self.today}\\shopee\\HTMLs"
        else:
            self.base_path = f"E:\\Data\\Crawl_Data_Collection\\PriceMate\\{self.today}\\{self.retailer}\\HTMLs"

        # if not self.category_input.find_one({"retailer": self.retailer, "region": self.region, "crawl_date": self.today}):
        #     self.category_input.update_many(
        #         {"retailer": self.retailer, "region": self.region},
        #         {"$set": {"Status": "Pending", "crawl_date": self.today}}
        #     )

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

    # def save_url(self, item):
    #     if not item:
    #         return
    #     if "_id" not in item:
    #         hash_id = self.generate_hash_id(item["ProductCode"], self.retailer, self.region)
    #     else:
    #         hash_id = item["_id"]
    #
    #     required_keys = {"_id": hash_id, "retailer": self.retailer, "region": self.region}
    #     item.update(required_keys)
    #     if "Status" not in item:
    #         item["Status"] = "Pending"
    #
    #     self.product_url.update_one({"_id": hash_id}, {"$set": item}, upsert=True)


    def save_price_log(self, price_log):
        if "_id" not in price_log:
            price_hash = self.generate_hash_id(self.retailer, self.region, str(price_log["ProductCode"]), self.today)
            price_log["_id"] = price_hash
        else:
            price_hash = price_log["_id"]
        self.price_logs.update_one({"_id": price_hash}, {"$set": price_log}, upsert=True)

    def update_category_status(self, hash_id, status):

        s = self.category_input.update_one(
            {"_id": hash_id},
            {"$set": {"Status": status, "last_crawled": self.today}}
        )
        print(f"Category Table Update: {hash_id}:", s.modified_count)



    def close(self, reason):
        self.mongo_client.close()
