from concurrent.futures import ThreadPoolExecutor

from config import *
def main_docs(doc):
    cat_url = doc['url']
    doc_id  = doc['_id']

    headers = {
        'Referer': 'https://www.amazon.sg/alm/storefront?almBrandId=QW1hem9uIEZyZXNo',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36',
        'device-memory': '8',
        'downlink': '1.25',
        'dpr': '1.25',
        'ect': '3g',
        'rtt': '300',
        'sec-ch-device-memory': '8',
        'sec-ch-dpr': '1.25',
        'sec-ch-ua': '"Google Chrome";v="141", "Not?A_Brand";v="8", "Chromium";v="141"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-ch-ua-platform-version': '"19.0.0"',
        'sec-ch-viewport-width': '1536',
        'viewport-width': '1536',
    }
    proxy_host = "api.zyte.com"
    proxy_port = "8011"
    proxy_auth = f"{current_proxy}:"

    proxies = {
        "http": "https://{}@{}:{}/".format(proxy_auth, proxy_host, proxy_port),
        "https": "http://{}@{}:{}/".format(proxy_auth, proxy_host, proxy_port)
    }

    response = requests.get(cat_url, headers=headers, proxies=proxies, verify='zyte-ca.crt')

    if response.status_code == 200:

        retry_count = 5
        for attempt in range(retry_count):

            selector = Selector(response.text)

            # --- Extract all category links ---
            cat_links = selector.xpath('//a[contains(@href, "/alm/category/")]/@href').getall()

            # --- If first XPath fails, use your 2nd XPath ---
            if not cat_links:
                cat_links = selector.xpath(
                    "//div[contains(@class, '_Y29ud_bxcGridContent')]//a[contains(@href, '/alm/category')]/@href").getall()
            if not cat_links:
                cat_links = selector.xpath(
                    "//span[contains(@class, 'a-button-inner')]/a[contains(@href, '/alm/category')]/@href"
                ).getall()

            if not cat_links:
                regex_links = re.findall(r'href="(/alm/category[^"]+)"', response.text)
                if regex_links:
                    cat_links = regex_links


            # ------------------------
            # ⭐ RETRY ONLY WHEN EMPTY
            # ------------------------
            if cat_links:
                break  # success → stop retrying

            print(f"Retry {attempt + 1}/{retry_count} → No category links found for {cat_url}")
            time.sleep(1)

            # try request again
            response = requests.get(cat_url, headers=headers, proxies=proxies, verify='zyte-ca.crt')
            if response.status_code != 200:
                continue

        # ------------------------------------
        # STILL EMPTY AFTER RETRIES? → NOT FOUND
        # ------------------------------------
        if not cat_links:
            print("❌ No category links even after retries:", cat_url)
            search_data.update_one({"_id": doc_id}, {"$set": {"Status": "NotFound"}})
            return

        # ------------------------------------
        # SUCCESS → CONTINUE YOUR NORMAL CODE
        # ------------------------------------
        category_urls = []
        for href in cat_links:
            if href.startswith("/"):
                full_url = "https://www.amazon.sg" + href.split("&amp;")[0].replace("&amp;", "&")
            else:
                full_url = href

            if full_url not in category_urls:
                category_urls.append(full_url)
            for url in category_urls:
                doc_insert = {
                    "url": url,
                    "Status": "Pending",
                }

                # ✅ Upsert to avoid duplicates
                raw_url.update_one(
                    {"url": url},
                    {"$setOnInsert": doc_insert},  # only insert if not already exists
                    upsert=True
                )

        # --- Print all found category URLs ---
        print("Found category URLs:")
        for url in category_urls:
            print(url)
        if cat_links:
            # If category URLs found, mark Done
            search_data.update_one({"_id": doc["_id"]}, {"$set": {"Status": "Done"}})
        else:
            # If no URLs found, mark Not Found
            search_data.update_one({"_id": doc["_id"]}, {"$set": {"Status": "Not Found"}})


        # ✅ Add status update logic here (after processing)


    # --- Print all page URLs ---


if __name__ == "__main__":
    with ThreadPoolExecutor(max_workers=15) as executor:
        docs = list(search_data.find({"Status": "Pending"}))
        executor.map(main_docs, docs)