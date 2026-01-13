import json
import time
from lxml import etree
from urllib.parse import quote
import scrapy
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from pricemate.spiders.base_spider import PricemateBaseSpider
cookies = {
    'PHPSESSID': 'ishm8i5r6ln97b0qnsh2kdpc3i',
    '_lscache_vary': '769f74cc97c99ba0a5d9d41eab626853',
    'sbjs_migrations': '1418474375998%3D1',
    'sbjs_current_add': 'fd%3D2025-10-17%2007%3A58%3A55%7C%7C%7Cep%3Dhttps%3A%2F%2Fpetloverscentre.com.ph%2F%7C%7C%7Crf%3Dhttps%3A%2F%2Fpetloverscentre.com.ph%2F',
    'sbjs_first_add': 'fd%3D2025-10-17%2007%3A58%3A55%7C%7C%7Cep%3Dhttps%3A%2F%2Fpetloverscentre.com.ph%2F%7C%7C%7Crf%3Dhttps%3A%2F%2Fpetloverscentre.com.ph%2F',
    'sbjs_current': 'typ%3Dtypein%7C%7C%7Csrc%3D%28direct%29%7C%7C%7Cmdm%3D%28none%29%7C%7C%7Ccmp%3D%28none%29%7C%7C%7Ccnt%3D%28none%29%7C%7C%7Ctrm%3D%28none%29%7C%7C%7Cid%3D%28none%29%7C%7C%7Cplt%3D%28none%29%7C%7C%7Cfmt%3D%28none%29%7C%7C%7Ctct%3D%28none%29',
    'sbjs_first': 'typ%3Dtypein%7C%7C%7Csrc%3D%28direct%29%7C%7C%7Cmdm%3D%28none%29%7C%7C%7Ccmp%3D%28none%29%7C%7C%7Ccnt%3D%28none%29%7C%7C%7Ctrm%3D%28none%29%7C%7C%7Cid%3D%28none%29%7C%7C%7Cplt%3D%28none%29%7C%7C%7Cfmt%3D%28none%29%7C%7C%7Ctct%3D%28none%29',
    'sbjs_udata': 'vst%3D2%7C%7C%7Cuip%3D%28none%29%7C%7C%7Cuag%3DMozilla%2F5.0%20%28Windows%20NT%2010.0%3B%20Win64%3B%20x64%29%20AppleWebKit%2F537.36%20%28KHTML%2C%20like%20Gecko%29%20Chrome%2F141.0.0.0%20Safari%2F537.36',
}

headers = {
    'accept': '*/*',
    'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
    'priority': 'u=1, i',
    'referer': 'https://petloverscentre.com.ph/product-category/harness/',
    'sec-ch-ua': '"Google Chrome";v="141", "Not?A_Brand";v="8", "Chromium";v="141"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36',
    'x-requested-with': 'XMLHttpRequest',
    # 'cookie': 'PHPSESSID=ishm8i5r6ln97b0qnsh2kdpc3i; _lscache_vary=769f74cc97c99ba0a5d9d41eab626853; sbjs_migrations=1418474375998%3D1; sbjs_current_add=fd%3D2025-10-17%2007%3A58%3A55%7C%7C%7Cep%3Dhttps%3A%2F%2Fpetloverscentre.com.ph%2F%7C%7C%7Crf%3Dhttps%3A%2F%2Fpetloverscentre.com.ph%2F; sbjs_first_add=fd%3D2025-10-17%2007%3A58%3A55%7C%7C%7Cep%3Dhttps%3A%2F%2Fpetloverscentre.com.ph%2F%7C%7C%7Crf%3Dhttps%3A%2F%2Fpetloverscentre.com.ph%2F; sbjs_current=typ%3Dtypein%7C%7C%7Csrc%3D%28direct%29%7C%7C%7Cmdm%3D%28none%29%7C%7C%7Ccmp%3D%28none%29%7C%7C%7Ccnt%3D%28none%29%7C%7C%7Ctrm%3D%28none%29%7C%7C%7Cid%3D%28none%29%7C%7C%7Cplt%3D%28none%29%7C%7C%7Cfmt%3D%28none%29%7C%7C%7Ctct%3D%28none%29; sbjs_first=typ%3Dtypein%7C%7C%7Csrc%3D%28direct%29%7C%7C%7Cmdm%3D%28none%29%7C%7C%7Ccmp%3D%28none%29%7C%7C%7Ccnt%3D%28none%29%7C%7C%7Ctrm%3D%28none%29%7C%7C%7Cid%3D%28none%29%7C%7C%7Cplt%3D%28none%29%7C%7C%7Cfmt%3D%28none%29%7C%7C%7Ctct%3D%28none%29; sbjs_udata=vst%3D2%7C%7C%7Cuip%3D%28none%29%7C%7C%7Cuag%3DMozilla%2F5.0%20%28Windows%20NT%2010.0%3B%20Win64%3B%20x64%29%20AppleWebKit%2F537.36%20%28KHTML%2C%20like%20Gecko%29%20Chrome%2F141.0.0.0%20Safari%2F537.36',
}

class PetPlSpider(PricemateBaseSpider):
    name = "pets_pl"

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
            slug = url.split("/")[-2]
            meta = {
                "url": url,
                "_id": hash_id,
                "slug":slug,
                "page": 1,
                "filename": f"{slug}_page.html",
                "should_be": ["products"]
            }
            yield from self.make_request(meta)

    def make_request(self, meta):
        params = {
            'post_id': '5684',
            'model_id': '1b46b0f',
            'product-page': str(meta["page"]),
            'raven_archive_query': json.dumps({
                "taxonomy": "product_cat",
                "term": meta["slug"]
            }),
            'action': 'raven_products_query',
        }

        query = "&".join([f"{k}={quote(str(v))}" for k, v in params.items()])
        api_url = f"https://petloverscentre.com.ph/wp-admin/admin-ajax.php?{query}"

        self.logger.info(f"📦 Fetching {meta['slug']} page {meta['page']}")

        yield scrapy.Request(
            url=api_url,
            headers=headers,
            cookies=cookies,
            callback=self.parse_product_list,
            meta=meta,
            dont_filter=True
        )

    def parse_product_list(self, response):
        meta = response.meta
        slug = meta.get("slug")
        doc_id = meta.get("_id")

        if not response.text.strip():
            self.logger.warning(f"⚠️ Empty response for {slug} page {meta['page']}")
            return

        try:
            data = json.loads(response.text)
        except json.JSONDecodeError:
            self.logger.error(f"❌ Invalid JSON for {slug} page {meta['page']}")
            self.logger.error(response.text[:400])
            return

        html_content = data.get("data", {}).get("products")
        if not isinstance(html_content, str) or not html_content.strip():
            self.logger.warning(f"⚠️ No products found for {slug} page {meta['page']}")
            self.category_input.update_one({"_id": doc_id}, {"$set": {"Status": "Done"}})
            return

        query_info = data.get("data", {}).get("query_results", {})
        total_pages = query_info.get("total_pages", 1)
        current_page = query_info.get("current_page", 1)

        tree = etree.HTML(html_content)
        links = tree.xpath('//a[@class="woocommerce-LoopProduct-link woocommerce-loop-product__link"]/@href')

        for link in links:
            product_url = link.strip()
            product_hash = self.generate_hash_id(product_url, self.retailer, self.region)
            item = {
                "_id": product_hash,
                "ProductURL": product_url,
                "Status": "Pending",
                "retailer": self.retailer,
                "region": self.region,
            }
            self.save_product(item)

        self.logger.info(f"✅ {slug} page {current_page}/{total_pages} — {len(links)} products")

        if current_page < total_pages:
            next_page = current_page + 1
            next_meta = meta.copy()
            next_meta["page"] = next_page
            next_meta["filename"] = f"{slug}_{next_page}page.html"
            yield from self.make_request(next_meta)


        self.category_input.update_one({"_id": doc_id}, {"$set": {"Status": "Done"}})


    def close(self, reason):
        self.mongo_client.close()

if __name__ == '__main__':
    from scrapy.cmdline import execute
    execute(
        "scrapy crawl pets_pl -a retailer=petloverscentre-ph -a region=ph -a Type=eshop -a RetailerCode=petloverscentre_ph".split())
