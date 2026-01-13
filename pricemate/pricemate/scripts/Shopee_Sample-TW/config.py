import json
import os
import sys
import re
from threading import Thread
from pymongo import MongoClient, UpdateOne

# --- CONFIGURATION ---
FILE_DIRECTORY = r"E:/Shopee_Page"
MONGO_URI = "mongodb://localhost:27017/"
DB_NAME = "shopee_sample_tw"
COLLECTION_NAME = "products_data"

# Shopee Image CDN
IMAGE_BASE_URL = "https://s-cf-tw.shopeesz.com/file/"


def get_mongo_collection():
    """Connect to MongoDB and return the collection."""
    try:
        client = MongoClient(MONGO_URI)
        db = client[DB_NAME]
        return db[COLLECTION_NAME]
    except Exception as e:
        print(f"Error connecting to MongoDB: {e}")
        return None


def price_raw_from_shopee(price_int):
    """Convert Shopee integer price (e.g., 26000000) to float (260.0)."""
    if not price_int:
        return 0.0
    return float(price_int) / 100000


def get_region_from_filename(filename):
    """Extracts 'tw', 'my', 'vn' from 'shopee.tw_...'"""
    try:
        if "shopee." in filename:
            return filename.split("shopee.")[1].split("_")[0]
        return "unknown"
    except:
        return "unknown"


def process_file(file_path, collection):
    """Reads a single JSON file and upserts data matching 100% reference headers."""
    try:
        filename = os.path.basename(file_path)
        region = get_region_from_filename(filename)

        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # Handle different JSON structures safely
        try:
            items = data.get('data', {}).get('centralize_item_card', {}).get('item_cards', [])
        except AttributeError:
            items = []

        if not items:
            print(f"  -> No items found in {filename}")
            return

        operations = []

        for item in items:
            # --- 1. Raw Data Extraction ---
            item_id = item.get('itemid')
            shop_id = item.get('shopid')
            shop_data = item.get('shop_data', {})
            shop_name = shop_data.get('shop_name', 'Unknown')

            # Construct URLs
            store_url = f"https://shopee.{region}/shop/{shop_id}"
            product_url = f"https://shopee.{region}/product/{shop_id}/{item_id}"

            display_asset = item.get('item_card_displayed_asset', {})
            product_name = display_asset.get('name', 'No Title')
            brand = item.get('global_brand', {}).get('display_name', '')

            # Price Processing
            price_info = item.get('item_card_display_price', {})
            # Current selling price
            raw_price = price_info.get('price', 0)
            final_price_raw = price_raw_from_shopee(raw_price)
            # Original price (WasPrice)
            strike_price = price_info.get('strikethrough_price', 0)
            regular_price_raw = price_raw_from_shopee(strike_price) if strike_price else final_price_raw
            # Discount/Offer info
            offer = price_info.get('discount', '')
            if offer: offer = f"{offer}%"

            # Stock
            is_sold_out = item.get('is_sold_out', False)
            is_available = not is_sold_out

            # Category Breadcrumb
            global_cat_ids = item.get('global_cat', {}).get('catid', [])
            category_hierarchy = " > ".join(str(cid) for cid in global_cat_ids) if global_cat_ids else ""

            # Images
            base_image_ids = display_asset.get('images', [])
            base_image_urls = [f"{IMAGE_BASE_URL}{img_id}" for img_id in base_image_ids]
            img_joined = "|".join(base_image_urls)

            # Retailer String Construction
            # Clean string similar to reference: .replace(" " or "  "," ").strip().lower()
            clean_shop_name = shop_name.replace(" ", "_").strip().lower()
            retailer_str = f"shopee_{clean_shop_name}_{region}"

            # --- 2. Variant Logic ---
            tier_variations = item.get('tier_variations', [])

            # Check if variants exist
            if tier_variations and len(tier_variations) > 0:
                primary_tier = tier_variations[0]
                options = primary_tier.get('options', [])
                var_images = primary_tier.get('images', [])

                for idx, pack_size in enumerate(options):
                    # Specific image for variant
                    v_img_id = var_images[idx] if idx < len(var_images) else None
                    if v_img_id:
                        # If variant has specific image, prepend it to the string or replace it?
                        # Reference implies "Images": img (singular/joined).
                        # Usually we want the specific image first.
                        v_img_url = f"{IMAGE_BASE_URL}{v_img_id}"
                        current_images = f"{v_img_url}|{img_joined}"
                    else:
                        current_images = img_joined

                    # Unique ID for Mongo
                    unique_id = f"{item_id}_{idx}"

                    # --- 3. Construct Document (MATCHING HEADERS 100%) ---
                    doc = {
                        "_id": unique_id,
                        # "Store name": shop_name.title(), # Commented in ref
                        "Store URL": store_url,
                        # "brand_filter": "",              # Commented in ref
                        "Id1": unique_id,  # Using Variant ID as Id1 placeholder
                        "source_id": unique_id,  # Using Variant ID as source_id placeholder
                        "ProductCode": item_id,
                        "Name": product_name,
                        "ProductURL": product_url,
                        "retailer_name": shop_name,
                        # "Seller URL": store_url,         # Commented in ref
                        "is_available": is_available,
                        "Brand": brand,
                        "Images": current_images,
                        "Promo_Type": "",
                        "per_unit_price": "",
                        "Barcode": "",
                        # "Currency": "TWD",               # Commented in ref
                        "WasPrice": regular_price_raw,  # Original Price
                        "Price": final_price_raw,  # Selling Price
                        "RRP": regular_price_raw,  # RRP usually same as WasPrice
                        "Pack_size": pack_size,  # Mapped Variant Name to Pack_size
                        "Offer_info": str(offer),
                        # "Monthly Item Sold": ...,        # Commented in ref
                        # "Historical Item Sold": ...,     # Commented in ref
                        # "Avg Rating": ...,               # Commented in ref
                        # "Total Review": ...,             # Commented in ref
                        "Category_Hierarchy": category_hierarchy,
                        "Status": "Done",
                        "region": region,
                        "retailer": retailer_str
                    }

                    operations.append(
                        UpdateOne({"_id": unique_id}, {"$set": doc}, upsert=True)
                    )

            else:
                # No variants (Single Item)
                unique_id = str(item_id)

                doc = {
                    "_id": unique_id,
                    "Store name": shop_name.title(),
                    "Store URL": store_url,
                    # "brand_filter": "",
                    # "Id1": unique_id,
                    # "source_id": unique_id,
                    "ProductCode": item_id,
                    "Name": product_name,
                    "ProductURL": product_url,
                    # "retailer_name": shop_name,
                    "Seller URL": store_url,
                    "is_available": is_available,
                    "Brand": brand,
                    "Images": img_joined,
                    # "Promo_Type": "",
                    # "per_unit_price": "",
                    # "Barcode": "",
                    "Currency": "TWD",
                    "WasPrice": regular_price_raw,
                    "Price": final_price_raw,
                    "RRP": regular_price_raw,
                    # "Pack_size": "",  # Empty for single items
                    # "Offer_info": str(offer),
                    # "Monthly Item Sold": ...,
                    # "Historical Item Sold": ...,
                    # "Avg Rating": ...,
                    # "Total Review": ...,
                    "Category_Hierarchy": category_hierarchy,
                    "Status": "Done",
                    "region": region,
                    "retailer": retailer_str
                }

                operations.append(
                    UpdateOne({"_id": unique_id}, {"$set": doc}, upsert=True)
                )

        # Execute Bulk Write
        if operations:
            collection.bulk_write(operations)
            print(f"  -> {filename}: Processed {len(operations)} items/variants.")

    except Exception as e:
        print(f"Error processing {file_path}: {e}")


def worker(file_list):
    """Thread worker function."""
    collection = get_mongo_collection()
    if not collection:
        return

    for file_path in file_list:
        process_file(file_path, collection)


if __name__ == '__main__':
    # 1. Get list of all JSON files in directory
    all_files = []
    if os.path.exists(FILE_DIRECTORY):
        for f in os.listdir(FILE_DIRECTORY):
            if f.endswith(".json") and "shopee" in f:
                all_files.append(os.path.join(FILE_DIRECTORY, f))
    else:
        print(f"Directory {FILE_DIRECTORY} not found.")
        sys.exit()

    total_files = len(all_files)
    print(f"Found {total_files} files to process.")

    # 2. Configure Threading
    NUM_THREADS = 5
    if total_files > 0:
        chunk_size = (total_files // NUM_THREADS) + 1
        chunks = [all_files[i:i + chunk_size] for i in range(0, total_files, chunk_size)]

        threads = []
        for chunk in chunks:
            t = Thread(target=worker, args=(chunk,))
            threads.append(t)
            t.start()

        for t in threads:
            t.join()

    print("-" * 30)
    print("Done. Data insertion complete.")