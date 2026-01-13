import json
import os
from pymongo import MongoClient, UpdateOne

# --- CONFIGURATION ---
FILE_DIRECTORY = "E:\Shopee_Page"
FILENAME_PATTERN = "shopee.tw_98425451_page_{}.json"

MONGO_URI = "mongodb://localhost:27017/"
DB_NAME = "shopee_sample_tw"
COLLECTION_NAME = "products_data"


def get_mongo_collection():
    try:
        client = MongoClient(MONGO_URI)
        db = client[DB_NAME]
        return db[COLLECTION_NAME]
    except Exception as e:
        print(f"Error connecting to MongoDB: {e}")
        return None


def extract_variants_from_json(file_path):
    extracted_docs = []

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        items = data.get('data', {}).get('centralize_item_card', {}).get('item_cards', [])

        for item in items:
            # --- 1. Common Data ---
            item_id = item.get('itemid')
            shop_id = item.get('shopid')
            shop_location = item.get('shop_data', {}).get('shop_location')

            display_asset = item.get('item_card_displayed_asset', {})
            title = display_asset.get('name', 'No Title')

            # Price Processing
            price_info = item.get('item_card_display_price', {})
            raw_price = price_info.get('price', 0)
            formatted_price = raw_price / 100000 if raw_price else 0

            is_sold_out = item.get('is_sold_out', False)
            sales_info = item.get('item_card_display_sold_count', {})

            # --- CATEGORY BREADCRUMB (Joined with >) ---
            # We prefer global_cat (list) for the breadcrumb. If not, use single catid.
            global_cat_ids = item.get('global_cat', {}).get('catid', [])
            cat_id_single = item.get('catid')

            if global_cat_ids:
                # Join list of ints into string: "100629 > 100651"
                category_breadcrumb = " > ".join(str(cid) for cid in global_cat_ids)
            else:
                category_breadcrumb = str(cat_id_single) if cat_id_single else ""

            # --- IMAGES (Joined with |) ---
            base_image_ids = display_asset.get('images', [])
            # Convert IDs to URLs first
            base_image_urls = [f"https://s-cf-tw.shopeesz.com/file/{img_id}" for img_id in base_image_ids]
            # Join with pipe
            images_joined = " | ".join(base_image_urls)

            # --- 2. Variant Logic ---
            tier_variations = item.get('tier_variations', [])

            # Scenario A: Product has variations
            if tier_variations:
                primary_tier = tier_variations[0]
                group_name = primary_tier.get('name', 'Variation')
                options = primary_tier.get('options', [])
                images = primary_tier.get('images', [])

                for idx, option_name in enumerate(options):
                    # Specific image for this variant
                    variant_img_id = images[idx] if idx < len(images) else None
                    variant_img_url = f"https://s-cf-tw.shopeesz.com/file/{variant_img_id}" if variant_img_id else ""

                    doc = {
                        "_id": f"{item_id}_{idx}",
                        "item_id": item_id,
                        "is_variant": True,
                        "variant_index": idx,
                        "variation_group": group_name,
                        "Name": option_name,
                        "Images": variant_img_url,

                        # Shared Info
                        "title": title,
                        "price": formatted_price,
                        "stock_status": "Sold Out" if is_sold_out else "Available",
                        "shop_id": shop_id,
                        "shop_location": shop_location,

                        # Formatted Fields
                        "category_breadcrumb": category_breadcrumb,  # e.g. "123 > 456 > 789"
                        "all_images": images_joined,  # e.g. "http... | http..."

                        "sales_historical": sales_info.get('historical_sold_count_text'),
                        "sales_monthly": sales_info.get('monthly_sold_count_text'),
                        "source_file": os.path.basename(file_path)
                    }
                    extracted_docs.append(doc)

            # Scenario B: No variations
            else:
                doc = {
                    "_id": str(item_id),
                    "item_id": item_id,
                    "is_variant": False,
                    "variation_name": "Default",

                    "title": title,
                    "price": formatted_price,
                    "stock_status": "Sold Out" if is_sold_out else "Available",
                    "shop_id": shop_id,
                    "shop_location": shop_location,

                    # Formatted Fields
                    "category_breadcrumb": category_breadcrumb,
                    "all_images": images_joined,

                    "sales_historical": sales_info.get('historical_sold_count_text'),
                    "sales_monthly": sales_info.get('monthly_sold_count_text'),
                    "source_file": os.path.basename(file_path)
                }
                extracted_docs.append(doc)

    except json.JSONDecodeError:
        print(f"Skipping {file_path}: Invalid JSON.")
    except Exception as e:
        print(f"Error processing {file_path}: {e}")

    return extracted_docs


def main():
    collection = get_mongo_collection()
    if collection is None:
        return

    page = 0
    total_variants = 0

    print(f"Starting import from {FILE_DIRECTORY}...")

    while True:
        current_file = FILENAME_PATTERN.format(page)
        full_path = os.path.join(FILE_DIRECTORY, current_file)

        if not os.path.exists(full_path):
            print(f"File {current_file} not found. Stopping.")
            break

        print(f"Processing Page {page}: {current_file}...")

        documents = extract_variants_from_json(full_path)

        if documents:
            operations = []
            for doc in documents:
                operations.append(
                    UpdateOne(
                        {"_id": doc["_id"]},
                        {"$set": doc},
                        upsert=True
                    )
                )

            if operations:
                result = collection.bulk_write(operations)
                count = len(documents)
                print(f"  -> Processed {count} variants.")
                total_variants += count
        else:
            print("  -> No data found.")

        page += 1

    print("-" * 50)
    print(f"Done! Processed {page} pages.")
    print(f"Total records stored: {total_variants}")


if __name__ == "__main__":
    main()