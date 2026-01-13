from config import *

import requests



if __name__ == '__main__':

    url = "https://www.coles.com.au/browse"

    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'en-US,en;q=0.9,hi;q=0.8',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36',
        'Cookie': 'visid_incap_2800108=kkHlWjHHREuVtQQ5w9OLBAIyGmcAAAAAQUIPAAAAAACPV+rOKbqY7jFlUx0xytxS; _ga=GA1.1.124555730.1729770007; WTPERSIST=; _fbp=fb.2.1729770007146.657028745441558762; BVBRANDID=ecd47f60-616a-469a-97f6-9756a8879a1a; s_ecid=MCMID|19139805243360655640853082410849548668; visid_incap_3206490=r1bzGRNVRuyJqAd6TNAYUHfOGWgAAAAAQUIPAAAAAACFlI5HC9rw7i2RK0w/e9um; ld_user=a48d7f17-8bad-4a1f-b945-e2da00bb7eab; visitorId=26fb84cc-c6bf-44c6-8859-e38e66b646e8; ORA_FPC=id=2ff1a4cb-a1c3-445b-ab8e-bd4b4df8f80d; analyticsIsLoggedIn=false; incap_ses_1592_2800108=uWPfbHPn6xdY8HeT1usXFlUCMGgAAAAAJPY7yI/6ags8Ym7hQHAg+g==; dsch-visitorid=cc3213cb-9bf5-4aad-b53e-71aaf7f8bf2a; nlbi_2800108_2670698=KL2/A31vBCkAzi975VPXvwAAAABob0gugKCcWngoeAadycHf; incap_ses_166_2800108=ZJjnYGfVp2AaHMVohcBNAkE4MGgAAAAAGTVz+WBW9oy9aNNVGIdLoA==; sessionId=d535673d-fdba-4fb8-b48a-4f22fbf899c4; AMCVS_0B3D037254C7DE490A4C98A6%40AdobeOrg=1; AMCV_0B3D037254C7DE490A4C98A6%40AdobeOrg=179643557%7CMCIDTS%7C20232%7CMCMID%7C19139805243360655640853082410849548668%7CMCAAMLH-1748595397%7C8%7CMCAAMB-1748595397%7CRKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y%7CMCOPTOUT-1747997797s%7CNONE%7CMCAID%7CNONE%7CvVersion%7C5.5.0; nlbi_2800108_3037207=6buCF5q8dxUF6Q6o5VPXvwAAAADCtqcA6oVaQ8uSbuRLa2cl; at_check=true; s_cc=true; kndctr_0B3D037254C7DE490A4C98A6_AdobeOrg_identity=CiYxOTEzOTgwNTI0MzM2MDY1NTY0MDg1MzA4MjQxMDg0OTU0ODY2OFIRCMS8zvKrMhgBKgRBVVMzMAPwAfnQ7-LvMg==; dsch-searchid=f20c6373-47d0-43c4-8eb8-49484841c25a; _gcl_au=1.1.2009473898.1747990606; _fs_dwell_passed=4c37d6b9-816d-4fea-bebc-84420d26e38c; incap_ses_166_3206490=sx5Pa2jAPD0b7sVohcBNAmM4MGgAAAAAOlZSu2pmdLpmSkcPVuZ1UA==; nlbi_3206490=IOGjM8aGqE/LM/Kvzp3KBgAAAADXsULy6q3mmbtco4vIhQzY; incap_ses_1571_2800108=JCrnUrRUtmCBWNL9h1DNFeA5MGgAAAAAXLyv2pW/sy6s7/+rfRsnkw==; incap_ses_1689_2800108=87LfL9l0wXOmsZvK0IhwF5M6MGgAAAAA7Xa8sOV99T1e2DdUIfFcBA==; incap_ses_948_2800108=0J/BZUZpkAcoSjqzS/knDZE7MGgAAAAAXsDygljF95aezJjAeYKArg==; incap_ses_946_2800108=O+FXAgGbrlxt9xsSU94gDaQ7MGgAAAAAAqQp2v2kMNbODcd0wO+m7g==; incap_ses_618_2800108=s67VByAV3lpmyapKC5STCLM7MGgAAAAAjwQU/B87U866q9VR+sE+PQ==; dsch-sessionid=38b4d5cf-d2f8-4117-ab67-edac2d079299; gpv_page=cusp%3Aon-special; kndctr_0B3D037254C7DE490A4C98A6_AdobeOrg_cluster=aus3; BVBRANDSID=cdcb4ed4-59ae-497a-b389-8244db41b74e; incap_ses_1363_2800108=7TxTXexBvyad7/3VkVnqEgRIMGgAAAAATilaEPcW4rCgCe1MZ2cPRQ==; fs_lua=1.1747994635654; fs_uid=#o-210D95-na1#a5910935-f13b-4e70-8a16-9ce5a8732d96:4c37d6b9-816d-4fea-bebc-84420d26e38c:1747990600930::6#74a7a6de#/1761306120; s_ips=585; mbox=PC#d7ef1154377b45e5851aca908efde116.36_0#1811239437|session#00c11d6fd0794683aa4679ae3eca1a34#1747996519; ad-memory-token=K9rn3b5n19VZ%2Ff3GaGzFEfoaKXYKmgEKDBIKCgg0OTU0NzUwUAoMEgoKCDUzNjY5NzJQCgwSCgoIODQyMTU0NVAKDBIKCgg5MDM4MDU3UAoMEgoKCDk2OTM5MTVQCgwSCgoINTY1NTEzMVAKDBIKCggzOTkyNjI5UAoMEgoKCDc1MTMzMDlQCgwSCgoIMjM1MTI2NVAKDBIKCgg3MjUwOTM1UBIMCIeQwcEGEIzGgdsBCpkBCgwSCgoIODA4NDY2MFAKDBIKCgg2NjE4NjUxUAoMEgoKCDgwODQ2NDlQCgwSCgoIMzg2MzE3MVAKDBIKCgg5MDQzMzYzUAoMEgoKCDk2MTU5MDBQCgwSCgoIMzU3MzQ5OVAKDBIKCgg5OTc4NjY0UAoMEgoKCDM5NjI1MTVQCgwSCgoIMTQ5MjQ0M1ASCwiikMHBBhD80PVKGgIIAiIA; gpv_pathNode=cusp%3Aon-special; s_sq=%5B%5BB%5D%5D; _ga_C8RCBCKHNM=GS2.1.s1747990605$o28$g1$t1747994659$j33$l0$h0$dSdSUssh9nXd-LrwOoVYHF_0ZSLAELb-8bA; s_tp=8149; s_ppv=cusp%253Aon-special%2C7%2C7%2C7%2C584%2C13%2C1; nlbi_2800108_2147483392=ZhCtWwZ6ogUE0VRM5VPXvwAAAABvOmtTedkBnt4maSdNe1Lg; reese84=3:0pXkiqGMB7FMFKP/Q/X6PA==:QK9OgDVTqc/buuC98H12WuF+1ueQzh56LiJ3iK/N4oWTqKAXYnNGPxpieN6USayqayosmsT8+vul9+9hEFiX7TxMcJHUKBjSCqRYDigRW5rekQXtxx6OzI2RKQhkWD9vuJixCbL6bEkNlyZ+TsAiHU5722FpXK5UjRSoi1wzFQPb8ZsFoMdnEtvJVm/h5XkwbWf7X+S4S7EDMswwf097RBKgmgUjSKwJht8WTcb+7UqMLGLO8Z/JEImJLeQZrVbhffPMYQJtaOD9zbR7t1BhuSNRKEKnPBNHff/UFnvQdPJluBaP7e5NVEiS+WpbJIIhhIbdJr9tq38ugAyRhn0hGKmcYK1uHpniNSsNJIXTc/yiD695m87rhRliY++Ht+Q0kH8HuiRkX+m8BBbF77yHpa7XZDTJZgZ5Y4JFpLVcRjJbB7dTVNpQK/aX5uZJpfurq6dsbXbA52i5xWj5F1WEhw==:nDfHmP/5dn9dyq9asfw2cqngMzRHXhbo8A43PoNE074=; s_ecid=MCMID|19139805243360655640853082410849548668; dsch-visitorid=420d4982-ab0e-4b18-a485-b0f0fdb5ec12'
    }

    response = requests.request("GET", url, headers=headers)
    if response.status_code != 200:
        Rprint("Somthing went wrong in response...", response.status_code)
        exit(212)

    category_input.delete_many({})

    sel_res = Selector(text=response.text)
    script_json = sel_res.xpath('//script[@id="__NEXT_DATA__"]//text()').get()
    response = json.loads(script_json)
    # $.props.pageProps.allProductCategories.catalogGroupView[17].name
    Categories = response['props']['pageProps']['allProductCategories']['catalogGroupView']
    for Main_Cat in Categories:
        name = Main_Cat['name']
        seoToken = Main_Cat['seoToken']
        items = {
            "Category Name": name,
            "UrlFriendlyName": seoToken,
            "Status": "Pending",
        }

        try:
            category_input.insert_one(items)
            Gprint("Successfully Added...")
        except:
            pass

    de = {
    "Dairy":	"dairy-eggs-fridge",
    "Pantry":	"pantry",
    "Drinks":	"drinks",
    "Frozen":	"frozen",
    "Household":	"household",
    "Health & Beauty":	"health-beauty",
    "Baby":	"baby",
    "Pet":	"pet"
    }
    for name, seoToken in de.items():
        # name = Main_Cat['name']
        # seoToken = Main_Cat['seoToken']
        items = {
            "Category Name": name,
            "UrlFriendlyName": seoToken,
            "Status": "Pending",
        }

        try:
            category_input.insert_one(items)
            Gprint("Successfully Added...")
        except:
            pass