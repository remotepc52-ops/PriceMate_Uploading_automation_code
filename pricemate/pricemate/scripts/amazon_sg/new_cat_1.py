from config import *
import requests
from parsel import Selector

headers = {
    'sec-ch-ua-platform': '"Windows"',
    'viewport-width': '1536',
    'device-memory': '8',
    'sec-ch-ua': '"Chromium";v="140", "Not=A?Brand";v="24", "Google Chrome";v="140"',
    'sec-ch-dpr': '1.25',
    'sec-ch-ua-mobile': '?0',
    'X-Requested-With': 'XMLHttpRequest',
    'Accept': 'text/html, */*; q=0.01',
    'sec-ch-viewport-width': '1536',
    'downlink': '1.45',
    'ect': '3g',
    'Referer': 'https://www.amazon.sg/alm/storefront?almBrandId=QW1hem9uIEZyZXNo',
    'sec-ch-device-memory': '8',
    'dpr': '1.25',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36',
    'rtt': '300',
    'sec-ch-ua-platform-version': '"19.0.0"',
}

params = {
    'ajaxTemplate': 'hamburgerMainContent',
    'pageType': 'FreshMerchandisedContent',
    'hmDataAjaxHint': '1',
    'navDeviceType': 'desktop',
    'isSmile': '0',
    'RegionalStores[]': [
        'QW1hem9uIEZyZXNo',
        'WDpqStVxNA',
        'KQENHJywk4',
    ],
    'isPrime': '0',
    'isBackup': 'false',
    'hashCustomerAndSessionId': '70d8313dee318af6d6e00df4ededbe7e8186f65b',
    'languageCode': 'en_SG',
    'environmentVFI': 'AmazonNavigationCards/development@B6370485488-AL2_aarch64',
    'secondLayerTreeName': 'AmazonPrimeVideo+amazon_fresh_store+Little_Farms+watsons+home_kitchen+diy-tools-and-auto+toys_games_crafts+sports_fitness_and_outdoors+computers_office+clothing_shoes_and_watches+electronics+mobile_smart_tech+books+music_dvd_and_blu_ray+video_games+health_household_personal_care+pets_supplies+beauty_and_grooming+baby+grocery+beer_wines_and_spirits+business_industry_science+global_store',
    'customerCountryCode': 'SG',
}

response = requests.get('https://www.amazon.sg/nav/ajax/hamburgerMainContent', params=params,proxies=proxies,verify='zyte-ca.crt', headers=headers)
print(response.status_code)
if response.status_code == 200:
    raw = response.json()
    html = raw.get("data", "")
    sel = Selector(text=html)

    for section in sel.css("section.category-section"):
        category = section.css(".hmenu-title::text").get()
        if category:
            category = category.strip()

        # ✅ Only process if the category is "Amazon Fresh"
        if category and category.lower() == "amazon fresh":
            for link in section.css("a.hmenu-item"):
                name = link.xpath("normalize-space(text())").get()
                url = link.attrib.get("href")

                if name and url:
                    full_url = "https://www.amazon.sg" + url if url.startswith("/") else url
                    doc = {
                        "category": category,
                        "name": name,
                        "url": full_url,
                        "Status": "Pending"
                    }
                    search_data.update_one(
                        {"url": doc["url"]},
                        {"$set": doc},
                        upsert=True
                    )
                    print("Inserted:", doc)
else:
    print("Request failed:", response.status_code)