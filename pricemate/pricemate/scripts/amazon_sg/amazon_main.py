from concurrent.futures import ThreadPoolExecutor

from config import *
from parsel import Selector
def process_document(doc):
    product_url = doc['ProductURL']
    ProductCode = doc['ProductCode']
    price = doc['Price']

    doc_id = doc['_id']

    # cookies = {
    #     'session-id': '356-0471235-3154402',
    #     'session-id-time': '2082787201l',
    #     'i18n-prefs': 'SGD',
    #     'lc-acbsg': 'en_SG',
    #     'ubid-acbsg': '356-9598858-3488666',
    #     'session-token': 'UZbNsX7Epn1rVONc+BdXsypBQckr985pLPHd/elhHB+JvUKiqIKYfcsHV61RX94qH3WlBD7OQAc/wRCRpCIhfeJrE3qCdGN0vmrxAiKONp0rGM0phL1SLw9GJ3+ZuhhT7VBI+asKsiVzut4+YUOdJEY30eRiwxYCpalxtbIcJGm/7mOjZrXxOoF+ftDDMfcPLaoh9ClX+dwet2zxO7x1agOQevU+Kx9Iij4hbwIUW8FXhAhbuFBV4zkHDzd5sw/qGXlG6fX1IaoiLrOYCGtP5Ig3rY2M3IAU7cX+hLG7WrWYey7p53muBcBiRoamUI3XqGNwGAT6rnymveSfje9/uxmJnTFE5pcX',
    #     'id_pkel': 'n1',
    #     'id_pk': 'eyJuIjoiMSJ9',
    #     'csm-hit': 'tb:s-7T196QB5Z3RN174B2YYH|1764865281871&t:1764865282947&adb:adblk_no',
    #     'rxc': 'AEW5fn8mvnPZMzsz6QU',
    # }

    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'en-US,en;q=0.9,hi;q=0.8',
        'cache-control': 'max-age=0',
        'device-memory': '8',
        'downlink': '1.3',
        'dpr': '1.25',
        'ect': '3g',
        'priority': 'u=0, i',
        'rtt': '300',
        'sec-ch-device-memory': '8',
        'sec-ch-dpr': '1.25',
        'sec-ch-ua': '"Chromium";v="142", "Google Chrome";v="142", "Not_A Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-ch-ua-platform-version': '"19.0.0"',
        'sec-ch-viewport-width': '1536',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36',
        'viewport-width': '1536',
        'cookie': 'session-id=356-0471235-3154402; session-id-time=2082787201l; i18n-prefs=SGD; lc-acbsg=en_SG; ubid-acbsg=356-9598858-3488666; rx=AQBjHDaa+5oSWmuh/O8fAX65xqg=@AQqNMmk=; session-token=EFxyFmdYi/0J52K1XAFbs4fr5RYewfBP7k+7k1Q3LA8di/BHoRkXAwT36kdFpqMrXqdNTslC1gVtQao2LIBLNwVflmnbveBI1Q4FMPdwsg7s3Ia/jC0PU8AFYYpv2112FfWikwRUVvP1oEKpVXpJZE9Bd0v+4mGql4vsgmIEJHLeqGpzx1pfHuVsrV6pgVH7sBrttggK9UL5/RxFdiJfITKITQ+4nwoawMVOsgdOa10lBwFqloYPTtrjtlEcE4z9ftImbCXFLJgbvg8z5O6wY79F00QLGSAKh5hE6OAfWGhM5L3rJAZ2S+dAurlaCcjE0ibI5e/XXsj5G2sWuLqtJbdHpfhIU2R8; csm-hit=tb:QH1WTPPXVZAWVCEMR95K+s-QQA6G3SWRT6PER0KC7RS|1764926382842&t:1764926382842&adb:adblk_no; rxc=AEW5fn+fqHDZMzszRAM',
    }

    proxy_host = "api.zyte.com"
    proxy_port = "8011"
    proxy_auth = f"{current_proxy}:"

    proxies = {
        "http": "https://{}@{}:{}/".format(proxy_auth, proxy_host, proxy_port),
        "https": "http://{}@{}:{}/".format(proxy_auth, proxy_host, proxy_port)
    }
    html_filename = f"{ProductCode}_page.html"
    html_filepath = os.path.join(html_path, html_filename)
    response = obj.to_requests(url=product_url, headers=headers, html_path=html_filepath,
                               should_be=["productTitle"], max_retry=10
                               )
    if not response:
        print(f"getting wrong response:{product_url}")
        main_data.update_one({"_id": doc_id}, {"$set": {"Status": "Not Found"}})

        return None
    elif 'Result Not Found' in response or 'This product is invalid.' in response or 'This page could not be found' in response:
        main_data.update_one(
            {'_id': id}, {'$set': {'Status': "Not found"}})
        print("Status Updated...")
    elif response:

        selector = Selector(text=response)

        name = selector.xpath('//span[@id="productTitle"]//text()').get().strip()
        breadcrumbs = selector.xpath(
            '//ul[contains(@class, "a-unordered-list") and contains(@class, "a-horizontal")]/li//a/text()').getall()


        # Clean and join
        breadcrumbs_clean = [crumb.strip() for crumb in breadcrumbs if crumb.strip() and 'Flash Player' not in crumb]
        breadcrumbs_joined = ' > '.join(breadcrumbs_clean)
        brand = selector.xpath('//tr[@class="a-spacing-small po-brand"]//span[@class="a-size-base po-break-word"]//text()').get()

        print(breadcrumbs_joined)
        print(brand)
        if not price:
            price = selector.xpath('//input[@id="twister-plus-price-data-price"]/@value').get()


        print(price)
        was_price_text = selector.xpath(
            '//span[contains(@class, "basisPrice")]//span[@class="a-offscreen"]/text()').get()

        was_price = None
        if was_price_text:
            match = re.search(r'[\d,.]+', was_price_text)  # matches numbers like 25.20
            if match:
                was_price = match.group()
                was_price = float(was_price.replace('S$', '').strip())

        if not was_price or price == was_price:
            rrp_price = price
            was_price = ''
        else:
            rrp_price = was_price

        pack_size = extract_size(name)



        barcode = selector.xpath('//td[span[contains(text(), "UPC")]]/following-sibling::td[1]/span/text()').get()
        per_unit_price = selector.xpath('//span[@class="a-size-mini aok-offscreen"]/text()').get() or ""
        if per_unit_price:
            per_unit_price = per_unit_price.strip().replace('S$', '').strip()
        stock = selector.xpath('//div[@id="availability-string"]/span//text()').get()
        if not stock:
            stock = selector.xpath("//div[@id='almOutOfStockAvailability_feature_div']//span[contains(text(), 'Out of Stock')]//text()").get()
        if " In Stock " in stock:
            stock = True
        else:
            stock = False
        print(stock)

        scripts = selector.xpath("//script[@type='text/javascript']/text()").getall()
        offer = selector.xpath(
            '//span[contains(@class, "savingPriceOverride") and contains(@class, "savingsPercentage")]//text()').get()
        data_json_text = None

        for script in scripts:
            if 'var data =' in script:
                pattern = re.compile(r"var data\s*=\s*({.*?});\s*A\.trigger", re.DOTALL)
                match = pattern.search(script)
                if match:
                    data_json_text = match.group(1)
                    break
        final_string = ""

        if not data_json_text:
            print("❌ Could not find var data block")
        else:
            data_json_text = re.sub(r'Date\.now\(\)', '0', data_json_text)  # Remove Date.now()
            data_json_text = re.sub(r"'", '"', data_json_text)  # Single to double quotes
            data_json_text = re.sub(r",(\s*[}\]])", r'\1', data_json_text)  # Remove trailing commas
            try:
                data = json.loads(data_json_text)

                images = data.get('colorImages', {}).get('initial', [])
                hi_res_urls = [img.get('hiRes') for img in images if img.get('hiRes')]

                final_string = '|'.join(hi_res_urls)
                if not final_string:
                    final_string = selector.xpath('//div[@id="imgTagWrapperId"]/img/@src').get()

                print("✅ Final hiRes URL string:")
                print(final_string)

            except json.JSONDecodeError as e:
                print(f"JSON parsing error: {e}")
            if not price:
                return

            Items = {"Name": name, "Promo_Type": "", "Price": price, "per_unit_price": per_unit_price,
                     "WasPrice": was_price,
                     "Offer_info": offer, "Pack_size": pack_size, "Barcode": "",
                     "Images": final_string,
                     "ProductURL": product_url, "is_available": stock,
                     "Status": "Done", "ParentCode": "", "ProductCode": ProductCode,
                     "retailer_name": "amazon-fresh-sg",
                     "Category_Hierarchy": breadcrumbs_joined, "Brand": brand, "RRP": rrp_price}
            product_data.insert_one(Items)
            main_data.update_one({"_id": doc_id}, {"$set": {"Status": "Done"}})
            print("DATA INSERTED")



if __name__ == "__main__":
    with ThreadPoolExecutor(max_workers=20) as executor:
        docs = list(main_data.find({"Status": "Pending"}))
        executor.map(process_document, docs)