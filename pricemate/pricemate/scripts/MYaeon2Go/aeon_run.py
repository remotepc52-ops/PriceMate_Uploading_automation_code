import subprocess
import time
import os
import pymongo
from datetime import datetime

# ---------------------------------------
# CONFIG
# ---------------------------------------
PROJECT_PATH = r"E:\Projects\KP\PriceMate\MYaeon2Go"
MONGO_URL = "mongodb://localhost:27017/"
DB_NAME = "pricemate_eshop_aeon_my"

# ---------------------------------------
# UTILITIES
# ---------------------------------------
def log(msg):
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {msg}")

def run_file(filename):
    """Run a Python file located inside the project folder."""
    file_path = os.path.join(PROJECT_PATH, filename)

    log(f"➡️ Running: {filename}")
    result = subprocess.run(["python", file_path])

    if result.returncode != 0:
        log(f"❌ Error running {filename}")
    else:
        log(f"✅ Finished: {filename}")

# ---------------------------------------
# DATABASE LOGIC
# ---------------------------------------
def get_db():
    """Return MongoDB database instance."""
    client = pymongo.MongoClient(MONGO_URL)
    return client[DB_NAME]


def has_pending_pl():
    """Check if pending PL exists, initialize/reset collections if needed."""
    db = get_db()

    today_key = datetime.today().strftime("%Y_%m_%d")
    product_collection_name = f"Product_Data_{today_key}"

    category_input = db["Category_Input"]

    # ----- Check if today's Product_Data exists -----
    existing_collections = [c["name"] for c in db.list_collections()]

    if product_collection_name not in existing_collections:
        log(f"⚠️ {product_collection_name} missing. Resetting Category_Input to Pending...")
        category_input.update_many({}, {"$set": {"Status": "Pending"}})
        db.create_collection(product_collection_name)

    product_data = db[product_collection_name]

    # Try to create index
    try:
        category_input.create_index("UrlFriendlyName", unique=True)
        product_data.create_index("ProductCode", unique=True)
    except Exception:
        pass  # ignore duplicate index creation error

    # Count pending
    pending_count = category_input.count_documents({"Status": "Pending"})
    log(f"Pending items: {pending_count}")

    return pending_count > 0, pending_count, category_input

# ---------------------------------------
# MAIN PROCESS
# ---------------------------------------
def main():
    log(f"📁 Project: {PROJECT_PATH}")
    log("🚀 Starting MYaeon2Go Processing Workflow...")

    # 1️⃣ RUN SITEMAP SCRAPER
    run_file("1. Sitemap.py")

    # 2️⃣ RUN PDP UNTIL ALL PENDING ARE PROCESSED
    while True:
        has_pending, pending_count, _ = has_pending_pl()

        if not has_pending:
            log("🎉 All Done! No pending items left.")
            break

        run_file("PDP.py")

        log(f"⏳ Waiting 30 minutes... (Pending: {pending_count})\n")
        time.sleep(30 * 60)


if __name__ == "__main__":
    main()
