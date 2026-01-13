import requests

headers = {
    'Content-Type': 'application/json; charset=utf-8',
    # 'Accept-Encoding': 'gzip',
    'language': 'en',
    'User-Agent': 'Dart/3.6 (dart:io)',
}

json_data = {
    'apiclientid': '7737876',
    'token': '867f931b1d91297967895d948d4275d2',
    'sign': '97215972d1b4744eb510e6d9f69b5f25',
    'lang': 'en',
    'store': 146,
}

response = requests.post(
    'https://goapp-dev-mobileapp.centralretail.com.vn/api/order2/ListCategoryNew',
    headers=headers,
    json=json_data,
)

print(response.json())
print(response.status_code)