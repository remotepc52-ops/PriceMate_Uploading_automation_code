import re
import scrapy
from pricemate.spiders.bs_spider import PricemateBaseSpider


headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'en-US,en;q=0.9',
    'if-none-match': 'W/"98a-gEb34o7iiP7PREe0dP+38O0t5V4"',
    'origin': 'https://shop.tiptop.co.id',
    'priority': 'u=1, i',
    'referer': 'https://shop.tiptop.co.id/',
    'sec-ch-ua': '"Not;A=Brand";v="99", "Google Chrome";v="139", "Chromium";v="139"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36',
    'x-api-key': '29ea3dcf-67c3-45f6-b5c4-d2628f7e09fa',
    'x-requested-with': 'XMLHttpRequest',
}

class TiptopPdpSpider(PricemateBaseSpider):
    name = "tiptop_pdp"


    def __init__(self, retailer, region, *args, **kwargs):
        super().__init__(retailer=retailer, region=region, *args, **kwargs)

    def start_requests(self):
        docs = self.product_url.find({
            "retailer": self.retailer,
            "region": self.region,
            "Status": "Pending"
        })

        for doc in docs:
            url = doc["ProductURL"]
            hash_id = doc.get("_id")
            match = re.search(r"[?&]key=([a-f0-9]+)", url)
            key = match.group(1)

            api_url = f'https://api.tiptop.co.id/api/web//product/{key}?outletId=63bcfc340bcec42a8f284bfd&userId='

            meta = {
                "url": api_url,
                "Prod_url":url,
                "_id": hash_id,
                "key": key,
                "filename": f"{key}_page.html",
                "should_be": ["data"]
            }

            yield scrapy.Request(
                url=api_url,
                headers=headers,
                callback=self.parse_pdp,
                meta=meta,
            )

    def parse_pdp(self, response):
        meta = response.meta
        key = meta.get("key")
        prod_url = meta.get("Prod_url")
        filename = meta.get("filename")
        doc_id = meta.get('_id')

        try:
            json_data = response.json()

            if not isinstance(json_data, dict) or "data" not in json_data:
                self.logger.error(f"Unexpected response format at {response.url}: {json_data}")
                return

            data = json_data["data"]

            name = data.get("name")
            parent_id = data.get("init_sku")
            cate_name = data.get("category_id", {}).get("name")
            sub_cate = data.get("sub_category_id", {}).get("name")
            bread = f"{cate_name}>{sub_cate}>{name}"

            for stock in data.get("info_product", {}).get("pricing_stock", []):
                pack_size = stock.get("name")
                img = stock.get("image")

                outlets = stock.get("pricing_stock_outlet", [])
                is_avai = not (not outlets or all(o.get("stock", 0) == 0 for o in outlets))

                for outlet in outlets:
                    prod_id = outlet.get("sku")
                    barcode = outlet.get("barcode")

                    special_price = outlet.get("special_price")
                    price = outlet.get("price")

                    if special_price is not None:
                        mrp = special_price
                        was_price = price
                        rrp = price
                    else:
                        mrp = price
                        rrp = price
                        was_price = ""

                    product_hash = self.generate_hash_id(prod_id, self.retailer, self.region)

                    item = {
                        "_id": product_hash,
                        "Name": name,
                        "Promo_Type": '',
                        "Price": mrp,
                        "per_unit_price": "",
                        "WasPrice": was_price,
                        "Offer_info": "",
                        "Pack_size": pack_size,
                        "Barcode": barcode,
                        "is_available": is_avai,
                        "Images": img,
                        "ProductURL": prod_url,
                        "Status": "Done",
                        "ParentCode": parent_id,
                        "ProductCode": prod_id,
                        "retailer_name": "tiptop_id",
                        "Category_Hierarchy": bread,
                        "Brand": "",
                        "RRP": rrp,
                        "region":"id",
                    }

                    try:
                        item_id = item.get("_id")
                        update_fields = {k: v for k, v in item.items() if k != "_id"}

                        self.product_table.update_one(
                            {"_id": item_id},
                            {"$set": update_fields},
                            upsert=True
                        )
                        print(f"✓ Inserted {name} - {pack_size} ({prod_id})")
                        self.product_url.update_one(
                            {"_id": doc_id},
                            {"$set": {"Status": "Done"}}
                        )
                    except Exception as e:
                        print(e)

        except Exception as e:
            self.logger.error(f"Failed to parse JSON for {response.url}: {e}")
            return

    def close(self, reason):
        import subprocess
        cmd = [
            "python",
            "upload_to_s3_direct.py",
            "--domain", "tiptop.co.id"
        ]
        subprocess.run(cmd, cwd=r"E:\pricemate_service")
        self.mongo_client.close()


if __name__ == '__main__':
    from scrapy.cmdline import execute
    execute("scrapy crawl tiptop_pdp -a retailer=tiptop-id -a region=id -a Type=eshop -a RetailerCode=tiptop_id".split())