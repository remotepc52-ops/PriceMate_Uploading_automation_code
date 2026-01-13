import re

import scrapy
import os
import json
import datetime
from pricemate.spiders.spider_lazada import PricemateBaseSpider
# from Common_Modual.common_functionality import extract_size_master

HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Language': 'en-US,en;q=0.9,hi;q=0.8',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36',
    'Cookie': 'superweb-locale=en_US; venderId=12; pickUpStoreId=; shipmentType=1; longitude=103.867744; latitude=1.355379; store=550989; _ga=GA1.1.540575064.1750654238; _fbp=fb.2.1750654239103.65353625236006938; ...',
}

def create_brand_mapping(json_data):
    brand_mapping = {}
    try:
        for filter_prop in json_data.get("data", {}).get("filterProperty", []):
            if filter_prop.get("propertyName") == "Brands":
                for brand in filter_prop.get("childProperties", []):
                    brand_id = brand.get("propertyId")
                    brand_name = brand.get("propertyName")
                    if brand_id and brand_name:
                        brand_mapping[brand_id] = brand_name
    except Exception as e:
        print(f"Error processing brand mapping: {e}")
    return brand_mapping

class ColdStorageCategorySpider(PricemateBaseSpider):
    name = "coldstorage_category"

    def __init__(self, retailer, region, *args, **kwargs):
        super().__init__(retailer, region, *args, **kwargs)

    @staticmethod
    def extract_size(size_string):
        try:
            size_string = size_string.strip()

            # 1️⃣ Look for patterns like "Size: 200ml" or "Pack Size: 2kg"
            pattern1 = r'(?:Size|Pack Size)[:\s]*([\d.]+)\s*(ml|mL|l|L|g|kg|oz|lb|packs?|pack|tablets?|capsules?)'
            match = re.search(pattern1, size_string, re.IGNORECASE)
            if match:
                size_value = match.group(1)
                size_unit = match.group(2)
                return f"{size_value} {size_unit}"

            # 2️⃣ Look for things like "200ml", "2kg", "90g", etc.
            pattern2 = r'([\d.]+)\s*(ml|mL|l|L|g|kg|oz|lb|packs?|pack|tablets?|capsules?)'
            match = re.search(pattern2, size_string, re.IGNORECASE)
            if match:
                size_value = match.group(1)
                size_unit = match.group(2)
                return f"{size_value} {size_unit}"

            # 3️⃣ Look for patterns like "90g×2" or "200ml x 3"
            pattern3 = r'([\d.]+)\s*(ml|mL|l|L|g|kg|oz|lb)\s*[×xX]\s*(\d+)'
            match = re.search(pattern3, size_string, re.IGNORECASE)
            if match:
                size = f"{match.group(1)} {match.group(2)}"
                quantity = match.group(3)
                return f"{size} x {quantity}"

            # 4️⃣ Look for just quantity (like "24本入り" or "2個")
            pattern4 = r'(\d+)\s*(個|本入り|袋|本)'
            match = re.search(pattern4, size_string, re.IGNORECASE)
            if match:
                quantity = f"{match.group(1)} {match.group(2)}"
                return quantity

            # If nothing matched
            return ""

        except Exception as e:
            print(f"Error extracting size: {e}")
            return ""

    def start_requests(self):
        meta = {
            "filename": "home_page_coldstorage_sg.html",
            "should_be": ["all-categories"]
        }
        yield scrapy.Request(
            "https://coldstorage.com.sg/",
            headers=HEADERS,
            callback=self.get_all_category,
            meta=meta
        )

    def get_all_category(self, response):
        all_categories = response.xpath('//div[@id="all-categories"]//div[@class="cascader__content"]//a')
        for cat in all_categories:
            category_url = cat.xpath('./@href').get()
            category_name = cat.xpath('.//text()').get()
            if not category_url.startswith('https://'):
                category_url = "https://coldstorage.com.sg" + category_url
            category_id = str(category_url.split('/category/')[-1].split('/')[0].replace("-", "_"))
            if not category_id.isnumeric():
                print(f"Invalid category id: {category_id}")
                continue

            item = {
                "_id": self.generate_hash_id(category_id, self.retailer, self.region),
                "CategoryId": category_id,
                "Category Name": category_name,
                "retailer": self.retailer,
                "region": self.region,
                "Category_Url": category_url,
                "Status": "Pending",
            }
            try:
                self.category_input.insert_one(item)
                print(f"Added category: {category_name}")
            except Exception:
                print(f"Already exists: {category_name}")

        total_pending = self.category_input.count_documents({
            "Status": "Pending",
            "retailer": self.retailer,
            "region": self.region
        })
        print("total_pending_categories: ", total_pending)
        for cat_item in self.category_input.find({
            "Status": "Pending",
            "retailer": self.retailer,
            "region": self.region
        }):
            yield from self.crawl_category_page(cat_item)

    def crawl_category_page(self, cat_item):
        category_id = str(cat_item['CategoryId'])
        category_url = str(cat_item['Category_Url'])
        category_name = str(cat_item['Category Name'])
        page_no = 1
        meta = {
            "category_id": category_id,
            "category_url": category_url,
            "category_name": category_name,
            "page_no": page_no,
            "filename": f"ColdStorage_Cat_{category_id}_page_{page_no}.html",
            "should_be": ["productList"]
        }
        payload = {
            'param': {'selected': category_id, 'pageSize': 20, 'page': page_no},
            'comm': {
                'dmTenantId': 10, 'venderId': 12, 'businessCode': 1, 'origin': 26,
                'superweb-locale': 'en_US', 'storeId': 550989,
                'pickUpStoreId': '', 'shipmentType': 1,
            },
        }
        post_headers = {
            'Accept': '*/*',
            'Accept-Language': 'en-US,en;q=0.9,hi;q=0.8',
            'Connection': 'keep-alive',
            'Content-Type': 'application/json;charset=UTF-8',
            'Cookie': HEADERS['Cookie']
        }
        yield scrapy.FormRequest(
            url="https://coldstorage.com.sg/api/item/templateData",
            method='POST',
            headers=post_headers,
            body=json.dumps(payload),
            callback=self.parse_category,
            meta=meta
        )

    def parse_category(self, response):
        meta = response.meta
        res_json = json.loads(response.text)
        brand_map = create_brand_mapping(res_json)
        products = res_json.get('data', {}).get("productList", [])
        category_id = meta["category_id"]
        category_name = meta["category_name"]
        page_no = meta["page_no"]
        total_pages = res_json.get('data', {}).get('pageInfo', {}).get('pageCount', 1)

        for product in products:
            try:
                name = product['wareName']
                stockcode = product['sku']
                product_url = f"https://coldstorage.com.sg/en/p/-/i/{stockcode}.html"
                filename = f"ColdStorage_PDP_{stockcode}.html" if stockcode else self.generate_hash_id(product_url, self.retailer, self.region) + ".html"
                price = round(float(product['promotionWareVO']['origPrice'] / 100), 2)
                was_price = round(float(product['promotionWareVO']['unitProPrice'] / 100), 2)
                per_unit_price = product.get('CupString', "")
                product_size = self.extract_size(name) or ""
                primary_image = product.get('wareImg', '').split("_")[0]
                is_available = product['status'] == 1
                brand_id = product.get('brand')
                brand = brand_map.get(str(brand_id), "").title() if brand_id else ""
                offer_info = "|".join([i.get('displayInfo', {}).get('proTag', '') for i in product['promotionWareVO'].get('promotionInfoList', [])
                                       if i.get('displayInfo', {}).get('proTag')])
                promo_type = "|".join([i.get('proType', '') for i in product['promotionWareVO'].get('promotionInfoList', [])
                                       if i.get('proType', '')])
                item = {
                    "Category_Name": category_name,
                    "ProductURL": product_url,
                    "ProductCode": stockcode,
                    "Name": name,
                    "Price": price,
                    "WasPrice": None if was_price == price else was_price,
                    "RRP": was_price if was_price else price,
                    "per_unit_price": per_unit_price,
                    "Offer_info": offer_info,
                    "Pack_size": product_size,
                    "Barcode": "",
                    "retailer_name": f"{self.retailer}_{self.region}",
                    "Category_Hierarchy": category_name,
                    "Brand": brand,
                    "Promo_Type": promo_type,
                    "Images": primary_image,
                    "is_available": is_available,
                    "Status": "Done",
                    "Parent": "Yes",
                    "filename": filename
                }
                self.save_product(item)
            except Exception as e:
                print(f"Error processing product {product.get('sku', '')}: {e}")

        if page_no < total_pages:
            # Next page
            next_page_no = page_no + 1
            meta_next = meta.copy()
            meta_next["page_no"] = next_page_no
            meta_next["filename"] = f"ColdStorage_Cat_{category_id}_page_{next_page_no}.html"
            payload_next = {
                'param': {'selected': category_id, 'pageSize': 20, 'page': next_page_no},
                'comm': {
                    'dmTenantId': 10, 'venderId': 12, 'businessCode': 1, 'origin': 26,
                    'superweb-locale': 'en_US', 'storeId': 550989,
                    'pickUpStoreId': '', 'shipmentType': 1,
                },
            }
            post_headers = {
                'Accept': '*/*',
                'Accept-Language': 'en-US,en;q=0.9,hi;q=0.8',
                'Connection': 'keep-alive',
                'Content-Type': 'application/json;charset=UTF-8',
                'Cookie': HEADERS['Cookie']
            }
            yield scrapy.FormRequest(
                url="https://coldstorage.com.sg/api/item/templateData",
                method='POST',
                headers=post_headers,
                body=json.dumps(payload_next),
                callback=self.parse_category,
                meta=meta_next
            )
        else:
            self.category_input.update_one({'CategoryId': category_id}, {'$set': {'Status': "Done"}})

    def close(self, reason):
        import subprocess

        cmd = [
            "python",
            "upload_to_s3_direct.py",
            "--domain", "coldstorage.com"
        ]
        subprocess.run(cmd, cwd=r"E:\pricemate_service")
        self.mongo_client.close()


if __name__ == '__main__':
    from scrapy.cmdline import execute
    execute('scrapy crawl coldstorage_category -a retailer=cold_storage-sg -a region=sg -a Type=eshop -a RetailerCode=cold_storage_sg'.split())
