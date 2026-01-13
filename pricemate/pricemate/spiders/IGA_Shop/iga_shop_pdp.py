import json
import re
from typing import Iterable, Any
from lxml import etree
import scrapy
import time
from urllib.parse import urljoin, quote
import os, sys

from scrapy.http import HtmlResponse

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from pricemate.spiders.base_spider import PricemateBaseSpider

# cookies = {
#     '_gcl_au': '1.1.747101471.1755681623',
#     '_fbp': 'fb.2.1755681625824.678799404594309228',
#     'ajs_anonymous_id': '89abafcc-5c7d-4514-9d49-8cf482dc86ab',
#     '_clck': 'eyisdv%5E2%5Efzl%5E0%5E2058',
#     '_gid': 'GA1.3.686520719.1758687172',
#     'iga-shop.retailerStoreId': '19071',
#     'iga-shop.shoppingMode': 'Planning',
#     'iga-shop.selectionType': 'undefined',
#     'ab.storage.deviceId.62bddbf0-eb6f-4a46-bde2-f29d41add7ca': '%7B%22g%22%3A%221db6927a-90af-803e-254a-79508a9e007e%22%2C%22c%22%3A1756209446921%2C%22l%22%3A1758708786471%7D',
#     '_gat_gtag_UA_184622586_1': '1',
#     '_dc_gtm_UA-184622586-1': '1',
#     '_ga_CWDKGZHRE0': 'GS2.1.s1758708786$o22$g1$t1758708931$j6$l0$h470271453',
#     '_ga': 'GA1.3.1754079848.1755681623',
#     '_uetsid': 'bd1ba7d098fc11f082b9519797eb5665',
#     '_uetvid': 'e7dde4207da611f0b92b8fcb6e702406',
#     '_clsk': '1t1emqz%5E1758708932396%5E5%5E1%5Ei.clarity.ms%2Fcollect',
#     'ab.storage.sessionId.62bddbf0-eb6f-4a46-bde2-f29d41add7ca': '%7B%22g%22%3A%2206054738-7bd2-be3e-4dd1-b46065060ca6%22%2C%22e%22%3A1758710733163%2C%22c%22%3A1758708786464%2C%22l%22%3A1758708933163%7D',
# }

headers = {
    'accept': '*/*',
    'accept-language': 'en-US,en;q=0.9',
    'priority': 'u=1, i',
    'referer': 'https://www.igashop.com.au/categories/Fruit_and_Vegetable/Fruit/1',
    'sec-ch-ua': '"Chromium";v="140", "Not=A?Brand";v="24", "Google Chrome";v="140"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'Host': 'www.igashop.com.au',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36',
    'x-shopping-mode': '33333333-3333-3333-3333-333333333333',
    'cookies':'__Host-next-auth.csrf-token=38a15933127e72be77d848f427c49f73915fec239c51247c6083ca4a43bcd4bd%7C1947995151322d16d531d5e0f4feb49e9b9e0d726c0cc69dab16b35621bf125f; __Secure-next-auth.callback-url=https%3A%2F%2Fwww.igashop.com.au; iga-shop.retailerStoreId=19071; iga-shop.shoppingMode=Planning; iga-shop.selectionType=undefined; _gcl_au=1.1.134727864.1758711066; _gid=GA1.3.1085318761.1758711066; _gat_gtag_UA_184622586_1=1; _dc_gtm_UA-184622586-1=1; _clck=1ebc4u9%5E2%5Efzl%5E0%5E2093; _fbp=fb.2.1758711065876.42054944440054035; ajs_anonymous_id=0867df9d-6df2-48a5-b390-4704ed9c8e88; _clsk=jqzibp%5E1758711067486%5E1%5E1%5Ei.clarity.ms%2Fcollect; _ga_CWDKGZHRE0=GS2.1.s1758711065$o1$g1$t1758711079$j46$l0$h353778699; _ga=GA1.3.2126365044.1758711066; _uetsid=5ed24c50993411f0b4268b14e1077398; _uetvid=5ed26320993411f0b7fe274ded7c488b',
}

class IgaPdpSpider(PricemateBaseSpider):
    name = "iga_pdp"
    custom_settings = {
            "HTTPERROR_ALLOWED_CODES": [404]
        }


    def __init__(self, retailer, region, *args, **kwargs):
        super().__init__(retailer=retailer, region=region, *args, **kwargs)

    def start_requests(self):

        docs = self.category_input.find({
            "retailer": self.retailer,
            "region": self.region,
            "Status": "Pending"
        })
        for doc in docs:
            url = doc["url"]
            hash_id = doc.get("_id")

            parts = url.strip("/").split("/")
            if len(parts) >= 3:
                parent_slug = parts[-3]  # Pantry
                product_slug = parts[-2].replace("-", "_")  # Breakfast-Foods

            meta = {
                "url": url,
                "_id": hash_id,
                "product_slug":product_slug,
                "parent_slug": parent_slug,
                "filename": f"PDP_{product_slug}_page.html",
                "should_be": ["items"],
                "handle_httpstatus_list": [404],
                "skip": 0,
                "fallback_used": False
            }
            yield scrapy.Request(
                url = f'https://www.igashop.com.au/api/storefront/stores/19071/categories/{product_slug}/search?sessionId=ff734231-32e4-489d-a5a9-9f0aff5fb7a8&take=20',
                # cookies=cookies,
                headers=headers,
                callback=self.get_pdp,
                meta=meta
            )

    def get_pdp(self, response):
        meta = response.meta
        doc_id = meta.get("_id")
        product_slug = meta.get("product_slug")
        parent_slug = meta.get("parent_slug")

        try:
            json_data = response.json()
        except Exception as e:
            self.logger.error(f"Failed to parse JSON for {response.url}: {e}")
            return

        total = json_data.get("total", 0)
        if total == 0 and not meta.get("fallback_used", False):
            if parent_slug:
                self.logger.info(f"No products for {product_slug}, retrying with parent {parent_slug}")
                api_url = f'https://www.igashop.com.au/api/storefront/stores/19071/categories/{parent_slug}/search?sessionId=ff734231-32e4-489d-a5a9-9f0aff5fb7a8&take=20'
                yield scrapy.Request(
                    url=api_url,
                    headers=headers,
                    # cookies=cookies,
                    callback=self.get_pdp,
                    meta={**meta, "url": api_url, "fallback_used": True},
                    dont_filter=True
                )
            return

        for data in json_data.get("items", []):
            prod_id = data.get('productId')
            name = data.get('name')
            brand = data.get('brand')
            offer = data.get('priceLabel') or ""
            price = data.get('priceNumeric')
            per_unit_price = data.get('pricePerUnit')
            was_price = data.get('wasPriceNumeric')
            rrp = was_price if was_price else price

            size = data.get("unitOfSize", {}).get("size")
            label = data.get("unitOfSize", {}).get("label")
            pack_size = f"{size} {label}".strip() if size and label else ""

            bread = ""
            if data.get("defaultCategory"):
                bread = data["defaultCategory"][0].get("categoryBreadcrumb", "")
                bread = bread.replace("/", ">")

            stock = data.get('available')
            barcode = data.get('barcode')
            if barcode == "notfound":
                barcode = ""
            img = data.get('image', {}).get('default')
            prod_url = f'https://www.igashop.com.au/product/{quote(name.replace(" ", "-"))}-{prod_id}'
            product_hash = self.generate_hash_id(prod_url, self.retailer, self.region)

            item = {
                "_id": product_hash,
                "Name": name,
                "Promo_Type": '',
                "Price": price,
                "per_unit_price": per_unit_price,
                "WasPrice": was_price,
                "Offer_info": offer,
                "Pack_size": pack_size,
                "Barcode": barcode,
                "is_available": stock,
                "Images": img,
                "ProductURL": prod_url,
                "Status": "Done",
                "ParentCode": prod_id,
                "ProductCode": prod_id,
                "retailer_name": "igashop-au",
                "Category_Hierarchy": bread,
                "Brand": brand,
                "RRP": rrp,
            }
            try:
                self.save_product(item)
                print(f"✓ Successfully inserted {prod_url}")
                if doc_id:
                    self.category_input.update_one(
                        {"_id": doc_id},
                        {"$set": {"Status": "Done"}}
                    )
            except Exception as e:
                print(e)

        # Handle pagination
        count = json_data.get("count", 0)
        skip = meta.get("skip", 0)

        # If we got 20 items, there might be a next page
        if count == 20:
            next_skip = skip + 20
            next_url = re.sub(r"skip=\d+", f"skip={next_skip}", response.url)
            if "skip=" not in next_url:
                sep = "&" if "?" in next_url else "?"
                next_url = f"{next_url}{sep}skip={next_skip}"
            meta = {
                "product_slug": product_slug,
                "parent_slug": parent_slug,
                "filename": f"{product_slug}_{next_skip}_page.html",
                "should_be": ["items"],
                "handle_httpstatus_list": [404],
                "skip": next_skip,
                "fallback_used": False
            }
            yield scrapy.Request(
                url=next_url,
                headers=headers,
                callback=self.get_pdp,
                meta=meta,
            )




    def close(self, reason):

        import subprocess
        cmd = [
            "python",
            "upload_to_s3_direct.py",
            "--domain", "igashop.com"
        ]
        subprocess.run(cmd, cwd=r"E:\pricemate_service")

        self.mongo_client.close()

if __name__ == '__main__':
    from scrapy.cmdline import execute
    execute("scrapy crawl iga_pdp -a retailer=iga-au -a region=au -a Type=eshop -a RetailerCode=iga_au".split())
