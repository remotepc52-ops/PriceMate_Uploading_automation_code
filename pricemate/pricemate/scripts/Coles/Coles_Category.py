import json
import math
import os
import sys
from threading import Thread

from Coles.Brand_Mapping import barcode_map_process
from config import *

def PL_Extraction(start,end):
    data_list = category_input.find({"Status":"Pending"}).skip(int(start)).limit(int(end))
    # data_list = category_input.find({ "UrlFriendlyName": {"$regex": "liquorland"} })
    for cat_item in data_list:
        id = cat_item['_id']
        UrlFriendlyName = str(cat_item['UrlFriendlyName'])
        Category_Name = str(cat_item['Category Name'])

        total_pages = 0
        page_no = 1
        total_result = 0

        # Duplicates Remove
        # Delete records where Ids is equal to 1 and Parent is equal to "No"
        # result = product_data.delete_many({"Category_Name": Category_Name})

        # Output the number of documents deleted
        # print(f"Deleted {result.deleted_count} documents.")

        data_extraction(id, total_result, UrlFriendlyName, Category_Name, page_no,total_pages)
        # break


def data_extraction(id,total_result,UrlFriendlyName,Category_Name, page_no,total_pages):
    try:
        filename = f'{Category_Name}_{page_no}.html'
        path =  os.path.join(html_path, filename)
        full_path = path.replace("\\","/")

        headers = {
            'accept':'*/*',
            'accept-language':'en-US,en;q=0.9',
            'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36',
            'x-nextjs-data':'1',
        }

        url = f'https://www.coles.com.au/_next/data/{api_version}/en/browse/{UrlFriendlyName}.json?page={page_no}&slug={UrlFriendlyName}'
        print(url)
        response = obj.to_requests(url = url, headers = headers, method = "GET", max_retry = 2,
                                   html_path = full_path, should_be = ['pageProps', 'searchResults'])

        if not response:
            headers = {
                'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
                'cookie': 'visid_incap_2800108=kkHlWjHHREuVtQQ5w9OLBAIyGmcAAAAAQUIPAAAAAACPV+rOKbqY7jFlUx0xytxS; incap_ses_968_2800108=6lWpfEFuTh42VfwOFwdvDQIyGmcAAAAANb8kzSN336vXFLxKmnlojg==; incap_ses_330_2800108=pi6XXS7JNBlqpeGwc2WUBAgyGmcAAAAAFXaseICcaZf8vNXsYcY9TA==; ApplicationGatewayAffinityCORS=ce1dd33cb7cfcf721c38e4c63f5c6894; ApplicationGatewayAffinity=ce1dd33cb7cfcf721c38e4c63f5c6894; nlbi_2800108=2wdXGBO4Fy2mrO2IjQyMFgAAAACy9BNaCYddWCnMJFihuZ2o; reese84=3:RYc44nE0iEk8KZg+PGQMqg==:lzyApTeeBniZRq4pS6vXj0aTTyQYclv1T9AuazdwBV8osd1ndGWTr5xz1uaatueQoSO0T8sAv7Dz4twCOj+W8W8oDKW8KD96PgIkZeJkIysc1cY7DMvLrz8H5xz69o0iorLI1MXxAEuCE4BBJYw3dMJDgqBrhePbOsApEM3VgM1y5fxm3QDbyGw7BkmjbMPJPTDYcYPq4oDYUX2X1/Uov5mvJfeD7eDYDz/ol9R2qOdXDGt5JEf3pHxENsFkbkr6gV6/Hben/ABl/4LRIzpXVPTzOZQ73gwSNjAyLmcKWcAUN5T+SDMN3Yu2VLXKdP8uAxHEnd9zYmIpkStzzXDHbqNhs/XDx3rce+8b+MZ0mJ+PVcf6Gb3y2fpmumYs6g9PQm9w3M38qrTGbDhwEKwiac5QIH7u8kZINA22MfeG51fZRfDO+triVFRR/3bUTm50/hk0P6GOtclIyajupoEYTzmAHo8Nm/4unE/D9WNIikc=:A8Y5HH+tfjUDMZDNIx4//6iMtP+t4kbrLxJ7EB4FXLs=; nlbi_2800108_2670698=s/UbO/jrBFrBZMOyjQyMFgAAAAAWOoGtFdauAXgDlzU6Yxg3; nlbi_2800108_2147483392=aHSRRCHmY2xAe13LjQyMFgAAAADM1bAmPpoKcEIkXC8htcVG; ld_user=4d6d8c7b-3f5a-4923-ae9c-f03f939a69c2; sessionId=8e998d5c-8d68-4172-9766-cbdf6f93d366; visitorId=c6aef8c0-230d-47b2-8797-13899485ca57; AMCVS_0B3D037254C7DE490A4C98A6%40AdobeOrg=1; analyticsIsLoggedIn=false; AMCV_0B3D037254C7DE490A4C98A6%40AdobeOrg=179643557%7CMCIDTS%7C20021%7CMCMID%7C19139805243360655640853082410849548668%7CMCAAMLH-1730374799%7C8%7CMCAAMB-1730374799%7CRKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y%7CMCOPTOUT-1729777200s%7CNONE%7CMCAID%7CNONE%7CvVersion%7C5.5.0; at_check=true; fs_lua=1.1729770001648; gpv_page=cusp%3Ahome; fs_uid=#o-210D95-na1#a5910935-f13b-4e70-8a16-9ce5a8732d96:d028310a-030f-412b-b0c8-e72438f9ed50:1729770001648::1#74a7a6de#/1761306003; s_cc=true; _gcl_au=1.1.1709473255.1729770005; kndctr_0B3D037254C7DE490A4C98A6_AdobeOrg_identity=CiYxOTEzOTgwNTI0MzM2MDY1NTY0MDg1MzA4MjQxMDg0OTU0ODY2OFIRCMS8zvKrMhgBKgRBVVMzMAPwAcS8zvKrMg==; kndctr_0B3D037254C7DE490A4C98A6_AdobeOrg_cluster=aus3; _ga=GA1.1.124555730.1729770007; ORA_FPC=id=20b9ee88-0b15-4fda-8557-c08b2d802c26; WTPERSIST=; _fbp=fb.2.1729770007146.657028745441558762; BVBRANDID=ecd47f60-616a-469a-97f6-9756a8879a1a; BVBRANDSID=1fad4895-7f11-47a3-96bc-cda24f9410a2; mbox=session#d7ef1154377b45e5851aca908efde116#1729771882|PC#d7ef1154377b45e5851aca908efde116.36_0#1793014805; s_ecid=MCMID|19139805243360655640853082410849548668; dsch-sessionid=3e841b93-b77d-4e39-890b-0619f86fd8aa; dsch-visitorid=fe72025d-6dda-4b51-9798-ad3b318ad620; ad-memory-token=cCPxZrwbQhqZJLNiVKO2LBL5x50KRQoMEgoKCDM1Mjc5NTdQCgwSCgoIMzAzODkzOVAKDBIKCgg4MDIwNjgwUAoMEgoKCDcwMzU4NzRQEgsIpeTouAYQ9oLZexoCCAIiAA%3D%3D; _ga_C8RCBCKHNM=GS1.1.1729770007.1.1.1729770023.44.0.0; s_ips=350; s_tp=6756; s_sq=colesonline-coles-global-prod%3D%2526c.%2526a.%2526activitymap.%2526page%253Dcusp%25253Abrowse%25253Aproduct-categories%2526link%253Dcoca-cola%252520classic%252520soft%252520drink%252520bottle%252520%25257C%252520600ml%252520down%252520down%252520%2525244.00%252520%2525246.67%252520per%2525201l%252520was%252520%2525244.25%252520on%252520aug%2525202024%252520add%2526region%253Dproduct-tiles%2526pageIDType%253D1%2526.activitymap%2526.a%2526.c%2526pid%253Dcusp%25253Abrowse%25253Aproduct-categories%2526pidt%253D1%2526oid%253Dfunctionry%252528%252529%25257B%25257D%2526oidt%253D2%2526ot%253DSECTION; s_ppv=cusp%253Abrowse%253Aproduct-categories%2C5%2C11%2C10%2C749%2C19%2C2; incap_ses_606_2800108=3lmRH/2tSlFF2uCm+PFoCBU0GmcAAAAAPDSayFxXeGnK7f8WQIV+MA==; s_ecid=MCMID|19139805243360655640853082410849548668; ad-memory-token=%2Fx%2BwElLXn0AqKvjqaUwKrqHL66AKRQoMEgoKCDM1Mjc5NTdQCgwSCgoIMzAzODkzOVAKDBIKCgg4MDIwNjgwUAoMEgoKCDcwMzU4NzRQEgsIlejouAYQh%2BqxMxoCCAIiAA%3D%3D; dsch-sessionid=3e841b93-b77d-4e39-890b-0619f86fd8aa; dsch-visitorid=fe72025d-6dda-4b51-9798-ad3b318ad620',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36'
            }

            url = f"https://www.coles.com.au/browse/{UrlFriendlyName}?page={page_no}"
            response = obj.to_requests(url=url, headers=headers, method="GET",
                                       html_path=full_path, should_be=['pageProps', 'searchResults'])

            if not response:
                print("Facing Response issues...")
                return None

            elif 'VerifyHuman' in response:
                print("Captcha Not Resolved after all retries executed...")
                return None

            elif 'Result Not Found' in response or 'This product is invalid.' in response or 'This page could not be found' in response:
                category_input.update_one({'_id': id}, {'$set': {'Status': "Not found"}})
                print("status updated...")
                return None

            else:
                selector_res = Selector(response)
                response = selector_res.xpath('//script[@id="__NEXT_DATA__"]//text()').get()
                if not response:
                    print("Getting blank script json data...", url)
                    return None

        if not response:
            print("Facing Response issues...")
            return None

        elif 'VerifyHuman' in response:
            print("Captcha Not Resolved after all retries executed...")

        elif 'Result Not Found' in response or 'This product is invalid.' in response or 'This page could not be found' in response:
            category_input.update_one({'_id':id},{'$set':{'Status':"Not found"}})
            print("status updated...")

        elif response:
            print("Getting Correct Response...")
            # print(response)
            try:res_json = json.loads(response)
            except:
                os.remove(path)
                return None
            try:check_bundles = res_json['pageProps']['searchResults']['results']
            except:
                os.remove(full_path)
                return

            if check_bundles:
                for product in check_bundles:

                    result_type = product['_type']
                    if result_type != "PRODUCT":
                        continue
                    product_id = product['id']

                    Name = product['name']
                    brand = product['brand']
                    if not brand:
                        brand = ""

                    PackageSize = product['size']

                    if PackageSize and brand and Name:
                        prouduct_full_name = f"{brand} {Name} {PackageSize}"

                    elif brand and Name:
                        prouduct_full_name = f"{brand} {Name}"

                    else:
                        prouduct_full_name = Name

                    # urlfriendluy_name = f"{brand}-{Name}-{PackageSize}".lower().replace(":", "-").replace(" ", "-").replace("&", "-").replace("%", "percent")

                    ProductURL = f"https://www.coles.com.au/product/p-{product_id}"
                    # print(ProductURL)

                    barcode = "" #product['Barcode']

                    checkPrice = product['pricing']
                    if checkPrice:
                        Price = product['pricing']['now']
                        WasPrice = product['pricing']['was']
                        if not WasPrice:
                            WasPrice = Price
                    else:
                        continue

                    if not Price and not WasPrice:
                        product_data.update_one({'_id': id}, {'$set': {'Status': "Done_1"}})
                        Gprint("✅ Status updated as Result ℹ️ Done...")
                        continue

                    if Price == WasPrice:
                        WasPrice = None

                    try:
                        per_unit_price = product['pricing']['comparable']
                        if not per_unit_price:
                            per_unit_price = ""
                    except:
                        per_unit_price = ""
                    try:
                        productimages = [f"https://www.coles.com.au/_next/image?url=https://productimages.coles.com.au/productimages/{img['uri']}&w=256&q=90"
                                         for img in product['imageUris']]
                        productimages  = "|".join(productimages)

                    except Exception as e:
                        print(e)
                        productimages = ""
                        # print(ProductURL)
                    try:
                        subCategory = product['onlineHeirs'][0]['subCategory']
                        category = product['onlineHeirs'][0]['category']
                        aisle = product['onlineHeirs'][0]['aisle']
                        breadcrumbs = f"{subCategory} > {category} > {aisle}"
                    except Exception as e:
                        print("Error in categoy coles:", e)
                        continue

                    try:
                        offer_info = product['pricing']['saveStatement']
                        promo_type = product['pricing']['promotionType']

                    except:
                        offer_info = ""
                        promo_type = ""

                    items = {}
                    items["HtmlPath"] = path
                    items["Page"] = page_no
                    items["Category_Name"] = Category_Name
                    items["Category_Url"] = UrlFriendlyName
                    items["ProductURL"] = ProductURL
                    items["ProductCode"] = product_id
                    items["Name"] = prouduct_full_name
                    items["Price"] = float(Price)
                    items["WasPrice"] = float(WasPrice) if WasPrice else None
                    items["RRP"] = WasPrice if WasPrice else Price
                    items["per_unit_price"] = per_unit_price
                    items["Offer_info"] = offer_info
                    items["Pack_size"] = PackageSize
                    items["Barcode"] = barcode
                    items["retailer_name"] = "coles"
                    items["Category_Hierarchy"] = breadcrumbs
                    items["Brand"] = brand
                    items["Promo_Type"] = promo_type
                    items["Images"] = productimages
                    items["Status"] = "Pending"

                    try:
                        product_data.insert_one(items)
                        print("Product Data Inserted...")

                    except Exception as e:
                        if 'duplicate key error' not in str(e):
                            print(e)

                if not total_result:
                    total_result = res_json['pageProps']['searchResults']['noOfResults']
                    total_pages = math.ceil(int(total_result) / 48)

                if page_no < total_pages:
                    page_no += 1
                    data_extraction(id, total_result, UrlFriendlyName, Category_Name, page_no, total_pages)
                else:
                    print("Next Page is not Available...")
                    category_input.update_one({'_id':id},{'$set':{'Status':"Done"}})
                    print("status updated...")

            else:
                print("Not Found Data In Next Page....")
                category_input.update_one({'_id':id},{'$set':{'Status':"Done"}})
                print("status updated...")

        else:
            print("Somthing Went Wrong in Requests...")


    except Exception as e:
        print(f"Error in Main Data Extraction function ",e)
        exc_type,exc_obj,exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type,fname,exc_tb.tb_lineno)


if __name__ == '__main__':
    #
    # start = 1
    # end = 1
    # PL_Extraction(start, end)
    # exit()
    #
    print(f"----- Main open ------- ")
    total_count = category_input.count_documents({'Status': 'Pending'})
    while total_count:
        total_count = category_input.count_documents({'Status': 'Pending'})
        print("Total Pending....",total_count)
        if not total_count:
            break

        if total_count > 18:
            variable_count = total_count // 1
        else:
            variable_count = total_count // total_count

        if variable_count == 0:
            variable_count = total_count ** 2

        count = 1
        threads = [Thread(target = PL_Extraction,args = (i,variable_count)) for i in
                   range(0,total_count,variable_count)]
        for th in threads:
            th.start()
        for th in threads:
            th.join()

        print(f"--------- Thread Ends ----------- ")
        time.sleep(5)

    if category_input.count_documents({'Status':'Pending'}) == 0:
        print("All Count Done...")

        # barcode_map_process(product_data)
