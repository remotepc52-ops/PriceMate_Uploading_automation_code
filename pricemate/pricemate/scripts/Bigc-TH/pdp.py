import json
import re
import os
import time
import requests
from scrapy.selector import Selector
from concurrent.futures import ThreadPoolExecutor
from config import *


def parse_price_million(price_str):
    if not price_str: return None
    try:
        cleaned = str(price_str).replace("฿", "").replace(",", "").strip()
        return float(cleaned)
    except Exception:
        return None


def extract_size(size_string):
    if not size_string: return ""
    try:
        size_string = size_string.strip()
        patterns = [
            r'(?:Size|Pack Size)[:\s]*([\d.]+)\s*(ml|mL|l|L|g|kg|oz|lb|packs?|pack|tablets?|capsules?)',
            r'([\d.]+)\s*(ml|mL|l|L|g|kg|oz|lb|packs?|pack|tablets?|capsules?)',
            r'([\d.]+)\s*(ml|mL|l|L|g|kg|oz|lb)\s*[×xX]\s*(\d+)',
            r'(\d+)\s*(個|本入り|袋|ชิ้น|box)'
        ]
        for p in patterns:
            match = re.search(p, size_string, re.IGNORECASE)
            if match:
                return f"{match.group(1)} {match.group(2)}"
        return ""
    except Exception:
        return ""


def process_document(doc):
    doc_id = doc['_id']
    prod_url = doc['ProductURL']
    prod_code = doc.get('ProductCode', '')

    slug = prod_url.split("/")[-1]

    if not os.path.exists(html_path):
        os.makedirs(html_path)

    html_filename = f"pdp_{slug}.html"
    html_filepath = os.path.join(html_path, html_filename)
    pdp_data = ""

    # --- 1. FETCHING ---
    if os.path.exists(html_filepath):
        with open(html_filepath, "r", encoding="utf-8") as f:
            pdp_data = f.read()
    else:
        headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        }
        for attempt in range(3):
            try:
                response = requests.get(prod_url, headers=headers, proxies=proxies1, verify=False, timeout=30)
                if response.status_code == 200:
                    pdp_data = response.text
                    with open(html_filepath, "w", encoding="utf-8") as f:
                        f.write(pdp_data)
                    break
                time.sleep(2)
            except Exception as e:
                print(f"Error fetching {prod_url}: {e}")
                time.sleep(2)

    if not pdp_data:
        print(f"❌ Failed to get HTML for {prod_url}")
        return

    data = Selector(text=pdp_data)

    # --- 2. DATA EXTRACTION ---
    next_data_script = data.xpath('//script[@id="__NEXT_DATA__"]/text()').get()

    product_detail = {}
    attributes = {}

    # Defaults
    name = ""
    name_en = ""
    brand = ""

    if next_data_script:
        try:
            json_blob = json.loads(next_data_script)
            product_detail = json_blob.get('props', {}).get('pageProps', {}).get('productDetail', {})
            attributes = product_detail.get('attributes', {})
        except Exception as e:
            print(f"Error parsing NEXT_DATA: {e}")

    # --- 3. FILL VARIABLES ---

    # --- NAME LOGIC (Updated to Fix Thai Names) ---
    # 1. Try explicit English Name attribute
    name = attributes.get('eng_name')

    # 2. Try Name EN field
    if not name:
        name = product_detail.get('name_en')

    # 3. Fallback: Try to format the SLUG if Name is still empty or likely Thai (simple check)
    # This turns "foot-steel-ruler-24" -> "Foot Steel Ruler 24"
    if not name:
        url_slug = product_detail.get('slug', '')
        if url_slug:
            # Remove numeric IDs at end of slug often found in URL
            clean_slug = re.sub(r'\.\d+$', '', url_slug)
            name = clean_slug.replace('-', ' ').title()

    # 4. Final Fallback: Thai Name
    if not name:
        name = product_detail.get('name')
    if not name:
        name = data.xpath('//h1/text()').get()

    # --- BRAND ---
    brand_slug = product_detail.get('brand', {}).get('slug')
    if brand_slug:
        brand = brand_slug.replace('-', ' ').title()
    else:
        brand = product_detail.get('brand', {}).get('name')
        if not brand:
            brand = data.xpath('//div[@id="pdp_brand-title"]/text()').get()
    if brand == "Other":
        brand = ""
    # --- CATEGORY ---
    breadcrumb = ""
    dept = attributes.get('department_name')
    sub_dept = attributes.get('sub_department_name')
    class_name = attributes.get('class_name')
    sub_class = attributes.get('sub_class_name')

    cat_parts = [x for x in [dept, sub_dept, class_name, sub_class] if x]
    if cat_parts:
        breadcrumb = " > ".join(cat_parts)

    if not breadcrumb and 'breadcrumb' in product_detail:
        bc_slugs = [b.get('slug') for b in product_detail['breadcrumb'] if b and b.get('slug')]
        if bc_slugs:
            breadcrumb = " > ".join([s.replace('-', ' ').title() for s in bc_slugs])

    if not breadcrumb:
        bc_list = data.xpath('//ul[contains(@class, "breadcrumb")]//li//a//text()').getall()
        breadcrumb = " > ".join([b.strip() for b in bc_list if b.strip()])

    # --- IMAGES ---
    image_list = []
    if 'images' in product_detail and isinstance(product_detail['images'], list):
        image_list = [img.get('url') for img in product_detail['images'] if img.get('url')]

    if not image_list:
        try:
            ld_json = data.xpath('string(//script[@type="application/ld+json"])').get()
            if ld_json:
                schema = json.loads(ld_json)
                img = schema.get('image')
                if isinstance(img, str):
                    image_list.append(img)
                elif isinstance(img, list):
                    image_list = img
        except:
            pass

    if not image_list:
        image_list = data.xpath('//div[contains(@class, "imageSlider")]//img/@src').getall()

    images = " | ".join(image_list)

    # --- PRICE ---
    price = 0.0
    if 'price_incl_tax' in product_detail:
        price = float(product_detail['price_incl_tax'])
    elif 'price_sales' in product_detail:
        price = float(product_detail['price_sales'])
    else:
        price_str = data.xpath('//div[contains(@class, "product_price_new")]/text()').get()
        price = parse_price_million(price_str)

    # --- UNIT ---
    unit = product_detail.get('unit', '')
    if not unit:
        unit_vals = data.xpath('//span[contains(@id, "price-unit")]/text()').getall()
        unit = unit_vals[-1].strip() if unit_vals else ""

    # CHANGE: Add :.2f here to match the other price fields
    per_unit_price = f"{price:.2f}/{unit}" if unit and price else f"{price:.2f}"

    # --- STOCK ---
    is_available = False

    # 1. Try checking JSON data first (most reliable)
    if 'stock' in product_detail:
        is_available = product_detail['stock'] == 'Y'

    # 2. Fallback to HTML check
    else:
        # Find the button containing the Thai text "Add to Cart"
        atc_btn = data.xpath('//button[contains(text(), "เพิ่มใส่รถเข็น")]')

        if atc_btn:

            is_disabled = atc_btn.xpath('@disabled').get()

            is_available = is_disabled is None
        else:
            # If button not found at all, assume unavailable
            is_available = False

    # --- RRP & WasPrice Logic ---
    rrp = price
    was_price_val = ""

    # 1. Try JSON First (if available)
    if 'price_base' in product_detail:
        try:
            raw_base = float(product_detail['price_base'])
            if raw_base > price:
                was_price_val = raw_base
                rrp = raw_base
        except:
            pass

    # 2. HTML Fallback (TARGETING YOUR SPECIFIC SNIPPET)
    if not was_price_val:
        # Look for the specific ID 'pdp_price-base' found in your HTML
        old_price_str = data.xpath('//span[@id="pdp_price-base"]/text()').get()

        # Secondary check: Look for the class name if ID fails
        if not old_price_str:
            old_price_str = data.xpath('//div[contains(@class, "product_baseprice")]/text()').get()

        if old_price_str:
            raw_base_html = parse_price_million(old_price_str)

            # Only apply if the old price is strictly greater than current price
            if raw_base_html and raw_base_html > price:
                was_price_val = raw_base_html
                rrp = raw_base_html
            else:
                # If found price is same or lower, treat as normal price
                was_price_val = ""
                rrp = price


    offer_info = ""
    if isinstance(was_price_val, float) and was_price_val > price:
        discount = round(((was_price_val - price) / was_price_val) * 100)
        offer_info = f"{discount}%"

    pack_size = extract_size(name)
    sku = product_detail.get('sku') or data.xpath('//span[@id="pdp_product-id"]/text()').get()

    # --- BARCODE FIX ---
    barcode = product_detail.get('main_barcode', '')
    if not barcode:
        barcode = sku  # BigC often uses SKU as Barcode (e.g. 885...)

    items = {
        "Name": name,
        "Promo_Type": "",
        "per_unit_price": per_unit_price,
        "Offer_info": offer_info,
        "Barcode": barcode,
        "Pack_size": pack_size,
        "Images": images,
        "Price": f"{price:.2f}",
        "WasPrice": f"{was_price_val:.2f}" if isinstance(was_price_val, (int, float)) else "",
        "RRP": f"{rrp:.2f}",
        "ProductURL": prod_url,
        "is_available": is_available,
        "Status": "Done",
        "ProductCode": sku,
        "Category_Hierarchy": breadcrumb,
        "Brand": brand,
        "retailer_name": "bigc-th",
        "retailer": "bigc",
        "region": "th"
    }

    try:
        if price:
            product_data.update_one(
                {"_id": doc_id},
                {"$set": items}
            )
            print(f"✅ Updated: {name[:30]}")
        else:
            print(f"❌ Price 0 for {prod_url}")

    except Exception as e:
        print(f"❌ Error updating product: {e}")


if __name__ == "__main__":
    with ThreadPoolExecutor(max_workers=50) as executor:
        docs = list(product_data.find({"Status": "Pending"}))
        print(f"Total Pending Documents: {len(docs)}")
        executor.map(process_document, docs)