import scrapy
import os
import sys
import json
from urllib.parse import quote

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from pricemate.spiders.base_spider import PricemateBaseSpider


class PetmrtPlSpider(PricemateBaseSpider):
    name = "pet_pl"

    custom_settings = {
        'RETRY_ENABLED': True,
        'RETRY_TIMES': 3,
        'RETRY_HTTP_CODES': [500, 502, 503, 504, 408, 429],
        'DOWNLOAD_DELAY': 1,
        'RANDOMIZE_DOWNLOAD_DELAY': True,
        'CONCURRENT_REQUESTS': 1,
    }

    def __init__(self, retailer, region, *args, **kwargs):
        super().__init__(retailer=retailer, region=region, *args, **kwargs)
        self.zenrows_api_key = "21ed11ef5c872bc7727680a52233027db4578a0e"

    def get_headers(self, referer=None):
        """Generate headers for each request"""
        headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
            'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
            'cache-control': 'max-age=0',
            'sec-ch-ua': '"Google Chrome";v="143", "Chromium";v="143", "Not A(Brand";v="24"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'none' if not referer else 'same-origin',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36',
        }
        if referer:
            headers['referer'] = referer
        return headers

    def build_zenrows_url(self, target_url, js_render=True):
        """Build ZenRows API URL with parameters"""
        encoded_url = quote(target_url, safe='')
        params = [
            f"apikey={self.zenrows_api_key}",
            f"url={encoded_url}",
        ]
        if js_render:
            params.append("js_render=true")
            params.append("premium_proxy=true")

        return f"https://api.zenrows.com/v1/?{'&'.join(params)}"

    def start_requests(self):
        """Start scraping from pending categories"""
        docs = self.category_input.find({
            "retailer": self.retailer,
            "region": self.region,
            "Status": "Pending"
        })

        for doc in docs:
            url = doc["url"]
            hash_id = doc.get("_id")
            slug = url.split(".vn/")[-1].split("/")[0]

            # Build first page URL
            page_url = f"{url}/page/1"
            zenrows_url = self.build_zenrows_url(page_url)

            meta = {
                "original_url": url,
                "page_url": page_url,
                "_id": hash_id,
                "slug": slug,
                "page": 1,
                "filename": f"{slug}_page.html",
                "should_be": ["rank-math-schema-pro"]
            }

            print(f" Starting scrape for: {url}")

            yield scrapy.Request(
                url=zenrows_url,
                headers=self.get_headers(referer=url),
                callback=self.parse_pl,
                meta=meta,
                dont_filter=True,
                errback=self.handle_error
            )

    def parse_pl(self, response):
        """Parse product listing page"""
        meta = response.meta
        doc_id = meta.get("_id")
        slug = meta.get("slug")
        page = meta.get("page", 1)
        original_url = meta.get("original_url")

        print(f"\n{'=' * 60}")
        print(f" Parsing Page {page} - Status: {response.status}")
        print(f" URL: {meta.get('page_url')}")
        print(f"{'=' * 60}\n")

        # Check if the page returned valid content
        json_text = response.xpath('//script[contains(@class, "rank-math-schema-pro")]/text()').get()

        breadcrumb_string = ""
        products_found = 0

        if json_text:
            try:
                data = json.loads(json_text)
                graph = data.get('@graph', [])

                # 1. Extract Breadcrumb
                for node in graph:
                    if node.get('@type') == 'BreadcrumbList':
                        items = node.get('itemListElement', [])
                        items.sort(key=lambda x: int(x['position']))
                        names = [item['item']['name'] for item in items]
                        breadcrumb_string = " > ".join(names)
                        print(f" Breadcrumb: {breadcrumb_string}")
                        break

                # 2. Extract Products
                for node in graph:
                    if node.get('@type') == 'ItemList':
                        for element in node.get('itemListElement', []):
                            product_data = element.get('item', {})

                            if 'url' in product_data:
                                pdp_url = product_data['url']
                                product_hash = self.generate_hash_id(pdp_url, self.retailer, self.region)

                                item = {
                                    "_id": product_hash,
                                    "ProductURL": pdp_url,
                                    "Category_Hierarchy": breadcrumb_string,
                                    "Status": "Pending",
                                    "retailer": self.retailer,
                                    "region": self.region,
                                }

                                self.save_product(item)
                                products_found += 1
                                print(f"  ✅ Product {products_found}: {pdp_url}")

                print(f"\n Total products found on page {page}: {products_found}\n")

            except json.JSONDecodeError as e:
                print(f" JSON Decode Error on {meta.get('page_url')}: {e}")
            except Exception as e:
                print(f" Error parsing Schema: {e}")
        else:
            print(f"  No JSON Schema found on page {page}")
            print(f"Response length: {len(response.body)} bytes")
            print(f"First 300 chars:\n{response.text[:300]}\n")

        # 3. Handle Pagination
        next_page_href = response.xpath('//a[contains(@class, "next") and contains(@class, "page-number")]/@href').get()

        if next_page_href and products_found > 0:
            next_page_num = page + 1
            next_page_url = response.urljoin(next_page_href)
            zenrows_url = self.build_zenrows_url(next_page_url)

            print(f"➡️  Moving to page {next_page_num}: {next_page_url}\n")

            yield scrapy.Request(
                url=zenrows_url,
                headers=self.get_headers(referer=meta.get('page_url')),
                callback=self.parse_pl,
                meta={
                    "original_url": original_url,
                    "page_url": next_page_url,
                    "_id": doc_id,
                    "slug": slug,
                    "page": next_page_num,
                    "filename": f"{slug}_page_{next_page_num}.html",
                    "should_be": ["rank-math-schema-pro"]
                },
                dont_filter=True,
                errback=self.handle_error
            )
        else:
            if not next_page_href:
                print(" No more pages found - Marking category as Done\n")
            elif products_found == 0:
                print("  No products found on this page - Stopping pagination\n")

            self.category_input.update_one(
                {"_id": doc_id},
                {"$set": {"Status": "Done"}}
            )
            print("✅ Category marked as Done\n")

    def handle_error(self, failure):
        """Handle request errors"""
        request = failure.request
        print(f"\n Request failed: {request.url}")
        print(f"Error: {failure.value}")

        # Try to mark category as failed if it has meta
        if hasattr(request, 'meta') and '_id' in request.meta:
            doc_id = request.meta['_id']
            self.category_input.update_one(
                {"_id": doc_id},
                {"$set": {"Status": "Failed", "Error": str(failure.value)}}
            )
            print(f"  Category {doc_id} marked as Failed\n")

    def close(self, reason):
        """Close spider and cleanup"""
        print(f"\n{'=' * 60}")
        print(f" Spider closing: {reason}")
        print(f"{'=' * 60}\n")
        self.mongo_client.close()


if __name__ == '__main__':
    from scrapy.cmdline import execute

    execute("scrapy crawl pet_pl -a retailer=petmart-ph -a region=ph -a Type=eshop -a RetailerCode=petmart_ph".split())