import datetime
import json

from Common_Modual.common_functionality import *
import pymongo
import os
from datetime import datetime
from dateutil.relativedelta import relativedelta, MO

# first_monday_date = (datetime.datetime.today() + relativedelta(weekday=MO(0))).date()
# Today1 = (datetime.today() + relativedelta(weekday=MO(1))).date()
Today1 = datetime.today()
obj = RequestsManager()

website = "Coles"
today = Today1.strftime("%Y_%m_%d")
# today = "2025_10_24"

conn = pymongo.MongoClient("mongodb://localhost:27017/")
db = conn[f"pricemate_eshop_coles_au"]

category_input = db['Category_Input']
coll_list = db.list_collections()


def get_current_api_version():
    import requests

    url = "https://www.coles.com.au/browse/down-down/beverages"

    payload = {}
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'en-US,en;q=0.9',
        'cache-control': 'max-age=0',
        'cookie': 'visid_incap_2800108=kkHlWjHHREuVtQQ5w9OLBAIyGmcAAAAAQUIPAAAAAACPV+rOKbqY7jFlUx0xytxS; incap_ses_968_2800108=6lWpfEFuTh42VfwOFwdvDQIyGmcAAAAANb8kzSN336vXFLxKmnlojg==; incap_ses_330_2800108=pi6XXS7JNBlqpeGwc2WUBAgyGmcAAAAAFXaseICcaZf8vNXsYcY9TA==; ApplicationGatewayAffinityCORS=ce1dd33cb7cfcf721c38e4c63f5c6894; ApplicationGatewayAffinity=ce1dd33cb7cfcf721c38e4c63f5c6894; nlbi_2800108=2wdXGBO4Fy2mrO2IjQyMFgAAAACy9BNaCYddWCnMJFihuZ2o; reese84=3:RYc44nE0iEk8KZg+PGQMqg==:lzyApTeeBniZRq4pS6vXj0aTTyQYclv1T9AuazdwBV8osd1ndGWTr5xz1uaatueQoSO0T8sAv7Dz4twCOj+W8W8oDKW8KD96PgIkZeJkIysc1cY7DMvLrz8H5xz69o0iorLI1MXxAEuCE4BBJYw3dMJDgqBrhePbOsApEM3VgM1y5fxm3QDbyGw7BkmjbMPJPTDYcYPq4oDYUX2X1/Uov5mvJfeD7eDYDz/ol9R2qOdXDGt5JEf3pHxENsFkbkr6gV6/Hben/ABl/4LRIzpXVPTzOZQ73gwSNjAyLmcKWcAUN5T+SDMN3Yu2VLXKdP8uAxHEnd9zYmIpkStzzXDHbqNhs/XDx3rce+8b+MZ0mJ+PVcf6Gb3y2fpmumYs6g9PQm9w3M38qrTGbDhwEKwiac5QIH7u8kZINA22MfeG51fZRfDO+triVFRR/3bUTm50/hk0P6GOtclIyajupoEYTzmAHo8Nm/4unE/D9WNIikc=:A8Y5HH+tfjUDMZDNIx4//6iMtP+t4kbrLxJ7EB4FXLs=; nlbi_2800108_2670698=s/UbO/jrBFrBZMOyjQyMFgAAAAAWOoGtFdauAXgDlzU6Yxg3; nlbi_2800108_2147483392=aHSRRCHmY2xAe13LjQyMFgAAAADM1bAmPpoKcEIkXC8htcVG; ld_user=4d6d8c7b-3f5a-4923-ae9c-f03f939a69c2; sessionId=8e998d5c-8d68-4172-9766-cbdf6f93d366; visitorId=c6aef8c0-230d-47b2-8797-13899485ca57; AMCVS_0B3D037254C7DE490A4C98A6%40AdobeOrg=1; analyticsIsLoggedIn=false; AMCV_0B3D037254C7DE490A4C98A6%40AdobeOrg=179643557%7CMCIDTS%7C20021%7CMCMID%7C19139805243360655640853082410849548668%7CMCAAMLH-1730374799%7C8%7CMCAAMB-1730374799%7CRKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y%7CMCOPTOUT-1729777200s%7CNONE%7CMCAID%7CNONE%7CvVersion%7C5.5.0; at_check=true; fs_lua=1.1729770001648; gpv_page=cusp%3Ahome; fs_uid=#o-210D95-na1#a5910935-f13b-4e70-8a16-9ce5a8732d96:d028310a-030f-412b-b0c8-e72438f9ed50:1729770001648::1#74a7a6de#/1761306003; s_cc=true; _gcl_au=1.1.1709473255.1729770005; kndctr_0B3D037254C7DE490A4C98A6_AdobeOrg_identity=CiYxOTEzOTgwNTI0MzM2MDY1NTY0MDg1MzA4MjQxMDg0OTU0ODY2OFIRCMS8zvKrMhgBKgRBVVMzMAPwAcS8zvKrMg==; kndctr_0B3D037254C7DE490A4C98A6_AdobeOrg_cluster=aus3; _ga=GA1.1.124555730.1729770007; ORA_FPC=id=20b9ee88-0b15-4fda-8557-c08b2d802c26; WTPERSIST=; _fbp=fb.2.1729770007146.657028745441558762; BVBRANDID=ecd47f60-616a-469a-97f6-9756a8879a1a; BVBRANDSID=1fad4895-7f11-47a3-96bc-cda24f9410a2; mbox=session#d7ef1154377b45e5851aca908efde116#1729771882|PC#d7ef1154377b45e5851aca908efde116.36_0#1793014805; s_ecid=MCMID|19139805243360655640853082410849548668; dsch-sessionid=3e841b93-b77d-4e39-890b-0619f86fd8aa; dsch-visitorid=fe72025d-6dda-4b51-9798-ad3b318ad620; ad-memory-token=cCPxZrwbQhqZJLNiVKO2LBL5x50KRQoMEgoKCDM1Mjc5NTdQCgwSCgoIMzAzODkzOVAKDBIKCgg4MDIwNjgwUAoMEgoKCDcwMzU4NzRQEgsIpeTouAYQ9oLZexoCCAIiAA%3D%3D; _ga_C8RCBCKHNM=GS1.1.1729770007.1.1.1729770023.44.0.0; s_ips=350; s_tp=6756; s_sq=colesonline-coles-global-prod%3D%2526c.%2526a.%2526activitymap.%2526page%253Dcusp%25253Abrowse%25253Aproduct-categories%2526link%253Dcoca-cola%252520classic%252520soft%252520drink%252520bottle%252520%25257C%252520600ml%252520down%252520down%252520%2525244.00%252520%2525246.67%252520per%2525201l%252520was%252520%2525244.25%252520on%252520aug%2525202024%252520add%2526region%253Dproduct-tiles%2526pageIDType%253D1%2526.activitymap%2526.a%2526.c%2526pid%253Dcusp%25253Abrowse%25253Aproduct-categories%2526pidt%253D1%2526oid%253Dfunctionry%252528%252529%25257B%25257D%2526oidt%253D2%2526ot%253DSECTION; s_ppv=cusp%253Abrowse%253Aproduct-categories%2C5%2C11%2C10%2C749%2C19%2C2; incap_ses_606_2800108=3lmRH/2tSlFF2uCm+PFoCBU0GmcAAAAAPDSayFxXeGnK7f8WQIV+MA==; s_ecid=MCMID|19139805243360655640853082410849548668; ad-memory-token=%2Fx%2BwElLXn0AqKvjqaUwKrqHL66AKRQoMEgoKCDM1Mjc5NTdQCgwSCgoIMzAzODkzOVAKDBIKCgg4MDIwNjgwUAoMEgoKCDcwMzU4NzRQEgsIlejouAYQh%2BqxMxoCCAIiAA%3D%3D; dsch-sessionid=3e841b93-b77d-4e39-890b-0619f86fd8aa; dsch-visitorid=fe72025d-6dda-4b51-9798-ad3b318ad620',
        'priority': 'u=0, i',
        'referer': 'https://www.coles.com.au/?srsltid=AfmBOoqFg8lD54P-5ZCYKnJJNHRDJLV1bV9-nPXCFCdulwd9w0LA-SBE',
        'sec-ch-ua': '"Chromium";v="130", "Google Chrome";v="130", "Not?A_Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36'
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    selector_res = Selector(response.text)

    script_json = selector_res.xpath('//script[@id="__NEXT_DATA__"]//text()').get()
    print(script_json)
    try:
        script_json = json.loads(script_json)

        current_api_version = script_json['buildId']

        open('api_version.txt', 'w').write(current_api_version)
        print("Successfully updated api_version.txt....", current_api_version)

    except:
        pass

print(f'Product_Data_{today}' not in coll_list)
if f'Product_Data_{today}' not in coll_list:
    get_current_api_version()
    category_input.update_many({}, {"$set": {"Status":"Pending"}})

api_version = open('api_version.txt').read().strip()

product_data = db[f'Product_Data_{today}']

product_data.create_index("ProductCode",unique = True)


# Base path
base_path = f"E:\\Data\\Crawl_Data_Collection\\PriceMate\\{website}\\{today}"

# Define paths for different file types
html_path = os.path.join(base_path, "Data_Files", "HTML_Files")
excel_path = os.path.join(base_path, "Data_Files", "Excel_Files")

# Create directories
os.makedirs(html_path, exist_ok=True)
os.makedirs(excel_path, exist_ok=True)

print(f"HTML files path: {html_path}")
print(f"Excel files path: {excel_path}")




