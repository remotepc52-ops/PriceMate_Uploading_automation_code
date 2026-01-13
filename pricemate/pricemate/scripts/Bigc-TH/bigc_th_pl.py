import json
from config import *
from concurrent.futures import ThreadPoolExecutor

headers = {
    'accept': '*/*',
    'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
    'cache-control': 'no-cache',
    'pragma': 'no-cache',
    'priority': 'u=1, i',
    'referer': 'https://www.bigc.co.th/',
    'sec-ch-ua': '"Chromium";v="142", "Google Chrome";v="142", "Not_A Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36',
    'x-nextjs-data': '1',
    # 'cookie': '__cf_bm=nOLORgHbT0ErsRwAvuQdPbgq4XU20LMI2emxJzA5bbA-1766498453-1.0.1.1-XpFIDEkEPOsspNvxMGzWgu09I0b0WpZy8YtOLv0yX5pnE7YTHH3_pYom.SPUsS0IP4jB8RxMGUBtPfjpLgw.t_VpVr8BS.XOGVg2ERyC62Q; a_b_testing=a; language=th; prx_langs=eyJkZWZhdWx0TGFuZ3VhZ2UiOiJ0aCIsImxhbmd1YWdlc0RhdGEiOlt7InBvc2l0aW9uIjoxLCJwcmVmaXgiOiJ0aCIsIm5hbWUiOiLguYTguJfguKIifSx7InBvc2l0aW9uIjoyLCJwcmVmaXgiOiJlbiIsIm5hbWUiOiJFbmdsaXNoIn1dLCJsYW5ndWFnZXMiOlsidGgiLCJlbiJdfQ==; cf_clearance=Y.dahRZfheO2_kuyucTAGUGpbmytb.hyvsbvM4DK9y0-1766498455-1.2.1.1-r9RqiHICbxBypOmiP918AI6EQdRc9mdrObOQtx0yc0nVlxgrpL2ZwMzCZEjV6VcVI2OKO7l9Em3odWjX5Fg909AZE4agr9NblwxZ6v2LnIGn0rWmbp4wYejzdgHHaH1h1QShFncQ_zKniJtDpNCp5J2eWBxVZiiP85aTZ8ZQjJGYFMGrT2p4dPubH4cDc59cc788zYTmJW7Zs.VjnS5bnklV9S0NLJhR_13tBIG.xNc; store_id=MTExOTA=; selected_warehouse=eyJzdG9yZV9pZCI6MTExOTAsIndhcmVob3VzZV9wYXJlbnRfaWQiOjQyOTQ5NjcyOTUsImxhdGl0dWRlIjoxMy43MTg5MjksImxvbmdpdHVkZSI6MTAwLjU2OTAzNCwicG9zdGFsIjoiMTAxMTAiLCJ3YXJlaG91c2VfbmFtZV9lbiI6IkJJR0MgRVhUUkEgUkFNQSA0Iiwid2FyZWhvdXNlX2RldGFpbHNfZW4iOiIiLCJ3YXJlaG91c2VfYWRkcmVzc19lbiI6Ik5vLiAyOTI5IFJhbWEgNCBSZC4sIEtsb25ndG9uLCBLbG9uZ3RvZXksIEJhbmdrb2sgMTAxMTAiLCJzdWJfZGlzdHJpY3RfZW4iOiJLbG9uZ3RvbiwiLCJkaXN0cmljdF9lbiI6Iktsb25ndG9leSIsInByb3ZpbmNlX2VuIjoiQmFuZ2tvayIsIndhcmVob3VzZV9uYW1lX3RoIjoi4Lia4Li04LmK4LiB4LiL4Li1IOC4nuC4o+C4sOC4o+C4suC4oSA0Iiwid2FyZWhvdXNlX2RldGFpbHNfdGgiOiIiLCJ3YXJlaG91c2VfYWRkcmVzc190aCI6IuC5gOC4peC4guC4l+C4teC5iCAyOTI5ICDguJbguJnguJkgICDguJ7guKPguLDguKPguLLguKEgNCAgIOC5geC4guC4p+C4hyDguITguKXguK3guIfguJXguLHguJkgICDguYDguILguJUgIOC4hOC4peC4reC4h+C5gOC4leC4oiAgIOC4iOC4seC4h+C4q+C4p+C4seC4lCAg4LiB4Lij4Li44LiH4LmA4LiX4Lie4LivIDEwMTEwIiwic3ViX2Rpc3RyaWN0X3RoIjoi4LmB4LiC4Lin4LiHIOC4hOC4peC4reC4h+C4leC4seC4mSIsImRpc3RyaWN0X3RoIjoi4LmA4LiC4LiVICDguITguKXguK3guIfguYDguJXguKIiLCJwcm92aW5jZV90aCI6IuC4geC4o+C4uOC4h+C5gOC4l+C4nuC4oeC4q+C4suC4meC4hOC4oyIsImNkMSI6IuC4geC4suC4o+C4o+C4seC4muC4quC4tOC4meC4hOC5ieC4suC5g+C4q+C5ieC4leC4tOC4lOC4leC5iOC4rSDguIjguLjguJTguJrguKPguLTguIHguLLguKPguKXguLnguIHguITguYnguLIg4Lia4Li04LmK4LiB4LiL4Li1IOC4nuC4o+C4sOC4o+C4suC4oSA0IiwiY2QyIjoiTmF0c2FyaW5lIFNlYW1tYWkiLCJjZDMiOiIwNjU3MjQ5NDcyIiwiY2Q0IjoibmF0c2FyaW5lLnNlYUBiaWdjLmNvLnRoIiwiY2Q1IjoiIiwiY2Q2IjoiQktLNCIsImNkNyI6Im5hdHNhcmluZS5zZWFAYmlnYy5jby50aCIsImNkOCI6IiIsImNkOSI6IiIsImNkMTAiOiIiLCJjZDExIjoiIiwiY2QxMiI6IiIsImNkMTMiOiIiLCJjZDE0IjoiIiwiY2QxNSI6IiIsImNkMTYiOiIiLCJjZDE3IjoiIiwiY2QxOCI6IiIsImNkMTkiOiIiLCJjZDIwIjoiIiwiaG9tZV9kZWxpdmVyeV9yYW5nZSI6Niwic2hpcHBpbmdfbWV0aG9kcyI6WzY1MzQsNjUzNSw2NTM2LDY1MzcsNjUzOCw2NTM5XSwib3Blbl90aW1lIjoiMDAwMC0wMC0wMCAwMjowMDowMDowMDAwMDAiLCJjbG9zZV90aW1lIjoiMDAwMC0wMC0wMCAxMjozMDowMDowMDAwMDAiLCJvcGVuX3dlZWtkYXkiOlswLDEsMiwzLDQsNSw2XSwid2FyZWhvdXNlX3R5cGVfZW4iOiJFeHRyYSIsIndhcmVob3VzZV90eXBlX3RoIjoiIiwiaXNfbm9uZWh1YiI6MCwiaXNfYXZhaWxhYmxlX3N0b3JlIjoxLCJleHByZXNzX2RlbGl2ZXJ5X3JhbmdlIjozLCJpbnN0YW50X2RlbGl2ZXJ5X3JhbmdlIjo3LCJkaXN0YW5jZSI6MC4wMjIxNCwic2VsZWN0ZWRfdGltZXN0YW1wIjoiMjAyNS0xMi0yM1QxNDowMzo0Mi4yNTRaIn0=',
}

def process_document(doc):
    doc_id = doc["_id"]
    url = doc['url']
    slug = doc['slug']

    page = 1
    last_page = None

    while True:
        html_filename = f"{slug}_page_{page}.json"
        html_filepath = os.path.join(html_path, html_filename)

        if os.path.exists(html_filepath):
            with open(html_filepath, "r", encoding="utf-8") as f:
                json_response = json.load(f)
        else:
            params = {
                "slug": slug,
                "page": page,
            }

            response = requests.post(
                f"https://www.bigc.co.th/_next/data/KEVlKY2y1wBI11OdOZRIs/category/{slug}.json",
                params=params,
                headers=headers,
                proxies=proxies,
                verify=False,
                timeout=60,
            )

            if response.status_code != 200:
                response = requests.post(
                    f"https://www.bigc.co.th/_next/data/KEVlKY2y1wBI11OdOZRIs/category/{slug}.json",
                    params=params,
                    headers=headers,
                    proxies=proxies,
                    verify=False,
                    timeout=60,
                )
            if response.status_code != 200:
                response = requests.post(
                    f"https://www.bigc.co.th/_next/data/KEVlKY2y1wBI11OdOZRIs/category/{slug}.json",
                    params=params,
                    headers=headers,
                    proxies=proxies,
                    verify=False,
                    timeout=60,
                )
            if response.status_code != 200:
                response = requests.post(
                    f"https://www.bigc.co.th/_next/data/KEVlKY2y1wBI11OdOZRIs/category/{slug}.json",
                    params=params,
                    headers=headers,
                    proxies=proxies,
                    verify=False,
                    timeout=60,
                )
            if response.status_code != 200:
                response = requests.post(
                    f"https://www.bigc.co.th/_next/data/KEVlKY2y1wBI11OdOZRIs/category/{slug}.json",
                    params=params,
                    headers=headers,
                    proxies=proxies,
                    verify=False,
                    timeout=60,
                )

            json_response = response.json()
            with open(html_filepath, "w", encoding="utf-8") as f:
                json.dump(json_response, f, indent=2)

        # ------------------------
        # SAFE DATA EXTRACTION
        # ------------------------
        product_category = json_response.get("pageProps", {}).get("productCategory", {})
        products_summary = product_category.get("products_summary", {})

        products = products_summary.get("products", [])
        last_page = products_summary.get("last_page")

        # 🛑 STOP if no products
        if not products:
            print(f"⚠️ No products | slug={slug} | page={page}")
            break

        # 🛑 STOP if page exceeds last_page
        if last_page and page > last_page:
            break

        # ------------------------
        # PRODUCT LOOP
        # ------------------------
        for d in products:
            prod_slug = d.get("slug")
            prod_id = d.get("product_id")
            sku = d.get("sku")

            if not prod_slug or not prod_id:
                continue

            full_url = f"https://www.bigc.co.th/product/{prod_slug}.{prod_id}"
            hash_id = generate_hash_id(full_url, "bigc", "th")

            items = {
                "_id": hash_id,
                "ProductURL": full_url,
                "ProductCode": str(sku),
                "Status": "Pending",
                "retailer": "bigc",
                "region": "th"
            }

            product_data.update_one(
                {"_id": hash_id},
                {"$set": items},
                upsert=True
            )

        print(f"✅ slug={slug} | page={page}/{last_page}")
        page += 1

    search_data.update_one({"_id": doc_id}, {"$set": {"Status": "Done"}})
    Bprint(f"☑️ [CATEGORY] {url} Done")

if __name__ == "__main__":
    # Fetch pending categories
    docs = list(search_data.find({"Status": "Pending"}))
    with ThreadPoolExecutor(max_workers=50) as executor:
        executor.map(process_document, docs)