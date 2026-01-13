import json
import os, sys
import re

import scrapy
from scrapy.http import JsonRequest
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from pricemate.spiders.base_spider import PricemateBaseSpider

cookies = {
    'splitSessionKey': '196382_GUEST',
    'connect.sid': 's%3ALTRZS5ezpaWUTL924mMRGVlssv0_p0P9.BcfKvNrWS0Ilp598F4v7sMwM7zMqvcajPBXN%2F4qNV2I',
    '_gcl_au': '1.1.617840886.1755589510',
    '_gid': 'GA1.3.952541996.1755589512',
    '_fbp': 'fb.2.1755589512045.969518376747507916',
    'ajs_anonymous_id': '1b9097aa-07a7-4637-84aa-05003fa0b1a9',
    'BVBRANDID': '0ee521a3-f8ba-4ba5-b928-b9683722f58a',
    'BVImplmain_site': '15457',
    '_dyid_server': '3175037975273696913',
    'sdt': '9ba0c59a-d0ea-4f16-8099-2ba4c86a4b31',
    'auth_token': '',
    'bm_mi': '0148AC1DB30D4E773ACAD373D73E59C8~YAAQBagRYLk4QquYAQAAHsbSwRw2pTDyxzbrsiAyZUFYTVqGkNfjvPHNM3h1xE0FXMb+XQP5xqq2Y3JPgRIxEQqZIeR0w+PNpGBI49T8qSeVuh6lGUsY4o1tx3ScGPYA+nz8CEzRLxMuQ9tg4iCqANp0z/hiyiGKDaMq2TI8xwqiqJszJBsvkKFhorv22NfsqtdbFVPunMGngX5MesqM1LQwanntJ3N2u3YWCuHSi3f8ttkQlBFd+wor8RaawzsuAtIXVO7GmUZjcTV6D1XXQvv9Hx6sIs+LwtT8VtSsj0VNL4vddDdCG+M7ZG76oQj7IW/DgTuMc+O7FxCVWy45eGlMEVMW4XTIPtzd2A5G3w==~1',
    'bm_sv': '64849C5222A784F56BD24C70C124FDE7~YAAQBagRYLo4QquYAQAAH8bSwRxZcxWqF2Uq/znMUQSHFpSATnws63GTVVysDbkLv/STVsnI+f2abBsPqcAJvI8hEECSOuS3T+WCTkviHhsLYMuQ2DpT6feOa0tb8rYEqhK6xMvWk8JW/3eaTbR4rVePy2fG5H3cGlBBEPUT1Hy5QvWyPLeRN+9wWS/LZKcpYIji4Jtf/D9mGw9fVMIaJ+V1M2mX8+s541SoMS19S9hv4RMQXlK76yw6QZIzWUCryFaF9yjX~1',
    'ak_bmsc': '42F6451C85DBFB554044DFEABD5DA030~000000000000000000000000000000~YAAQ9u/IF64mS7GYAQAAtTHdwRycXhzMMzmND8dWKG0x4kcIweoTkMt0yohl/qnLSSQzC6xzVU364xWIvu4FLoIRdoEjHkaV120LjQIIs8ZFd6ZkajyYGB9KawfhT9Yg4L7rwftng8xsrU54o/e1wjW9omPuBkvmiXIlgp8eUZ126mNEa12B0k9Qg1nRgzqpLragqLCrPXSgVPzno6E+zZklUPivjhK0ufIiSRx3kUMot7ishYTwU9M54zeMcpw5+JJ6poM4ihNpGTF6SKYwmiaN6WS6YzWMeyulYF6UjWRztrIBmOWoRvL+/RO/3Q6ytlkloPAx/QCvYLuOwX437W3bFA84bjX4P/aumO2V8CLW2Or9gp+Ot3RHTyuC8+NrtEvto3rxeLT7ngNOzQaeffhnKs2piPykprnjNGYLAsZ2mHc7BALWw1Tl5y3Gf4N7lrZg5kBCsnMtEcQnQTMAI1lOBQ==',
    '_tt_enable_cookie': '1',
    '_ttp': '01K30Z1ZQ4JJRC06R2FZ1RDWYR_.tt.2',
    'ttcsid': '1755600453361::W_ROUJRITGuL2FWtbqQJ.1.1755600453361',
    'BVBRANDSID': '0a23e555-1c5a-43da-b3ff-3ecd8cdac2e1',
    'ttcsid_C6EVLQAR90G6DE87S3HG': '1755600453357::fMiEUetVcIsDlX5zgyx0.1.1755600470974',
    '__rtbh.lid': '%7B%22eventType%22%3A%22lid%22%2C%22id%22%3A%22tdVLI7A2U7M8oWs3VRuL%22%2C%22expiryDate%22%3A%222026-08-19T10%3A50%3A21.826Z%22%7D',
    '_ga': 'GA1.3.1526938207.1755589511',
    'amp_2050dd_fairprice.com.sg': 'AAbxsUaG43u1JKIIHXfarn...1j30sl2ib.1j30vc3ie.1h.0.1h',
    '__rtbh.uid': '%7B%22eventType%22%3A%22uid%22%2C%22id%22%3A%22undefined%22%2C%22expiryDate%22%3A%222026-08-19T11%3A04%3A39.042Z%22%7D',
    'amp_2050dd': 'AAbxsUaG43u1JKIIHXfarn...1j30slbta.1j31019fj.n.0.n',
    '_dyjsession': 'ug8mtcyno3sdp57mngq8jdvnaf894d5a',
    'analytics_session_id': '1755597942698',
    'analytics_session_id.last_access': '1755601484262',
    '_gat_UA-52974559-8': '1',
    '_ga_J1DDCJKLXQ': 'GS2.1.s1755589511$o1$g1$t1755601554$j60$l0$h0',
    '_dd_s': 'rum=2&id=14518e21-fc4b-49dc-af81-a4215e68721a&created=1755597938823&expire=1755602425819',
}

headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'en-US,en;q=0.9',
    'cache-control': 'max-age=0',
    'priority': 'u=0, i',
    'sec-ch-ua': '"Not;A=Brand";v="99", "Google Chrome";v="139", "Chromium";v="139"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36',
}

class FairpricePdpSpider(PricemateBaseSpider):
    name = "fairprice_pdp"

    def __init__(self, retailer, region, *args, **kwargs):
        super().__init__(retailer=retailer, region=region, *args, **kwargs)

    def start_requests(self):

        docs = self.product_table.find({
            "retailer": self.retailer,
            "region": self.region,
            "Status": "Pending"
        })
        for doc in docs:
            url = doc.get("ProductURL")
            hash_id = doc.get("_id")
            parent = doc.get("parent_id")
            slug = url.split("product/")[-1].split("/")[0]

            meta = {
                "url": url,
                "_id": hash_id,
                "Parent_id": parent,
                "filename": f"PDP_{slug}_page.html",
                "should_be": ["__NEXT_DATA__"]
            }
            yield scrapy.Request(
                url,
                cookies=cookies,
                headers=headers,
                callback=self.process_category,
                meta=meta
            )
    def process_category(self, response):
        meta = response.meta
        referer_url = meta.get("url")
        doc_id = meta.get("_id")
        parent_id = meta.get("Parent_id")

        data = response.xpath('//div[@class="sc-747538d2-0 dJBCT"]')
        for prod in data:
            orignal_price = prod.xpath('//span[@class="sc-ab6170a9-1 sc-747538d2-5 jBFJrC eQpgNG"]/text()').get()
            was_price = prod.xpath('//div[@class="sc-747538d2-4 gUoXMU"]//span/text()').get()
            orignal_price = float(orignal_price.replace("$", "").replace(",", "").strip()) if orignal_price else None
            was_price = float(was_price.replace("$", "").replace(",", "").strip()) if was_price else ""
            if was_price:
                rrp = was_price
            else:
                rrp = orignal_price
            # -------- Offer 1 --------
            promo_text_list = prod.xpath('//span[@class="sc-ab6170a9-1 hdrKgd"]/text()').getall()
            offer_1 = " ".join(t.strip() for t in promo_text_list if t.strip())

            # -------- Offer 2 --------
            promo = prod.xpath('//div[@class="sc-1959a32f-3 KOojL"]/h2/span/text()').get()
            promo_date = prod.xpath('//p[@class="sc-1959a32f-5 jpCzxC"]/span/text()').get()

            if promo and promo_date:
                offer_2 = f"{promo} ({promo_date})"
            elif promo:
                offer_2 = promo
            else:
                offer_2 = ""

            # -------- Final Result --------
            if offer_1 and offer_2:
                promo_text = f"{offer_1} | {offer_2}"
            elif offer_1:
                promo_text = offer_1
            elif offer_2:
                promo_text = offer_2
            else:
                promo_text = ""
            name = prod.xpath('//span[@class="sc-ab6170a9-1 eZAqam"]/text()').get()
            pack_size = prod.xpath('//span[@class="sc-ab6170a9-1 sc-e94e62e6-3 fMJPUe cvQTxq"]/span/text()').get()
            brand = prod.xpath('//span[@class="sc-747538d2-9 dxlClk"]/a/text()').get()
            img_url = response.xpath('.//img[@class="sc-97911d6b-11 gCTnZK"]/@src').getall()
            image_urls = " | ".join(img_url)

            breadcumb = response.xpath('//div[@class="sc-1b42ef49-2 jyBMPd"]/a[@class="sc-1b42ef49-1 cuemoG"]/text()').getall()
            bread = " > ".join(dict.fromkeys([b.strip() for b in breadcumb if b.strip()]))
            stock = response.xpath('//div[@class="sc-f40c9526-9 gHiBft"]/span')
            if stock:
                stock = False
            else:
                stock = True
            barcode = response.xpath('//script[@type="application/ld+json"]/text()').re_first(r'"mpn"\s*:\s*"([^"]+)"')
            sku = response.xpath('//script[@type="application/ld+json"]/text()').re_first(r'"sku"\s*:\s*"([^"]+)"')
            product_hash = self.generate_hash_id(referer_url, self.retailer, self.region)
            item = {"_id":product_hash,"Name": name, "Promo_Type": "", "Price": orignal_price, "per_unit_price": "",
                     "WasPrice": was_price,
                     "Offer_info": promo_text, "Pack_size": pack_size, "Barcode": barcode,
                     "Images": image_urls,
                     "ProductURL": referer_url, "is_available": stock,
                     "Status": "Done", "ParentCode": parent_id, "ProductCode": sku,
                     "retailer_name": "FairPrice",
                     "Category_Hierarchy": bread, "Brand": brand, "RRP": rrp}
            try:
                self.save_product(item)
                print(f"✓ Successfully inserted {referer_url}")
                if doc_id:
                    self.product_table.update_one(
                        {"_id": doc_id},
                        {"$set": {"Status": "Done"}}
                    )
                else:
                    self.product_table.update_one(
                        {"_id": doc_id},
                        {"$set": {"Status": "Not Found"}}
                    )
            except Exception as e:
                print(e)
                self.product_table.update_one(
                    {"_id": doc_id},
                    {"$set": {"Status": "Not Found"}}
                )


    def close(self, reason):
        import subprocess

        cmd = [
            "python",
            "upload_to_s3_direct.py",
            "--domain", "fairprice.com"
        ]
        subprocess.run(cmd, cwd=r"E:\pricemate_service")
        self.mongo_client.close()

if __name__ == '__main__':
    from scrapy.cmdline import execute
    execute("scrapy crawl fairprice_pdp -a retailer=ntuc-fairprice-sg -a region=sg -a Type=eshop -a RetailerCode=ntuc_fairprice_sg".split())