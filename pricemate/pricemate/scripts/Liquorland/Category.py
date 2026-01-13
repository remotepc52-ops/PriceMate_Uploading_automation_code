import json
import math
from threading import Thread
from config import *
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed

def get_product_images(product_id, uom):
    filename = f'Img_{product_id}.html'
    path = os.path.join(html_path, filename)
    full_path = path.replace("\\", "/")

    if uom:
        url = f"https://inject.skulibrary.com/api/?type=fc&code={product_id}&uom={uom}"
    else:
        url = f"https://inject.skulibrary.com/api/?type=fc&code={product_id}"

    headers = {
        'Accept': '*/*',
        'Accept-Language': 'en-US,en;q=0.9,hi;q=0.8',
        'Connection': 'keep-alive',
        'Cookie': 'AWSELB=515BB9F31A8E84D70899596280C8A727AF5100D9DF907E9D536FA8CEC0BFE3E649A0787AF3EEE9614FB4F686C652AD93A573E0A37307578899D5C10F3FAA9F02F9850F96E5; AWSELBCORS=515BB9F31A8E84D70899596280C8A727AF5100D9DF907E9D536FA8CEC0BFE3E649A0787AF3EEE9614FB4F686C652AD93A573E0A37307578899D5C10F3FAA9F02F9850F96E5'
    }

    response = obj.to_requests(url=url, headers=headers, html_path=full_path, should_be=['"result"'])
    if '"result":404' in response:
        return []
    res = json.loads(response)

    try: product_images = [i.get('Zoom') for i in res['data']['images'] if i.get('Zoom')]
    except: product_images = []
    return product_images


def PL_Extraction(start,end):
    data_list = category_input.find({"Status":"Pending"}).skip(int(start)).limit(int(end))
    for cat_item in data_list:

        total_pages = 0
        page_no = 1
        total_result = 0

        # ------ Duplicates Remove ---------
        # Delete records where Ids is equal to 1 and Parent is equal to "No"
        # result = product_data.delete_many({"Category_Name": Category_Name})
        #
        # # Output the number of documents deleted
        # Bprint(f"Deleted {result.deleted_count} documents.")

        data_extraction(cat_item)
        # break


def data_extraction(cat_item, total_pages = 0, page_no = 1, total_result = 0):
    try:
        ID = cat_item['_id']
        CategoryId = str(cat_item['CategoryId'])
        title = str(cat_item['title'])
        itemCount = str(cat_item['itemCount'])
        CategoryName = str(cat_item['CategoryName'])
        SubCategoryName = str(cat_item['SubCategoryName'])
        Category_Url = str(cat_item['Category_Url'])
        Category_Url_ls = str(cat_item['Category_Url']).split("liquorland.com.au/")[-1].split("/")
        if len(Category_Url_ls) == 1:
            Category_Url_ls = str(cat_item['Category_Url']).split("liquorland.com.au/")[-1].split("?")
            Category_Url_ls[1] = f"?{Category_Url_ls[1]}"

        filename = f'{CategoryId}_{page_no}.html'
        path =  os.path.join(html_path, filename)
        full_path = path.replace("\\","/")

        start_index = (page_no-1) * 60

        # TODO --> Use Postalcode --> Burwood Heights, 3151 VIC | "Burwood One" in Victoria Australia
        headers = {
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'en-US,en;q=0.9,hi;q=0.8',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36',
            'cookie': '__uzma=302a557a-5eb9-4068-941d-462e07b6794a; __uzmb=1743510054; _gcl_au=1.1.477868672.1743510056; _fbp=fb.2.1743510056799.979000897791569590; _gid=GA1.3.1620793631.1743510057; _y2=1%3AeyJjIjp7fX0%3D%3AMTc0OTg2MjMwNA%3D%3D%3A99; KP_UIDz-ssn=0agM6d4SLMuDc0glgam6ogaWlbAnJhXE3UkFvlf49shFpuAk2KEJqX9jQNyKSasbGZravmXUJ2SpJoek71Ve0hyJJuC5jyYSA3X38cxKQWIptPg0qdVTyWYC9r4guLUu8Sz6cZCr307DDSGivEsrzw1BsEMbf8EXYX4Tyl9; KP_UIDz=0agM6d4SLMuDc0glgam6ogaWlbAnJhXE3UkFvlf49shFpuAk2KEJqX9jQNyKSasbGZravmXUJ2SpJoek71Ve0hyJJuC5jyYSA3X38cxKQWIptPg0qdVTyWYC9r4guLUu8Sz6cZCr307DDSGivEsrzw1BsEMbf8EXYX4Tyl9; ORA_FPC=id=eebb06a6-fe6a-4e14-9118-6938b567a5aa; kampyle_userid=a09a-e81c-ddb5-03bb-71b6-251e-85c0-e179; _hjSessionUser_3303846=eyJpZCI6ImVmYzBlMTYzLWZjMjEtNTczNy1hNjIxLTExMzExM2ZhM2U4ZSIsImNyZWF0ZWQiOjE3NDM1MTAwNTcxMzQsImV4aXN0aW5nIjp0cnVlfQ==; WTPERSIST=; _hjSession_3303846=eyJpZCI6ImJjMmY1NTFlLWFmMjYtNGIzNy05NmQyLWIwOWU3YmU0M2YzMSIsImMiOjE3NDM1NzQwMjk2MjYsInMiOjAsInIiOjAsInNiIjowLCJzciI6MCwic2UiOjAsImZzIjowLCJzcCI6MH0=; AMCVS_0B3D037254C7DE490A4C98A6%40AdobeOrg=1; AMCV_0B3D037254C7DE490A4C98A6%40AdobeOrg=1075005958%7CMCIDTS%7C20180%7CMCMID%7C84783557377023754803114217230757611528%7CMCAAMLH-1744178830%7C7%7CMCAAMB-1744178830%7CRKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y%7CMCOPTOUT-1743581230s%7CNONE%7CvVersion%7C4.4.1; s_cc=true; CL_LL_02_UBT=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJjX3JvbGUiOiJBbm9ueW1vdXMiLCJjX2lkIjoiezA0YWI4ZjI0LTJiOGQtNGQ3YS04OTI1LTE5MGJjN2Y3YmVjOX0iLCJjX2JyYW5kIjoibGwiLCJjX2F4X2lkIjoiIiwibmJmIjoxNzQzNTc0MTExLCJleHAiOjE3NDg3NjE3MTEsImlhdCI6MTc0MzU3NDExMSwiaXNzIjoic2VsZiIsImF1ZCI6Imh0dHBzOi8vd3d3LmNvbGVzbGlxdW9yLmNvbS5hdSJ9.1WbZq2dA8Nrt85wyA9iabkEDiJ3wbw-QeWE9gdc46m8; CL_LL_02_ULN=; CL_LL_02_UFN=; CL_LL_02_UAID=; CL_LL_02_UPOA=false; CL_LL_02_UDP=false; ADRUM=s=1743576722600&r=https%3A%2F%2Fwww.liquorland.com.au%2F; cto_bundle=zp7j9l9xJTJGZ25OenZsa1Y1eG9mN3RPQUtyNW03R3liRWloJTJCeTFaNHVNMm02cjRsY2cyQzFwZnolMkJYSk5VZGhpa1ZqZjU4dVc2MlFrbUxXTXJxbE1DWjF3dDZkRklxdHNYTXFEOVFMUTB0UVElMkY3UWw0dSUyRkt6ZHdzMDJRNGtRWkpjSHlyWE5VUnY0MUZYYWZtc0tuWlRIY3Z5eG11eFVScDRYNnkySnY5ZyUyRktYQU04U1FTa1BzckUxV0IxTmxFSVZySjR6anc2aHFLcktJY0E4ZkJQVEtucjdzRG1FMDlubHRyWWpDc2ZPZGQ3d0lwcDFSZlFnMWY5d2hSeHUydWxlU3lVbzduMmdhYW5oQ1RWV2hmTGRsSGtlczNKZyUzRCUzRA; _gat_gtag_UA_38224966_1=1; kampyleUserSession=1743578222290; kampyleUserSessionsCount=8; kampyleSessionPageCounter=1; _ga=GA1.1.516804259.1743510056; __uzmc=6676422038450; __uzmd=1743578246; _ga_MZBX8BWCCN=GS1.1.1743574029.2.1.1743578252.20.0.0; _yi=1%3AeyJsaSI6eyJjIjowLCJjb2wiOjE2NDk2MzkwNjgsImNwZyI6MjY2NTcwLCJjcGkiOjUxMTM4ODExMTA5LCJzYyI6MSwidHMiOjE3NDM1MTAwNjAzNTR9LCJzZSI6eyJjIjoyLCJlYyI6NTMsImxhIjoxNzQzNTc4MjU1ODUwLCJwIjo5LCJzYyI6NDIxNH0sInUiOnsiaWQiOiJjYzhmNDk5OC04ZWQ1LTQ3OTItOWVhMi1mM2Q1MWVmZWI2ZTUiLCJmbCI6IjAifX0%3D%3ALTE4MDY5MDc0ODg%3D%3A99',
        }


        api_url = f'https://www.liquorland.com.au/api/products/ll/vic/{Category_Url_ls[0]}?page={page_no}&sort=&show=60&facets={Category_Url_ls[1]}'
        scraperurl = f"http://api.scraperapi.com?api_key={scraper_api_key}&url={api_url}"

        response = obj.to_requests(url = api_url, headers = headers, html_path = full_path,should_be = ['"products"'], proxies = proxies, verify=False)

        if not response:
            Hprint("Getting Blank Response.....", api_url)
            category_input.update_one({'_id': ID}, {'$set': {'Status': "Not found"}})
            Rprint("Status updated as Result Not Found...")
            return None

        elif 'VerifyHuman' in response:
            Rprint("Captcha Not Resolved after all retries executed...")

        elif 'Result Not Found' in response or 'This product is invalid.' in response or 'This page could not be found' in response:
            category_input.update_one({'_id':ID}, {'$set':{'Status': "Not found"}})
            Rprint("Status updated as Result Not Found...")

        elif response:
            Gprint("Getting Correct Response...")
            res_json = json.loads(response)

            # products[0].category
            products = res_json['products']
            if products:
                for items in products:
                    # continue

                    product_id = items['sellItemId']
                    if not product_id:
                        product_id = items['id'].split("_")[0]

                    Name = items['name']
                    productUrl = items['productUrl']
                    ProductURL = f"https://www.liquorland.com.au{productUrl}"

                    offer_info = items.get('promotion', {}).get('calloutText')
                    Price = items.get("price").get("current")
                    WasPrice =  items.get("price").get("normal")
                    if not Price and WasPrice or WasPrice == Price:
                        Price = WasPrice
                        WasPrice = None

                    if not Price and not WasPrice:
                        product_data.update_one({'_id': ID}, {'$set': {'Status': "Done_1"}})
                        Gprint("✅ Status updated as Result ℹ️ Done...")
                        continue

                    # try:
                    #     per_unit_price = items['pricePerUnit']
                    #     if not per_unit_price:
                    #         per_unit_price = ""
                    # except:
                    per_unit_price = ""

                    try:
                        abbreviation = items.get('unitOfMeasureLabel', "") or ""
                        PackageSize = f"{abbreviation}".strip()
                    except:
                        PackageSize = ""

                    product_images = get_product_images(product_id, PackageSize)
                    # print(product_images)

                    product_images = "|".join(product_images)

                    breadcrumbs = items['category']

                    brand = items.get('brand', "")
                    if not brand:
                        brand = ""

                    is_available = items['isAvailable']

                    items = {}
                    items["full_path"] = full_path
                    items["Category_Url"] = Category_Url
                    items["Category_Name"] = breadcrumbs
                    items["ProductURL"] = ProductURL
                    items["ProductCode"] = product_id
                    items["Name"] = Name
                    items["Price"] = Price
                    items["WasPrice"] = WasPrice
                    items["RRP"] = WasPrice if WasPrice else Price
                    items["per_unit_price"] = per_unit_price
                    items["Offer_info"] = offer_info
                    items["Pack_size"] = PackageSize
                    items["Barcode"] = ""
                    items["retailer_name"] = "liquorland"
                    items["Category_Hierarchy"] = breadcrumbs
                    items["Brand"] = brand
                    items["Promo_Type"] = ""
                    items["Images"] = product_images
                    items["is_available"] = is_available
                    items["Status"] = "Done"

                    try:
                        product_data.insert_one(items)
                        print("Product Data Inserted...")

                    except Exception as e:
                        if 'duplicate key error' not in str(e):
                            print(e)

                if not total_result:
                    total_pages = res_json['meta']['page']['total']

                if page_no < total_pages:
                    Yprint("Going for next page -->", page_no)
                    page_no += 1

                    data_extraction(cat_item, total_pages, page_no, total_result)

                else:
                    Yprint("Next Page is not Available...")
                    category_input.update_one({'_id':ID}, {'$set':{'Status': "Done"}})
                    Bprint("status updated...")

            else:
                Yprint("Not Found Data In Next Page....")
                category_input.update_one({'_id':ID}, {'$set':{'Status': "Done"}})
                Bprint("status updated...")

        else:
            Rprint("Somthing Went Wrong in Requests...")


    except Exception as e:
        Rprint(f"Error in Main Data Extraction function ",e)


if __name__ == '__main__':

    Gprint(f"----- Main open ------- ")
    total_count = category_input.count_documents({'Status': 'Pending'})

    while total_count:
        total_count = category_input.count_documents({'Status': 'Pending'})
        if not total_count:
            break

        Yprint("Total Pending....",total_count)
        if total_count >= 25:
            variable_count = total_count // 25
        else:
            variable_count = total_count // total_count

        if variable_count == 0:
            variable_count = total_count ** 2

        count = 1
        threads = [Thread(target = PL_Extraction,args = (i, variable_count)) for i in
                   range(0, total_count, variable_count)]

        for th in threads:
            th.start()
        for th in threads:
            th.join()

        Hprint(f"--------- Thread Ends ----------- ")
        time.sleep(5)

    if category_input.count_documents({'Status':'Pending'}) == 0:
        Gprint("All Count Done...")
