import scrapy
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from pricemate.spiders.base_spider import PricemateBaseSpider

cookies = {
    '_fbp': 'fb.1.1759835619244.418966476792689519',
    'useOfCookieNotice': 'true',
    'XSRF-TOKEN': 'eyJpdiI6ImVsb0pzQkpVVmRGMmpYU0NIVlRQd0E9PSIsInZhbHVlIjoiVUF0ek5Bb21iaWZDeXhDU2NaRGlaY0tKZmNleE8xTDhYb2JweWhUWVorXC9MNEtscHJRR0RWUnJkV3BEUkdpaW8iLCJtYWMiOiJlMDI3NDM1YTllMTJmODk3MWMzYmRkN2RhZTFlZmQ1MzViODVjMTk2YjEwNGJmY2EyMGU0N2Q1OWVkMzk5MWU5In0%3D',
    'laravel_session': 'eyJpdiI6IjJmNjVYbUNvOTB3K0ppaXAzK3ZFelE9PSIsInZhbHVlIjoiSE1oUEJ1MGpJUDRnSFZxamJ5NXUrT2Zia0t6QVZiXC9zNEJSWDhlak1VMHZYaTgxejNKU01UOG5HWE1rT1loNGgiLCJtYWMiOiI0NTQ5ZDU4YzkyNmU0OGI5ODc1ZjdjZTZmNzFmMjBmOTcwYzgyY2QzMDE3NjFkZTM0YzA2NDdkNjUzZjViYzQyIn0%3D',
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
    # 'cookie': '_fbp=fb.1.1759835619244.418966476792689519; useOfCookieNotice=true; XSRF-TOKEN=eyJpdiI6ImVsb0pzQkpVVmRGMmpYU0NIVlRQd0E9PSIsInZhbHVlIjoiVUF0ek5Bb21iaWZDeXhDU2NaRGlaY0tKZmNleE8xTDhYb2JweWhUWVorXC9MNEtscHJRR0RWUnJkV3BEUkdpaW8iLCJtYWMiOiJlMDI3NDM1YTllMTJmODk3MWMzYmRkN2RhZTFlZmQ1MzViODVjMTk2YjEwNGJmY2EyMGU0N2Q1OWVkMzk5MWU5In0%3D; laravel_session=eyJpdiI6IjJmNjVYbUNvOTB3K0ppaXAzK3ZFelE9PSIsInZhbHVlIjoiSE1oUEJ1MGpJUDRnSFZxamJ5NXUrT2Zia0t6QVZiXC9zNEJSWDhlak1VMHZYaTgxejNKU01UOG5HWE1rT1loNGgiLCJtYWMiOiI0NTQ5ZDU4YzkyNmU0OGI5ODc1ZjdjZTZmNzFmMjBmOTcwYzgyY2QzMDE3NjFkZTM0YzA2NDdkNjUzZjViYzQyIn0%3D',
}

class SnrCateSpider(PricemateBaseSpider):
    name = "snr_cate"

    def __init__(self, retailer, region, *args, **kwargs):
        super().__init__(retailer=retailer, region=region, *args, **kwargs)

    def start_requests(self):
        url = 'https://www.snrshopping.com/category/shop-all-categories'

        yield scrapy.Request(
            url=url,
            cookies=cookies,
            headers=headers,
            callback=self.get_cate,
            meta={
                'url': url,
                "filename": f"Cate_{self.generate_hash_id(url)}.html",
                "should_be": ["nav-item dropdown shop-all-categories0"]
            }

        )
    def get_cate(self, response):
        category_links = response.xpath('//li[contains(@class,"shop_li")]//a/@href').getall()

        # remove duplicates and filter only valid category URLs
        category_links = list({
            link.strip()
            for link in category_links
            if link and '/category/shop-all-categories/' in link
        })

        for cate_url in category_links:
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
            print(f"Inserted: {cate_url}")

    def close(self, reason):
        self.mongo_client.close()

if __name__ == '__main__':
    from scrapy.cmdline import execute
    execute("scrapy crawl snr_cate -a retailer=snrshopping-ph -a region=ph -a Type=eshop -a RetailerCode=snrshopping_ph".split())