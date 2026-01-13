import json
import math
import re, unicodedata
import time
from parsel import Selector
from urllib.parse import quote
import scrapy
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from pricemate.spiders.base_spider import PricemateBaseSpider

cookies = {
    'SPC_F': '0AXhSdTWf9nAuk2tNbe3kUeroYC3nWiu',
    'REC_T_ID': '8b9ef820-9a07-11f0-b184-caf6988b41b1',
    '_QPWSDCXHZQA': 'dfc64379-ddad-4f3d-cf8d-4204d8c810e8',
    'REC7iLP4Q': '11e6e0de-2f01-4d05-8d64-98099cf9752f',
    'SPC_SEC_SI': 'v1-U1ZvSWVpSVF4c0hQQmlSTEiN0HMcd3WcRLRmr8iMfTKKeIDyzXAXBopEYBM/ec5CBwe99lnBLBYiDTkN1yKJH04o8Az6IpYjHDsuNHq4qxk=',
    'SPC_SI': 'fz7jaAAAAABrNzcxTm5CZdFSBAAAAAAAblB1dHh1Wjk=',
    'SPC_CLIENTID': 'MEFYaFNkVFdmOW5Biucaaueswsfyflkd',
    'SPC_ST': '.VmcxdDRWaWRBRHlNVXNxUbQozHeD2ZXK2GNpx/9zyI1plrwuqhJINj0VxjtWYyXZxiOPh83pr261mB11Jr1pJUU0vJKm5JHIQRIDl/QpTCKh19CVXBbxorqTF094mZTdsbf70TTXCBdIfXqvHiWdYN++RCTtVvc/+rrPpUeDgNkvTgWMiZVV3p4ymnjOrTWsQbg2My8NGExqjP0RYkt/Olq7pOZ4VdtAvjve2EufZHsWEd+IOag2kCRcg80pAWC1s+KPAaalPRkewIXPvZbiqg==',
    'SPC_U': '1648708561',
    'SPC_T_IV': 'ODdiYmFWaUtPZkRQbmRYYg==',
    'SPC_R_T_ID': 'XmOnWKGNfXbCFPgaM9xoo87BU80BwvgFK4qB0rH+/DK6MVUuhR6h4z1brAMmWwI9T2rsI5viqU0Y2kWBBi+2slkqtjIP8l0GNSld/EAt36e0H5BEgvkWa8rWw0yTpP40oIRPq5Gg0BM+Q+0JDuVEd/jDdBY6UWXMPY58S1kpIdU=',
    'SPC_R_T_IV': 'ODdiYmFWaUtPZkRQbmRYYg==',
    'SPC_T_ID': 'XmOnWKGNfXbCFPgaM9xoo87BU80BwvgFK4qB0rH+/DK6MVUuhR6h4z1brAMmWwI9T2rsI5viqU0Y2kWBBi+2slkqtjIP8l0GNSld/EAt36e0H5BEgvkWa8rWw0yTpP40oIRPq5Gg0BM+Q+0JDuVEd/jDdBY6UWXMPY58S1kpIdU=',
    'csrftoken': '1yCEaoeXuIWwsx9gS5Rij98uZ29AtmSm',
    '_sapid': 'a84ee458c7613130ad13285ad794082f051cae5e22f6601ba6574e56',
    'SPC_CDS_CHAT': 'cdb88010-ecd0-4370-a56f-8998cc3594f8',
    'SPC_EC': '.YWpVaHYza0lSbHB6RFg0SFKQMXV0PgQpUDg9MwYafnM9+0aJRGrXh094FfaL8qLE6WUWH4Us5PIqA3w3cdoDQsNWjU8M3tLhYemT8Q954ua/XW4/HrSTFMbY6jJrfVa6x3eA2qbl1lIEJDbBJEqPdky65oNClX4H0GfiWtL8AY9FjHsRTX72c0P4qjE52tZbgeE45hP7eWA3rrf+drmscKrhpL8NhdSs9U7SBHXJsgkMA45zrolDwqt240KvsyTYOmrpjPfAsw+fg2ubfaVNMA==',
    'shopee_webUnique_ccd': 'ngJfVvs3BNeX2Vhzm3dS1A%3D%3D%7CCRqp0gJY%2F%2Fltt3bj2u4GVVxcWA8iOkZRyRJdarMqer8aA%2BkigIptL5%2Bcsi9f%2Bc0eVUtRRBWNRqzIvQ%3D%3D%7CZt3L1%2BtGk7CdaMdH%7C08%7C3',
    'ds': 'c65731baf53402da16e4db2115956ee6',
}

headers = {
    'Accept': '*/*',
    'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8',
    'Connection': 'keep-alive',
    'If-None-Match-': '55b03-ae89cdd793acbfe9d2adb7499e6c6fd7',
    'Referer': 'https://shopee.co.id/supermarket',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36',
    'X-API-SOURCE': 'pc',
    'X-Requested-With': 'XMLHttpRequest',
    'X-Shopee-Language': 'id',
    'af-ac-enc-dat': '7c7a51b0cd7b2d4b',
    'af-ac-enc-sz-token': 'ngJfVvs3BNeX2Vhzm3dS1A==|CRqp0gJY//ltt3bj2u4GVVxcWA8iOkZRyRJdarMqer8aA+kigIptL5+csi9f+c0eVUtRRBWNRqzIvQ==|Zt3L1+tGk7CdaMdH|08|3',
    'sec-ch-ua': '"Chromium";v="140", "Not=A?Brand";v="24", "Google Chrome";v="140"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'x-sap-ri': '1ba6e368588a031ea198203b070135792ca4be932e64fe8fb850',
    'x-sap-sec': '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',
    'x-sz-sdk-version': '1.12.22-1',
    # 'Cookie': 'SPC_F=0AXhSdTWf9nAuk2tNbe3kUeroYC3nWiu; REC_T_ID=8b9ef820-9a07-11f0-b184-caf6988b41b1; _QPWSDCXHZQA=dfc64379-ddad-4f3d-cf8d-4204d8c810e8; REC7iLP4Q=11e6e0de-2f01-4d05-8d64-98099cf9752f; SPC_SEC_SI=v1-U1ZvSWVpSVF4c0hQQmlSTEiN0HMcd3WcRLRmr8iMfTKKeIDyzXAXBopEYBM/ec5CBwe99lnBLBYiDTkN1yKJH04o8Az6IpYjHDsuNHq4qxk=; SPC_SI=fz7jaAAAAABrNzcxTm5CZdFSBAAAAAAAblB1dHh1Wjk=; SPC_CLIENTID=MEFYaFNkVFdmOW5Biucaaueswsfyflkd; SPC_ST=.VmcxdDRWaWRBRHlNVXNxUbQozHeD2ZXK2GNpx/9zyI1plrwuqhJINj0VxjtWYyXZxiOPh83pr261mB11Jr1pJUU0vJKm5JHIQRIDl/QpTCKh19CVXBbxorqTF094mZTdsbf70TTXCBdIfXqvHiWdYN++RCTtVvc/+rrPpUeDgNkvTgWMiZVV3p4ymnjOrTWsQbg2My8NGExqjP0RYkt/Olq7pOZ4VdtAvjve2EufZHsWEd+IOag2kCRcg80pAWC1s+KPAaalPRkewIXPvZbiqg==; SPC_U=1648708561; SPC_T_IV=ODdiYmFWaUtPZkRQbmRYYg==; SPC_R_T_ID=XmOnWKGNfXbCFPgaM9xoo87BU80BwvgFK4qB0rH+/DK6MVUuhR6h4z1brAMmWwI9T2rsI5viqU0Y2kWBBi+2slkqtjIP8l0GNSld/EAt36e0H5BEgvkWa8rWw0yTpP40oIRPq5Gg0BM+Q+0JDuVEd/jDdBY6UWXMPY58S1kpIdU=; SPC_R_T_IV=ODdiYmFWaUtPZkRQbmRYYg==; SPC_T_ID=XmOnWKGNfXbCFPgaM9xoo87BU80BwvgFK4qB0rH+/DK6MVUuhR6h4z1brAMmWwI9T2rsI5viqU0Y2kWBBi+2slkqtjIP8l0GNSld/EAt36e0H5BEgvkWa8rWw0yTpP40oIRPq5Gg0BM+Q+0JDuVEd/jDdBY6UWXMPY58S1kpIdU=; csrftoken=1yCEaoeXuIWwsx9gS5Rij98uZ29AtmSm; _sapid=a84ee458c7613130ad13285ad794082f051cae5e22f6601ba6574e56; SPC_CDS_CHAT=cdb88010-ecd0-4370-a56f-8998cc3594f8; SPC_EC=.YWpVaHYza0lSbHB6RFg0SFKQMXV0PgQpUDg9MwYafnM9+0aJRGrXh094FfaL8qLE6WUWH4Us5PIqA3w3cdoDQsNWjU8M3tLhYemT8Q954ua/XW4/HrSTFMbY6jJrfVa6x3eA2qbl1lIEJDbBJEqPdky65oNClX4H0GfiWtL8AY9FjHsRTX72c0P4qjE52tZbgeE45hP7eWA3rrf+drmscKrhpL8NhdSs9U7SBHXJsgkMA45zrolDwqt240KvsyTYOmrpjPfAsw+fg2ubfaVNMA==; shopee_webUnique_ccd=ngJfVvs3BNeX2Vhzm3dS1A%3D%3D%7CCRqp0gJY%2F%2Fltt3bj2u4GVVxcWA8iOkZRyRJdarMqer8aA%2BkigIptL5%2Bcsi9f%2Bc0eVUtRRBWNRqzIvQ%3D%3D%7CZt3L1%2BtGk7CdaMdH%7C08%7C3; ds=c65731baf53402da16e4db2115956ee6',
}

class SupermarketCateSpider(PricemateBaseSpider):
    name = "supermarket_cate"

    def __init__(self, retailer, region, *args, **kwargs):
        super().__init__(retailer=retailer, region=region, *args, **kwargs)



    def start_requests(self):
        url = 'https://shopee.co.id/api/v4/traffic/page_component/get_mart_home_page?feature_toggle=mixed_category_module&is_cc_installment_payment_eligible=true&is_non_cc_installment_payment_eligible=true'

        yield scrapy.Request(
            url=url,
            cookies=cookies,
            headers=headers,
            callback=self.get_cat,
            meta={
                "url": url,
                "filename": f"cat_{self.generate_hash_id(url)}.html",
                "should_be": ["data"]
            }

        )
    def get_cat(self, response):

        try:
            json_data = json.loads(response.text)
        except Exception as e:
            self.logger.error("❌ Failed to parse JSON: %s", e)
            return

            # Debug: confirm top-level shape
        print("in get_cat() — top keys:", list(json_data.keys()))
        components = json_data.get("data", {}).get("page", {}).get("data", [])
        print("components count:", len(components))

        found = False
        for comp in components:
            if comp.get("component_type_id") == "mixed_category_module":
                found = True
                homepage_categories = comp.get("data", {}).get("data", {}).get("homepage_categories", []) or []
                print("homepage_categories count:", len(homepage_categories))

                inserted = 0
                for entry in homepage_categories:
                    category = entry.get("category") or {}
                    catid = category.get("catid")
                    parent_catid = category.get("parent_catid")
                    display_name = category.get("display_name") or category.get("default_name") or ""

                    if not (catid and parent_catid and display_name and display_name.strip()):
                        print("  skipping malformed category:", category)
                        continue

                    # Inline cleaning: preserve case, remove problematic chars, replace spaces -> '-'
                    name_clean = re.sub(r"[^\w\s-]", "", display_name).strip()
                    name_clean = re.sub(r"[\s]+", "-", name_clean)

                    cate_url = f"https://shopee.co.id/supermarket/{name_clean}-cat.{parent_catid}.{catid}"
                    print("  built:", cate_url)

                    try:
                        hash_id = self.generate_hash_id(cate_url, self.retailer, self.region)
                        self.category_input.update_one(
                            {"_id": hash_id},
                            {"$set": {
                                "url": cate_url,
                                "Status": "Pending",
                                "retailer": self.retailer,
                                "region": self.region
                            }},
                            upsert=True
                        )
                        inserted += 1
                        print("   ✅ Inserted:", cate_url)
                    except Exception as e:
                        self.logger.error("❌ Mongo update failed for %s: %s", cate_url, e)

                print("Finished component — inserted/updated:", inserted)
                break

        if not found:
            print("mixed_category_module NOT found in components (structure changed?)")

    def close(self, reason):
        self.mongo_client.close()

if __name__ == '__main__':
    from scrapy.cmdline import execute
    execute(
        "scrapy crawl supermarket_cate -a retailer=shopee_supermarket_id -a region=id -a Type=eshop -a RetailerCode=shopee_supermarket_id".split())