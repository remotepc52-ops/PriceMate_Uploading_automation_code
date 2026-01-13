import json
import re
import time
import urllib

from Common_Modual.common_functionality import Rprint
from parsel import Selector
from urllib.parse import quote
import scrapy
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# from pricemate.spiders.base_spider import PricemateBaseSpider
from pricemate.spiders.base_spider import PricemateBaseSpider

cookies = {
        '_ga': 'GA1.1.547981432.1749189992',
        'mp_d7f79c10b89f9fa3026f2fb08d3cf36d_mixpanel': '%7B%22distinct_id%22%3A%20%22%24device%3A19743d91b718a6-063cd8524c853c-26011e51-144000-19743d91b718a6%22%2C%22%24device_id%22%3A%20%2219743d91b718a6-063cd8524c853c-26011e51-144000-19743d91b718a6%22%2C%22%24initial_referrer%22%3A%20%22%24direct%22%2C%22%24initial_referring_domain%22%3A%20%22%24direct%22%7D',
        '_ga_MN0XLNH39T': 'GS2.1.s1752151324$o10$g1$t1752152104$j60$l0$h0',}

headers = {
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8,hi;q=0.7',
        # 'origin': 'https://www.mydin.my',
        'priority': 'u=1, i',
        # 'referer': 'https://www.mydin.my/',
        # 'sec-ch-ua': '"Google Chrome";v="137", "Chromium";v="137", "Not/A)Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        # 'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36',
    }

class MydinPdpSpider(PricemateBaseSpider):
    name = "mydin_pdp"

    def __init__(self, retailer, region, *args, **kwargs):
        super().__init__(retailer=retailer, region=region, *args, **kwargs)

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
        docs = self.category_input.find({
            "retailer": self.retailer,
            "region": self.region,
            "Status": "Pending"
        })
        for doc in docs:
            cate_url = doc.get('url')
            cat = doc.get('cat_id')
            hash_id = doc.get("_id")
            slug = cate_url.rstrip("/").split("/")[-1]
            page = 1
            url = f'https://myapi.mydin.my/magento/products?body=[%7B%22filter%22:%7B%22category_id%22:%7B%22eq%22:{cat}%7D%7D,%22pageSize%22:48,%22currentPage%22:{page},%22sort%22:%7B%22position%22:%22ASC%22%7D%7D,%7B%22products%22:%22products-custom-query%22,%22metadata%22:%7B%22fields%22:%22%5Cn++++++++++++++++++++aggregations(filter:+%7B+category:+%7B+includeDirectChildrenOnly:+true+%7D+%7D)+%7B%5Cn++++++++++++++++++++++++attribute_code%5Cn++++++++++++++++++++++++count%5Cn++++++++++++++++++++++++label%5Cn++++++++++++++++++++++++options+%7B%5Cn++++++++++++++++++++++++++++count%5Cn++++++++++++++++++++++++++++label%5Cn++++++++++++++++++++++++++++value%5Cn++++++++++++++++++++++++%7D%5Cn++++++++++++++++++++%7D%5Cn++++++++++++++++++++page_info+%7B%5Cn++++++++++++++++++++++++current_page%5Cn++++++++++++++++++++++++page_size%5Cn++++++++++++++++++++++++total_pages%5Cn++++++++++++++++++++%7D%5Cn++++++++++++++++++++total_count%5Cn++++++++++++++++++++sort_fields+%7B%5Cn++++++++++++++++++++++++default%5Cn++++++++++++++++++++++++options+%7B%5Cn++++++++++++++++++++++++++++label%5Cn++++++++++++++++++++++++++++value%5Cn++++++++++++++++++++++++%7D%5Cn++++++++++++++++++++%7D%5Cn++++++++++++++++++++items+%7B%5Cn++++++++++++++++++++++++id%5Cn++++++++++++++++++++++++sku%5Cn++++++++++++++++++++++++mfgCode%5Cn++++++++++++++++++++++++url_key%5Cn++++++++++++++++++++++++name%5Cn++++++++++++++++++++++++custom_productdescription%5Cn++++++++++++++++++++++++custom_productname%5Cn++++++++++++++++++++++++image+%7B%5Cn++++++++++++++++++++++++++++url%5Cn++++++++++++++++++++++++++++label%5Cn++++++++++++++++++++++++%7D%5Cn++++++++++++++++++++++++thumbnail+%7B%5Cn++++++++++++++++++++++++++++url%5Cn++++++++++++++++++++++++++++label%5Cn++++++++++++++++++++++++%7D%5Cn++++++++++++++++++++++++tier_prices+%7B%5Cn++++++++++++++++++++++++++++qty%5Cn++++++++++++++++++++++++++++value%5Cn++++++++++++++++++++++++%7D%5Cn++++++++++++++++++++++++price_tiers+%7B%5Cn++++++++++++++++++++++++++++quantity%5Cn++++++++++++++++++++++++++++discount+%7B%5Cn++++++++++++++++++++++++++++++++amount_off%5Cn++++++++++++++++++++++++++++++++percent_off%5Cn++++++++++++++++++++++++++++%7D%5Cn++++++++++++++++++++++++%7D%5Cn++++++++++++++++++++++++price_range+%7B%5Cn++++++++++++++++++++++++++++minimum_price+%7B%5Cn++++++++++++++++++++++++++++++++final_price+%7B%5Cn++++++++++++++++++++++++++++++++++++currency%5Cn++++++++++++++++++++++++++++++++++++value%5Cn++++++++++++++++++++++++++++++++%7D%5Cn++++++++++++++++++++++++++++++++regular_price+%7B%5Cn++++++++++++++++++++++++++++++++++++currency%5Cn++++++++++++++++++++++++++++++++++++value%5Cn++++++++++++++++++++++++++++++++%7D%5Cn++++++++++++++++++++++++++++%7D%5Cn++++++++++++++++++++++++++++maximum_price+%7B%5Cn++++++++++++++++++++++++++++++++final_price+%7B%5Cn++++++++++++++++++++++++++++++++++++currency%5Cn++++++++++++++++++++++++++++++++++++value%5Cn++++++++++++++++++++++++++++++++%7D%5Cn++++++++++++++++++++++++++++++++regular_price+%7B%5Cn++++++++++++++++++++++++++++++++++++currency%5Cn++++++++++++++++++++++++++++++++++++value%5Cn++++++++++++++++++++++++++++++++%7D%5Cn++++++++++++++++++++++++++++%7D%5Cn++++++++++++++++++++++++%7D%5Cn++++++++++++++++++++++++...+on+ConfigurableProduct+%7B%5Cn++++++++++++++++++++++++++++configurable_options+%7B%5Cn++++++++++++++++++++++++++++++++attribute_code%5Cn++++++++++++++++++++++++++++%7D%5Cn++++++++++++++++++++++++++++variants+%7B%5Cn++++++++++++++++++++++++++++++++attributes+%7B%5Cn++++++++++++++++++++++++++++++++++++code%5Cn++++++++++++++++++++++++++++++++++++label%5Cn++++++++++++++++++++++++++++++++++++uid%5Cn++++++++++++++++++++++++++++++++%7D%5Cn++++++++++++++++++++++++++++++++product+%7B%5Cn++++++++++++++++++++++++++++++++++++salable_quantity%5Cn++++++++++++++++++++++++++++++++++++quantity%5Cn++++++++++++++++++++++++++++++++++++sku%5Cn++++++++++++++++++++++++++++++++++++price_range+%7B%5Cn++++++++++++++++++++++++++++++++++++++++minimum_price+%7B%5Cn++++++++++++++++++++++++++++++++++++++++++++final_price+%7B%5Cn++++++++++++++++++++++++++++++++++++++++++++++++currency%5Cn++++++++++++++++++++++++++++++++++++++++++++++++value%5Cn++++++++++++++++++++++++++++++++++++++++++++%7D%5Cn++++++++++++++++++++++++++++++++++++++++++++regular_price+%7B%5Cn++++++++++++++++++++++++++++++++++++++++++++++++currency%5Cn++++++++++++++++++++++++++++++++++++++++++++++++value%5Cn++++++++++++++++++++++++++++++++++++++++++++%7D%5Cn++++++++++++++++++++++++++++++++++++++++%7D%5Cn++++++++++++++++++++++++++++++++++++++++maximum_price+%7B%5Cn++++++++++++++++++++++++++++++++++++++++++++final_price+%7B%5Cn++++++++++++++++++++++++++++++++++++++++++++++++currency%5Cn++++++++++++++++++++++++++++++++++++++++++++++++value%5Cn++++++++++++++++++++++++++++++++++++++++++++%7D%5Cn++++++++++++++++++++++++++++++++++++++++++++regular_price+%7B%5Cn++++++++++++++++++++++++++++++++++++++++++++++++currency%5Cn++++++++++++++++++++++++++++++++++++++++++++++++value%5Cn++++++++++++++++++++++++++++++++++++++++++++%7D%5Cn++++++++++++++++++++++++++++++++++++++++%7D%5Cn++++++++++++++++++++++++++++++++++++%7D%5Cn++++++++++++++++++++++++++++++++++++tier_prices+%7B%5Cn++++++++++++++++++++++++++++++++++++++++qty%5Cn++++++++++++++++++++++++++++++++++++++++value%5Cn++++++++++++++++++++++++++++++++++++%7D%5Cn++++++++++++++++++++++++++++++++%7D%5Cn++++++++++++++++++++++++++++%7D%5Cn++++++++++++++++++++++++%7D%5Cn++++++++++++++++++++++++...+on+SimpleProduct+%7B%5Cn++++++++++++++++++++++++++++salable_quantity%5Cn++++++++++++++++++++++++++++quantity%5Cn++++++++++++++++++++++++++++sku%5Cn++++++++++++++++++++++++%7D%5Cn++++++++++++++++++++++++...+on+BundleProduct+%7B%5Cn++++++++++++++++++++++++++++sku%5Cn++++++++++++++++++++++++++++items+%7B%5Cn++++++++++++++++++++++++++++++++options+%7B%5Cn++++++++++++++++++++++++++++++++++++product+%7B%5Cn++++++++++++++++++++++++++++++++++++++++sku%5Cn++++++++++++++++++++++++++++++++++++++++salable_quantity%5Cn++++++++++++++++++++++++++++++++++++++++quantity%5Cn++++++++++++++++++++++++++++++++++++%7D%5Cn++++++++++++++++++++++++++++++++%7D%5Cn++++++++++++++++++++++++++++%7D%5Cn++++++++++++++++++++++++%7D%5Cn++++++++++++++++++++%7D%5Cn++++++++++++++++%22%7D%7D,%7B%7D]'

            current_proxy = '2c6ea6e6d8c14216a62781b8f850cd5b'

            proxy_host = "api.zyte.com"
            proxy_port = "8011"
            proxy_auth = f"{current_proxy}:"

            proxy_url = f"https://{proxy_auth}@{proxy_host}:{proxy_port}"

            meta = {
                # "proxy": "http://21ed11ef5c872bc7727680a52233027db4578a0e:@api.zenrows.com:8001",
                # "proxy": proxy_url,
                "url": url,
                "Prod_url": url,
                "_id": hash_id,
                "filename": f"{slug}_page.html",
                "page":page,
                "cat": cat,
                "should_be": ["data"]
            }

            yield scrapy.Request(
                url=url,
                headers=headers,
                callback=self.process_document,
                dont_filter=True,
                meta=meta,
            )
    def process_document(self, response):
        meta = response.meta
        cat_id = meta.get("cat")
        page = meta.get("page", 1)
        doc_id = meta.get("_id")

        data = json.loads(response.body)
        products = data.get('data', {}).get('products', {}).get('items', [])



        for main in products:
            product_id = main.get('id')
            parent_id = main.get('sku')
            name = main.get('custom_productname')
            key = main.get('url_key')
            price = main.get('price_range').get('minimum_price').get('final_price').get('value')
            original_price = float(price) if price else 0.0

            product_url = f"https://www.mydin.my/product/{key}"


            response_main = (
                f'https://myapi.mydin.my/magento/productDetails?body=[{{"filter":{{"url_key":{{"eq":"{key}"}}}}}},'
                '{"productDetails":"product-details-custom-query","metadata":{"fields":"items{name quantity media_gallery{url} }"}}]'
            )

            yield scrapy.Request(
                url=response_main,
                cookies=cookies,
                headers=headers,
                callback=self.parse_detail,
                meta={
                    "original_price": original_price,
                    "product_id": product_id,
                    "parent_id": parent_id,
                    "product_url": product_url,
                    # "breadcrumb": breadcrumb,
                    "cat": cat_id,
                    "doc_id": doc_id,
                    "filename": f"PDP_{key}_page.html",
                    "should_be": ["data"]
                }
            )

        # --- PAGINATION ---
        next_page = page + 1
        if len(products) == 48:
            next_query_body = [
                {
                    "filter": {
                        "category_id": {"eq": cat_id}
                    },
                    "pageSize": 48,
                    "currentPage": next_page,
                    "sort": {"position": "ASC"}
                },
                {
                    "products": "products-custom-query",
                    "metadata": {
                        "fields": "items{id sku name custom_productname url_key price_range{minimum_price{final_price{value}}}}"
                    }
                },
                {}
            ]
            encoded_next_body = urllib.parse.quote(json.dumps(next_query_body))
            next_product_url = f"https://myapi.mydin.my/magento/products?body={encoded_next_body}"

            yield scrapy.Request(
                url=next_product_url,
                callback=self.process_document,
                cookies=cookies,
                headers=headers,
                meta={"cat": cat_id, "page": next_page, "doc_id": doc_id,"filename": f"PDP_{key}_{next_page}_page.html",
                    "should_be": ["data"]}
            )

    def parse_detail(self, response):
        meta = response.meta
        prod_url = meta.get('product_url')
        cat = meta.get('cat')
        doc_id = meta.get('doc_id')
        data = json.loads(response.text)
        products = data.get("data", {}).get("products", {}).get('items', [])

        # data.products.items[0].name
        for item in products:
            main_name = item.get('name')
            quantity = item.get('quantity')
            if quantity == 0:
                is_available = False
            else:
                is_available = True
            media_gallery = item.get('media_gallery', [])
            image_urls = []
            for image in media_gallery:
                url = image.get('url')
                if url:
                    image_urls.append(url)
            joined_urls = '|'.join(image_urls)
            breadcrumb = f"All Product > {main_name}"
            pack_size = self.extract_size(main_name)
            product_hash = self.generate_hash_id(prod_url, self.retailer, self.region)

            if meta.get("original_price") == 0:
                self.product_table.update_one(
                    {'_id': doc_id},{"$set":{"Status": 'Not Found'}} )
                Rprint("Price Not Found...")

            pdp_item = {"_id": product_hash,"Name": main_name, "Promo_Type": "", "Price": meta.get("original_price"), "per_unit_price": "",
                     "WasPrice": "",
                     "Offer_info": "", "Pack_size": pack_size, "Barcode": "",
                     "Images": joined_urls,
                     "ProductURL": prod_url, "is_available": is_available,
                     "Status": "Done", "ParentCode": meta.get("parent_id"), "ProductCode": meta.get("product_id"),

                     "Category_Hierarchy": breadcrumb, "Brand": "", "RRP": meta.get("original_price")}
            try:
                self.save_product(pdp_item)
                print(f"✓ Successfully inserted {prod_url}")
                if doc_id:
                    self.category_input.update_one(
                        {"_id": doc_id},
                        {"$set": {"Status": "Done"}}
                    )
            except Exception as e:
                print(e)



    def close(self, reason):
        # import subprocess
        # cmd = [
        #     "python",
        #     "upload_to_s3_direct.py",
        #     "--domain", "mydin.my"
        # ]
        # subprocess.run(cmd, cwd=r"E:\pricemate_service")
        self.mongo_client.close()

if __name__ == '__main__':
    from scrapy.cmdline import execute
    execute('scrapy crawl mydin_pdp -a retailer=mydin-my -a region=my -a Type=eshop -a RetailerCode=mydin_my'.split())