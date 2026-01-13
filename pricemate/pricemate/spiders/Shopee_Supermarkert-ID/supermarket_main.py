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

headers = {
    'Accept': 'application/json',
    # 'Accept-Encoding': 'gzip, deflate, br, zstd',
    'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8',
    'af-ac-enc-dat': '3babd6970e495bd5',
    'af-ac-enc-sz-token': 'DJzWBdVFQUBY+1g9pbjTlQ==|DRqp0gJY//ltt3bj2u4GVVxcWA8iOkZRyRJdar4QTb8aA+kigIptL5+csi9f+c0eVUtRRBWNRqzIvQ==|Zt3L1+tGk7CdaMdH|08|3',
    'Connection': 'keep-alive',
    'Content-Type': 'application/json',
    'Cookie': 'SPC_F=0AXhSdTWf9nAuk2tNbe3kUeroYC3nWiu; REC_T_ID=8b9ef820-9a07-11f0-b184-caf6988b41b1; _QPWSDCXHZQA=dfc64379-ddad-4f3d-cf8d-4204d8c810e8; REC7iLP4Q=11e6e0de-2f01-4d05-8d64-98099cf9752f; SPC_SEC_SI=v1-U1ZvSWVpSVF4c0hQQmlSTEiN0HMcd3WcRLRmr8iMfTKKeIDyzXAXBopEYBM/ec5CBwe99lnBLBYiDTkN1yKJH04o8Az6IpYjHDsuNHq4qxk=; SPC_SI=fz7jaAAAAABrNzcxTm5CZdFSBAAAAAAAblB1dHh1Wjk=; SPC_CLIENTID=MEFYaFNkVFdmOW5Biucaaueswsfyflkd; SPC_ST=.VmcxdDRWaWRBRHlNVXNxUbQozHeD2ZXK2GNpx/9zyI1plrwuqhJINj0VxjtWYyXZxiOPh83pr261mB11Jr1pJUU0vJKm5JHIQRIDl/QpTCKh19CVXBbxorqTF094mZTdsbf70TTXCBdIfXqvHiWdYN++RCTtVvc/+rrPpUeDgNkvTgWMiZVV3p4ymnjOrTWsQbg2My8NGExqjP0RYkt/Olq7pOZ4VdtAvjve2EufZHsWEd+IOag2kCRcg80pAWC1s+KPAaalPRkewIXPvZbiqg==; ...',
    'd-nonptcha-sync': 'AAAG3yynKCgA|6|B61wEysenmT7Ig=',
    'Host': 'shopee.co.sg',
    'Referer': 'https://shopee.co.sg/supermarket/all-products?page=0',
    'sec-ch-ua': '"Chromium";v="140", "Not=A?Brand";v="24", "Google Chrome";v="140"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'sz-token': 'DJzWBdVFQUBY+1g9pbjTlQ==|DRqp0gJY//ltt3bj2u4GVVxcWA8iOkZRyRJdar4QTb8aA+kigIptL5+csi9f+c0eVUtRRBWNRqzIvQ==|Zt3L1+tGk7CdaMdH|08|3',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36',
    'X-API-SOURCE': 'pc',
    'X-CSRFToken': '1yCEaoeXuIWwsx9gS5Rij98uZ29AtmSm',
    'X-Requested-With': 'XMLHttpRequest',
    'x-sap-ri': '27a4e368fc8ab3c664ae903a0701f6fe2e301f9672d8ae45d43a',
    'x-sap-sec': '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',
    'X-Shopee-Language': 'sg',
    'x-sz-sdk-version': '1.12.22-1',
}


class SupermarketSpider(PricemateBaseSpider):
    name = "supermarket_main"

    def __init__(self, retailer, region, *args, **kwargs):
        super().__init__(retailer=retailer, region=region, *args, **kwargs)



    def start_requests(self):
        url = 'https://shopee.co.sg/api/v4/search/search_mart_items?by=relevancy&limit=25&newest=0&order=desc'

        yield scrapy.Request(
            url=url,
            # cookies=cookies,
            headers=headers,
            callback=self.parse_pdp,
            meta={
                "url": url,
                "filename": f"PDP_{self.generate_hash_id(url)}.html",
                "page": 0,
                "should_be": ["data"]
            }

        )
    def parse_pdp(self, response):
        def format_shopee_price(price):
            formatted_price = price / 100000
            r = f"{formatted_price:,.2f}".replace('.', ',')
            if r.endswith(',00'):
                r = r[:-3]
            return r.replace(",", "")
        meta = response.meta
        page = meta.get("page", 0)
        data_ = {"total": 0}
        json_data = json.loads(response.text)

        try:
            total = json_data['data']['items']
        except Exception as e:
            print("Error --> ", e)
            return
        try:
            product_list = json_data['data']['items']
        except:
            try:
                product_list = json_data['data']['centralize_item_card']['item_cards']
            except:
                try:
                    product_list = json_data['centralize_item_card']['item_cards']
                except:
                    product_list = json_data['items']

        for product in product_list:
            data_['total'] += 1
            try:  # data.items[1].item_basic.shopid
                shopid = product['item_basic']['shopid']
            except:
                shopid = product['shopid']

            try:
                shop_name = ''.join(product['item_basic']['shop_name'].split())
            except:
                try:
                    shop_name = ''.join(product['shop_name'].split())
                except:
                    shop_name = ''.join(product['shop_data']['shop_name'].split())

            try:
                brand = product['item_basic']['brand']
            except:
                try:
                    brand = product['brand']
                except:
                    brand = product['global_brand'].get('display_name', "")

            try:
                historical_sold = product['item_basic']['historical_sold']
            except:
                try:
                    historical_sold = product['historical_sold']
                except:
                    historical_sold = product['item_card_display_sold_count']['historical_sold_count']
                    if not historical_sold:
                        historical_sold = product['item_card_display_sold_count'].get('historical_sold_count_text', 0)

            try:
                sold = product['item_basic']['sold']
            except:
                try:
                    sold = product['sold']
                except:
                    sold = product['item_card_display_sold_count']['monthly_sold_count']
                    if not sold:
                        sold = product['item_card_display_sold_count'].get('monthly_sold_count_text', 0)

            try:
                itemid = product['item_basic']['itemid']
            except:
                itemid = product['itemid']

            product_url = f"https://shopee.co.sg/Vanish-i.{shopid}.{itemid}"

            # data.items[0].item_basic.price
            try:
                regular_price1 = product['item_basic']['price']
            except:
                try:
                    regular_price1 = product['price']
                except:
                    regular_price1 = product['item_card_display_price']['price']

            try:
                price_before_discount1 = product['item_basic']['price_before_discount']
            except:
                try:
                    price_before_discount1 = product['price_before_discount']
                except:
                    price_before_discount1 = product['item_card_display_price'].get('strikethrough_price', "")

            # If there's no price before discount, consider the regular and final price to be the same
            if not price_before_discount1:
                markdown = ""
                regular_price = format_shopee_price(regular_price1)
                final_price = format_shopee_price(regular_price1)
            else:
                if price_before_discount1 > regular_price1:
                    regular_price_candidate = price_before_discount1
                    markdown_price_candidate = regular_price1
                else:
                    regular_price_candidate = regular_price1
                    markdown_price_candidate = price_before_discount1

                regular_price = format_shopee_price(regular_price_candidate)
                final_price = format_shopee_price(markdown_price_candidate)
                markdown = format_shopee_price(markdown_price_candidate)
            if regular_price > final_price:
                rrp =regular_price
            else:
                rrp =final_price
            try:
                try:
                    status = product['item_basic']['status']
                except:
                    status = product['status']

                if status:
                    isOos = False

                else:
                    isOos = True
            except:
                isOos = True

            # product name from website
            try:
                product_name = product['item_basic']['name']
            except:
                try:
                    product_name = product['name']
                except:
                    product_name = product['item_card_displayed_asset']['name']

            try:  # $.data.centralize_item_card.item_cards[1].item_rating.rating_star
                ratingScore = product['item_basic']['item_rating']['rating_star']
                if ratingScore:
                    ratingScore = round(float(ratingScore), 1)
            except:
                ratingScore = product['item_rating']['rating_star']
                if ratingScore:
                    ratingScore = round(float(ratingScore), 1)

            try:  # $.data.items[9].item_basic.item_rating.rating_count[0]
                reviews = product['item_basic']['item_rating']['rating_count']
                reviews = int(reviews[0])
            except:
                reviews = product['item_rating']['rating_count'][0]
                reviews = int(reviews)

            try:  # data.items[0].item_basic.discount
                offer = product['item_basic']['discount']
            except:
                offer = product['discount']

            try:
                images = product['item_basic']['images']
                base_url = "https://down-my.img.susercontent.com/file/"
                img = "|".join([base_url + image for image in images])

            except:
                images = product['image']
                base_url = "https://down-my.img.susercontent.com/file/"
                img = "|".join([base_url + image for image in images])

            item = {
                # "Store name": shop_name.title(),
                # "Store URL": StoreURL,
                # "brand_filter": "",
                "ProductCode": itemid,
                "Name": product_name,
                "ProductURL": product_url,
                "retailer_name": "shopee_supermarket_sg",
                # "Seller URL": StoreURL,
                "is_available": True if not isOos else False,
                "Brand": brand,
                "Images": img,
                "Promo_Type": "",
                "per_unit_price": "",
                "Barcode": "",
                # "Currency": CurrencySymbol,
                "WasPrice": regular_price,
                "Price": final_price,
                "RRP": rrp,
                "Offer_info": offer,
                # "Monthly Item Sold": sold,
                # "Historical Item Sold": historical_sold,
                # "Avg Rating": ratingScore,
                # "Total Review": reviews,
                "Category_Hierarchy": "",
                "Status": "Done",

            }
            self.save_product(item)
            print(f"Product URL Inserted !")

        no_more = json_data.get("data", {}).get("no_more", False)
        if not no_more:
            next_page = page + 1
            # construct the next API URL accordingly, using offset or page param
            next_url = f"https://shopee.co.sg/api/v4/search/search_mart_items?by=relevancy&limit=25&newest={next_page * 25}&order=desc"
            meta = {"page": next_page, "filename": f"PDP_{self.generate_hash_id(next_url)}_{next_page}.html",
                    "should_be": ["data"]}
            yield scrapy.Request(url=next_url,
                                 callback=self.parse_pdp,
                                 meta=meta,
                                 )

            print(f"Product URL Inserted !")

    def close(self, reason):
        self.mongo_client.close()

if __name__ == '__main__':
    from scrapy.cmdline import execute
    execute(
        "scrapy crawl supermarket_main -a retailer=shopee_supermarket_sg -a region=sg -a Type=eshop -a RetailerCode=shopee_supermarket_sg".split())