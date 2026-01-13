import json
import re
import time
from urllib.parse import quote
import scrapy
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from pricemate.spiders.base_spider import PricemateBaseSpider

cookies = {
    '__cf_bm': 'Y7NIy3lF5I0va5bZDisIGgEIhfMfjHlhbxBFtV5lYkI-1759128822-1.0.1.1-MhAW37OvgTCBbzoWrY7FjK.lF2B_Db75au2ypUG5hjXrixTmrkYaMIuh7k0XDz.yWyrt1TV2hUT.hJUCbxs6tECGvIZ5r6e1lDvkfVZx.RA',
    '_cfuvid': '43ysba7IRvIVEQjehUAxkvv0hxXYCnQRfJZCiJFAHLU-1759128822635-0.0.1.1-604800000',
    'cf_clearance': 'SYcs.aM94MYZQE7zmy9WQV5LL9nsgzNnzrLKSyR4n7Q-1759128824-1.2.1.1-EKrKSr8R9nJVfkOkqIK6MlgMr8En_EhzgROVJ52D9SWqZJ9.ABsHQOTKrdHr_urKWjbchQqYoUKZK8peXf3zQfTfGHzamq9Icn9tlEDaGkNC1JtXE3wdCVpCeTKWbOYxP7KFotiaTNeOn3.HZp0ZTlmx17irE1qmq1JbJmRlL2cnEJw04ScSco409KT_Gs_APDrTsfXsOFrxhcPvZyIWf.1_Vo6WtTF4ZEqKyKw0mOg',
    'Blibli-Additional-Parameter-Signature': '',
    'Blibli-Is-Member': 'false',
    'Blibli-Is-Remember': 'false',
    'Blibli-Device-Id': 'U.275ab4e2-57e1-405f-8314-f0a11526aaf6',
    'Blibli-Device-Id-Signature': '9c89794dcd7998f2270ee4a5733d66911fba3290',
    'Blibli-Session-Id': '0e000973-9e65-479e-bbe3-2e78589b6ca8',
    'Blibli-Signature': '52130cf66a218adde225f20f3a9dab229b7af5c1',
    'Blibli-User-Id': '0e000973-9e65-479e-bbe3-2e78589b6ca8',
    'Blibli-Unm-Signature': '5b9bfc34dd973697f7325e006da1d60b3bafa34d',
    'Blibli-Unm-Id': '0e000973-9e65-479e-bbe3-2e78589b6ca8',
    'Blibli-dv-token': 'JT_0ruW5SgdVerJLk36zqg6w2idjNwfX8FW3RgHETi5Gv_',
    'forterToken': '73a8483943384833b4d2a7c8dc580f70_1759129202012__UDF43-m4_25ck_',
}

headers = {
    'Accept': 'application/json, text/plain, */*',
    # 'Accept-Encoding': 'gzip, deflate, br, zstd',
    'Accept-Language': 'en-US,en;q=0.9',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    # 'Cookie': '__cf_bm=Y7NIy3lF5I0va5bZDisIGgEIhfMfjHlhbxBFtV5lYkI-1759128822-1.0.1.1-MhAW37OvgTCBbzoWrY7FjK.lF2B_Db75au2ypUG5hjXrixTmrkYaMIuh7k0XDz.yWyrt1TV2hUT.hJUCbxs6tECGvIZ5r6e1lDvkfVZx.RA; _cfuvid=43ysba7IRvIVEQjehUAxkvv0hxXYCnQRfJZCiJFAHLU-1759128822635-0.0.1.1-604800000; cf_clearance=SYcs.aM94MYZQE7zmy9WQV5LL9nsgzNnzrLKSyR4n7Q-1759128824-1.2.1.1-EKrKSr8R9nJVfkOkqIK6MlgMr8En_EhzgROVJ52D9SWqZJ9.ABsHQOTKrdHr_urKWjbchQqYoUKZK8peXf3zQfTfGHzamq9Icn9tlEDaGkNC1JtXE3wdCVpCeTKWbOYxP7KFotiaTNeOn3.HZp0ZTlmx17irE1qmq1JbJmRlL2cnEJw04ScSco409KT_Gs_APDrTsfXsOFrxhcPvZyIWf.1_Vo6WtTF4ZEqKyKw0mOg; Blibli-Additional-Parameter-Signature=; Blibli-Is-Member=false; Blibli-Is-Remember=false; Blibli-Device-Id=U.275ab4e2-57e1-405f-8314-f0a11526aaf6; Blibli-Device-Id-Signature=9c89794dcd7998f2270ee4a5733d66911fba3290; Blibli-Session-Id=0e000973-9e65-479e-bbe3-2e78589b6ca8; Blibli-Signature=52130cf66a218adde225f20f3a9dab229b7af5c1; Blibli-User-Id=0e000973-9e65-479e-bbe3-2e78589b6ca8; Blibli-Unm-Signature=5b9bfc34dd973697f7325e006da1d60b3bafa34d; Blibli-Unm-Id=0e000973-9e65-479e-bbe3-2e78589b6ca8; Blibli-dv-token=JT_0ruW5SgdVerJLk36zqg6w2idjNwfX8FW3RgHETi5Gv_; forterToken=73a8483943384833b4d2a7c8dc580f70_1759129202012__UDF43-m4_25ck_',
    'Host': 'www.blibli.com',
    'Referer': 'https://www.blibli.com/',
    'sec-ch-ua': '"Chromium";v="140", "Not=A?Brand";v="24", "Google Chrome";v="140"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36',
}

class BlibliCateSpider(PricemateBaseSpider):
    name = "blibli_cate"

    def __init__(self, retailer, region, *args, **kwargs):
        super().__init__(retailer=retailer, region=region, *args, **kwargs)

    def start_requests(self):
        url = 'https://www.blibli.com/backend/content-api/categories/d137b99d-10ef-48cd-a668-aebb3c11b111/children'

        yield scrapy.Request(
            url=url,
            headers=headers,
            callback=self.parse,
            meta={
                "filename": f"Cate_{self.generate_hash_id(url)}.html",
                "should_be": ["data"]
            })

    def parse(self, response):
        data = response.json()
        for cate in data.get("data", []):
            cate_id = cate["categoryCode"]
            cat_url = cate.get("redirectUrl")
            cate_url = f'https://www.blibli.com{cat_url}'

            hash_id = self.generate_hash_id(cate_url, self.retailer, self.region)
            self.category_input.update_one(
                {"_id": hash_id},
                {"$set": {"url": cate_url, "cate_id": cate_id, "Status": "Pending", "Platform": self.retailer,
                          "Country": self.region}},
                upsert=True
            )
            print(f"inserted: {cate_url}")

    def close(self, reason):
        self.mongo_client.close()

if __name__ == '__main__':
    from scrapy.cmdline import execute
    execute( "scrapy crawl blibli_cate -a retailer=Blibli -a region=id -a Type=eshop -a RetailerCode=blibli_id".split())