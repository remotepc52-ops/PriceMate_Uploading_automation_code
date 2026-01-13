from lxml import etree
import scrapy
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from pricemate.spiders.base_spider import PricemateBaseSpider

cookies = {
    '_fbp': 'fb.1.1765799270473.308641203.AQ',
    'cfz_google-analytics': '%7B%22aNwx__ga%22%3A%7B%22v%22%3A%224186622f-1f72-4e02-87c6-8a7bb5553760%22%2C%22e%22%3A1797335276818%7D%7D',
    'cfz_facebook-pixel': '%7B%22JYoB_fb-pixel%22%3A%7B%22v%22%3A%22fb.2.1765799276818.2144017997%22%2C%22e%22%3A1797335276818%7D%7D',
    'PHPSESSID': '2hrc116t4cdvku6hfqgcmp01u9',
    'cf_clearance': 'eXtSaX69gxPT9qE7ElgbpAVbq2vuPzfHP3MU62vTjSs-1765948721-1.2.1.1-9hf8qN_NBCY9iX.yabaf2geJEFHAVfq4a.Tyy2C6Wqxp_f1TIZfZyjdebSwYUAU3CgT7AF2OTLaSO1_o26XlG8SPhUtx9JPuOrD18mCAtqNUOFlNfdy3hNPKN0XwKegW.EdceY4qzGRp2JuqlH51.oK3QeE3kpXcF5vFAv2Eq62iYsyMrAaqoTazZHXoeyOp57NhQRLti9KWPTmgN8LSKr3oBW1O4DulV0dlVyhM_SQ',
    'sbjs_migrations': '1418474375998%3D1',
    'sbjs_current_add': 'fd%3D2025-12-17%2004%3A48%3A46%7C%7C%7Cep%3Dhttps%3A%2F%2Fwww.petmart.vn%2F%7C%7C%7Crf%3Dhttps%3A%2F%2Fwww.petmart.vn%2F%3F__cf_chl_tk%3DT4BllIQO4aG2vyoc6fSoNQVpy_wkam.Zwk_7b5yHdHA-1765948714-1.0.1.1-XDW5_TRyFkeAz.ie63MvB1PpTLAkEW5zcTlslMPQR54',
    'sbjs_first_add': 'fd%3D2025-12-17%2004%3A48%3A46%7C%7C%7Cep%3Dhttps%3A%2F%2Fwww.petmart.vn%2F%7C%7C%7Crf%3Dhttps%3A%2F%2Fwww.petmart.vn%2F%3F__cf_chl_tk%3DT4BllIQO4aG2vyoc6fSoNQVpy_wkam.Zwk_7b5yHdHA-1765948714-1.0.1.1-XDW5_TRyFkeAz.ie63MvB1PpTLAkEW5zcTlslMPQR54',
    'sbjs_current': 'typ%3Dtypein%7C%7C%7Csrc%3D%28direct%29%7C%7C%7Cmdm%3D%28none%29%7C%7C%7Ccmp%3D%28none%29%7C%7C%7Ccnt%3D%28none%29%7C%7C%7Ctrm%3D%28none%29%7C%7C%7Cid%3D%28none%29%7C%7C%7Cplt%3D%28none%29%7C%7C%7Cfmt%3D%28none%29%7C%7C%7Ctct%3D%28none%29',
    'sbjs_first': 'typ%3Dtypein%7C%7C%7Csrc%3D%28direct%29%7C%7C%7Cmdm%3D%28none%29%7C%7C%7Ccmp%3D%28none%29%7C%7C%7Ccnt%3D%28none%29%7C%7C%7Ctrm%3D%28none%29%7C%7C%7Cid%3D%28none%29%7C%7C%7Cplt%3D%28none%29%7C%7C%7Cfmt%3D%28none%29%7C%7C%7Ctct%3D%28none%29',
    'sbjs_udata': 'vst%3D1%7C%7C%7Cuip%3D%28none%29%7C%7C%7Cuag%3DMozilla%2F5.0%20%28Windows%20NT%2010.0%3B%20Win64%3B%20x64%29%20AppleWebKit%2F537.36%20%28KHTML%2C%20like%20Gecko%29%20Chrome%2F143.0.0.0%20Safari%2F537.36',
    'sbjs_session': 'pgs%3D1%7C%7C%7Ccpg%3Dhttps%3A%2F%2Fwww.petmart.vn%2F',
    '_gcl_au': '1.1.973005143.1765948728',
    '_ga': 'GA1.1.870746522.1765948729',
    '_tt_enable_cookie': '1',
    '_ttp': '01KCNBYA7C535YYN8ZXHKP1F55_.tt.1',
    'ttcsid_CJG8JLRC77U39U03S42G': '1765948729582::bYwAPJg4_HxVGvYr47LK.1.1765948732058.0',
    'ttcsid': '1765948729583::gbzhXCS4ZYctjnrBXaL9.1.1765948732059.0',
    '_ga_ZKRDYCTQCP': 'GS2.1.s1765948728$o1$g1$t1765948737$j51$l0$h1723054703',
}

headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
    'cache-control': 'max-age=0',
    'priority': 'u=0, i',
    'referer': 'https://www.petmart.vn/sitemap_index.xml',
    'sec-ch-ua': '"Google Chrome";v="143", "Chromium";v="143", "Not A(Brand";v="24"',
    'sec-ch-ua-arch': '"x86"',
    'sec-ch-ua-bitness': '"64"',
    'sec-ch-ua-full-version': '"143.0.7499.110"',
    'sec-ch-ua-full-version-list': '"Google Chrome";v="143.0.7499.110", "Chromium";v="143.0.7499.110", "Not A(Brand";v="24.0.0.0"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-model': '""',
    'sec-ch-ua-platform': '"Windows"',
    'sec-ch-ua-platform-version': '"19.0.0"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36',
    # 'cookie': '_fbp=fb.1.1765799270473.308641203.AQ; cfz_google-analytics=%7B%22aNwx__ga%22%3A%7B%22v%22%3A%224186622f-1f72-4e02-87c6-8a7bb5553760%22%2C%22e%22%3A1797335276818%7D%7D; cfz_facebook-pixel=%7B%22JYoB_fb-pixel%22%3A%7B%22v%22%3A%22fb.2.1765799276818.2144017997%22%2C%22e%22%3A1797335276818%7D%7D; PHPSESSID=2hrc116t4cdvku6hfqgcmp01u9; cf_clearance=eXtSaX69gxPT9qE7ElgbpAVbq2vuPzfHP3MU62vTjSs-1765948721-1.2.1.1-9hf8qN_NBCY9iX.yabaf2geJEFHAVfq4a.Tyy2C6Wqxp_f1TIZfZyjdebSwYUAU3CgT7AF2OTLaSO1_o26XlG8SPhUtx9JPuOrD18mCAtqNUOFlNfdy3hNPKN0XwKegW.EdceY4qzGRp2JuqlH51.oK3QeE3kpXcF5vFAv2Eq62iYsyMrAaqoTazZHXoeyOp57NhQRLti9KWPTmgN8LSKr3oBW1O4DulV0dlVyhM_SQ; sbjs_migrations=1418474375998%3D1; sbjs_current_add=fd%3D2025-12-17%2004%3A48%3A46%7C%7C%7Cep%3Dhttps%3A%2F%2Fwww.petmart.vn%2F%7C%7C%7Crf%3Dhttps%3A%2F%2Fwww.petmart.vn%2F%3F__cf_chl_tk%3DT4BllIQO4aG2vyoc6fSoNQVpy_wkam.Zwk_7b5yHdHA-1765948714-1.0.1.1-XDW5_TRyFkeAz.ie63MvB1PpTLAkEW5zcTlslMPQR54; sbjs_first_add=fd%3D2025-12-17%2004%3A48%3A46%7C%7C%7Cep%3Dhttps%3A%2F%2Fwww.petmart.vn%2F%7C%7C%7Crf%3Dhttps%3A%2F%2Fwww.petmart.vn%2F%3F__cf_chl_tk%3DT4BllIQO4aG2vyoc6fSoNQVpy_wkam.Zwk_7b5yHdHA-1765948714-1.0.1.1-XDW5_TRyFkeAz.ie63MvB1PpTLAkEW5zcTlslMPQR54; sbjs_current=typ%3Dtypein%7C%7C%7Csrc%3D%28direct%29%7C%7C%7Cmdm%3D%28none%29%7C%7C%7Ccmp%3D%28none%29%7C%7C%7Ccnt%3D%28none%29%7C%7C%7Ctrm%3D%28none%29%7C%7C%7Cid%3D%28none%29%7C%7C%7Cplt%3D%28none%29%7C%7C%7Cfmt%3D%28none%29%7C%7C%7Ctct%3D%28none%29; sbjs_first=typ%3Dtypein%7C%7C%7Csrc%3D%28direct%29%7C%7C%7Cmdm%3D%28none%29%7C%7C%7Ccmp%3D%28none%29%7C%7C%7Ccnt%3D%28none%29%7C%7C%7Ctrm%3D%28none%29%7C%7C%7Cid%3D%28none%29%7C%7C%7Cplt%3D%28none%29%7C%7C%7Cfmt%3D%28none%29%7C%7C%7Ctct%3D%28none%29; sbjs_udata=vst%3D1%7C%7C%7Cuip%3D%28none%29%7C%7C%7Cuag%3DMozilla%2F5.0%20%28Windows%20NT%2010.0%3B%20Win64%3B%20x64%29%20AppleWebKit%2F537.36%20%28KHTML%2C%20like%20Gecko%29%20Chrome%2F143.0.0.0%20Safari%2F537.36; sbjs_session=pgs%3D1%7C%7C%7Ccpg%3Dhttps%3A%2F%2Fwww.petmart.vn%2F; _gcl_au=1.1.973005143.1765948728; _ga=GA1.1.870746522.1765948729; _tt_enable_cookie=1; _ttp=01KCNBYA7C535YYN8ZXHKP1F55_.tt.1; ttcsid_CJG8JLRC77U39U03S42G=1765948729582::bYwAPJg4_HxVGvYr47LK.1.1765948732058.0; ttcsid=1765948729583::gbzhXCS4ZYctjnrBXaL9.1.1765948732059.0; _ga_ZKRDYCTQCP=GS2.1.s1765948728$o1$g1$t1765948737$j51$l0$h1723054703',
}

class PetmartCateSpider(PricemateBaseSpider):
    name = "petmart_cate"

    def __init__(self, retailer, region, *args, **kwargs):
        super().__init__(retailer=retailer, region=region, *args, **kwargs)

    def start_requests(self):
        # all_url = ['https://www.petmart.vn/product-sitemap1.xml', 'https://www.petmart.vn/product-sitemap2.xml', 'https://www.petmart.vn/product-sitemap3.xml','https://www.petmart.vn/product-sitemap4.xml', 'https://www.petmart.vn/product-sitemap5.xml', 'https://www.petmart.vn/product-sitemap6.xml', 'https://www.petmart.vn/product-sitemap7.xml', 'https://www.petmart.vn/product-sitemap8.xml']
        # for sitemaps in all_url:
        sitemaps = "https://www.petmart.vn/product_cat-sitemap.xml"
        yield scrapy.Request(
            url=sitemaps,
            cookies=cookies,
            headers=headers,
            callback=self.parse_pl,
            meta={
                'sitemap_url': sitemaps,
                "filename": f"Pl_{self.generate_hash_id(sitemaps)}.html",
                "should_be": ["url"]
            }

        )

    def parse_pl(self, response):
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
    execute("scrapy crawl petmart_cate -a retailer=petmart-ph -a region=ph -a Type=eshop -a RetailerCode=petmart_ph".split())