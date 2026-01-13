# from urllib.parse import quote
# import scrapy
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
#     'enableNewAuthFlowBrowser': 'true',
#     'coveo_visitorId': '066dedb0-7bcd-43dc-8a44-244897274b27',
#     'returningVisitor': 'true',
#     'unleash-properties': '%7B%22channel%22%3A%22web%22%2C%22country%22%3A%22au%22%2C%22division%22%3A%22retail%22%7D',
#     'ctz': '-5.5',
#     'rxVisitor': '1760421745988HI88819HEEL1O9AQVR2E877IJV949IA7',
#     'dtSa': '-',
#     'dtPC': '10$25831572_440h9p10$26082040_827h1vADUFMVCARCJSLNUNWMMBRWAMFAPFRFFQ-0e0',
#     'rxvt': '1760427883599|1760425831576',
#     '__RequestVerificationToken': '_t2RpxI0BbMY_hqb1GDTrcSvnpn-M5I2RXWJ6aKnRgnxJvXm6YQOeb4DWpt4v8wukn_MCZGFJplpWhQNndwqFpMQ91R5uF79zUkugl904wY1',
#     '__cf_bm': 'hLwdtsMl.QJXo.ICcg_aIpkmvnq0veMqstAfOlN0gpg-1761027700-1.0.1.1-aorCSn6mQ50jTsFhcuWuwTbSLVX4D4epKwHpCfkB3rH_Du60YsJ3t4C0MOu6FKGvM.AJTLUOToT895g6AiUmINOUQrV6Y_N4oZjlihlieB8',
#     'cf_clearance': 'rA0E4h3kn5yqHkTDyBoBcEpn7bfBqZk_kQAcioJWmgc-1761027702-1.2.1.1-dGlIpzruckx4X3_Dq1SIY.r9tUheZyFqXfuU7P0xodslfAO5B5YbE8EWhI5k9IJ8hvNdeSIjSxfmq8AHwljx_mJ5LkAhhtkA.aKTElce4iSyaoVhhRdByh6HgWcE1Gq.7ozu_ZC1ULVpqEJHqWTsJqvXMCyXnBRSSbMCcilQ_sNLuwMlii35Yft_uJxkfSsjdJfQi4F3CgmIGYVeBoFw_DdfYeTHXF64Vj8KDfsI6Dg',
#     'guest-token-storage': '{"expires":1761459705479,"s":432000,"token":"eyJhbGciOiJSUzI1NiIsImtpZCI6IkJGRTFEMDBBRUZERkVDNzM4N0E1RUFFMzkxNjRFM0MwMUJBNzVDODciLCJ4NXQiOiJ2LUhRQ3VfZjdIT0hwZXJqa1dUandCdW5YSWMiLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJodHRwczovL2J1bm5pbmdzLmNvbS5hdS8iLCJuYmYiOjE3NjEwMjc3MDQsImlhdCI6MTc2MTAyNzcwNCwiZXhwIjoxNzYxNDU5NzA0LCJhdWQiOlsiQ2hlY2tvdXQtQXBpIiwiY3VzdG9tZXJfYnVubmluZ3MiLCJWb3VjaGVyLUFwaSIsIkJhc2tldC1BcGkiLCJodHRwczovL2J1bm5pbmdzLmNvbS5hdS9yZXNvdXJjZXMiXSwic2NvcGUiOlsiY2hrOmV4ZWMiLCJjbTphY2Nlc3MiLCJlY29tOmFjY2VzcyIsImNoazpwdWIiLCJ2Y2g6cHVibGljIiwiYnNrOnB1YiJdLCJhbXIiOlsiZXh0ZXJuYWwiXSwiY2xpZW50X2lkIjoiYnVkcF9ndWVzdF91c2VyX2F1Iiwic3ViIjoiYTM2YTQ2ZjEtMDEyNC00MjY3LTg4YjMtNDQyNWIzMzExZDEzIiwiYXV0aF90aW1lIjoxNzYxMDI3NzAzLCJpZHAiOiJsb2NhbGxvb3BiYWNrIiwiYi1pZCI6ImEzNmE0NmYxLTAxMjQtNDI2Ny04OGIzLTQ0MjViMzMxMWQxMyIsImItcm9sZSI6Imd1ZXN0IiwiYi10eXBlIjoiZ3Vlc3QiLCJsb2NhbGUiOiJlbl9BVSIsImItY291bnRyeSI6IkFVIiwiYWN0aXZhdGlvbl9zdGF0dXMiOiJGYWxzZSIsInVzZXJfbmFtZSI6ImEzNmE0NmYxLTAxMjQtNDI2Ny04OGIzLTQ0MjViMzMxMWQxMyIsImItcmJhYyI6W3siYXNjIjoiYTM2YTQ2ZjEtMDEyNC00MjY3LTg4YjMtNDQyNWIzMzExZDEzIiwidHlwZSI6IkMiLCJyb2wiOlsiQ0hLOkd1ZXN0IiwiVkNIOkd1ZXN0Il19LHsiYXNjIjoiZUNvbW1lcmNlLWEzNmE0NmYxLTAxMjQtNDI2Ny04OGIzLTQ0MjViMzMxMWQxMyIsInR5cGUiOiJDVFhTIiwicm9sIjpbIkJTSzpHdWVzdCJdfV0sInNpZCI6Ijg2NEFENEZGNjA4MzUzMjY0NThGNDlGM0JDMTU3NjMxIiwianRpIjoiMEMyNzVDQjkyMEIwQkE4OEE3MjI4M0FFMkFEMEEyNkQifQ.M8w9D6YRs5IunzjzLCmuZ0CDoevWbXsGVwbdK2qg0Hp9X052GpNN73lnLVtaUEq__k5uy-Bs8XTxvi5hbHnz_ggu72IrxLU_miG8ren3n1hV-jRpA5ZqNEOalnuOsKCr3azsOe5B-rWvZo4aaSkm0eK8HHHriS12jjVp3qhz_ro8JU27hyomEyP0fO6_FPs2Xn8LN78bBZO9I0YbNr7f8ennUqPHE1mRsWkhWDyzM7PK2OrCznc8mej7ZivkiIeAGGHxYHvnMFS9p135M9u7cYA5KMtv0Huhpz39ju8V7lw3o3MygXeLPp1Anxdes5Or26PTjAR-xC3LlYPSKKUasg","clientToken":true}',
#     'GuestAuthentication': 'eyJhbGciOiJSUzI1NiIsImtpZCI6IkJGRTFEMDBBRUZERkVDNzM4N0E1RUFFMzkxNjRFM0MwMUJBNzVDODciLCJ4NXQiOiJ2LUhRQ3VfZjdIT0hwZXJqa1dUandCdW5YSWMiLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJodHRwczovL2J1bm5pbmdzLmNvbS5hdS8iLCJuYmYiOjE3NjEwMjc3MDQsImlhdCI6MTc2MTAyNzcwNCwiZXhwIjoxNzYxNDU5NzA0LCJhdWQiOlsiQ2hlY2tvdXQtQXBpIiwiY3VzdG9tZXJfYnVubmluZ3MiLCJWb3VjaGVyLUFwaSIsIkJhc2tldC1BcGkiLCJodHRwczovL2J1bm5pbmdzLmNvbS5hdS9yZXNvdXJjZXMiXSwic2NvcGUiOlsiY2hrOmV4ZWMiLCJjbTphY2Nlc3MiLCJlY29tOmFjY2VzcyIsImNoazpwdWIiLCJ2Y2g6cHVibGljIiwiYnNrOnB1YiJdLCJhbXIiOlsiZXh0ZXJuYWwiXSwiY2xpZW50X2lkIjoiYnVkcF9ndWVzdF91c2VyX2F1Iiwic3ViIjoiYTM2YTQ2ZjEtMDEyNC00MjY3LTg4YjMtNDQyNWIzMzExZDEzIiwiYXV0aF90aW1lIjoxNzYxMDI3NzAzLCJpZHAiOiJsb2NhbGxvb3BiYWNrIiwiYi1pZCI6ImEzNmE0NmYxLTAxMjQtNDI2Ny04OGIzLTQ0MjViMzMxMWQxMyIsImItcm9sZSI6Imd1ZXN0IiwiYi10eXBlIjoiZ3Vlc3QiLCJsb2NhbGUiOiJlbl9BVSIsImItY291bnRyeSI6IkFVIiwiYWN0aXZhdGlvbl9zdGF0dXMiOiJGYWxzZSIsInVzZXJfbmFtZSI6ImEzNmE0NmYxLTAxMjQtNDI2Ny04OGIzLTQ0MjViMzMxMWQxMyIsImItcmJhYyI6W3siYXNjIjoiYTM2YTQ2ZjEtMDEyNC00MjY3LTg4YjMtNDQyNWIzMzExZDEzIiwidHlwZSI6IkMiLCJyb2wiOlsiQ0hLOkd1ZXN0IiwiVkNIOkd1ZXN0Il19LHsiYXNjIjoiZUNvbW1lcmNlLWEzNmE0NmYxLTAxMjQtNDI2Ny04OGIzLTQ0MjViMzMxMWQxMyIsInR5cGUiOiJDVFhTIiwicm9sIjpbIkJTSzpHdWVzdCJdfV0sInNpZCI6Ijg2NEFENEZGNjA4MzUzMjY0NThGNDlGM0JDMTU3NjMxIiwianRpIjoiMEMyNzVDQjkyMEIwQkE4OEE3MjI4M0FFMkFEMEEyNkQifQ.M8w9D6YRs5IunzjzLCmuZ0CDoevWbXsGVwbdK2qg0Hp9X052GpNN73lnLVtaUEq__k5uy-Bs8XTxvi5hbHnz_ggu72IrxLU_miG8ren3n1hV-jRpA5ZqNEOalnuOsKCr3azsOe5B-rWvZo4aaSkm0eK8HHHriS12jjVp3qhz_ro8JU27hyomEyP0fO6_FPs2Xn8LN78bBZO9I0YbNr7f8ennUqPHE1mRsWkhWDyzM7PK2OrCznc8mej7ZivkiIeAGGHxYHvnMFS9p135M9u7cYA5KMtv0Huhpz39ju8V7lw3o3MygXeLPp1Anxdes5Or26PTjAR-xC3LlYPSKKUasg',
#     'SC_ANALYTICS_GLOBAL_COOKIE': '5df20b49c47e449b959b3985fac8547c|False',
#     '__cf_bm': '10Mfh3yBrbMqrWHjBe7MzSblYomeYXUmwGcOihNZOo4-1761027729-1.0.1.1-hMnnzBCgZQ.TL0qbpGHq_YoQFB713o3CGRZhK6UX4cRkxt3zTNgjP7K6sYv2azTaZg2vC.OuZhK5gAmKSGFfQTkosatHFWQ6.w8.JF1EdKKVjN4okZSxhu4tywqiHZD5',
#     '_cfuvid': 'Mf09f8cTZcsRrHkRmFkPD_em75SrWxsuqeqOSVn3XLA-1761027729567-0.0.1.1-604800000',
#     'dtCookie': 'v_4_srv_3_sn_DC167B6B77ACF6F74EE9C210B5002836_perc_100000_ol_0_mul_1_app-3Aea7c4b59f27d43eb_1_app-3A538efd036e45e9dd_0_rcs-3Acss_0',
#     'AccessTokenCookie': '%7B%22tokenvalue%22%3A%22a36a46f1-0124-4267-88b3-4425b3311d13-1761027703%22%2C%22lastchecktime%22%3A%2210%2F21%2F2025%206%3A22%3A08%20AM%22%7D',
#     'origin_path': '/',
#     'AWSALB': '74ceIC5nb9OIW2ECL92yeSqS/po79a7g8KEntcxFcErMgCw0QZv3u9INQT58REYn5uAIeE23smBlIJwF9N+nKJEaQdHPFndrwaVSQRHV/lr1EYKSg2//jHaNSbYG',
#     'AWSALBCORS': '74ceIC5nb9OIW2ECL92yeSqS/po79a7g8KEntcxFcErMgCw0QZv3u9INQT58REYn5uAIeE23smBlIJwF9N+nKJEaQdHPFndrwaVSQRHV/lr1EYKSg2//jHaNSbYG',
#     'LiSESSIONID': '246E17347FC9648399DFF25F7C3EC17E',
#     'inside-au12': '1018695040-20b0b907563f4a59fbb3f6f2241ef46a012fbdfbfbc28e6e1290c54c3bcb5192-0-0',
#     'ROUTE': '.api-6cc897ff8c-x6j2n',
#     '_cfuvid': '2PEFi_ujJPGUmlTnbAWeGOJDOkXe.u6oeCZ4Y_qzsow-1761027896903-0.0.1.1-604800000',
# }
#
# headers = {
#     'accept': 'application/json, text/plain, */*',
#     'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
#     'clientid': 'mHPVWnzuBkrW7rmt56XGwKkb5Gp9BJMk',
#     'content-type': 'application/json',
#     'correlationid': 'aa625480-ae46-11f0-9923-053e9c76de31',
#     'country': 'AU',
#     'currency': 'AUD',
#     'locale': 'en_AU',
#     'locationcode': '6400',
#     'origin': 'https://www.bunnings.com.au',
#     'priority': 'u=1, i',
#     'referer': 'https://www.bunnings.com.au/',
#     'sec-ch-ua': '"Google Chrome";v="141", "Not?A_Brand";v="8", "Chromium";v="141"',
#     'sec-ch-ua-arch': '"x86"',
#     'sec-ch-ua-bitness': '"64"',
#     'sec-ch-ua-full-version': '"141.0.7390.67"',
#     'sec-ch-ua-full-version-list': '"Google Chrome";v="141.0.7390.67", "Not?A_Brand";v="8.0.0.0", "Chromium";v="141.0.7390.67"',
#     'sec-ch-ua-mobile': '?0',
#     'sec-ch-ua-model': '""',
#     'sec-ch-ua-platform': '"Windows"',
#     'sec-ch-ua-platform-version': '"19.0.0"',
#     'sec-fetch-dest': 'empty',
#     'sec-fetch-mode': 'cors',
#     'sec-fetch-site': 'same-origin',
#     'sessionid': '3ac2a810-a8c3-11f0-bc41-ffb3a16559f6',
#     'stream': 'RETAIL',
#     'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36',
#     'userid': 'anonymous',
#     'x-dtpc': '3$27786322_618h37vUFPEAJQCCUQULROVUTOUHFFUHFOHIPUL-0e0',
#     'x-region': 'VICMetro',
#     # 'cookie': 'personalization_session_id=42091470-9e7c-11f0-9c25-05a3b860e1dd; defaultStoreId=6400; defaultRegionCode=VICMetro; _evga_dbf4={%22uuid%22:%2276ae763ad7eb5422%22}; _sfid_4bdd={%22anonymousId%22:%2276ae763ad7eb5422%22%2C%22consents%22:[]}; BVBRANDID=d0bf7229-a302-49c0-8c11-e1ca56361080; recentSearches=offer; nodeServed=true; uSessionId=3ac2a810-a8c3-11f0-bc41-ffb3a16559f6; budp_au#lang=en; ASP.NET_SessionId=tmxtxwodf1ffe5exqhdiysif; enableNewAuthFlowBrowser=true; coveo_visitorId=066dedb0-7bcd-43dc-8a44-244897274b27; returningVisitor=true; unleash-properties=%7B%22channel%22%3A%22web%22%2C%22country%22%3A%22au%22%2C%22division%22%3A%22retail%22%7D; ctz=-5.5; rxVisitor=1760421745988HI88819HEEL1O9AQVR2E877IJV949IA7; dtSa=-; dtPC=10$25831572_440h9p10$26082040_827h1vADUFMVCARCJSLNUNWMMBRWAMFAPFRFFQ-0e0; rxvt=1760427883599|1760425831576; __RequestVerificationToken=_t2RpxI0BbMY_hqb1GDTrcSvnpn-M5I2RXWJ6aKnRgnxJvXm6YQOeb4DWpt4v8wukn_MCZGFJplpWhQNndwqFpMQ91R5uF79zUkugl904wY1; __cf_bm=hLwdtsMl.QJXo.ICcg_aIpkmvnq0veMqstAfOlN0gpg-1761027700-1.0.1.1-aorCSn6mQ50jTsFhcuWuwTbSLVX4D4epKwHpCfkB3rH_Du60YsJ3t4C0MOu6FKGvM.AJTLUOToT895g6AiUmINOUQrV6Y_N4oZjlihlieB8; cf_clearance=rA0E4h3kn5yqHkTDyBoBcEpn7bfBqZk_kQAcioJWmgc-1761027702-1.2.1.1-dGlIpzruckx4X3_Dq1SIY.r9tUheZyFqXfuU7P0xodslfAO5B5YbE8EWhI5k9IJ8hvNdeSIjSxfmq8AHwljx_mJ5LkAhhtkA.aKTElce4iSyaoVhhRdByh6HgWcE1Gq.7ozu_ZC1ULVpqEJHqWTsJqvXMCyXnBRSSbMCcilQ_sNLuwMlii35Yft_uJxkfSsjdJfQi4F3CgmIGYVeBoFw_DdfYeTHXF64Vj8KDfsI6Dg; guest-token-storage={"expires":1761459705479,"s":432000,"token":"eyJhbGciOiJSUzI1NiIsImtpZCI6IkJGRTFEMDBBRUZERkVDNzM4N0E1RUFFMzkxNjRFM0MwMUJBNzVDODciLCJ4NXQiOiJ2LUhRQ3VfZjdIT0hwZXJqa1dUandCdW5YSWMiLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJodHRwczovL2J1bm5pbmdzLmNvbS5hdS8iLCJuYmYiOjE3NjEwMjc3MDQsImlhdCI6MTc2MTAyNzcwNCwiZXhwIjoxNzYxNDU5NzA0LCJhdWQiOlsiQ2hlY2tvdXQtQXBpIiwiY3VzdG9tZXJfYnVubmluZ3MiLCJWb3VjaGVyLUFwaSIsIkJhc2tldC1BcGkiLCJodHRwczovL2J1bm5pbmdzLmNvbS5hdS9yZXNvdXJjZXMiXSwic2NvcGUiOlsiY2hrOmV4ZWMiLCJjbTphY2Nlc3MiLCJlY29tOmFjY2VzcyIsImNoazpwdWIiLCJ2Y2g6cHVibGljIiwiYnNrOnB1YiJdLCJhbXIiOlsiZXh0ZXJuYWwiXSwiY2xpZW50X2lkIjoiYnVkcF9ndWVzdF91c2VyX2F1Iiwic3ViIjoiYTM2YTQ2ZjEtMDEyNC00MjY3LTg4YjMtNDQyNWIzMzExZDEzIiwiYXV0aF90aW1lIjoxNzYxMDI3NzAzLCJpZHAiOiJsb2NhbGxvb3BiYWNrIiwiYi1pZCI6ImEzNmE0NmYxLTAxMjQtNDI2Ny04OGIzLTQ0MjViMzMxMWQxMyIsImItcm9sZSI6Imd1ZXN0IiwiYi10eXBlIjoiZ3Vlc3QiLCJsb2NhbGUiOiJlbl9BVSIsImItY291bnRyeSI6IkFVIiwiYWN0aXZhdGlvbl9zdGF0dXMiOiJGYWxzZSIsInVzZXJfbmFtZSI6ImEzNmE0NmYxLTAxMjQtNDI2Ny04OGIzLTQ0MjViMzMxMWQxMyIsImItcmJhYyI6W3siYXNjIjoiYTM2YTQ2ZjEtMDEyNC00MjY3LTg4YjMtNDQyNWIzMzExZDEzIiwidHlwZSI6IkMiLCJyb2wiOlsiQ0hLOkd1ZXN0IiwiVkNIOkd1ZXN0Il19LHsiYXNjIjoiZUNvbW1lcmNlLWEzNmE0NmYxLTAxMjQtNDI2Ny04OGIzLTQ0MjViMzMxMWQxMyIsInR5cGUiOiJDVFhTIiwicm9sIjpbIkJTSzpHdWVzdCJdfV0sInNpZCI6Ijg2NEFENEZGNjA4MzUzMjY0NThGNDlGM0JDMTU3NjMxIiwianRpIjoiMEMyNzVDQjkyMEIwQkE4OEE3MjI4M0FFMkFEMEEyNkQifQ.M8w9D6YRs5IunzjzLCmuZ0CDoevWbXsGVwbdK2qg0Hp9X052GpNN73lnLVtaUEq__k5uy-Bs8XTxvi5hbHnz_ggu72IrxLU_miG8ren3n1hV-jRpA5ZqNEOalnuOsKCr3azsOe5B-rWvZo4aaSkm0eK8HHHriS12jjVp3qhz_ro8JU27hyomEyP0fO6_FPs2Xn8LN78bBZO9I0YbNr7f8ennUqPHE1mRsWkhWDyzM7PK2OrCznc8mej7ZivkiIeAGGHxYHvnMFS9p135M9u7cYA5KMtv0Huhpz39ju8V7lw3o3MygXeLPp1Anxdes5Or26PTjAR-xC3LlYPSKKUasg","clientToken":true}; GuestAuthentication=eyJhbGciOiJSUzI1NiIsImtpZCI6IkJGRTFEMDBBRUZERkVDNzM4N0E1RUFFMzkxNjRFM0MwMUJBNzVDODciLCJ4NXQiOiJ2LUhRQ3VfZjdIT0hwZXJqa1dUandCdW5YSWMiLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJodHRwczovL2J1bm5pbmdzLmNvbS5hdS8iLCJuYmYiOjE3NjEwMjc3MDQsImlhdCI6MTc2MTAyNzcwNCwiZXhwIjoxNzYxNDU5NzA0LCJhdWQiOlsiQ2hlY2tvdXQtQXBpIiwiY3VzdG9tZXJfYnVubmluZ3MiLCJWb3VjaGVyLUFwaSIsIkJhc2tldC1BcGkiLCJodHRwczovL2J1bm5pbmdzLmNvbS5hdS9yZXNvdXJjZXMiXSwic2NvcGUiOlsiY2hrOmV4ZWMiLCJjbTphY2Nlc3MiLCJlY29tOmFjY2VzcyIsImNoazpwdWIiLCJ2Y2g6cHVibGljIiwiYnNrOnB1YiJdLCJhbXIiOlsiZXh0ZXJuYWwiXSwiY2xpZW50X2lkIjoiYnVkcF9ndWVzdF91c2VyX2F1Iiwic3ViIjoiYTM2YTQ2ZjEtMDEyNC00MjY3LTg4YjMtNDQyNWIzMzExZDEzIiwiYXV0aF90aW1lIjoxNzYxMDI3NzAzLCJpZHAiOiJsb2NhbGxvb3BiYWNrIiwiYi1pZCI6ImEzNmE0NmYxLTAxMjQtNDI2Ny04OGIzLTQ0MjViMzMxMWQxMyIsImItcm9sZSI6Imd1ZXN0IiwiYi10eXBlIjoiZ3Vlc3QiLCJsb2NhbGUiOiJlbl9BVSIsImItY291bnRyeSI6IkFVIiwiYWN0aXZhdGlvbl9zdGF0dXMiOiJGYWxzZSIsInVzZXJfbmFtZSI6ImEzNmE0NmYxLTAxMjQtNDI2Ny04OGIzLTQ0MjViMzMxMWQxMyIsImItcmJhYyI6W3siYXNjIjoiYTM2YTQ2ZjEtMDEyNC00MjY3LTg4YjMtNDQyNWIzMzExZDEzIiwidHlwZSI6IkMiLCJyb2wiOlsiQ0hLOkd1ZXN0IiwiVkNIOkd1ZXN0Il19LHsiYXNjIjoiZUNvbW1lcmNlLWEzNmE0NmYxLTAxMjQtNDI2Ny04OGIzLTQ0MjViMzMxMWQxMyIsInR5cGUiOiJDVFhTIiwicm9sIjpbIkJTSzpHdWVzdCJdfV0sInNpZCI6Ijg2NEFENEZGNjA4MzUzMjY0NThGNDlGM0JDMTU3NjMxIiwianRpIjoiMEMyNzVDQjkyMEIwQkE4OEE3MjI4M0FFMkFEMEEyNkQifQ.M8w9D6YRs5IunzjzLCmuZ0CDoevWbXsGVwbdK2qg0Hp9X052GpNN73lnLVtaUEq__k5uy-Bs8XTxvi5hbHnz_ggu72IrxLU_miG8ren3n1hV-jRpA5ZqNEOalnuOsKCr3azsOe5B-rWvZo4aaSkm0eK8HHHriS12jjVp3qhz_ro8JU27hyomEyP0fO6_FPs2Xn8LN78bBZO9I0YbNr7f8ennUqPHE1mRsWkhWDyzM7PK2OrCznc8mej7ZivkiIeAGGHxYHvnMFS9p135M9u7cYA5KMtv0Huhpz39ju8V7lw3o3MygXeLPp1Anxdes5Or26PTjAR-xC3LlYPSKKUasg; SC_ANALYTICS_GLOBAL_COOKIE=5df20b49c47e449b959b3985fac8547c|False; __cf_bm=10Mfh3yBrbMqrWHjBe7MzSblYomeYXUmwGcOihNZOo4-1761027729-1.0.1.1-hMnnzBCgZQ.TL0qbpGHq_YoQFB713o3CGRZhK6UX4cRkxt3zTNgjP7K6sYv2azTaZg2vC.OuZhK5gAmKSGFfQTkosatHFWQ6.w8.JF1EdKKVjN4okZSxhu4tywqiHZD5; _cfuvid=Mf09f8cTZcsRrHkRmFkPD_em75SrWxsuqeqOSVn3XLA-1761027729567-0.0.1.1-604800000; dtCookie=v_4_srv_3_sn_DC167B6B77ACF6F74EE9C210B5002836_perc_100000_ol_0_mul_1_app-3Aea7c4b59f27d43eb_1_app-3A538efd036e45e9dd_0_rcs-3Acss_0; AccessTokenCookie=%7B%22tokenvalue%22%3A%22a36a46f1-0124-4267-88b3-4425b3311d13-1761027703%22%2C%22lastchecktime%22%3A%2210%2F21%2F2025%206%3A22%3A08%20AM%22%7D; origin_path=/; AWSALB=74ceIC5nb9OIW2ECL92yeSqS/po79a7g8KEntcxFcErMgCw0QZv3u9INQT58REYn5uAIeE23smBlIJwF9N+nKJEaQdHPFndrwaVSQRHV/lr1EYKSg2//jHaNSbYG; AWSALBCORS=74ceIC5nb9OIW2ECL92yeSqS/po79a7g8KEntcxFcErMgCw0QZv3u9INQT58REYn5uAIeE23smBlIJwF9N+nKJEaQdHPFndrwaVSQRHV/lr1EYKSg2//jHaNSbYG; LiSESSIONID=246E17347FC9648399DFF25F7C3EC17E; inside-au12=1018695040-20b0b907563f4a59fbb3f6f2241ef46a012fbdfbfbc28e6e1290c54c3bcb5192-0-0; ROUTE=.api-6cc897ff8c-x6j2n; _cfuvid=2PEFi_ujJPGUmlTnbAWeGOJDOkXe.u6oeCZ4Y_qzsow-1761027896903-0.0.1.1-604800000',
# }
#
# class BunningsPlSpider(PricemateBaseSpider):
#     name = "bunnings_pl"
#
#     def __init__(self, retailer, region, *args, **kwargs):
#         super().__init__(retailer=retailer, region=region, *args, **kwargs)
#
#     def start_requests(self):
#         docs = self.category_input.find({
#             "retailer": self.retailer,
#             "region": self.region,
#             "Status": "Pending"
#         })
#         for doc in docs:
#             url = doc["url"]
#             hash_id = doc.get("_id")
#             slug = url.split("/")[-1].split("/")[0]
#             meta = {
#                 "url": url,
#                 "_id": hash_id,
#                 "slug":slug,
#                 "page": 1,
#                 "filename": f"{slug}_page.html",
#                 "should_be": ["sc-36e24d7e-7 cQoVOJ"]
#             }
#             yield scrapy.Request(
#                 url,
#                 cookies=cookies,
#                 headers=headers,
#                 callback=self.parse_pl,
#                 meta=meta,
#             )
#
#     def parse_pl(self, response):
#         meta = response.meta
#         doc_id = meta.get("_id")
#         slug = meta.get("slug")
#         cate_url = meta.get("url")
#         page = int(meta.get("page", 1))
#         links = response.xpath('//div[@data-testid="productTileContainer"]/a/@href').getall()
#
#         for link in links:
#             pdp_url = f'https://www.bunnings.com.au{link}'
#             product_hash = self.generate_hash_id(pdp_url, self.retailer, self.region)
#             item = {
#                 "_id": product_hash,
#                 "ProductURL": pdp_url,
#                 "Status": "Pending",
#                 "retailer": self.retailer,
#                 "region": self.region,
#             }
#             self.save_product(item)
#             print(f"Product Inserted !")
#         next_button = response.xpath('//button[@aria-label="Next page" and not(@disabled)]')
#         if next_button:
#             next_page = page + 1
#             next_page_url = f'{cate_url}?page={next_page}'
#             yield scrapy.Request(
#                 url=next_page_url,
#                 cookies=cookies,
#                 headers=headers,
#                 callback=self.parse_pl,
#                 meta={
#                     "url": cate_url,
#                     "_id": doc_id,
#                     "slug": slug,
#                     "page": next_page,
#                     "filename": f"{slug}_page{next_page}.html",
#                     "should_be": ["sc-36e24d7e-7 cQoVOJ"],
#                 }
#             )
#         else:
#             self.category_input.update_one(
#                 {"_id": doc_id},
#                 {"$set": {"Status": "Done"}}
#             )
#
#             # print(f"Product URL: {pdp_url}")
#
#     def close(self, reason):
#         self.mongo_client.close()
#
# if __name__ == '__main__':
#     from scrapy.cmdline import execute
#     execute("scrapy crawl bunnings_pl -a retailer=bunnings_au -a region=au -a Type=eshop -a RetailerCode=bunnings_au".split())