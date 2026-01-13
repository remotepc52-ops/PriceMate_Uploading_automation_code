from concurrent.futures import ThreadPoolExecutor


from config import *
def main_docs(doc):
    cat_url = doc['url']
    doc_id = doc['_id']

    cookies = {
        'session-id': '357-6665496-3216146',
        'session-id-time': '2082787201l',
        'i18n-prefs': 'SGD',
        'lc-acbsg': 'en_SG',
        'ubid-acbsg': '357-7543284-8435468',
        'mp_d7f79c10b89f9fa3026f2fb08d3cf36d_mixpanel': '%7B%22distinct_id%22%3A%20%22%24device%3A199bd36bcf3b8a-063792c15ffea58-26061851-144000-199bd36bcf3b8a%22%2C%22%24device_id%22%3A%20%22199bd36bcf3b8a-063792c15ffea58-26061851-144000-199bd36bcf3b8a%22%2C%22%24initial_referrer%22%3A%20%22%24direct%22%2C%22%24initial_referring_domain%22%3A%20%22%24direct%22%7D',
        'rxc': 'ADChSkWyOJ/jhULfBRw',
        'session-token': 'FlfWaCmaMBGMyKruLSAwvxbhnCwk5rotIXjj58x0vxfQ6ojZUExA1TkI+M8Oovqu6egn6deqjVABDQFpLde5CO7usyNqm8cf/9hWPkHqHBgk6qFnc8FbEnFW03+jYZOmG9PfIQxM/OvLPcKZU0YDISU3ch1uwrjS4u0NcBQ/QR8bsmSgDFG8YcQp5R+4R15ZcYt6Cka8hF65DjYwiVxgUFzr+7YITlu1QwwhNh+59k/jQ3PZ/h4ozbkJTvv8Q7b8BKaoMpzPq7cqcqShfInuGjPzXnQS6Fl4BtCPVnSZzd4hLH/9wgaTeuoXqEX7cYIMV31k7wyvys0T6aoxUIP8hqMhwmmRMgak',
        'csm-hit': 'tb:SH71QAPZQMN1BAW5R8KF+s-QA8TE42FCMWSC5G8GMH9|1759818592791&t:1759818592791&adb:adblk_no',
    }

    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8,hi;q=0.7',
        'cache-control': 'max-age=0',
        'device-memory': '8',
        'downlink': '1.35',
        'dpr': '1.25',
        'ect': '3g',
        'priority': 'u=0, i',
        'rtt': '350',
        'sec-ch-device-memory': '8',
        'sec-ch-dpr': '1.25',
        'sec-ch-ua': '"Google Chrome";v="141", "Not?A_Brand";v="8", "Chromium";v="141"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-ch-ua-platform-version': '"19.0.0"',
        'sec-ch-viewport-width': '1536',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'none',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36',
        'viewport-width': '1536',
        # 'cookie': 'session-id=357-6665496-3216146; session-id-time=2082787201l; i18n-prefs=SGD; lc-acbsg=en_SG; ubid-acbsg=357-7543284-8435468; session-token=Rsg5naw5kU6QXB0GxzhAcXnIkgGB6fnq8v50YiCczVtZEaw8pQzS4eaelP4RajiVi/aq8cAq6/nLWHAGOs+pC2lXxjepO7FmDmvxoIB2Z0+li+Ujlw4/EtypTicW7t+cFzlBb3tEHAi4pCWo/9gDj/J87YyP2+nYlmUmblfsmmY/FSFxQx4zUrzVFaKrKW9TOi4Oaaa6+knyPlPtC+WjdJ9VlR63VfZKydRzZMTaQJC6c8sOHFHw5q0FGQUM5eRuZHF3gVm3Ci4B+1mFyFUEinIp9z7ls8eouVIHTz80Ze8GFHj//zXMS66QvZeDYevcI8a8s25ZqAJ36jt+pN5HNlg//0tmd2Tz; mp_d7f79c10b89f9fa3026f2fb08d3cf36d_mixpanel=%7B%22distinct_id%22%3A%20%22%24device%3A199bd36bcf3b8a-063792c15ffea58-26061851-144000-199bd36bcf3b8a%22%2C%22%24device_id%22%3A%20%22199bd36bcf3b8a-063792c15ffea58-26061851-144000-199bd36bcf3b8a%22%2C%22%24initial_referrer%22%3A%20%22%24direct%22%2C%22%24initial_referring_domain%22%3A%20%22%24direct%22%7D; csm-hit=tb:SH71QAPZQMN1BAW5R8KF+s-SH71QAPZQMN1BAW5R8KF|1759816519848&t:1759816519849&adb:adblk_no; rxc=ADChSkWzIZ/jhULfBRw',
    }



    while cat_url:
        print(f"Scraping page: {cat_url}")
        response = requests.get(cat_url, cookies=cookies, headers=headers)

        if response.status_code != 200:
            print(f"Failed to fetch {cat_url}, status code {response.status_code}")
            break

        selector = Selector(response.text)

        # --- Handle 'See all results' link ---
        see_all_url = selector.xpath('//a[@id="apb-desktop-browse-search-see-all"]/@href').get()
        if see_all_url:
            full_url = "https://www.amazon.sg" + see_all_url
            print(f"Found 'See all results' link: {full_url}")
            try:
                raw_url.insert_one({"url": full_url, "Status": "Pending"})
                print("Inserted 'See all results' URL as pending category.")
            except Exception as e:
                print(f"Error inserting see-all URL: {e}")
            search_data.update_one({"_id": doc_id}, {"$set": {"Status": "Done"}})
            break

        # --- Extract product blocks ---
        main_path = selector.xpath('//div[@data-cy="asin-faceout-container"]')
        if not main_path:
            main_path = selector.xpath('//div[@class="_c3ViY_gridCell_3gkoz"]')

        if not main_path:
            print(f"No products found for {cat_url}")
            search_data.update_one({"_id": doc_id}, {"$set": {"Status": "NotFound"}})
            break

        for main in main_path:
            p_url = main.xpath(".//a[contains(@href, '/dp/')]/@href").get()
            if not p_url:
                continue

            asin_match = re.search(r'/dp/([A-Z0-9]{10})', p_url)
            if not asin_match:
                continue

            asin = asin_match.group(1)
            price_text = main.xpath(".//span[@class='a-price']//span[@class='a-offscreen']/text()").get()
            if price_text:
                try:
                    price = float(price_text.replace('S$', '').strip())
                except:
                    price = None
            else:
                price = None

            name = main.xpath('.//span[@class="a-truncate-full a-offscreen"]/text()').get()
            if not name:
                name = main.xpath('.//h2//span/text()').get()

            product_data = {
                "ProductURL": "https://www.amazon.sg" + p_url,
                "ProductCode": asin,
                "Name": name,
                "Price": price,
                "CategoryURL": cat_url,
                "Status": "Pending"
            }

            print(product_data)

            try:
                main_data.insert_one(product_data)
                print("Inserted product.")
            except Exception as e:
                print(f"Error inserting product: {e}")

        # --- Pagination: find the next page link ---
        next_page = selector.xpath(
            '//a[contains(@class, "s-pagination-next") and not(contains(@aria-disabled, "true"))]/@href'
        ).get()

        if next_page:
            cat_url = "https://www.amazon.sg" + next_page
            print(f"Next page found: {cat_url}")
            time.sleep(2)  # avoid being blocked
        else:
            print("No more pages found.")
            cat_url = None

    # --- Mark as done when pagination ends ---
    search_data.update_one({"_id": doc_id}, {"$set": {"Status": "Done"}})
    print("Category scraping complete.")
if __name__ == "__main__":
    with ThreadPoolExecutor(max_workers=15) as executor:

        # 1️⃣ FIRST: PROCESS search_data → Status: NotFound
        retry_docs = list(search_data.find({"Status": "NotFound"}))
        for d in retry_docs:
            d["source"] = "search_data"   # mark where this came from
        print(f"Retrying failed category URLs: {len(retry_docs)}")
        executor.map(main_docs, retry_docs)

        # 2️⃣ SECOND: PROCESS raw_url → Status: Pending
        docs = list(raw_url.find({"Status": "Pending"}))
        for d in docs:
            d["source"] = "raw_url"
        print(f"Processing pending subcategory URLs: {len(docs)}")
        executor.map(main_docs, docs)
