import scrapy
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from pricemate.spiders.base_spider import PricemateBaseSpider
cookies = {
    'localization': 'PH',
    '_shopify_y': '794087fa-8ee5-4e01-9b7e-6a8a05617d2b',
    '_tracking_consent': '3.AMPS_AUWA_f_f_7AUxuHq8TwWPRARDwt06mw',
    '_shopify_analytics': ':AZnDo_lHAAEAyjgraiEIWjqyLm3AJM5zK8iheTo7GvecDngxOjZXOPHfHpjclA:',
    'WISHLIST_TOTAL': '0',
    'WISHLIST_PRODUCTS_IDS': '{}',
    'WISHLIST_PRODUCTS_IDS_SET': '1',
    'WISHLIST_UUID': 'null',
    'WISHLIST_IP_ADDRESS': '103.108.231.19',
    '_fbp': 'fb.2.1759923940325.201946050156262699',
    '_shopify_essential': ':AZnDo_krAAEAJcV4OFMGoPvpVclvtlYeKLU8lGItv_JPCfbU_ts3QX_HCMxQiUGlcdguQIDcplLurErvI8cbUEmpgG204IiMo4dSOaVCuopHHc7B8JBzWET2a8Lha2vVFKfeXpRw0eBw21TQZqd2uDvyD5lMpHeoNiBliDsk5d97KyW19xnnP3mGkZGraNm6ShHj9u37RpW_eLSX0-UkYZU8X8gxGpfhGVWDU71VkGF_L9s08UMLgFPkT0Qjk-TX1u2XWhbVzJ_GEaHbLDTctc4xL330Dks9DMXr9nlPwxIKKWqYM7m2tvME96rWaSbTjsMHEA:',
    '_shopify_s': 'ce2c843c-a624-4d28-aea7-4ebcf3634705',
    'epb_previous_pathname': '/products/babyjoy-nipples-silicone-large-600-in-house-trade-account',
    'fsb_previous_pathname': '/products/babyjoy-nipples-silicone-large-600-in-house-trade-account',
    'keep_alive': 'eyJ2IjoyLCJ0cyI6MTc1OTkyNjc2OTU3OSwiZW52Ijp7IndkIjowLCJ1YSI6MSwiY3YiOjEsImJyIjoxfSwiYmh2Ijp7Im1hIjoyMDUsImNhIjowLCJrYSI6MCwic2EiOjg5LCJrYmEiOjAsInRhIjowLCJ0IjoyMTE2LCJubSI6MSwibXMiOjAsIm1qIjowLjg3LCJtc3AiOjAuOCwidmMiOjAsImNwIjowLCJyYyI6MCwia2oiOjAsImtpIjowLCJzcyI6MC4xOCwic2oiOjAuMiwic3NtIjowLjgxLCJzcCI6NiwidHMiOjAsInRqIjowLCJ0cCI6MCwidHNtIjowfSwic2VzIjp7InAiOjUsInMiOjE3NTk5MjM5MzMzMTcsImQiOjI3ODV9fQ%3D%3D',
}

headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
    'cache-control': 'max-age=0',
    'if-none-match': '"cacheable:6d12ae9896cf24b868e272e135c3667f"',
    'priority': 'u=0, i',
    'referer': 'https://southstardrug.com.ph/collections/kids-baby',
    'sec-ch-ua': '"Google Chrome";v="141", "Not?A_Brand";v="8", "Chromium";v="141"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36',
    # 'cookie': 'localization=PH; _shopify_y=794087fa-8ee5-4e01-9b7e-6a8a05617d2b; _tracking_consent=3.AMPS_AUWA_f_f_7AUxuHq8TwWPRARDwt06mw; _shopify_analytics=:AZnDo_lHAAEAyjgraiEIWjqyLm3AJM5zK8iheTo7GvecDngxOjZXOPHfHpjclA:; WISHLIST_TOTAL=0; WISHLIST_PRODUCTS_IDS={}; WISHLIST_PRODUCTS_IDS_SET=1; WISHLIST_UUID=null; WISHLIST_IP_ADDRESS=103.108.231.19; _fbp=fb.2.1759923940325.201946050156262699; _shopify_essential=:AZnDo_krAAEAJcV4OFMGoPvpVclvtlYeKLU8lGItv_JPCfbU_ts3QX_HCMxQiUGlcdguQIDcplLurErvI8cbUEmpgG204IiMo4dSOaVCuopHHc7B8JBzWET2a8Lha2vVFKfeXpRw0eBw21TQZqd2uDvyD5lMpHeoNiBliDsk5d97KyW19xnnP3mGkZGraNm6ShHj9u37RpW_eLSX0-UkYZU8X8gxGpfhGVWDU71VkGF_L9s08UMLgFPkT0Qjk-TX1u2XWhbVzJ_GEaHbLDTctc4xL330Dks9DMXr9nlPwxIKKWqYM7m2tvME96rWaSbTjsMHEA:; _shopify_s=ce2c843c-a624-4d28-aea7-4ebcf3634705; epb_previous_pathname=/products/babyjoy-nipples-silicone-large-600-in-house-trade-account; fsb_previous_pathname=/products/babyjoy-nipples-silicone-large-600-in-house-trade-account; keep_alive=eyJ2IjoyLCJ0cyI6MTc1OTkyNjc2OTU3OSwiZW52Ijp7IndkIjowLCJ1YSI6MSwiY3YiOjEsImJyIjoxfSwiYmh2Ijp7Im1hIjoyMDUsImNhIjowLCJrYSI6MCwic2EiOjg5LCJrYmEiOjAsInRhIjowLCJ0IjoyMTE2LCJubSI6MSwibXMiOjAsIm1qIjowLjg3LCJtc3AiOjAuOCwidmMiOjAsImNwIjowLCJyYyI6MCwia2oiOjAsImtpIjowLCJzcyI6MC4xOCwic2oiOjAuMiwic3NtIjowLjgxLCJzcCI6NiwidHMiOjAsInRqIjowLCJ0cCI6MCwidHNtIjowfSwic2VzIjp7InAiOjUsInMiOjE3NTk5MjM5MzMzMTcsImQiOjI3ODV9fQ%3D%3D',
}

class SouthPlSpider(PricemateBaseSpider):
    name = "south_pl"

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
            slug = url.split("collections/")[-1].split("/")[0]
            meta = {
                "proxy": "http://21ed11ef5c872bc7727680a52233027db4578a0e:@api.zenrows.com:8001",
                "url": url,
                "_id": hash_id,
                "slug":slug,
                "page": 1,
                "filename": f"{slug}_page.html",
                "should_be": ["card__information"]
            }
            yield scrapy.Request(
                url = f"{url}?page=1",
                cookies=cookies,
                headers=headers,
                callback=self.parse_pl,
                meta=meta,
                dont_filter=True
            )

    def parse_pl(self, response):
        meta = response.meta
        doc_id = meta.get("_id")
        slug = meta.get("slug")
        page = int(meta.get("page", 1))  # Always starts from 1 and increases

        links = response.xpath('//div[@class="card__information"]/h3/a/@href').getall()
        for link in links:
            pdp_url = f'https://southstardrug.com.ph{link}'
            product_hash = self.generate_hash_id(pdp_url, self.retailer, self.region)
            item = {
                "_id": product_hash,
                "ProductURL": pdp_url,
                "Status": "Pending",
                "retailer": self.retailer,
                "region": self.region,
            }
            self.save_product(item)
            print(f" ✅ Inserted -> {pdp_url}")

        # 📌 Use fixed XPath to find next page link
        next_page_href = response.xpath('//a[contains(@aria-label, "Next page")]/@href').get()
        if next_page_href:
            next_page_url = response.urljoin(next_page_href)
            next_page_num = page + 1
            yield response.follow(
                next_page_url,
                callback=self.parse_pl,
                meta={
                    "proxy": "http://21ed11ef5c872bc7727680a52233027db4578a0e:@api.zenrows.com:8001",
                    "url": next_page_url,
                    "_id": doc_id,
                    "slug": slug,
                    "page": next_page_num,
                    "filename": f"{slug}_page{next_page_num}.html",
                    "should_be": ["card__information"]
                }
            )
            print(f"➡️ Going to next page {next_page_num}: {next_page_url}")
        else:
            print("🚫 No more pages found.")
        self.category_input.update_one(
            {"_id": doc_id},
            {"$set": {"Status": "Done"}}
        )
        print("Inserted ✅")

    def close(self, reason):
        self.mongo_client.close()

if __name__ == '__main__':
    from scrapy.cmdline import execute
    execute("scrapy crawl south_pl -a retailer=southstardrug-ph -a region=ph -a Type=eshop -a RetailerCode=southstardrug_ph".split())