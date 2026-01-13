from concurrent.futures import ThreadPoolExecutor, as_completed

from time import sleep

from config import *

MAX_WORKERS = 30  # Tune based on your system + proxy limits


def fetch_batch(skip, limit):
    data_list = product_data.find({"Status": "Pending"}).skip(skip).limit(limit)
    for cat_item in data_list:
        ID = cat_item['_id']
        product_code = str(cat_item['ProductCode'])
        ProductURL = str(cat_item['ProductURL'])
        data_extraction(ID, product_code, ProductURL)


def data_extraction(ID, product_code, url):
    try:
        filename = f'PDP_{product_code}.html'
        path = os.path.join(html_path, filename)
        full_path = path.replace("\\", "/")

        headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'accept-language': 'en-US,en;q=0.9',
            'cache-control': 'max-age=0',
            'cookie': 'deviceId=49952601-5d52-4845-a616-5386dc82d596; i18next=en-US; _ga=GA1.1.1975098177.1730966093; spressoDeviceId=1ff7be27-0a8a-4da3-b7ca-63183692e7b0; locationCaptured=true; interstitialCount=IntcIjY2ZDE5NzU5N2QzMGU2YjI1NzFmNTg0NFwiOjIsXCI2NmZmYWFjODIwY2FkZTVmNGQ5YjAzMjhcIjoyfSI=; crumb=M7djxpZbMOYh6myXBc82GGmFb7ShNfjwymfzdcphD8X; selectedPostalCode=55100; locationIdentifierIds=63b70a81277ca7244135741e,63b70a81277ca724413572f2; _ga_JGW88X53V2=GS1.1.1733723923.8.1.1733724104.0.0.0; aeon-my.web.sid=Fe26.2**2f66350d69ca1ad3d459042e2f157799ae82b8e6a4b27b0f9437fc6fbb30c738*Rf5TB4rxMip4CjRFuiarew*BxXRpFLnZkxZRMYP8gBtf1kKhtUrNby5Fg438pClSxM1VstWcXVH2g_yEa57zWTQ**3eaf5525edd290bd5dd6d75735c4d3bf572970129c676f9ae74addf452d77c5d*TCLuLrFttvuquQaQaoUH62wUgrsvJBvJbloIOIsIxrI; datadome=0wXxTuH7g9gQkdFx6LbCwRiUaAs9yoLc3w84Bz_4ghXuDvV~8vk86HYwJlshjvwoSnHDm2exa8lb3p1e4ZsYbZ7M2mnTfuXlExKJwsXcPjg4_G0IVHzBlAl4rX4rEO8U; superSession={%22id%22:%2249952601-5d52-4845-a616-5386dc82d596-1733723923902%22%2C%22expiry%22:1733725905739}; _dd_s=rum=0&expire=1733725003826',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36'
        }

        proxy = "http://21ed11ef5c872bc7727680a52233027db4578a0e:@api.zenrows.com:8001"

        proxies = {"http": proxy, "https": proxy}


        # scraperurl = f"http://api.scraperapi.com?api_key={scraper_api_key}&url={url}"
        response = obj.to_requests(url = url, headers=headers, should_be=['id="product-page"'], html_path=full_path, proxies=proxies,verify=False)

        if not response:    
            print("❌Getting blank response..... ❌", url)
            return None

        elif 'VerifyHuman' in response:
            print("❌ Captcha Not Resolved after all retries executed..❌")

        elif 'Result Not Found' in response or 'Sorry, the product you  are looking for' in response or 'This page could not be found' in response:
            product_data.update_one({'_id': ID}, {'$set': {'Status': "Not found"}})
            print("✅ Status updated as Result ℹ️ Not Found...")

        elif response:

            res_selector = Selector(text=response)

            additional_json = res_selector.xpath('//script[@id="script-schema-data"]//text()').get()
            print(additional_json)
            additional_json = json.loads(additional_json)

            # # desc = c_replace(res_selector.xpath('//*[@name="description"]/@content').get()) or None
            # try:
            #     desc = c_replace(additional_json['description']) or None
            # except:
            #     desc = None

            originalPrice = res_selector.xpath(
                '//div[@data-qa="pdp-details-price"]//span[@class="EdAT6MbjNO5qhmk5qsxO"]//text()').get() or None
            if originalPrice:
                originalPrice = float(originalPrice.replace("RM", "").strip())
            try:
                salePrice = res_selector.xpath(
                    '//div[@data-qa="pdp-details-price"]//span[contains(@class,"X0RsB269dboGUMEWcNmH")]//text()').get()
                if salePrice:
                    salePrice = float(salePrice.replace("RM ", "").strip())

                else:
                    print("Sale Price Should not be blank....", url)
                    return None
            except:
                salePrice = originalPrice
                originalPrice = None

            is_available = res_selector.xpath('//div[@data-qa="pdp-controls-atc"]//button[contains(text(),"ADD TO CART")]')
            if is_available:
                is_available = True
            else:
                is_available = False

            brand = res_selector.xpath('//*[@data-qa="pdp-name"]//h1//preceding-sibling::a//text()').get()
            if brand:
                brand = c_replace(brand)
            else:
                brand = ""
            pname = c_replace(res_selector.xpath('//*[@data-qa="pdp-name"]//h1//text()').get())

            pack_size = res_selector.xpath('//div[@class="czXzIdRs3ZRSbzoP4pWb"]//text()').get()
            if pack_size:
                PackageSize = c_replace(pack_size)
            else:
                PackageSize = ""

            producttitle = c_replace(f"{brand} {pname} {PackageSize}")

            # if not salePrice and originalPrice or originalPrice == salePrice:    #from
            #     salePrice = originalPrice
            #     originalPrice = None
            #
            # elif not originalPrice:
            #     print("salePrice should not be blank....")
            #     return None
            #
            # if not salePrice and not originalPrice:
            #     return None                         #tooo


            if not salePrice and not originalPrice:
                product_data.update_one({'_id': ID}, {'$set': {'Status': "Done_1"}})
                print("✅ Status updated as Result ℹ️ Done...")
                return None

            offer_info = res_selector.xpath(
                '//section[@id="product-page"]//strong[contains(@class, "MLKxmD9NRGxajI5YmpwP")]//text()').get()
            if offer_info:
                offer_info = offer_info.strip()


            breadcrumbs = res_selector.xpath('//div[@data-qa="pdp-breadcrumb-large"]//a/text()').getall()
            if breadcrumbs:
               breadcrumbs = " > ".join(c_replace(breadcrumbs))

            images = res_selector.xpath('//div[@class="hXfilatiriYNA8J7Th9F"]//img/@src').getall()
            images = ["https://"+img.split("https://")[-1] for img in images]
            product_images = " | ".join(images)

            Items = {
                "htmlpath": full_path,
                "Name": producttitle,
                "Promo_Type": "",
                "Price": salePrice,
                "per_unit_price": "",
                "WasPrice": originalPrice,
                "Offer_info": offer_info,
                "Pack_size": PackageSize,
                "Barcode": "",
                "Images": product_images,
                "ProductURL": url,
                "is_available": is_available,
                "ProductCode": product_code,
                "retailer_name": "myaeon2go",
                "Category_Hierarchy": breadcrumbs,
                "Brand": brand,
                "RRP": originalPrice if originalPrice else salePrice,
                "Status": "Done",
                }

            try:
                product_data.update_one({'_id': ID}, {'$set': Items})
                print("✅ Status updated as Result ℹ️ Done...")

            except Exception as e:
                if 'duplicate key error' not in str(e):
                    print("❌ Error: Unable to save data to database.", e)

        else:
            print("Somthing Went Wrong in Requests...")


    except Exception as e:
        print(f"Error in Main Data Extraction function ", e)


if __name__ == '__main__':
    print("🚀 Starting data scraping...")
    retry = 0

    while retry <= 5:
        retry += 1
        total_count = product_data.count_documents({'Status': 'Pending'})
        if not total_count:
            print("🎉 Finished processing all records!")
            break

        print("Total Pending:", total_count)

        batch_size = math.ceil(total_count / MAX_WORKERS)
        tasks = []

        with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
            for i in range(0, total_count, batch_size):
                tasks.append(executor.submit(fetch_batch, i, batch_size))

            for future in as_completed(tasks):
                try:
                    future.result()
                except Exception as e:
                    print(f"❌ Error in thread: {e}")

        print("--------- Batch Finished -----------")
        sleep(5)
