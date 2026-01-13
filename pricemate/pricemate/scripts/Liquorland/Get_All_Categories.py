from config import *


# TODO --> Use Postalcode --> Burwood Heights, 3151 VIC | "Burwood One" in Victoria Australia

headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'en-US,en;q=0.9,hi;q=0.8',

    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36',
    'Cookie': '__uzma=302a557a-5eb9-4068-941d-462e07b6794a; __uzmb=1743510054; _gcl_au=1.1.477868672.1743510056; _fbp=fb.2.1743510056799.979000897791569590; _gid=GA1.3.1620793631.1743510057; _y2=1%3AeyJjIjp7fX0%3D%3AMTc0OTg2MjMwNA%3D%3D%3A99; KP_UIDz-ssn=0agM6d4SLMuDc0glgam6ogaWlbAnJhXE3UkFvlf49shFpuAk2KEJqX9jQNyKSasbGZravmXUJ2SpJoek71Ve0hyJJuC5jyYSA3X38cxKQWIptPg0qdVTyWYC9r4guLUu8Sz6cZCr307DDSGivEsrzw1BsEMbf8EXYX4Tyl9; KP_UIDz=0agM6d4SLMuDc0glgam6ogaWlbAnJhXE3UkFvlf49shFpuAk2KEJqX9jQNyKSasbGZravmXUJ2SpJoek71Ve0hyJJuC5jyYSA3X38cxKQWIptPg0qdVTyWYC9r4guLUu8Sz6cZCr307DDSGivEsrzw1BsEMbf8EXYX4Tyl9; ORA_FPC=id=eebb06a6-fe6a-4e14-9118-6938b567a5aa; kampyle_userid=a09a-e81c-ddb5-03bb-71b6-251e-85c0-e179; _hjSessionUser_3303846=eyJpZCI6ImVmYzBlMTYzLWZjMjEtNTczNy1hNjIxLTExMzExM2ZhM2U4ZSIsImNyZWF0ZWQiOjE3NDM1MTAwNTcxMzQsImV4aXN0aW5nIjp0cnVlfQ==; WTPERSIST=; _hjSession_3303846=eyJpZCI6ImJjMmY1NTFlLWFmMjYtNGIzNy05NmQyLWIwOWU3YmU0M2YzMSIsImMiOjE3NDM1NzQwMjk2MjYsInMiOjAsInIiOjAsInNiIjowLCJzciI6MCwic2UiOjAsImZzIjowLCJzcCI6MH0=; AMCVS_0B3D037254C7DE490A4C98A6%40AdobeOrg=1; AMCV_0B3D037254C7DE490A4C98A6%40AdobeOrg=1075005958%7CMCIDTS%7C20180%7CMCMID%7C84783557377023754803114217230757611528%7CMCAAMLH-1744178830%7C7%7CMCAAMB-1744178830%7CRKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y%7CMCOPTOUT-1743581230s%7CNONE%7CvVersion%7C4.4.1; s_cc=true; CL_LL_02_UBT=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJjX3JvbGUiOiJBbm9ueW1vdXMiLCJjX2lkIjoiezA0YWI4ZjI0LTJiOGQtNGQ3YS04OTI1LTE5MGJjN2Y3YmVjOX0iLCJjX2JyYW5kIjoibGwiLCJjX2F4X2lkIjoiIiwibmJmIjoxNzQzNTc0MTExLCJleHAiOjE3NDg3NjE3MTEsImlhdCI6MTc0MzU3NDExMSwiaXNzIjoic2VsZiIsImF1ZCI6Imh0dHBzOi8vd3d3LmNvbGVzbGlxdW9yLmNvbS5hdSJ9.1WbZq2dA8Nrt85wyA9iabkEDiJ3wbw-QeWE9gdc46m8; CL_LL_02_ULN=; CL_LL_02_UFN=; CL_LL_02_UAID=; CL_LL_02_UPOA=false; CL_LL_02_UDP=false; cto_bundle=PP-XDV9xJTJGZ25OenZsa1Y1eG9mN3RPQUtyNW9SalluMjU0cCUyQm53OTByWWNWVmklMkJFVGlZR3EwUkozS3klMkZFVGF2Y3c3TGRuTTJKcUlta25HUjVPWW5pbEFFdjhMdjB3RmJzQUlmR2pleGlyOHpqSnlwc1NKYjAyTURWVkIlMkZ4ZEx1ZkdXV1NvekN5VXc5dGNkSTVZNjRCbElwazVvS1hHWnVoTkU5UyUyQk9DMnhQalZlZlBMcHBmMnI0RGtvJTJCWHZxS2NEY3JTWkJ4N3hBayUyRkVBWTdBM2FVaVJjOHVPZUxvYWV5JTJCZERYcTJwUWQ2Um5nNkpOOEtPSFJpaDdrclFQbW1IM2dWeE9DdnJRSEY4SjBKV1Q4RDN6RHN0ZmpOQSUzRCUzRA; _ga=GA1.3.516804259.1743510056; kampyleUserSession=1743575744638; kampyleUserSessionsCount=6; kampyleSessionPageCounter=1; _yi=1%3AeyJsaSI6eyJjIjowLCJjb2wiOjE2NDk2MzkwNjgsImNwZyI6MjY2NTcwLCJjcGkiOjUxMTM4ODExMTA5LCJzYyI6MSwidHMiOjE3NDM1MTAwNjAzNTR9LCJzZSI6eyJjIjoyLCJlYyI6MzQsImxhIjoxNzQzNTc2NzIyMjYzLCJwIjo2LCJzYyI6MjY4M30sInUiOnsiaWQiOiJjYzhmNDk5OC04ZWQ1LTQ3OTItOWVhMi1mM2Q1MWVmZWI2ZTUiLCJmbCI6IjAifX0%3D%3ALTE4MDY5MDc0ODg%3D%3A99; ADRUM=s=1743576722600&r=https%3A%2F%2Fwww.liquorland.com.au%2F; __uzmc=5766816634311; __uzmd=1743576723; _ga_MZBX8BWCCN=GS1.1.1743574029.2.1.1743576723.60.0.0; __uzmc=8812016952851; __uzmd=1743577202'
}

if __name__ == '__main__':

    url = "https://www.liquorland.com.au/api/navigation/ll/vic"

    payload = {}
    scraperurl = f"http://api.scraperapi.com?api_key={scraper_api_key}&url={url}"
    response = requests.request("GET", url, headers=headers,proxies=proxies,verify=False, data=payload)
    if response.status_code != 200:
        Rprint("Somthing went wrong in response...", response.status_code)
        exit(212)

    category_input.drop()

    response = json.loads(response.text)

    for Main_Cat in response:
        MenuName = Main_Cat['name']

        navigationItems = Main_Cat['navigationItems']
        if not navigationItems:
            continue

        for cat in navigationItems:

            title = cat['title']

            for sub_cat in cat['facets']:
                itemCount = sub_cat['itemCount']
                category_name = sub_cat['title']
                Category_Url = sub_cat['url']
                if not str(Category_Url).startswith('https'):
                    Category_Url = f"https://www.liquorland.com.au{Category_Url}"

                Category_ID = generate_hashId(Category_Url)

                items = {
                    "CategoryId": Category_ID,
                    "title": title,
                    "itemCount": itemCount,
                    "CategoryName": MenuName,
                    "SubCategoryName": category_name,
                    "Category_Url": Category_Url,
                    "Status": "Pending",
                }

                category_input.insert_one(items)
                Gprint("Successfully Added...", category_name)

            else:
                moreurl = cat['more']['url']
                if not moreurl:
                    continue


                category_name = cat['more']['title']
                Category_Url = cat['more']['url']
                if not str(Category_Url).startswith('https'):
                    Category_Url = f"https://www.liquorland.com.au{Category_Url}"

                Category_ID = generate_hashId(Category_Url)

                items = {
                    "CategoryId": Category_ID,
                    "title": title,
                    "itemCount": "",
                    "CategoryName": MenuName,
                    "SubCategoryName": category_name,
                    "Category_Url": Category_Url,
                    "Status": "Pending",
                }

                category_input.insert_one(items)
                Gprint("Successfully Added...", category_name)