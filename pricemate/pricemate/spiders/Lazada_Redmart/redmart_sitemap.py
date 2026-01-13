import json
import time
from lxml import etree
from urllib.parse import quote
import scrapy
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from pricemate.spiders.base_spider import PricemateBaseSpider

cookies = {
    't_fv': '1759478515485',
    't_uid': 'OlFoc5rl9UwoIHewkAZMHhciSVPkdVWE',
    't_sid': 'hDMu4eL3z26V1pySBLn1M94bDcpZiknq',
    'utm_channel': 'NA',
    'hng': 'SG|en-SG|SGD|702',
    'userLanguageML': 'en',
    'lwrid': 'AgGZqReJV%2BqhdLfRbodAX39uIwDz',
    '_m_h5_tk': '858cbab944653d1aeb15a8d5f36b38b5_1759486435672',
    '_m_h5_tk_enc': '5a741a1142c7a76a074a4abb0847c6e0',
    'lzd_cid': 'fee28704-6b72-492e-8d82-e746dbb64f2a',
    '_tb_token_': '70e4e0e43e3ee',
    'lzd_sid': '130dd3efcb70c08abd24cf3ce3ddb2ea',
    'lwrtk': 'AAIEaN/zeLYvklRMwBmw7weEc+oXqOsGwacqfKfLwZ94jwJYRMP6It4=',
    'epssw': '10*Bpzss6hO_e9ykassUNxeOIrRmRmPEqsGsiY2kvssO-AsA7DoOxVCp-yjWqrJQCKsR4qQOND0ssFQO-Xb8GXXHOWRUCNsFva1BP4mL_-fRRV-EFsaOOv44rsavKba_ds0sbDf6IUuzFsazRQn6asJUvNMrhakGSFJ-aBEhKj7r89THdBmJ0kVptLcKAZ8ABwO5hF8X_rX-CCQ9J_qBCnlHysnKJ13WNymCdvQGaCHb-xlPptssssssRrbORl-i9JZbkSQjDokl4I1RaspbWwpga_fBmiaLIua9MPX6yK976XKhNgoNX7sV2oEOUP4f2S1EM4si6..',
    'isg': 'BB4esvHw-pYiqi7yeu9gevfIb7Rg3-JZlKrrv8imF2FA677FMG_MaPTJ5-9nU9px',
    'tfstk': 'gXpIBs6hEy4I5EAAOToa1CUUav6Sdck4NusJm3eU29Bdw8TD5DjPz3n5FHTWUDxR8zT1KdRUUwuhF3LVFquq3x-HfOX-uq5EDe0GegHPyf5pBMOR5quq3ARIdA_juUki4xCOqNILpJC-fNIFATIRean1Wgs0wyLReci1VMURv8CKBhIf2TQJyTn6XNjReMLRectOSghocRsgIN-IDetat0VbAL7_e8p1XDbvA0elXdsC9ZKpdzaSmM1CkBQtJn2gQ1KlNLquF_tpiUjvJy35rdt9pILx7W7pGgt2NHHLB9JHvICJH4VJY97CBpdb28K1dNTDeF4I5ZpHXKXO_xnXXdYexdtz2YIwuNKHpTMxm96dJOsMUV2dPCdJL6XuJ4_kChppNgS43ZG6S7Z1i8s1uci_Z7qd0L3xKX9Rg6IGbZosfSoC9Gj1uci_Z7fdjGqqfcNqA',
}

headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
    'cache-control': 'max-age=0',
    'priority': 'u=0, i',
    'sec-ch-ua': '"Chromium";v="140", "Not=A?Brand";v="24", "Google Chrome";v="140"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'none',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36',
    # 'cookie': 't_fv=1759478515485; t_uid=OlFoc5rl9UwoIHewkAZMHhciSVPkdVWE; t_sid=hDMu4eL3z26V1pySBLn1M94bDcpZiknq; utm_channel=NA; hng=SG|en-SG|SGD|702; userLanguageML=en; lwrid=AgGZqReJV%2BqhdLfRbodAX39uIwDz; _m_h5_tk=858cbab944653d1aeb15a8d5f36b38b5_1759486435672; _m_h5_tk_enc=5a741a1142c7a76a074a4abb0847c6e0; lzd_cid=fee28704-6b72-492e-8d82-e746dbb64f2a; _tb_token_=70e4e0e43e3ee; lzd_sid=130dd3efcb70c08abd24cf3ce3ddb2ea; lwrtk=AAIEaN/zeLYvklRMwBmw7weEc+oXqOsGwacqfKfLwZ94jwJYRMP6It4=; epssw=10*Bpzss6hO_e9ykassUNxeOIrRmRmPEqsGsiY2kvssO-AsA7DoOxVCp-yjWqrJQCKsR4qQOND0ssFQO-Xb8GXXHOWRUCNsFva1BP4mL_-fRRV-EFsaOOv44rsavKba_ds0sbDf6IUuzFsazRQn6asJUvNMrhakGSFJ-aBEhKj7r89THdBmJ0kVptLcKAZ8ABwO5hF8X_rX-CCQ9J_qBCnlHysnKJ13WNymCdvQGaCHb-xlPptssssssRrbORl-i9JZbkSQjDokl4I1RaspbWwpga_fBmiaLIua9MPX6yK976XKhNgoNX7sV2oEOUP4f2S1EM4si6..; isg=BB4esvHw-pYiqi7yeu9gevfIb7Rg3-JZlKrrv8imF2FA677FMG_MaPTJ5-9nU9px; tfstk=gXpIBs6hEy4I5EAAOToa1CUUav6Sdck4NusJm3eU29Bdw8TD5DjPz3n5FHTWUDxR8zT1KdRUUwuhF3LVFquq3x-HfOX-uq5EDe0GegHPyf5pBMOR5quq3ARIdA_juUki4xCOqNILpJC-fNIFATIRean1Wgs0wyLReci1VMURv8CKBhIf2TQJyTn6XNjReMLRectOSghocRsgIN-IDetat0VbAL7_e8p1XDbvA0elXdsC9ZKpdzaSmM1CkBQtJn2gQ1KlNLquF_tpiUjvJy35rdt9pILx7W7pGgt2NHHLB9JHvICJH4VJY97CBpdb28K1dNTDeF4I5ZpHXKXO_xnXXdYexdtz2YIwuNKHpTMxm96dJOsMUV2dPCdJL6XuJ4_kChppNgS43ZG6S7Z1i8s1uci_Z7qd0L3xKX9Rg6IGbZosfSoC9Gj1uci_Z7fdjGqqfcNqA',
}


class RedmartCateSpider(PricemateBaseSpider):
    name = "redmart_cate"

    def __init__(self, retailer, region, *args, **kwargs):
        super().__init__(retailer=retailer, region=region, *args, **kwargs)

    def start_requests(self):
        sitemaps = 'https://redmart.lazada.sg/redmart-sitemap-categories-1.xml.gz'

        yield scrapy.Request(
            url=sitemaps,
            cookies=cookies,
            headers=headers,
            callback=self.parse,
            meta={
                "proxy": "http://21ed11ef5c872bc7727680a52233027db4578a0e:@api.zenrows.com:8001",
                'sitemap_url': sitemaps,
                "filename": f"Sitemap_{self.generate_hash_id(sitemaps)}.html",
                "should_be": ["url"]
            }

        )

    def parse(self, response):
        sitemap_url = response.meta['sitemap_url']
        namespaces = {'ns': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
        try:
            root = etree.fromstring(response.body)

            loc_elements = root.xpath('//ns:loc', namespaces=namespaces)

            for loc in loc_elements:
                cate_url = loc.text.strip()
                hash_id = self.generate_hash_id(cate_url, self.retailer, self.region)
                self.category_input.update_one(
                    {"_id": hash_id},
                    {"$set": {"url": cate_url, "Status": "Pending", "retailer": self.retailer, "region": self.region}},
                    upsert=True
                )
                print(f"inserted: {cate_url}")

        except Exception as e:
            print(f"Failed to fetch sitemap {sitemap_url}:{e}")



    def close(self, reason):
        self.mongo_client.close()

if __name__ == '__main__':
    from scrapy.cmdline import execute
    execute("scrapy crawl redmart_cate -a retailer=lazada_redmart_sg -a region=sg -a Type=eshop -a RetailerCode=lazada_redmart_sg".split())