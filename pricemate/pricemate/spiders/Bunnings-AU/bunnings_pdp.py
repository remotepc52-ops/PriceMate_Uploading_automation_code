# import json
# from urllib.parse import quote
# import scrapy
# import re
# import os, sys
# sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# from pricemate.spiders.base_spider import PricemateBaseSpider
#
# cookies = {
#     'personalization_session_id': '42091470-9e7c-11f0-9c25-05a3b860e1dd',
#     'defaultStoreId': '6400',
#     'defaultRegionCode': 'VICMetro',
#     '_evga_dbf4': '{%22uuid%22:%2276ae763ad7eb5422%22}',
#     '_sfid_4bdd': '{%22anonymousId%22:%2276ae763ad7eb5422%22%2C%22consents%22:[]}',
#     'BVBRANDID': 'd0bf7229-a302-49c0-8c11-e1ca56361080',
#     'recentSearches': 'offer',
#     'nodeServed': 'true',
#     'uSessionId': '3ac2a810-a8c3-11f0-bc41-ffb3a16559f6',
#     'budp_au#lang': 'en',
#     'ASP.NET_SessionId': 'tmxtxwodf1ffe5exqhdiysif',
#     '_cfuvid': '5N52kJ8rDQgoqYaywENo8ZgQcX.CfuyyT0HDyoTP1zU-1760421691806-0.0.1.1-604800000',
#     'enableNewAuthFlowBrowser': 'true',
#     'coveo_visitorId': '066dedb0-7bcd-43dc-8a44-244897274b27',
#     'returningVisitor': 'true',
#     'unleash-properties': '%7B%22channel%22%3A%22web%22%2C%22country%22%3A%22au%22%2C%22division%22%3A%22retail%22%7D',
#     'guest-token-storage': '{"expires":1760853697512,"s":432000,"token":"eyJhbGciOiJSUzI1NiIsImtpZCI6IkJGRTFEMDBBRUZERkVDNzM4N0E1RUFFMzkxNjRFM0MwMUJBNzVDODciLCJ4NXQiOiJ2LUhRQ3VfZjdIT0hwZXJqa1dUandCdW5YSWMiLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJodHRwczovL2J1bm5pbmdzLmNvbS5hdS8iLCJuYmYiOjE3NjA0MjE2OTYsImlhdCI6MTc2MDQyMTY5NiwiZXhwIjoxNzYwODUzNjk2LCJhdWQiOlsiQ2hlY2tvdXQtQXBpIiwiY3VzdG9tZXJfYnVubmluZ3MiLCJWb3VjaGVyLUFwaSIsIkJhc2tldC1BcGkiLCJodHRwczovL2J1bm5pbmdzLmNvbS5hdS9yZXNvdXJjZXMiXSwic2NvcGUiOlsiY2hrOmV4ZWMiLCJjbTphY2Nlc3MiLCJlY29tOmFjY2VzcyIsImNoazpwdWIiLCJ2Y2g6cHVibGljIiwiYnNrOnB1YiJdLCJhbXIiOlsiZXh0ZXJuYWwiXSwiY2xpZW50X2lkIjoiYnVkcF9ndWVzdF91c2VyX2F1Iiwic3ViIjoiYTc3YTQ5OTYtZjRlOS00ZGM3LWJlNTctNDE2ZGQ3ZDk3NGYzIiwiYXV0aF90aW1lIjoxNzYwNDIxNjk1LCJpZHAiOiJsb2NhbGxvb3BiYWNrIiwiYi1pZCI6ImE3N2E0OTk2LWY0ZTktNGRjNy1iZTU3LTQxNmRkN2Q5NzRmMyIsImItcm9sZSI6Imd1ZXN0IiwiYi10eXBlIjoiZ3Vlc3QiLCJsb2NhbGUiOiJlbl9BVSIsImItY291bnRyeSI6IkFVIiwiYWN0aXZhdGlvbl9zdGF0dXMiOiJGYWxzZSIsInVzZXJfbmFtZSI6ImE3N2E0OTk2LWY0ZTktNGRjNy1iZTU3LTQxNmRkN2Q5NzRmMyIsImItcmJhYyI6W3siYXNjIjoiYTc3YTQ5OTYtZjRlOS00ZGM3LWJlNTctNDE2ZGQ3ZDk3NGYzIiwidHlwZSI6IkMiLCJyb2wiOlsiQ0hLOkd1ZXN0IiwiVkNIOkd1ZXN0Il19LHsiYXNjIjoiZUNvbW1lcmNlLWE3N2E0OTk2LWY0ZTktNGRjNy1iZTU3LTQxNmRkN2Q5NzRmMyIsInR5cGUiOiJDVFhTIiwicm9sIjpbIkJTSzpHdWVzdCJdfV0sInNpZCI6IjA2M0U5REM3NDg2MjkyNzA3MjY4MDE0Rjg0Mzc1NTFFIiwianRpIjoiNjA2Njk5OTg1MDVGODQwQjQ3NTdFQTUwQUI3NDFFODMifQ.cVi5-iwVoMisPRfm9Xfqbr8OaHx7RXnrYhqCgT6caa5vfVYEirbZ2yrkfoBbL9lt3OJbfOx7Qrqdv5I8MEdNMPLIuw7ZUt_wv0r4l-ajiNt4WfPPnynmuh35AJ0rN0YwpNtDqIAnUok82AD_rVD4iPUQLtvtGRcuJqdtysMZJrEFXmzcgR0UxZrlaxwXeAKX8KX_aa43__G7Ar5dB5Bb4ujq891CRz9ETxiuB_vL_VyStQyesZEtTS1e-aGhqVGYe9khDY62foY2XePVdBApi7fsfjWBWR1if4ad1OMxRYpOg0PrLd0VGBE6dScVRL2dpFbCyOrUtnIcb8QeG8xysw","clientToken":true}',
#     'GuestAuthentication': 'eyJhbGciOiJSUzI1NiIsImtpZCI6IkJGRTFEMDBBRUZERkVDNzM4N0E1RUFFMzkxNjRFM0MwMUJBNzVDODciLCJ4NXQiOiJ2LUhRQ3VfZjdIT0hwZXJqa1dUandCdW5YSWMiLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJodHRwczovL2J1bm5pbmdzLmNvbS5hdS8iLCJuYmYiOjE3NjA0MjE2OTYsImlhdCI6MTc2MDQyMTY5NiwiZXhwIjoxNzYwODUzNjk2LCJhdWQiOlsiQ2hlY2tvdXQtQXBpIiwiY3VzdG9tZXJfYnVubmluZ3MiLCJWb3VjaGVyLUFwaSIsIkJhc2tldC1BcGkiLCJodHRwczovL2J1bm5pbmdzLmNvbS5hdS9yZXNvdXJjZXMiXSwic2NvcGUiOlsiY2hrOmV4ZWMiLCJjbTphY2Nlc3MiLCJlY29tOmFjY2VzcyIsImNoazpwdWIiLCJ2Y2g6cHVibGljIiwiYnNrOnB1YiJdLCJhbXIiOlsiZXh0ZXJuYWwiXSwiY2xpZW50X2lkIjoiYnVkcF9ndWVzdF91c2VyX2F1Iiwic3ViIjoiYTc3YTQ5OTYtZjRlOS00ZGM3LWJlNTctNDE2ZGQ3ZDk3NGYzIiwiYXV0aF90aW1lIjoxNzYwNDIxNjk1LCJpZHAiOiJsb2NhbGxvb3BiYWNrIiwiYi1pZCI6ImE3N2E0OTk2LWY0ZTktNGRjNy1iZTU3LTQxNmRkN2Q5NzRmMyIsImItcm9sZSI6Imd1ZXN0IiwiYi10eXBlIjoiZ3Vlc3QiLCJsb2NhbGUiOiJlbl9BVSIsImItY291bnRyeSI6IkFVIiwiYWN0aXZhdGlvbl9zdGF0dXMiOiJGYWxzZSIsInVzZXJfbmFtZSI6ImE3N2E0OTk2LWY0ZTktNGRjNy1iZTU3LTQxNmRkN2Q5NzRmMyIsImItcmJhYyI6W3siYXNjIjoiYTc3YTQ5OTYtZjRlOS00ZGM3LWJlNTctNDE2ZGQ3ZDk3NGYzIiwidHlwZSI6IkMiLCJyb2wiOlsiQ0hLOkd1ZXN0IiwiVkNIOkd1ZXN0Il19LHsiYXNjIjoiZUNvbW1lcmNlLWE3N2E0OTk2LWY0ZTktNGRjNy1iZTU3LTQxNmRkN2Q5NzRmMyIsInR5cGUiOiJDVFhTIiwicm9sIjpbIkJTSzpHdWVzdCJdfV0sInNpZCI6IjA2M0U5REM3NDg2MjkyNzA3MjY4MDE0Rjg0Mzc1NTFFIiwianRpIjoiNjA2Njk5OTg1MDVGODQwQjQ3NTdFQTUwQUI3NDFFODMifQ.cVi5-iwVoMisPRfm9Xfqbr8OaHx7RXnrYhqCgT6caa5vfVYEirbZ2yrkfoBbL9lt3OJbfOx7Qrqdv5I8MEdNMPLIuw7ZUt_wv0r4l-ajiNt4WfPPnynmuh35AJ0rN0YwpNtDqIAnUok82AD_rVD4iPUQLtvtGRcuJqdtysMZJrEFXmzcgR0UxZrlaxwXeAKX8KX_aa43__G7Ar5dB5Bb4ujq891CRz9ETxiuB_vL_VyStQyesZEtTS1e-aGhqVGYe9khDY62foY2XePVdBApi7fsfjWBWR1if4ad1OMxRYpOg0PrLd0VGBE6dScVRL2dpFbCyOrUtnIcb8QeG8xysw',
#     'ctz': '-5.5',
#     'rxVisitor': '1760421745988HI88819HEEL1O9AQVR2E877IJV949IA7',
#     'dtSa': '-',
#     'SC_ANALYTICS_GLOBAL_COOKIE': '5df20b49c47e449b959b3985fac8547c|False',
#     '_cfuvid': 'wSlQvcFfIqM_JgtOQz7U5j7x3uu8uCDj0UylgOpVG_c-1760426080364-0.0.1.1-604800000',
#     'dtPC': '10$25831572_440h9p10$26082040_827h1vADUFMVCARCJSLNUNWMMBRWAMFAPFRFFQ-0e0',
#     'dtCookie': 'v_4_srv_10_sn_3265B942F4AAD726F407AACDC4883E21_perc_100000_ol_0_mul_1_app-3Aea7c4b59f27d43eb_1_app-3A538efd036e45e9dd_0_rcs-3Acss_1',
#     'rxvt': '1760427883599|1760425831576',
#     'AccessTokenCookie': '%7B%22tokenvalue%22%3A%22a77a4996-f4e9-4dc7-be57-416dd7d974f3-1760421695%22%2C%22lastchecktime%22%3A%2210%2F14%2F2025%208%3A17%3A00%20AM%22%7D',
#     '__RequestVerificationToken': '_t2RpxI0BbMY_hqb1GDTrcSvnpn-M5I2RXWJ6aKnRgnxJvXm6YQOeb4DWpt4v8wukn_MCZGFJplpWhQNndwqFpMQ91R5uF79zUkugl904wY1',
#     '__cf_bm': 'CV7.N1a8boKRDln77mhVAAJqzORRbWUmt3PfGiYvP2I-1760429821-1.0.1.1-0QyKvNgGBsrXB21_Cqkmiajg5qj3OukcfMjX_xjM27Yqg.uZxM7QSJHSWS7deb.HrmfHL4SUKD17rXpFWi.adEBz.kYAtugu4xYF5926o_A',
#     'origin_path': '/sandleford-450-x-600mm-no-smoking-plastic-sign_p3291261',
#     'AWSALB': 'qIWaXGuHQWW2XHpPm3359Ec/tMhkAQMSe3+Oxojf5F9Vak9bwQylTSqP5FO2Op6k9iIYdL0hQEOyA8UAdfrTPFpvGCP7zZaVs/5VRfgCbZlTM5baDBAuEDCQI8vR',
#     'AWSALBCORS': 'qIWaXGuHQWW2XHpPm3359Ec/tMhkAQMSe3+Oxojf5F9Vak9bwQylTSqP5FO2Op6k9iIYdL0hQEOyA8UAdfrTPFpvGCP7zZaVs/5VRfgCbZlTM5baDBAuEDCQI8vR',
#     'LiSESSIONID': 'B53DED5D53E1812C0F80882CD85CFC9E',
#     'cf_clearance': 'n0tNN16Bldt9fkM8HDbCgUDOx9lVxd3jwFUcMHZgyP8-1760429822-1.2.1.1-D1wq5B3yDYzr6xXNCTmdUEWY4BZwrQMeQTzXoRxo.RLSj6RSv3H89379gwefiADY8gmMu4Qe33h3TXesmKmtAITCqnnNzsTCaCKyH6jA33Ew1Tz.bK.r1EUZQjJ8QOvE58DlsGdN4FZ.Vg_c_QQC9XwV_OirmskEwd3xUmqqey3aPq2rVQ2X5ghDtKv7jpwU7Y7thgx3KYJ2SylRWtxLeoBsNuFAuiaPRBgTjZ3b25s',
#     'ROUTE': '.api-6db5bc497d-nbtpj',
#     'inside-au12': '1018695040-20b0b907563f4a59fbb3f6f2241ef46a012fbdfbfbc28e6e1290c54c3bcb5192-0-0',
# }
#
# headers = {
#     'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
#     'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
#     'cache-control': 'max-age=0',
#     'priority': 'u=0, i',
#     'referer': 'https://www.bunnings.com.au/products/garden/letterboxes/letterbox-signs?page=2',
#     'sec-ch-ua': '"Google Chrome";v="141", "Not?A_Brand";v="8", "Chromium";v="141"',
#     'sec-ch-ua-arch': '"x86"',
#     'sec-ch-ua-bitness': '"64"',
#     'sec-ch-ua-full-version': '"141.0.7390.67"',
#     'sec-ch-ua-full-version-list': '"Google Chrome";v="141.0.7390.67", "Not?A_Brand";v="8.0.0.0", "Chromium";v="141.0.7390.67"',
#     'sec-ch-ua-mobile': '?0',
#     'sec-ch-ua-model': '""',
#     'sec-ch-ua-platform': '"Windows"',
#     'sec-ch-ua-platform-version': '"19.0.0"',
#     'sec-fetch-dest': 'document',
#     'sec-fetch-mode': 'navigate',
#     'sec-fetch-site': 'same-origin',
#     'sec-fetch-user': '?1',
#     'upgrade-insecure-requests': '1',
#     'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36',
#     # 'cookie': 'personalization_session_id=42091470-9e7c-11f0-9c25-05a3b860e1dd; defaultStoreId=6400; defaultRegionCode=VICMetro; _evga_dbf4={%22uuid%22:%2276ae763ad7eb5422%22}; _sfid_4bdd={%22anonymousId%22:%2276ae763ad7eb5422%22%2C%22consents%22:[]}; BVBRANDID=d0bf7229-a302-49c0-8c11-e1ca56361080; recentSearches=offer; nodeServed=true; uSessionId=3ac2a810-a8c3-11f0-bc41-ffb3a16559f6; budp_au#lang=en; ASP.NET_SessionId=tmxtxwodf1ffe5exqhdiysif; _cfuvid=5N52kJ8rDQgoqYaywENo8ZgQcX.CfuyyT0HDyoTP1zU-1760421691806-0.0.1.1-604800000; enableNewAuthFlowBrowser=true; coveo_visitorId=066dedb0-7bcd-43dc-8a44-244897274b27; returningVisitor=true; unleash-properties=%7B%22channel%22%3A%22web%22%2C%22country%22%3A%22au%22%2C%22division%22%3A%22retail%22%7D; guest-token-storage={"expires":1760853697512,"s":432000,"token":"eyJhbGciOiJSUzI1NiIsImtpZCI6IkJGRTFEMDBBRUZERkVDNzM4N0E1RUFFMzkxNjRFM0MwMUJBNzVDODciLCJ4NXQiOiJ2LUhRQ3VfZjdIT0hwZXJqa1dUandCdW5YSWMiLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJodHRwczovL2J1bm5pbmdzLmNvbS5hdS8iLCJuYmYiOjE3NjA0MjE2OTYsImlhdCI6MTc2MDQyMTY5NiwiZXhwIjoxNzYwODUzNjk2LCJhdWQiOlsiQ2hlY2tvdXQtQXBpIiwiY3VzdG9tZXJfYnVubmluZ3MiLCJWb3VjaGVyLUFwaSIsIkJhc2tldC1BcGkiLCJodHRwczovL2J1bm5pbmdzLmNvbS5hdS9yZXNvdXJjZXMiXSwic2NvcGUiOlsiY2hrOmV4ZWMiLCJjbTphY2Nlc3MiLCJlY29tOmFjY2VzcyIsImNoazpwdWIiLCJ2Y2g6cHVibGljIiwiYnNrOnB1YiJdLCJhbXIiOlsiZXh0ZXJuYWwiXSwiY2xpZW50X2lkIjoiYnVkcF9ndWVzdF91c2VyX2F1Iiwic3ViIjoiYTc3YTQ5OTYtZjRlOS00ZGM3LWJlNTctNDE2ZGQ3ZDk3NGYzIiwiYXV0aF90aW1lIjoxNzYwNDIxNjk1LCJpZHAiOiJsb2NhbGxvb3BiYWNrIiwiYi1pZCI6ImE3N2E0OTk2LWY0ZTktNGRjNy1iZTU3LTQxNmRkN2Q5NzRmMyIsImItcm9sZSI6Imd1ZXN0IiwiYi10eXBlIjoiZ3Vlc3QiLCJsb2NhbGUiOiJlbl9BVSIsImItY291bnRyeSI6IkFVIiwiYWN0aXZhdGlvbl9zdGF0dXMiOiJGYWxzZSIsInVzZXJfbmFtZSI6ImE3N2E0OTk2LWY0ZTktNGRjNy1iZTU3LTQxNmRkN2Q5NzRmMyIsImItcmJhYyI6W3siYXNjIjoiYTc3YTQ5OTYtZjRlOS00ZGM3LWJlNTctNDE2ZGQ3ZDk3NGYzIiwidHlwZSI6IkMiLCJyb2wiOlsiQ0hLOkd1ZXN0IiwiVkNIOkd1ZXN0Il19LHsiYXNjIjoiZUNvbW1lcmNlLWE3N2E0OTk2LWY0ZTktNGRjNy1iZTU3LTQxNmRkN2Q5NzRmMyIsInR5cGUiOiJDVFhTIiwicm9sIjpbIkJTSzpHdWVzdCJdfV0sInNpZCI6IjA2M0U5REM3NDg2MjkyNzA3MjY4MDE0Rjg0Mzc1NTFFIiwianRpIjoiNjA2Njk5OTg1MDVGODQwQjQ3NTdFQTUwQUI3NDFFODMifQ.cVi5-iwVoMisPRfm9Xfqbr8OaHx7RXnrYhqCgT6caa5vfVYEirbZ2yrkfoBbL9lt3OJbfOx7Qrqdv5I8MEdNMPLIuw7ZUt_wv0r4l-ajiNt4WfPPnynmuh35AJ0rN0YwpNtDqIAnUok82AD_rVD4iPUQLtvtGRcuJqdtysMZJrEFXmzcgR0UxZrlaxwXeAKX8KX_aa43__G7Ar5dB5Bb4ujq891CRz9ETxiuB_vL_VyStQyesZEtTS1e-aGhqVGYe9khDY62foY2XePVdBApi7fsfjWBWR1if4ad1OMxRYpOg0PrLd0VGBE6dScVRL2dpFbCyOrUtnIcb8QeG8xysw","clientToken":true}; GuestAuthentication=eyJhbGciOiJSUzI1NiIsImtpZCI6IkJGRTFEMDBBRUZERkVDNzM4N0E1RUFFMzkxNjRFM0MwMUJBNzVDODciLCJ4NXQiOiJ2LUhRQ3VfZjdIT0hwZXJqa1dUandCdW5YSWMiLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJodHRwczovL2J1bm5pbmdzLmNvbS5hdS8iLCJuYmYiOjE3NjA0MjE2OTYsImlhdCI6MTc2MDQyMTY5NiwiZXhwIjoxNzYwODUzNjk2LCJhdWQiOlsiQ2hlY2tvdXQtQXBpIiwiY3VzdG9tZXJfYnVubmluZ3MiLCJWb3VjaGVyLUFwaSIsIkJhc2tldC1BcGkiLCJodHRwczovL2J1bm5pbmdzLmNvbS5hdS9yZXNvdXJjZXMiXSwic2NvcGUiOlsiY2hrOmV4ZWMiLCJjbTphY2Nlc3MiLCJlY29tOmFjY2VzcyIsImNoazpwdWIiLCJ2Y2g6cHVibGljIiwiYnNrOnB1YiJdLCJhbXIiOlsiZXh0ZXJuYWwiXSwiY2xpZW50X2lkIjoiYnVkcF9ndWVzdF91c2VyX2F1Iiwic3ViIjoiYTc3YTQ5OTYtZjRlOS00ZGM3LWJlNTctNDE2ZGQ3ZDk3NGYzIiwiYXV0aF90aW1lIjoxNzYwNDIxNjk1LCJpZHAiOiJsb2NhbGxvb3BiYWNrIiwiYi1pZCI6ImE3N2E0OTk2LWY0ZTktNGRjNy1iZTU3LTQxNmRkN2Q5NzRmMyIsImItcm9sZSI6Imd1ZXN0IiwiYi10eXBlIjoiZ3Vlc3QiLCJsb2NhbGUiOiJlbl9BVSIsImItY291bnRyeSI6IkFVIiwiYWN0aXZhdGlvbl9zdGF0dXMiOiJGYWxzZSIsInVzZXJfbmFtZSI6ImE3N2E0OTk2LWY0ZTktNGRjNy1iZTU3LTQxNmRkN2Q5NzRmMyIsImItcmJhYyI6W3siYXNjIjoiYTc3YTQ5OTYtZjRlOS00ZGM3LWJlNTctNDE2ZGQ3ZDk3NGYzIiwidHlwZSI6IkMiLCJyb2wiOlsiQ0hLOkd1ZXN0IiwiVkNIOkd1ZXN0Il19LHsiYXNjIjoiZUNvbW1lcmNlLWE3N2E0OTk2LWY0ZTktNGRjNy1iZTU3LTQxNmRkN2Q5NzRmMyIsInR5cGUiOiJDVFhTIiwicm9sIjpbIkJTSzpHdWVzdCJdfV0sInNpZCI6IjA2M0U5REM3NDg2MjkyNzA3MjY4MDE0Rjg0Mzc1NTFFIiwianRpIjoiNjA2Njk5OTg1MDVGODQwQjQ3NTdFQTUwQUI3NDFFODMifQ.cVi5-iwVoMisPRfm9Xfqbr8OaHx7RXnrYhqCgT6caa5vfVYEirbZ2yrkfoBbL9lt3OJbfOx7Qrqdv5I8MEdNMPLIuw7ZUt_wv0r4l-ajiNt4WfPPnynmuh35AJ0rN0YwpNtDqIAnUok82AD_rVD4iPUQLtvtGRcuJqdtysMZJrEFXmzcgR0UxZrlaxwXeAKX8KX_aa43__G7Ar5dB5Bb4ujq891CRz9ETxiuB_vL_VyStQyesZEtTS1e-aGhqVGYe9khDY62foY2XePVdBApi7fsfjWBWR1if4ad1OMxRYpOg0PrLd0VGBE6dScVRL2dpFbCyOrUtnIcb8QeG8xysw; ctz=-5.5; rxVisitor=1760421745988HI88819HEEL1O9AQVR2E877IJV949IA7; dtSa=-; SC_ANALYTICS_GLOBAL_COOKIE=5df20b49c47e449b959b3985fac8547c|False; _cfuvid=wSlQvcFfIqM_JgtOQz7U5j7x3uu8uCDj0UylgOpVG_c-1760426080364-0.0.1.1-604800000; dtPC=10$25831572_440h9p10$26082040_827h1vADUFMVCARCJSLNUNWMMBRWAMFAPFRFFQ-0e0; dtCookie=v_4_srv_10_sn_3265B942F4AAD726F407AACDC4883E21_perc_100000_ol_0_mul_1_app-3Aea7c4b59f27d43eb_1_app-3A538efd036e45e9dd_0_rcs-3Acss_1; rxvt=1760427883599|1760425831576; AccessTokenCookie=%7B%22tokenvalue%22%3A%22a77a4996-f4e9-4dc7-be57-416dd7d974f3-1760421695%22%2C%22lastchecktime%22%3A%2210%2F14%2F2025%208%3A17%3A00%20AM%22%7D; __RequestVerificationToken=_t2RpxI0BbMY_hqb1GDTrcSvnpn-M5I2RXWJ6aKnRgnxJvXm6YQOeb4DWpt4v8wukn_MCZGFJplpWhQNndwqFpMQ91R5uF79zUkugl904wY1; __cf_bm=CV7.N1a8boKRDln77mhVAAJqzORRbWUmt3PfGiYvP2I-1760429821-1.0.1.1-0QyKvNgGBsrXB21_Cqkmiajg5qj3OukcfMjX_xjM27Yqg.uZxM7QSJHSWS7deb.HrmfHL4SUKD17rXpFWi.adEBz.kYAtugu4xYF5926o_A; origin_path=/sandleford-450-x-600mm-no-smoking-plastic-sign_p3291261; AWSALB=qIWaXGuHQWW2XHpPm3359Ec/tMhkAQMSe3+Oxojf5F9Vak9bwQylTSqP5FO2Op6k9iIYdL0hQEOyA8UAdfrTPFpvGCP7zZaVs/5VRfgCbZlTM5baDBAuEDCQI8vR; AWSALBCORS=qIWaXGuHQWW2XHpPm3359Ec/tMhkAQMSe3+Oxojf5F9Vak9bwQylTSqP5FO2Op6k9iIYdL0hQEOyA8UAdfrTPFpvGCP7zZaVs/5VRfgCbZlTM5baDBAuEDCQI8vR; LiSESSIONID=B53DED5D53E1812C0F80882CD85CFC9E; cf_clearance=n0tNN16Bldt9fkM8HDbCgUDOx9lVxd3jwFUcMHZgyP8-1760429822-1.2.1.1-D1wq5B3yDYzr6xXNCTmdUEWY4BZwrQMeQTzXoRxo.RLSj6RSv3H89379gwefiADY8gmMu4Qe33h3TXesmKmtAITCqnnNzsTCaCKyH6jA33Ew1Tz.bK.r1EUZQjJ8QOvE58DlsGdN4FZ.Vg_c_QQC9XwV_OirmskEwd3xUmqqey3aPq2rVQ2X5ghDtKv7jpwU7Y7thgx3KYJ2SylRWtxLeoBsNuFAuiaPRBgTjZ3b25s; ROUTE=.api-6db5bc497d-nbtpj; inside-au12=1018695040-20b0b907563f4a59fbb3f6f2241ef46a012fbdfbfbc28e6e1290c54c3bcb5192-0-0',
# }
#
# class BunningsPdpSpider(PricemateBaseSpider):
#     name = "bunnings_pdp"
#
#     def __init__(self, retailer, region, *args, **kwargs):
#         super().__init__(retailer=retailer, region=region, *args, **kwargs)
#     @staticmethod
#     def extract_size(size_string):
#         try:
#             size_string = size_string.strip()
#
#             units = r'ml|mL|l|L|g|kg|oz|lb|m|cm|meter|meters|packs?|pack|tablets?|capsules?'
#
#             # 1️⃣ Size or Pack Size with single value
#             pattern1 = rf'(?:Size|Pack Size)[:\s]*([\d.]+)\s*({units})'
#             match = re.search(pattern1, size_string, re.IGNORECASE)
#             if match:
#                 return f"{match.group(1)} {match.group(2)}"
#
#             # 2️⃣ Simple number + unit
#             pattern2 = rf'([\d.]+)\s*({units})'
#             match = re.search(pattern2, size_string, re.IGNORECASE)
#             if match:
#                 return f"{match.group(1)} {match.group(2)}"
#
#             # 3️⃣ Pattern for dimensions with unit after second number, e.g. "180 x 90cm"
#             pattern3 = rf'([\d.]+)\s*[×xX]\s*([\d.]+)\s*({units})'
#             match = re.search(pattern3, size_string, re.IGNORECASE)
#             if match:
#                 return f"{match.group(1)} x {match.group(2)} {match.group(3)}"
#
#             # 4️⃣ Quantity with Japanese units
#             pattern4 = r'(\d+)\s*(個|本入り|袋|本)'
#             match = re.search(pattern4, size_string, re.IGNORECASE)
#             if match:
#                 return f"{match.group(1)} {match.group(2)}"
#
#             # 5️⃣ Pack size "Pk250", "Pack10"
#             pattern5 = r'\b(Pk|Pack)(\d+)\b'
#             match = re.search(pattern5, size_string, re.IGNORECASE)
#             if match:
#                 return f"{match.group(1)}{match.group(2)}"
#
#             return ""
#
#         except Exception as e:
#             return ""
#
#
#     def start_requests(self):
#
#         docs = self.product_table.find({
#             "retailer": self.retailer,
#             "region": self.region,
#             "Status": "Pending"
#         })
#         for doc in docs:
#             url = doc.get("ProductURL")
#             hash_id = doc.get("_id")
#             slug = url.split("/")[-1].split("_")[0]
#
#             meta = {
#                 "url": url,
#                 "_id": hash_id,
#                 "filename": f"Pdp_{slug}_page.html",
#                 "should_be": ["data-reactroot"]
#             }
#             yield scrapy.Request(
#                 url,
#                 cookies=cookies,
#                 headers=headers,
#                 callback=self.process_category,
#                 meta=meta
#             )
#     def process_category(self, response):
#         meta = response.meta
#         prod_url = meta.get("url")
#         doc_id = meta.get("_id")
#
#         # raw_json = response.xpath('//script[@type="application/json"]/text()').get()
#         # product_json = json.loads(raw_json)
#         #prod_details_getting_using_xpath
#
#         name = response.xpath('//h1[@data-locator="product-title"]/text()').get()
#         brand = response.xpath('//a[@data-locator="product-brand-name"]/text()').get()
#         sku = response.xpath('//p[@data-locator="product-item-number"]/text()[2]').get()
#         size = self.extract_size(name)
#
#         price_str = response.xpath('concat(normalize-space(//p[@data-locator="product-price"]/text()[1]), normalize-space(//p[@data-locator="product-price"]/sup))').get()
#         # price = float(price_str.replace('$', '').replace(',', ''))
#         price = price_str.replace('$', '').replace(',', '')
#         # wasprice = response.xpath('//p[@data-locator="product-price"]/span[2]/text()').get()
#         stock = bool(response.xpath('//button[@data-locator="atcButton-pdp" and contains(., "Add to Cart")]'))
#         rrp = price
#         image_urls = response.xpath('//div[@class="gap-2 flex"]//img/@src').getall()
#         image = ' | '.join(image_urls)
#         if not image_urls:
#             image_urls = response.xpath('//div[contains(@class, "group relative")]//img/@src').getall()
#             image = ' | '.join(image_urls)
#
#         breadcrumb_items = response.xpath('//nav[@aria-label="Breadcrumb"]//li//span[@itemprop="title"]/text()').getall()
#         breadcrumb = ' > '.join(breadcrumb_items)
#
#         product_hash = self.generate_hash_id(prod_url, self.retailer, self.region)
#         item = {"_id": product_hash, "Name": name, "Promo_Type": "", "Price": price, "per_unit_price": "",
#                 "WasPrice": "",
#                 "Offer_info": "", "Pack_size": size, "Barcode": "",
#                 "Images": image,
#                 "ProductURL": prod_url, "is_available": stock,
#                 "Status": "Done", "ParentCode": "", "ProductCode": sku,
#                 "retailer_name": "bunnings_au",
#                 "Category_Hierarchy": breadcrumb, "Brand": brand, "RRP": rrp}
#
#         try:
#             self.save_product(item)
#             print(f"✓ Successfully inserted {prod_url}")
#             if doc_id:
#                 self.product_table.update_one(
#                     {"_id": doc_id},
#                     {"$set": {"Status": "Done"}}
#                 )
#         except Exception as e:
#             print(e)
#
#
#
#     def close(self, reason):
#         self.mongo_client.close()
#
# if __name__ == '__main__':
#     from scrapy.cmdline import execute
#     execute("scrapy crawl bunnings_pdp -a retailer=bunnings_au -a region=au -a Type=eshop -a RetailerCode=bunnings_au".split())
#
#
