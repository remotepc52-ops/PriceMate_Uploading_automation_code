from config import *
from threading import Thread
import json
import sys

# from renam_shops import fix_shopee_pagination

updated_urls = {
    "https://shopee.com.my/rabigoo?entryPoint=ShopBySearch&searchKeyword=rabigoo": "https://shopee.com.my/rabigoo",
    "https://shopee.com.my/fsh_grocerymart?entryPoint=ShopBySearch&searchKeyword=fsh_grocery%20mart": "https://shopee.com.my/fsh_grocerymart",
    "https://shopee.com.my/bbkiddy?entryPoint=ShopBySearch&searchKeyword=babykiddy": "https://shopee.com.my/bbkiddy",
    "https://shopee.com.my/kedaiubathockheng?entryPoint=ShopBySearch&searchKeyword=kedaiubathockheng": "https://shopee.com.my/kedaiubathockheng",
    "https://shopee.com.my/babymalaysia2020?entryPoint=ShopBySearch&searchKeyword=baby%20malaysia": "https://shopee.com.my/babymalaysia2020",
    "https://th.shp.ee/ShceMqK": "https://shopee.co.th/mamypoko_official_store",
    "https://th.shp.ee/Tq6bDMG": "https://shopee.co.th/babyloveofficial",
    "https://th.shp.ee/67ggWKh": "https://shopee.co.th/sunnybabythailand",
    "https://th.shp.ee/PNG64Fg": "https://shopee.co.th/pigeon_officialstore",
    "https://th.shp.ee/63ynrZW": "https://shopee.co.th/unicharmpc_official_store",
    "https://th.shp.ee/yB2bDy1": "https://shopee.co.th/kao_officialshop",
    "https://th.shp.ee/B5j9Q16": "https://shopee.co.th/lifree_official_store",
    "https://th.shp.ee/GiEE1cT": "https://shopee.co.th/certaintyofficial",
    "https://th.shp.ee/J55HpX4": "https://shopee.co.th/kleenexscott_thailand",
    "https://shopee.vn/vacababy?entryPoint=ShopBySearch&searchKeyword=vaca": "https://shopee.vn/vacababy",
    "https://shopee.vn/xuandinhpham?entryPoint=ShopBySearch&searchKeyword=t%E1%BB%95ng%20kho%20%C4%83n%20v%E1%BA%B7t%20th%E1%BB%B1c%20ph%E1%BA%A9m": "https://shopee.vn/xuandinhpham",
    "https://vn.shp.ee/pkLXzKQ": "https://shopee.vn/shop/863711032",
    "https://vn.shp.ee/goHq95L": "https://shopee.vn/sunmate_officialstore",
}

data_ = {"total": 0}


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

def Review_Extraction(start, end):

    data_list = Input_Table.find({"Status": "Pending"}).skip(int(start)).limit(int(end))
    for cat_item in data_list:
        Id = cat_item['_id']

        # TODO - Duplicates Remove
        product_data.delete_many({'Id1': Id})
        Data_Extraction(cat_item)


def Data_Extraction(cat_item, page = 0):
    try:
        Id = cat_item['_id']
        StoreURL = cat_item['url']
        # Type = cat_item['Type']
        # retailer_name = cat_item['retailer_name']
        # Retailer_Code = cat_item['Retailer Code']
        # Brand_Store = cat_item['Brand Store']
        # Store_Type = cat_item['Store Type']
        # Country = cat_item["Country"]



        # Normalize: strip query params to improve match accuracy
        def get_updated_url(original_url):
            # First, try exact match
            if original_url in updated_urls:
                return updated_urls[original_url]

            # Then, try by matching the base path (without query string)
            base_url = original_url.split('?')[0]
            for key in updated_urls:
                if key.split('?')[0] == base_url:
                    return updated_urls[key]

            # If still not found, return the original
            return original_url

        StoreURL1 = get_updated_url(StoreURL)

        # print("Scraping shopee All Pages...")
        url = StoreURL1
        if "?" in url:
            url = f"{url}&page={page}"
        else:
            url = f"{url}?page={page}"


        region_lower = region.lower()
        if region_lower in region_mapping:
            domain, CurrencySymbol, region_name = region_mapping[region_lower]
        else:
            print("Getting Wrong Region Name....", region_lower)
            return None

        shopid = url.split(f"{domain}/")[-1].split('shop/')[-1].split("/")[0].split("?")[0].split("#")[0] #.replace(".", "_")
        # print(url)
        filename = f'{domain.split("//")[-1]}_{shopid}_page_{page}.json'

        full_path = os.path.join(html_path, filename)
        full_path = full_path.replace("\\", "/")

        if not os.path.exists(full_path):
            # print("─────"*10)
            print("──────────Page Save Not Found──────────")
            print(full_path)
            print(StoreURL)
            # print("─────"*10)
            # time.sleep(100)

        if os.path.exists(full_path):
            print(f"File {full_path} already exists.")
            response = open(full_path, 'r', encoding='utf-8').read()
            if 'Not Found' in response:
                s = Input_Table.update_one({"_id": Id}, {"$set": {'Status': 'Not Found', "HtmlPath": full_path}})
                print("Input Status Updated...", s.modified_count)
                return None

            json_data = json.loads(response)

            try:
                # try:total = json_data['data'] ['items']
                try:total = json_data['data'] ['total']
                except:
                    try:total = json_data['data'] ['total_count'] #total_count
                    except:total = json_data['total_count'] #total_count
                    if not total:
                        s = Input_Table.update_one({"_id": Id}, {"$set": {'Status': 'Not Found', "HtmlPath": full_path}})
                        print("Input Status Updated...", s.modified_count)
                        return None
            except Exception as e:
                print("Error --> ", e)
                return

            try:
                product_list = json_data['data'] ['items']
            except:
                try:
                    product_list = json_data['data']['centralize_item_card']['item_cards']
                except:
                    try:
                        product_list = json_data['centralize_item_card']['item_cards']
                    except:
                        product_list = json_data['items']

            for product in product_list:
                data_['total'] += 1
                try: # data.items[1].item_basic.shopid
                    shopid = product['item_basic']['shopid']
                except:
                    shopid = product['shopid']


                try:
                    shop_name = ''.join(product['item_basic']['shop_name'].split())
                except:
                    try: shop_name = ''.join(product['shop_name'].split())
                    except: shop_name = ''.join(product['shop_data']['shop_name'].split())

                try:
                    brand = product['item_basic']['brand']
                except:
                    try:brand = product['brand']
                    except:brand =  product['global_brand'].get('display_name', "")



                try:
                    historical_sold = product['item_basic']['historical_sold']
                except:
                    try:historical_sold = product['historical_sold']
                    except:
                        historical_sold = product['item_card_display_sold_count']['historical_sold_count']
                        if not historical_sold:
                            historical_sold = product['item_card_display_sold_count'].get('historical_sold_count_text', 0)


                try:
                    sold = product['item_basic']['sold']
                except:
                    try:sold = product['sold']
                    except:
                        sold = product['item_card_display_sold_count']['monthly_sold_count']
                        if not sold:
                            sold = product['item_card_display_sold_count'].get('monthly_sold_count_text', 0)

                try:
                    itemid = product['item_basic']['itemid']
                except:
                    itemid = product['itemid']

                product_url = f"https://{domain}/Vanish-i.{shopid}.{itemid}"

                # data.items[0].item_basic.price
                try:
                    pack_size = product["tier_variations"][0]["options"][0]
                except:
                    try:pack_size = product["tier_variations"]["options"]
                    except:pack_size =""
                try:
                    regular_price1 = product['item_basic']['price']
                except:
                    try:regular_price1 = product['price']
                    except:regular_price1 = product['item_card_display_price']['price']

                try:
                    price_before_discount1 = product['item_basic']['price_before_discount']
                except:
                    try:price_before_discount1 = product['price_before_discount']
                    except:price_before_discount1 = product['item_card_display_price'].get('strikethrough_price', "")

                # ------------------ Price handling (REPLACEMENT) ------------------
                # At this point you already have:
                #   regular_price1 (product['item_basic']['price'] or similar)
                #   price_before_discount1 (product['item_basic']['price_before_discount'] or similar)

                # Compute raw numeric prices (floats) from Shopee integer values
                regular_price_raw = price_raw_from_shopee(regular_price1)
                price_before_discount_raw = price_raw_from_shopee(
                    price_before_discount1) if price_before_discount1 != "" else 0.0

                # If there's no price before discount, treat final as the only price
                if not price_before_discount1:
                    markdown = ""
                    # Format for display (strings) using your existing functions
                    if region_lower in ("vn", "sg", "my"):
                        regular_price = format_vietnamese_price(regular_price1)
                    else:
                        regular_price = format_shopee_price(regular_price1)

                    final_price = regular_price
                    # Raw final price same as regular_price_raw
                    final_price_raw = regular_price_raw

                else:
                    # Determine which value is the original and which is the markdown
                    if price_before_discount1 > regular_price1:
                        regular_price_candidate = price_before_discount1
                        markdown_price_candidate = regular_price1
                    else:
                        regular_price_candidate = regular_price1
                        markdown_price_candidate = price_before_discount1

                    # Raw numeric values
                    regular_price_raw = price_raw_from_shopee(regular_price_candidate)
                    final_price_raw = price_raw_from_shopee(markdown_price_candidate)
                    markdown_raw = final_price_raw  # for clarity

                    # Formatted strings for display
                    if region_lower in ("vn", "sg", "my"):
                        regular_price = format_vietnamese_price(regular_price_candidate)
                        final_price = format_vietnamese_price(markdown_price_candidate)
                        markdown = format_vietnamese_price(markdown_price_candidate)
                    elif region_lower == "id":
                        regular_price = format_indonesian_price(regular_price_candidate)
                        final_price = format_indonesian_price(markdown_price_candidate)
                        markdown = format_indonesian_price(markdown_price_candidate)
                    else:
                        regular_price = format_shopee_price(regular_price_candidate)
                        final_price = format_shopee_price(markdown_price_candidate)
                        markdown = format_shopee_price(markdown_price_candidate)

                # If final equals regular (strings), keep one empty for WasPrice string


                # Ensure final_price_raw exists (fall back)
                if 'final_price_raw' not in locals():
                    final_price_raw = regular_price_raw
                if 'markdown_raw' not in locals():
                    markdown_raw = price_raw_from_shopee(price_before_discount1) if price_before_discount1 else 0.0

                if final_price_raw == regular_price_raw:
                    regular_price_raw = ""
                    rrp = final_price_raw
                else:
                    rrp = regular_price_raw
                # ---------------- end replacement ------------------

                try:
                    try:
                        status = product['item_basic']['status']
                    except:
                        status = product['status']

                    if status:
                        isOos = False

                    else:
                        isOos = True
                except:
                    isOos = True

                # product name from website
                try:
                    product_name = product['item_basic']['name']
                except:
                    try:product_name = product['name']
                    except:product_name = product['item_card_displayed_asset']['name']

                try: #$.data.centralize_item_card.item_cards[1].item_rating.rating_star
                    ratingScore = product['item_basic']['item_rating']['rating_star']
                    if ratingScore:
                        ratingScore = round(float(ratingScore), 1)
                except:
                    ratingScore = product['item_rating']['rating_star']
                    if ratingScore:
                        ratingScore = round(float(ratingScore), 1)


                try: # $.data.items[9].item_basic.item_rating.rating_count[0]
                    reviews = product['item_basic']['item_rating']['rating_count']
                    reviews = int(reviews[0])
                except:
                    reviews = product['item_rating']['rating_count'][0]
                    reviews = int(reviews)

                try: # data.items[0].item_basic.discount
                    offer = product['item_card_display_price']['discount']
                except:
                    offer = product['discount']

                try:
                    images = product['item_card_displayed_asset']['images']
                    base_url = "https://down-my.img.susercontent.com/file/"
                    img = "|".join([base_url + image for image in images])

                except:
                    images = product['image']
                    base_url = "https://down-my.img.susercontent.com/file/"
                    img = "|".join([base_url + image for image in images])

                item = {
                # "Store name": shop_name.title(),
                "Store URL": StoreURL,
                # "brand_filter": "",
                "source_id":"9518c0e0-4d99-4882-8530-ea5e8337e059",
                "ProductCode": itemid,
                "Name": product_name,
                "ProductURL": product_url,
                "retailer_name": shop_name,
                # "Seller URL": StoreURL,
                "is_available": True if not isOos else False,
                "Brand": brand,
                "Images": img,
                "Promo_Type": "",
                "per_unit_price": "",
                "Barcode": "",
                # "Currency": CurrencySymbol,
                "WasPrice": regular_price_raw,
                "Price": final_price_raw,
                "RRP": rrp,
                "Pack_size":pack_size,
                "Offer_info": offer,
                # "Monthly Item Sold": sold,
                # "Historical Item Sold": historical_sold,
                # "Avg Rating": ratingScore,
                # "Total Review": reviews,
                "Category_Hierarchy": "",
                "Status": "Done",
                "region": region_lower,
                "retailer": f"shopee_{shop_name}_{region_lower}".replace(" " or "  ","_").strip('_').lower()

                }
                print(product_url)
                try:
                    # Input_Table.insert_one(item)
                    product_data.insert_one(item)
                except:
                    pass

            try:noMorePages = json_data['data']['no_more']
            except:
                try:noMorePages = json_data['data']['nomore']
                except:noMorePages = json_data['nomore']

            # if not SKU_bench_mark:
            #     SKU_bench_mark = total

            Crawled_Total = product_data.count_documents({'Id1': Id})
            page += 1

            # shopid = url.split(f"{domain}/")[-1].split('shop/')[-1].split("/")[0].split("?")[0].split("#")[0]
            # nextpage_filename = f'{domain.split("//")[-1]}_{shopid}_page_{page}.json'
            # # nextpage_filename = f'shopee.ph_{shopid}_page_{page}.json'
            # # filename = f'{region_lower}_{shopid}_{page + 1}.html'
            #
            #
            # nextpage_path = os.path.join(html_path, nextpage_filename)
            # nextpage_path = nextpage_path.replace("\\", "/")
            # print(nextpage_path)

            # if not noMorePages and Crawled_Total < int(SKU_bench_mark):
            if not noMorePages:
                print("Going To Shopee Next Page...", page)
                Data_Extraction(cat_item,  page=page)

            else:
                print("Next page is not available.....", page)
                difference_ratio = (int(Crawled_Total) - int(total)) / int(total)
                difference_ratio = round(difference_ratio * 100, 2)
                print(difference_ratio)  # Output: 0.2 (i.e., 20% increase from b to a)

                s = Input_Table.update_one({"_id": Id}, {"$set": {'Status': 'Done',
                                                                  'Diff_Ratio_%': difference_ratio,
                                                                  'Expected_Total': total,
                                                                  "Crawled_Total": Crawled_Total}})
                print("Input Status Updated...", s.modified_count)

                return None

    except Exception as e:
        print(f"Error in Main Data Extraction function ", e)
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # website = "shopee_supermarket"
    # website = "shopee_petsmore"
    # website = "shopee_bigpharmacy"
    # website = "shopee_guardian"
    # website = "shopee_caringpharmacyn"
    # website = "shopee_mydin"
    # website = "shopee_lotus"
    website = "shopee"
    # website = "shopee_watson"
    # website = "shopee_watsons"

    # type = "eshop"
    type = "marketplace"

    regions = [
        "my",
        # "vn",
        # "sg",
        # "ph",
        # "th",
        # "id"
    ]
    for region in regions:

        Total_Dict = {
            "Total": 0
        }

        # meta_data = get_configration(f"pricemate_eshop_{website}_{region}")
        meta_data = get_configration(f"pricemate_{type}_{website}_{region}")
        html_path = meta_data.get('html_path')
        # excel = meta_data.get('excel')

        Input_Table = meta_data.get('Input_Table')
        product_data = meta_data.get('search_data')


        # def has_sold_out_items(directory_path):
        #     files = [f for f in os.listdir(directory_path)]
        #     return any("sold.out.items" in f for f in files)
        # if has_sold_out_items(pdp_html_path):
        #     print("Has Sold Out Product....")
        #     fix_shopee_pagination(pdp_html_path)

        retry = 0
        total_count = Input_Table.count_documents({'Status': 'Pending'})
        print(f"{region} | Total Pending: ", total_count)
        if not total_count:
            continue

        if total_count >= 1:
            variable_count = total_count // 1
        else:
            variable_count = total_count // total_count

        if variable_count == 0:
            variable_count = total_count ** 1

        count = 1
        threads = [Thread(target=Review_Extraction, args=(i, variable_count)) for i in
                   range(0, total_count, variable_count)]

        for th in threads:
            th.start()

        for th in threads:
            th.join()

        retry += 1
        print("--------- Thread Ends ----------- ")

        # if region == "ID":
        #     StoreURL = "https://shopee.co.id/opellaid"
        # elif region == "VN":
        #     StoreURL = "https://shopee.vn/molfixofficialstore"
        #
        # Id = ObjectId('6874cdae41277a2bca15ace0')
        # Marketplace = "SHP"
        # Country = region
        # StoreURL = StoreURL
        # seller_type = ""
        # Brand_filter = "No filter"
        # expected_sku_count = 143
        # Data_Extraction(Marketplace, Id, Country, StoreURL, seller_type, Brand_filter, expected_sku_count)
        # print("Total: ", data_['total'])