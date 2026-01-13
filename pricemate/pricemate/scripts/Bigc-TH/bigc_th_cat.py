import requests
from config import *

headers = {
    "accept": "application/json, text/plain, */*",
    "accept-language": "en-US,en;q=0.9",
    "device-info": "Mozilla/5.0",
    "language": "th",
    "origin": "https://www.bigc.co.th",
    "platform": "web-desktop",
    "referer": "https://www.bigc.co.th/",
    "store-id": "11190",
    "user-agent": "Mozilla/5.0"
}

BASE_URL = "https://www.bigc.co.th/category/"

response = requests.get(
    "https://openapi.bigc.co.th/cms/v1/menu/main",
    headers=headers,
    proxies=proxies,
    verify=False
)

def collect_categories(categories):
    """
    categories: list of category dicts
    """
    for cat in categories:
        if not isinstance(cat, dict):
            continue

        cat_id = cat.get("id")
        slug = cat.get("slug")

        if cat_id and slug:
            full_url = f"{BASE_URL}{slug}"

            hash_id = generate_hash_id(full_url, "bigc-th", "th")

            item = {
                "_id": hash_id,
                "slug": slug,
                "url": full_url,
                "Status": "Pending"
            }

            try:
                search_data.update_one(
                    {"_id": hash_id},
                    {"$set": item},
                    upsert=True
                )
                print(f"✅ Saved: {slug} → {full_url}")
            except Exception as e:
                print(f"❌ DB error ({slug}): {e}")

if response.status_code == 200:
    data = response.json()
    menus = data.get("data", {}).get("menus", [])

    for menu in menus:
        children = menu.get("children", [])
        collect_categories(children)

else:
    print("Request failed:", response.status_code)
