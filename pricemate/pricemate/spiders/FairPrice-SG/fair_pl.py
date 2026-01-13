import json
import os, sys
import re

import scrapy
from scrapy.http import JsonRequest
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from pricemate.spiders.base_spider import PricemateBaseSpider

cookies = {
    'sdt': 'cfb72b16-3ec0-45bc-a447-ea14b125c206',
    'BVBRANDID': '0d9c2968-538b-49d8-a85b-a29af1ab260f',
    'splitSessionKey': '159361_GUEST',
    'connect.sid': 's%3AytFShIvFfWje9PelizjmSCWYSKjDoxDs.tbxrEB%2BiJfBN9nQOql1rbem19hIFpJexL%2B2jLvDrofI',
    'ak_bmsc': '66E5CC955836342D9DE62660AB853E3C~000000000000000000000000000000~YAAQZUZYaBU4Gn+ZAQAAqicsvR2vXJ64PSpngEYOfTQ0thQLpGJny5m3q3v2EYiPs2hCfqx0LKJVWDS3eoJKLxBAhlTmoA9GmZlgTdp30UhYIXsafiqW7leNc8Tvbrww6oqnZVX4qsC+TXRQpasRdYi4GB5m8v3TIJ4xQjLQs7IPEx+Blo3ZgiduA5VA1oQButD5Z5g5LDkrm7AxJZK6M+8p62XpETb4GWhsYLp3SLSnU7durMd2bPzX9JH+QsOwZN5sCMh3Wc5LL6gQuNkwRGOtE4ulNQQrYUni3InXfUSn6YdCALEWSCg2pKJvxmkT7K5Qev2YxMUK/nm5htJWuUK4mKDs91L6xjXizBeMoHJzRzLFiPsfLuirHHuUYhJxHSgmX7a7asUDhcMtu77m1Jd5Iw==',
    '_dyid_server': '2931843608286111478',
    '_dyjsession': 'n75yk71xaqql0uxkr24s73ujmy6gm78p',
    'bm_mi': 'ED2C21641CC36DA5EECEE47269BC58ED~YAAQZUZYaM87Gn+ZAQAAT1ItvR0kzvfujB+0HaMAMsv2sGvASYuePG1JaGWxgMPSP4EyunxlWmbOTuZkHmf8+E9MD616c0Hj8gVx8kp2/WLxAbeOE7Et7gkq7ABu20pa7LThBbP8IkRZ0/aB0R8iGQgCGkaFv1qA+EPeFquiXHQ5J3E88HT80Wa7vCk2KI/OyXwEmw7A0TPAFJkzTPf40feoa8ksTwcNvIQ1Sj/Llmq6n6MKxKYzONE+6cP0AdKPtyG9RsPVKH5IdTZGv5+mWKKmHHyqADtmp6KKGDV5uXS+G5BewwUig0cJYboY6UnPkUYLcfn7OStR8bxzxiK66DiZzch8l838VhbSW2aEfQ==~1',
    'bm_sv': '8A4FE791C2A2FFA9CF425A2A20F79E78~YAAQZUZYaNA7Gn+ZAQAAT1ItvR1+PEPJ7F7xLtTL+9Wy3NSBap3+GZ85zmc1gGK2rPo/4eTNYzfOOb95BhpN4O33m4Dnuow1Zd3LzpuRJ7GEsxwtzgd3tbVqLKpAzNGYXKfN0nS7uQAZz13JbGYhdYgTbVAx0F3YVRf4zsWawXK+cZ1Gz8SDut4sIXv0+EPWoSk+0ydWZZ7mCkvXm3nni2uv6/1y7dWBiC9a8LHKBw4oJ6uTFMvwXHqeL0mzm2XVC344lYFJ~1',
    'amp_2050dd': 'ppmE6T74rJVbCKwnyUcsKq...1j6uiocdh.1j6uiqlfh.3.0.3',
    '_dd_s': 'rum=2&id=cea57bf4-9d1c-47d6-8544-eac03b98722c&created=1759815413477&expire=1759816395385',
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
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36',
    # 'cookie': 'sdt=cfb72b16-3ec0-45bc-a447-ea14b125c206; BVBRANDID=0d9c2968-538b-49d8-a85b-a29af1ab260f; splitSessionKey=159361_GUEST; connect.sid=s%3AytFShIvFfWje9PelizjmSCWYSKjDoxDs.tbxrEB%2BiJfBN9nQOql1rbem19hIFpJexL%2B2jLvDrofI; ak_bmsc=66E5CC955836342D9DE62660AB853E3C~000000000000000000000000000000~YAAQZUZYaBU4Gn+ZAQAAqicsvR2vXJ64PSpngEYOfTQ0thQLpGJny5m3q3v2EYiPs2hCfqx0LKJVWDS3eoJKLxBAhlTmoA9GmZlgTdp30UhYIXsafiqW7leNc8Tvbrww6oqnZVX4qsC+TXRQpasRdYi4GB5m8v3TIJ4xQjLQs7IPEx+Blo3ZgiduA5VA1oQButD5Z5g5LDkrm7AxJZK6M+8p62XpETb4GWhsYLp3SLSnU7durMd2bPzX9JH+QsOwZN5sCMh3Wc5LL6gQuNkwRGOtE4ulNQQrYUni3InXfUSn6YdCALEWSCg2pKJvxmkT7K5Qev2YxMUK/nm5htJWuUK4mKDs91L6xjXizBeMoHJzRzLFiPsfLuirHHuUYhJxHSgmX7a7asUDhcMtu77m1Jd5Iw==; _dyid_server=2931843608286111478; _dyjsession=n75yk71xaqql0uxkr24s73ujmy6gm78p; bm_mi=ED2C21641CC36DA5EECEE47269BC58ED~YAAQZUZYaM87Gn+ZAQAAT1ItvR0kzvfujB+0HaMAMsv2sGvASYuePG1JaGWxgMPSP4EyunxlWmbOTuZkHmf8+E9MD616c0Hj8gVx8kp2/WLxAbeOE7Et7gkq7ABu20pa7LThBbP8IkRZ0/aB0R8iGQgCGkaFv1qA+EPeFquiXHQ5J3E88HT80Wa7vCk2KI/OyXwEmw7A0TPAFJkzTPf40feoa8ksTwcNvIQ1Sj/Llmq6n6MKxKYzONE+6cP0AdKPtyG9RsPVKH5IdTZGv5+mWKKmHHyqADtmp6KKGDV5uXS+G5BewwUig0cJYboY6UnPkUYLcfn7OStR8bxzxiK66DiZzch8l838VhbSW2aEfQ==~1; bm_sv=8A4FE791C2A2FFA9CF425A2A20F79E78~YAAQZUZYaNA7Gn+ZAQAAT1ItvR1+PEPJ7F7xLtTL+9Wy3NSBap3+GZ85zmc1gGK2rPo/4eTNYzfOOb95BhpN4O33m4Dnuow1Zd3LzpuRJ7GEsxwtzgd3tbVqLKpAzNGYXKfN0nS7uQAZz13JbGYhdYgTbVAx0F3YVRf4zsWawXK+cZ1Gz8SDut4sIXv0+EPWoSk+0ydWZZ7mCkvXm3nni2uv6/1y7dWBiC9a8LHKBw4oJ6uTFMvwXHqeL0mzm2XVC344lYFJ~1; amp_2050dd=ppmE6T74rJVbCKwnyUcsKq...1j6uiocdh.1j6uiqlfh.3.0.3; _dd_s=rum=2&id=cea57bf4-9d1c-47d6-8544-eac03b98722c&created=1759815413477&expire=1759816395385',
}


class FairpricePlSpider(PricemateBaseSpider):
    name = "fairprice_pl"

    def __init__(self, retailer, region, *args, **kwargs):
        super().__init__(retailer=retailer, region=region, *args, **kwargs)

    def start_requests(self):
        docs = self.category_input.find({
            "retailer": self.retailer,
            "region": self.region,
            "Status": "Pending"
        })
        for doc in docs:
            url = doc["url"]
            hash_id = doc.get("_id")
            parent = doc.get("Parent_id")
            slug = url.split("category/")[-1].split("/")[0]
            meta = {
                "url": url,
                "_id": hash_id,
                "Parent_id":parent,
                "filename": f"{slug}_page.html",
                "should_be": ["product-collection"]
            }
            yield scrapy.Request(
                url,
                cookies=cookies,
                headers=headers,
                callback=self.parse_pl,
                meta=meta
            )

    def parse_pl(self, response):
        meta = response.meta
        doc_id = meta.get("_id")
        parent_id = meta.get("Parent_id")
        links = response.xpath('//a[contains(@class, "sc-e68f503d-3")]/@href').getall()

        for link in links:
            pdp_url = f'https://www.fairprice.com.sg{link}'
            product_hash = self.generate_hash_id(pdp_url, self.retailer, self.region)
            item = {
                "_id": product_hash,
                "ProductURL": pdp_url,
                "parent_id":parent_id,
                "Status": "Pending",
                "retailer": self.retailer,
                "region": self.region,
            }
            self.save_product(item)
            self.category_input.update_one(
                {"_id": doc_id},
                {"$set": {"Status": "Done"}}
            )
            self.logger.info(f"Product URL: {pdp_url}")

    def close(self, reason):
        self.mongo_client.close()

if __name__ == '__main__':
    from scrapy.cmdline import execute
    execute("scrapy crawl fairprice_pl -a retailer=ntuc-fairprice-sg -a region=sg -a Type=eshop -a RetailerCode=ntuc_fairprice_sg".split())