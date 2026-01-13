import json
import re
import time
from lxml import etree
from urllib.parse import quote
import scrapy
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from pricemate.spiders.bs_spider import PricemateBaseSpider

cookies = {
    '__Host-authjs.csrf-token': 'dd755a40bfc15904486e46871fdc1f98986acb530599b8b89a44ae2a40d1a7d8%7Caa782220112e9316cc8e223ea3ba1de33b52554e3140b6fb825e700804f47a22',
    '__Secure-next-auth.callback-url': 'https%3A%2F%2Fwww.metromart.com',
    'token': 'eyJhbGciOiJIUzI1NiJ9.eyJpZCI6MTU0NDM4NDcsInR5cGUiOiJndWVzdCIsInNob3AtaWQiOjIxMjQsImlhdCI6MTc2MzYyMzc1NH0.oVwYJlDGmzwqC4gkkgrGhiObs_GxDdfqHSWnKWWo1S0',
    'addressObject': '%7B%22kind%22%3A%22home%22%2C%22label%22%3A%22Novaliches%20Proper%22%2C%22address1%22%3A%22Quezon%20City%2C%20Metro%20Manila%2C%20Philippines%22%2C%22latitude%22%3A%2214.720093%22%2C%22longitude%22%3A%22121.03781%22%2C%22areaId%22%3A124%2C%22userId%22%3A15443847%2C%22id%22%3A2670252%2C%22address2%22%3Anull%2C%22city%22%3A%22Quezon%20City%22%2C%22landmark%22%3Anull%2C%22postCode%22%3Anull%7D',
    'areaId': '124',
    'hasUserAddress': 'true',
    'shopId': '2110',
    'shopSlug': 'sm-hypermarket-north-edsa',
}

headers = {
    'accept': 'text/x-component',
    'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
    'baggage': 'sentry-environment=vercel-production,sentry-release=9f9b3653118c77a7cf726703b187f16c709b86c7,sentry-public_key=3e10e277c451ec42dec7fe16c0175b3f,sentry-trace_id=47a0eda228b84fd9a88112e904321c22,sentry-sampled=false,sentry-sample_rand=0.14269384233665605,sentry-sample_rate=0.02',
    'content-type': 'text/plain;charset=UTF-8',
    'next-action': '962196e6b9607b28f29e729546253e0725c3e87d',
    'next-router-state-tree': '%5B%22%22%2C%7B%22children%22%3A%5B%22shops%22%2C%7B%22children%22%3A%5B%5B%22slug%22%2C%22sm-hypermarket-north-edsa%22%2C%22d%22%5D%2C%7B%22children%22%3A%5B%22departments%22%2C%7B%22children%22%3A%5B%5B%22department-id%22%2C%2243777%22%2C%22d%22%5D%2C%7B%22children%22%3A%5B%22__PAGE__%22%2C%7B%7D%2C%22%2Fshops%2Fsm-hypermarket-north-edsa%2Fdepartments%2F43777%22%2C%22refresh%22%5D%7D%2Cnull%2Cnull%2Ctrue%5D%7D%2Cnull%2Cnull%5D%7D%2Cnull%2Cnull%5D%7D%2Cnull%2Cnull%5D%7D%2Cnull%2Cnull%2Ctrue%5D',
    'origin': 'https://www.metromart.com',
    'priority': 'u=1, i',
    'referer': 'https://www.metromart.com/shops/sm-hypermarket-north-edsa/departments/43777',
    'sec-ch-ua': '"Chromium";v="142", "Google Chrome";v="142", "Not_A Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'sentry-trace': '47a0eda228b84fd9a88112e904321c22-91015cc08c440b98-0',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36',
    'x-deployment-id': 'dpl_HUA5TzdbAUs9pVRDa9UzJ3Z8dRJ7',
    # 'cookie': '__Host-authjs.csrf-token=dd755a40bfc15904486e46871fdc1f98986acb530599b8b89a44ae2a40d1a7d8%7Caa782220112e9316cc8e223ea3ba1de33b52554e3140b6fb825e700804f47a22; __Secure-next-auth.callback-url=https%3A%2F%2Fwww.metromart.com; token=eyJhbGciOiJIUzI1NiJ9.eyJpZCI6MTU0NDM4NDcsInR5cGUiOiJndWVzdCIsInNob3AtaWQiOjIxMjQsImlhdCI6MTc2MzYyMzc1NH0.oVwYJlDGmzwqC4gkkgrGhiObs_GxDdfqHSWnKWWo1S0; addressObject=%7B%22kind%22%3A%22home%22%2C%22label%22%3A%22Novaliches%20Proper%22%2C%22address1%22%3A%22Quezon%20City%2C%20Metro%20Manila%2C%20Philippines%22%2C%22latitude%22%3A%2214.720093%22%2C%22longitude%22%3A%22121.03781%22%2C%22areaId%22%3A124%2C%22userId%22%3A15443847%2C%22id%22%3A2670252%2C%22address2%22%3Anull%2C%22city%22%3A%22Quezon%20City%22%2C%22landmark%22%3Anull%2C%22postCode%22%3Anull%7D; areaId=124; hasUserAddress=true; shopId=2110; shopSlug=sm-hypermarket-north-edsa',
}

data = '[{"page":2,"query":"include=weights,take-y-weight,take-y-products,favorites,fmcg-campaign,fmcg-campaign.fmcg-campaign-vouchers,dhz-campaign-brand,department&fields[products]=alcoholic,amount-in-cents,base-amount-in-cents,business-max-items-count,buy-x,buy-x-take-y,bulk,bulk-quantity-threshold,delicate,description,dhz-campaign-brand,dhz-campaign-brand-priority,image-url,image-740x740,max-items-count,name,percent-off,priority,require-legal-age,sari-sari-max-items-count,size,sold-as,status,take-y,weight-metric,weight-multiplier,weighted,weighted-disclaimer,fmcg-campaign,fmcg-campaign.fmcg-campaign-vouchers,department,aisle,shop,buy-x-weight,take-y-products,take-y-weight,weights&fields[fmcg-campaigns]=kind,status,fmcg-campaign-vouchers&fields[weights]=value,default&filter[aisle.id]=174795,174794,181861,181862,181863,181864&filter[sub-aisle.id]=&filter[brand.id]=&fields[fmcg-campaign-vouchers]=discount-in-cents,minimum-spend-in-cents&filter[shop.id]=2110&filter[status]=available&page[size]=30&sort=fmcg-campaign.status=[active],fmcg-campaign.kind=[free-delivery,peso-discount,free-shopping-fee,display-only],-monthly-popular-score,-updated-at","v2":true,"resource":"products"}]'
class SmHyperPlSpider(PricemateBaseSpider):
    name = "sm_hyper_pl"

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
            slug = url.split("/")[-1].split("/")[0]
            dep_id = url.rstrip("/").split("/")[-1]
            current_proxy = '2c6ea6e6d8c14216a62781b8f850cd5b'

            proxy_host = "api.zyte.com"
            proxy_port = "8011"
            proxy_auth = f"{current_proxy}:"

            proxy_url = f"https://{proxy_auth}@{proxy_host}:{proxy_port}"

            meta = {
                'proxy': proxy_url,
                "url": url,
                "_id": hash_id,
                "slug": slug,
                "page": 1,
                "dep_id": dep_id,
                "dont_redirect": True,
                "handle_httpstatus_all": True,
                "http2": True,
                "filename": f"{slug}_page.html",
                "should_be": ["data"]
            }
            yield scrapy.Request(
                url,
                method="POST",
                cookies=cookies,
                headers=headers,
                callback=self.parse_pl,
                body=data,
                meta=meta,
                dont_filter=True
            )

    def parse_pl(self, response):
        meta = response.meta
        cate_url = meta.get("url")
        doc_id = meta.get("_id")
        slug = meta.get("slug")
        dep_id = meta.get("dep_id")
        page = meta.get("page", 1)

        # Extract JSON chunk
        text = response.text
        match = re.search(r'1:\s*(\{[\s\S]*\})', text)

        if not match:
            print("✗ JSON not found in page", page)
            return

        data = json.loads(match.group(1))

        products = data.get("data", [])
        print(f"✓ Page {page} → {len(products)} products")

        # Stop if no more data
        if not products:
            print("✓ Reached last page.")
            return

            # Process products
        for product in products:
            attributes = product.get("attributes", {})
            relationships = product.get("relationships", {})
            links = product.get("links", {})

            name = attributes.get("name")
            mrp = attributes.get("amount-in-cents")
            price = mrp / 100 if mrp else ""
            was_pri = attributes.get("base-amount-in-cents")
            was_price = was_pri / 100 if was_pri else ""
            product_id = product.get("id")
            image = attributes.get("image-url")

            if name:
                parts = name.split()
                if len(parts) < 3:
                    brand = " ".join(parts[:2])  # first 2 words
                else:
                    brand = parts[0]  # first 1 word
            else:
                brand = ""


            status = attributes.get("status")
            if status == "available":
                stock = True
            else:
                stock = False
            # prod_url = attributes.get("prod_url")
            pack_size = attributes.get("size")

            if was_price == mrp or was_price is None:
                rrp = price
                was_price = ""
            else:
                rrp = was_price
            product_hash = self.generate_hash_id(product_id, self.retailer, self.region)
            item = {"_id": product_hash, "Name": name, "Promo_Type": "", "Price": price, "per_unit_price": "",
                    "WasPrice": was_price,
                    "Offer_info": "", "Pack_size": pack_size, "Barcode": "",
                    "Images": image,
                    "ProductURL": "", "is_available": stock,
                    "Status": "Done", "ParentCode": "", "ProductCode": product_id,
                    "retailer_name": "metromart_sm_hypermarket-ph",
                    "Category_Hierarchy": "", "Brand": brand, "RRP": rrp}
            try:
                self.save_product(item)
                print(f"✓ Saved product: {name}")

            except Exception as e:
                print("Error saving product:", e)
            # ---------- PAGINATION REQUEST ----------
        next_page = page + 1

        next_payload = f"""[{{"page":{next_page},"query":"include=weights,take-y-weight,take-y-products,favorites,fmcg-campaign,fmcg-campaign.fmcg-campaign-vouchers,dhz-campaign-brand,department&fields[products]=alcoholic,amount-in-cents,base-amount-in-cents,business-max-items-count,buy-x,buy-x-take-y,bulk,bulk-quantity-threshold,delicate,description,dhz-campaign-brand,dhz-campaign-brand-priority,image-url,image-740x740,max-items-count,name,percent-off,priority,require-legal-age,sari-sari-max-items-count,size,sold-as,status,take-y,weight-metric,weight-multiplier,weighted,weighted-disclaimer,fmcg-campaign,fmcg-campaign.fmcg-campaign-vouchers,department,aisle,shop,buy-x-weight,take-y-products,take-y-weight,weights&fields[fmcg-campaigns]=kind,status,fmcg-campaign-vouchers&fields[weights]=value,default&filter[aisle.id]=174795,174794,181861,181862,181863,181864&filter[sub-aisle.id]=&filter[brand.id]=&fields[fmcg-campaign-vouchers]=discount-in-cents,minimum-spend-in-cents&filter[shop.id]=2110&filter[status]=available&page[size]=30&sort=fmcg-campaign.status=[active],fmcg-campaign.kind=[free-delivery,peso-discount,free-shopping-fee,display-only],-monthly-popular-score,-updated-at","v2":true,"resource":"products"}}]"""

        next_url = f"https://www.metromart.com/shops/sm-hypermarket-north-edsa/departments/{dep_id}"
        print(f"Going to next page = {next_page}...{next_url}✅")
        meta = {

            "slug": slug,
            "page": next_page,
            "dont_redirect": True,
            "handle_httpstatus_all": True,
            "http2": True,
            "filename": f"{slug}_page_{next_page}.html",
            "should_be": ["data"]
        }

        yield scrapy.Request(
            next_url,
            method="POST",
            body=next_payload,
            cookies=cookies,
            headers=headers,
            callback=self.parse_pl,
            meta=meta,
            dont_filter=True
        )

        self.category_input.update_one({"_id": doc_id},{"$set": {"Status": "Done"}})
    def close(self, reason):
        self.mongo_client.close()

if __name__ == '__main__':
    from scrapy.cmdline import execute
    execute("scrapy crawl sm_hyper_pl -a retailer=metromart_sm_hypermarket-ph -a region=ph -a Type=eshop -a RetailerCode=metromart_sm_hypermarket_ph".split())