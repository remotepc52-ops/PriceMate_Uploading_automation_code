from threading import Thread
from time import sleep
from config import *

def fetch_data(start, end):
    data_list = product_data.find({"Status": "Pending"}).skip(int(start)).limit(int(end))
    # data_list = search_data.find({ "ProductURL": { "$regex": "6748" } })
    for cat_item in data_list:
        ID = cat_item['_id']
        ProductURL = str(cat_item['ProductURL'])
        ProductCode = str(cat_item['ProductCode'])

        data_extraction(ID, ProductURL, ProductCode)


def data_extraction(ID, url, product_code):
    try:


        filename = f'PDP_{product_code}.html'
        path = os.path.join(html_path, filename)
        full_path = path.replace("\\", "/")

        headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'accept-language': 'en-US,en;q=0.9,hi;q=0.8',
            'cache-control': 'max-age=0',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36',
            # 'Cookie': 'visid_incap_2800108=kkHlWjHHREuVtQQ5w9OLBAIyGmcAAAAAQUIPAAAAAACPV+rOKbqY7jFlUx0xytxS; _ga=GA1.1.124555730.1729770007; WTPERSIST=; _fbp=fb.2.1729770007146.657028745441558762; BVBRANDID=ecd47f60-616a-469a-97f6-9756a8879a1a; s_ecid=MCMID|19139805243360655640853082410849548668; _gcl_au=1.1.319304760.1740045763; nlbi_2800108_2670698=+D24Hb7eekbfrzbg5VPXvwAAAAAsvNq4ePxqCuOp2Qqg7Wgq; AMCVS_0B3D037254C7DE490A4C98A6%40AdobeOrg=1; nlbi_2800108_3037207=KRHgA2PSlE89ygBP5VPXvwAAAAC6GBvW6QoEgdxCTg6bbSgC; at_check=true; s_cc=true; incap_ses_423_2800108=qG1CbIs+oTnr3nHmVMzeBYc+EWgAAAAAyq6jmP6UmIzVt2NhIlLGZw==; incap_ses_1287_2800108=fDe5L1CkWkAo6dvl+FfcEYuqEWgAAAAAl6A0QamkioTrIHPLU4mddg==; nlbi_2800108=TDaRL6GhDENdajWL5VPXvwAAAABBWTDtskzx4Y6jpLbGb8yc; incap_ses_811_2800108=E2dpH65OmFRRSDI4fEBBCw1LGGgAAAAAhRkuU4GDgKWb5HLqh2SZuQ==; incap_ses_1469_2800108=235WKNhBlF07if2+/+9iFNyPGGgAAAAAoRvzvBRkENekV2vIZx7Ddw==; visid_incap_3206490=r1bzGRNVRuyJqAd6TNAYUHfOGWgAAAAAQUIPAAAAAACFlI5HC9rw7i2RK0w/e9um; nlbi_3206490=ug7CdOTARwNmw+j4zp3KBgAAAABDHXK29WyXiGiRE0uD30/q; AMCV_0B3D037254C7DE490A4C98A6%40AdobeOrg=179643557%7CMCIDTS%7C20214%7CMCMID%7C19139805243360655640853082410849548668%7CMCAAMLH-1747126526%7C8%7CMCAAMB-1747126526%7CRKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y%7CMCOPTOUT-1746528926s%7CNONE%7CMCAID%7CNONE%7CvVersion%7C5.5.0; kndctr_0B3D037254C7DE490A4C98A6_AdobeOrg_identity=CiYxOTEzOTgwNTI0MzM2MDY1NTY0MDg1MzA4MjQxMDg0OTU0ODY2OFIRCMS8zvKrMhgBKgRBVVMzMAPwAeHJuqbqMg==; s_sq=%5B%5BB%5D%5D; incap_ses_339_2800108=WO3LYYypOD3heARmA1+0BEHkGWgAAAAA8SPyLS8lT+Efxg/t5IT9lQ==; incap_ses_339_3206490=duz9SB1JbDN2igRmA1+0BFPkGWgAAAAAlmKrLAPCprWeBmCP7mPhrA==; _fs_dwell_passed=1fecae82-9235-438d-a15d-0ce4c9b9c478; gpv_page=cusp%3Aproduct%3Aproduct-details; kndctr_0B3D037254C7DE490A4C98A6_AdobeOrg_cluster=aus3; BVBRANDSID=5c93e8cc-2e7c-4561-ba8f-bd5dfc9d6f27; incap_ses_50_2800108=q7iZdZDjE2DNxtEZEKOxAFDlGWgAAAAACaBp6u0y4FSR/U33aFUCOA==; incap_ses_50_3206490=7mB3YWLn+j+/wtgZEKOxAKTmGWgAAAAA5UU2IwHg2XYIhJ2PSeiqaw==; incap_ses_974_2800108=W2HmPpgPhEhQmV/JKliEDcrmGWgAAAAAxPcWkzIZDYpNzLWoylMX8Q==; ld_user=a48d7f17-8bad-4a1f-b945-e2da00bb7eab; sessionId=2b3c6dda-b436-44e9-8144-40599f4ae7fd; visitorId=26fb84cc-c6bf-44c6-8859-e38e66b646e8; incap_ses_974_3206490=HVkOYOrSpzoHml/JKliEDcvmGWgAAAAArJvbJnlD7a5ZkAbCTQdvYg==; analyticsIsLoggedIn=false; reese84=3:7h+spX8K6ZhiSsSBTcv9cA==:LsKmgO1IMKBIge+JD2zZ+epq/mXsEfdq9ARIUrPI6JwtZXb32KvilEECT/BJI8MT5o2wmT1efMsWP4vwCvgajrjYvqWfuXVXOvkhGDEfc4GOcxD/0R14P8VGnng3UZhFieLadscIIdGQPN+Lo8ItiRe651NTjJxRz9jcpA7qyo2PvLbnTKEoSS7ij13jXFqhr5p6gpg3chYjJupJptK5YjeDder5V1zcSD428q0F26rPcWlBujx5tYRmBVB02VApJSM08zwmN8YsvcvC44AqM5/S97erKl9r1cGeN4B26IAYjEbp3BlEeWHCIF2lCXzFOLQ5w1sBHOXvGa+byaaezqJrtDGcOAXxc82OSCJ3KmjPN4eq0kBDLyNLOfDoHrJC7NlS9IlTGc3q5b/GR5LZspjNMeL2qA7xkH4OMQg2O4JTzcDmVWX9yuEDA4s7jcZs1Ysa2ar4sQCrzp/tr9CTKw==:iosRA3gAE8hIFIG/K25/RZ9efS6LNM6EX58nkvUa9zk=; s_ips=806; ORA_FPC=id=2ff1a4cb-a1c3-445b-ab8e-bd4b4df8f80d; nlbi_2800108_2147483392=xp0oMPnQODKjywiN5VPXvwAAAACfi0apdTXoF+wPW9LROvmW; fs_lua=1.1746528016962; fs_uid=#o-210D95-na1#a5910935-f13b-4e70-8a16-9ce5a8732d96:1fecae82-9235-438d-a15d-0ce4c9b9c478:1746526247117::5#74a7a6de#/1761306096; mbox=PC#d7ef1154377b45e5851aca908efde116.36_0#1809772819|session#11fa25b37cf04da991e6d7f7704ba7c3#1746529879; s_tp=4891; s_ppv=cusp%253Aproduct%253Aproduct-details%2C16%2C16%2C16%2C806%2C9%2C1; gpv_pathNode=cusp%3Aproduct%3Aproduct-details; _ga_C8RCBCKHNM=GS2.1.s1746527323$o24$g1$t1746528022$j53$l0$h0; s_ecid=MCMID|19139805243360655640853082410849548668; dsch-visitorid=420d4982-ab0e-4b18-a485-b0f0fdb5ec12'
        }

        # scraper_url = f'http://api.scraperapi.com/?api_key={scraper_api_key}&url={url}&keep_headers=true&country_code=au'

        apikey = '21ed11ef5c872bc7727680a52233027db4578a0e'

        params1 = {
            'url': url,
            'apikey': apikey,
            'custom_headers': 'true'
        }

        response = obj.to_requests(url='https://api.zenrows.com/v1/', headers=headers, params=params1, verify=False,
                                       html_path=full_path, should_be=['id="__NEXT_DATA__"'], max_retry=5)
        if not response:    
            Hprint("❌Getting blank response..... ❌", url)
            return None

        elif 'VerifyHuman' in response:
            Rprint("❌ Captcha Not Resolved after all retries executed..❌")

        elif 'Result Not Found' in response or 'Sorry, the product you  are looking for' in response or 'This page could not be found' in response:
            product_code.update_one({'_id': ID}, {'$set': {'Status': "Not found"}})
            Rprint("✅ Status updated as Result ℹ️ Not Found...")

        elif response:
            sel_res = Selector(text=response)
            json_data = sel_res.xpath('//script[@id="__NEXT_DATA__"]//text()').get()

            res_json = json.loads(json_data)

            Products = res_json['props']['pageProps']['product'] # $.props.pageProps.product

            GTIN = Products.get('gtin', "") or ""
            variation_by = Products.get('variations', "") or ""

            Variation_data = {}

            if variation_by:
                for Key in variation_by:
                    if not Key.startswith("by"):
                        continue

                    RelatedIds = []
                    By_Variant = variation_by[Key]
                    for v in By_Variant:
                        variant_id = str(v['id'])
                        RelatedIds.append(variant_id)
                    if RelatedIds:
                        Variation_data[Key.replace("by", "")] = RelatedIds

            v_data = []
            if Variation_data:
                for k, v in Variation_data.items():
                    value = ', '.join(v)
                    v_data.append(f"{k}:{value}")

            v_data = "|".join(v_data)

            is_available = Products['availability']

            Items = {
                "is_available": is_available,
                "Barcode": GTIN,
                "Variation_Data": v_data,
                "Status": "Done"
                     }

            try:
                product_data.update_one({'_id': ID}, {'$set': Items})
                Gprint("✅ Status updated as Result ℹ️ Done...")

            except Exception as e:
                print(e)
        else:
            Rprint("Somthing Went Wrong in Requests...")


    except Exception as e:
        Rprint(f"Error in Main Data Extraction function ", e)


if __name__ == '__main__':
    Gprint("🚀 Starting data scraping...")
    retry = 0
    while True and retry <= 5:
        retry += 1

        total_count = product_data.count_documents({'Status': 'Pending'})
        if not total_count:
            print("All Done...")
            break

        Bprint("Total Pending....", total_count)
        if total_count > 50:
            variable_count = total_count // 50
        else:
            variable_count = total_count // total_count

        if variable_count == 0:
            variable_count = total_count ** 2

        count = 1
        threads = [Thread(target=fetch_data, args=(i, variable_count)) for i in
                   range(0, total_count, variable_count)]

        for th in threads:
            th.start()

        for th in threads:
            th.join()

        Hprint(f"--------- Thread Ends ----------- ")
        sleep(5)

    if product_data.count_documents({'Status': 'Pending'}) == 0:
        Gprint("🎉 Finished processing all records!")
