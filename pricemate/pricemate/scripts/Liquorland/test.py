import hashlib

import requests
import json
import os
from concurrent.futures import ThreadPoolExecutor, as_completed
LOG_FILE = "image_log.json"

# Load existing log or initialize empty
if os.path.exists(LOG_FILE):
    try:
        with open(LOG_FILE, "r") as f:
            image_log = json.load(f)
    except json.JSONDecodeError:
        print("[WARNING] Log file was empty or invalid. Starting fresh.")
        image_log = {}
else:
    image_log = {}

def get_image_hash(url):
    try:
        response = requests.get(url, stream=True, timeout=5)
        if response.status_code == 200:
            hash_md5 = hashlib.md5()
            for chunk in response.iter_content(4096):
                hash_md5.update(chunk)
            return hash_md5.hexdigest()
    except requests.RequestException:
        pass
    return None

def check_image_url(product_id, i):
    url = f"https://imagevault.skulibrary.com/ColesLiquor/NoPrefix/e2520ee2b408c79be0916bdd062e372f1423c031/images/2400/id/CLG-{product_id}-{i}.jpg"
    try:
        response = requests.head(url, timeout=3)
        if response.status_code == 200:
            return url
    except requests.RequestException:
        pass
    return None

def get_product_images(product_id, max_images=10):
    if product_id in image_log:
        print(f"[LOG] Skipping {product_id}, already processed.")
        return image_log[product_id]

    product_images = []
    seen_hashes = set()

    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = {
            executor.submit(check_image_url, product_id, i): i
            for i in range(1, max_images)
        }
        for future in as_completed(futures):
            url = future.result()
            if not url:
                continue

            img_hash = get_image_hash(url)
            if img_hash and img_hash not in seen_hashes:
                seen_hashes.add(img_hash)
                product_images.append(url)
            else:
                print(f"[SKIP] Duplicate image at {url}")

    product_images.sort()
    image_log[product_id] = product_images

    # Save updated log
    with open(LOG_FILE, "w") as f:
        json.dump(image_log, f, indent=2)

    return product_images

# Example usage
product_id = "8232735"
images = get_product_images(product_id)
print(images)
