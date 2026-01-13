import json

import scrapy
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from pricemate.spiders.base_spider import PricemateBaseSpider

headers = {
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8',
    'Connection': 'keep-alive',
    'Content-Type': 'application/json;charset=UTF-8',
    'Origin': 'https://www.discountdrugstores.com.au',
    'Referer': 'https://www.discountdrugstores.com.au/',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'cross-site',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest',
    'sec-ch-ua': '"Google Chrome";v="141", "Not?A_Brand";v="8", "Chromium";v="141"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
}

class DiscountPlSpider(PricemateBaseSpider):
    name = "discount_pl"

    def __init__(self, retailer, region, *args, **kwargs):
        super().__init__(retailer=retailer, region=region, *args, **kwargs)

    def start_requests(self):
        payload = {
            'session_id': '6Ywxxl4gzGypTO0xmrjhFmJItrcjI5HiraitTRPo',
            'version': '2',
            'source': 'DDSPharmacyWebsite',
            'sort_by': '',
            'optimize': 1,
            'o_page': 0,
            'o_per_page': 100,  # fetch more per request
            'category_id': '138',
            'business_id': '2',
        }

        docs = self.category_input.find({
            "retailer": self.retailer,
            "region": self.region,
            "Status": "Pending"
        })
        for doc in docs:
            url = doc["url"]
            hash_id = doc.get("_id")
            slug = url.split("/")[-2].split("/")[0]
            meta = {
                "url": url,
                "_id": hash_id,
                "slug":slug,
                "payload": payload,
                "page": 1,
                "filename": f"{slug}_page.html",
                "should_be": ["items"]
            }
            yield scrapy.Request(
                url = "https://app.medmate.com.au/connect/api/get_products_list",
                method="POST",
                headers=headers,
                body=json.dumps(payload),
                callback=self.parse_pl,
                meta=meta,
                dont_filter=True
            )

    def parse_pl(self, response):
        meta = response.meta
        doc_id = meta.get("_id")
        slug = meta.get("slug")
        payload = meta.get("payload")
        cate_url = meta.get("url")
        page = int(meta.get("page", 0))

        try:
            data = json.loads(response.text)

        except Exception as e:
            self.logger.error(f"❌ Failed to parse JSON (page {page}): {e}")
            return

        # --- Recursive extraction (works for nested data) ---


        stack = [data]
        count = 0

        while stack:
            node = stack.pop()
            if isinstance(node, list):
                stack.extend(node)
            elif isinstance(node, dict):
                node_slug = node.get("slug")
                node_drugcode = node.get("drugcode")
                if node_slug and node_drugcode:
                    pdp_url = f"https://www.discountdrugstores.com.au/shop/product/{node_slug}/?id={node_drugcode.lower()}"
                    product_hash = self.generate_hash_id(pdp_url, self.retailer, self.region)

                    item = {
                        "_id": product_hash,
                        "ProductURL": pdp_url,
                        # "slug": node_slug,
                        # "drugcode": node_drugcode,
                        "Status": "Pending",
                        "retailer": self.retailer,
                        "region": self.region,
                    }
                    self.save_product(item)
                    count += 1
                    print(f"✅ Inserted -> {pdp_url}")
                stack.extend(node.values())

        print(f"✅ Page {page}: {count} products saved")

        # Stop pagination if no more products found
        if count == 0:
            print(f"🚫 No products found on page {page} — stopping pagination.")
            self.category_input.update_one({"_id": doc_id}, {"$set": {"Status": "Done"}})
            print("✅ Category marked Done.")
            return

        # --- Next page (POST pagination) ---
        next_page = page + 1
        payload["o_page"] = next_page

        next_meta = {
            "_id": doc_id,
            "url": meta["url"],
            "slug": slug,
            "payload": payload,
            "page": next_page,
            "filename": f"{slug}_page{next_page}.json",
            "should_be": ["items"]
        }

        print(f"➡️ Requesting next page {next_page}")
        yield scrapy.Request(
            url="https://app.medmate.com.au/connect/api/get_products_list",
            method="POST",
            headers=headers,
            body=json.dumps(payload),
            callback=self.parse_pl,
            meta=next_meta,
            dont_filter=True,
        )
    def close(self, reason):
        import subprocess

        cmd = [
            "python",
            "upload_to_s3_direct.py",
            "--domain", "discountdrugstores.com"
        ]
        subprocess.run(cmd, cwd=r"E:\pricemate_service")
        self.mongo_client.close()

if __name__ == '__main__':
    from scrapy.cmdline import execute
    execute("scrapy crawl discount_pl -a retailer=discount_drug-au -a region=au -a Type=eshop -a RetailerCode=discount_drug_au".split())