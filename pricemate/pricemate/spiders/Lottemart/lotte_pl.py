import json
import time
from lxml import etree
from urllib.parse import quote
import scrapy
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from pricemate.spiders.base_spider import PricemateBaseSpider

cookies = {
    'visid_incap_3263173': 'zul3081bQcyLdHa4CUTjdquwXGkAAAAAQUIPAAAAAAAwqgafpMpWlKiOdCn2pPE4',
    'incap_ses_1139_3263173': 'KPmDQAhFB2NoLxtC8IrOD6uwXGkAAAAAEDh6wXZfP0F7vAkwico4Vw==',
    '_gid': 'GA1.3.425766354.1767682224',
    'incap_ses_1789_3263173': 'UT+uBYplrhyH9j5mg87TGFWxXGkAAAAA3Hg/fGJJQhPeXpfBwK3r+w==',
    'cookiesession1': '678ADA7B6D84D8D601C858181B0B7B4C',
    'visid_incap_3263089': 'Q81c4b5tRq+dc49XoapMprOyXGkAAAAAQUIPAAAAAAAmBz5/C9/+iO7qRvYx97U+',
    'incap_ses_1789_3263089': 'RubBU5zZU0Ww1EVmg87TGLSyXGkAAAAA9I2HSCXn0GaoxnHmp6DNGA==',
    '_ga_8Q90GTQPFL': 'GS2.1.s1767682224$o1$g1$t1767682740$j60$l0$h0',
    '_ga': 'GA1.1.1994700430.1767682224',
    '_ga_W3RDM1W0G3': 'GS2.1.s1767682870$o1$g1$t1767682941$j60$l0$h0',
}

headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
    'cache-control': 'max-age=0',
    'priority': 'u=0, i',
    'sec-ch-ua': '"Google Chrome";v="143", "Chromium";v="143", "Not A(Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Linux"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'none',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36',
    # 'cookie': 'visid_incap_3263173=zul3081bQcyLdHa4CUTjdquwXGkAAAAAQUIPAAAAAAAwqgafpMpWlKiOdCn2pPE4; incap_ses_1139_3263173=KPmDQAhFB2NoLxtC8IrOD6uwXGkAAAAAEDh6wXZfP0F7vAkwico4Vw==; _gid=GA1.3.425766354.1767682224; incap_ses_1789_3263173=UT+uBYplrhyH9j5mg87TGFWxXGkAAAAA3Hg/fGJJQhPeXpfBwK3r+w==; cookiesession1=678ADA7B6D84D8D601C858181B0B7B4C; visid_incap_3263089=Q81c4b5tRq+dc49XoapMprOyXGkAAAAAQUIPAAAAAAAmBz5/C9/+iO7qRvYx97U+; incap_ses_1789_3263089=RubBU5zZU0Ww1EVmg87TGLSyXGkAAAAA9I2HSCXn0GaoxnHmp6DNGA==; _ga_8Q90GTQPFL=GS2.1.s1767682224$o1$g1$t1767682740$j60$l0$h0; _ga=GA1.1.1994700430.1767682224; _ga_W3RDM1W0G3=GS2.1.s1767682870$o1$g1$t1767682941$j60$l0$h0',
}


class LottePlSpider(PricemateBaseSpider):
    name = "lote_pl"

    def __init__(self, retailer, region, *args, **kwargs):
        super().__init__(retailer=retailer, region=region, *args, **kwargs)

    def start_requests(self):
        url = "https://order.lottemart.co.id/sitemap-products/lotte-grosir-alam-sutera.xml"
        current_proxy = '2c6ea6e6d8c14216a62781b8f850cd5b'

        proxy_host = "api.zyte.com"
        proxy_port = "8011"
        proxy_auth = f"{current_proxy}:"

        proxy_url = f"https://{proxy_auth}@{proxy_host}:{proxy_port}"

        yield scrapy.Request(
            url=url,
            cookies=cookies,
            headers=headers,
            callback=self.parse_cat,
            meta={
                "proxy": proxy_url,
                'sitemap_url': url,
                "filename": f"PL_{self.generate_hash_id(url)}.html",
                "should_be": ["url"]
            }

            )

    def parse_cat(self, response):
        sitemap_url = response.meta['sitemap_url']
        namespaces = {'ns': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
        try:
            root = etree.fromstring(response.body)

            loc_elements = root.xpath('//ns:loc', namespaces=namespaces)

            for loc in loc_elements:
                cate_url = loc.text.strip()
                hash_id = self.generate_hash_id(cate_url, self.retailer, self.region)
                self.product_table.update_one(
                    {"_id": hash_id},
                    {"$set": {"ProductURL": cate_url, "Status": "Pending", "retailer": self.retailer, "region": self.region}},
                    upsert=True
                )
                print(f"inserted: {cate_url} ✅ ")

        except Exception as e:
            print(f"Failed to fetch sitemap {sitemap_url}:{e}")



    def close(self, reason):
        self.mongo_client.close()

if __name__ == '__main__':
    from scrapy.cmdline import execute
    execute("scrapy crawl lote_pl -a retailer=lottemartgrosir-id -a region=id -a Type=eshop -a RetailerCode=lottemartgrosir_id".split())