from config import *
import xml.etree.ElementTree as ET
from concurrent.futures import ThreadPoolExecutor, as_completed

def gather_filtered_urls_from_sitemap(sitemap_url):
    try:
        hashid = generate_hashId(sitemap_url)
        filename = f'sitemap_{hashid}.html'
        filepath = os.path.join(html_path, filename)
        print(filepath)

        path = filepath.replace("\\\\", "//").replace("\\", "/")
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as file:
                content = file.read()

        else:
            headers = {
                'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
                'accept-language': 'en-US,en;q=0.9',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36 Edg/134.0.0.0',
                # 'cookie': 'affinity="28423559711649ff"',
            }

            # Fetch the sitemap
            response = requests.get(sitemap_url, headers=headers, stream=True, proxies=proxies,  verify=False, timeout=100)
            response.raise_for_status()
            content = response.text
            with open(path, "w", encoding="utf-8") as file:
                file.write(content)

        # Regular expression to extract <loc> URLs
        loc_pattern = re.compile(r"<loc>(.*?)</loc>", re.IGNORECASE)

        # Find all matching URLs
        all_urls = loc_pattern.findall(content)

        # Filter URLs if filter_keyword is provided
        # if filter_keyword:
        all_urls = [url for url in all_urls if filter_keyword in url]

        return all_urls


    except requests.RequestException as e:
        print(f"Error fetching the sitemap: {e}")
        return []
    except ET.ParseError as e:
        print(f"Error parsing the sitemap XML: {e}")
        return []


if __name__ == '__main__':
    sitemap_urls = [
        "https://myaeon2go.com/sitemap-products.xml",
        "https://myaeon2go.com/sitemap-products-2.xml"
                    ]
    for sitemap_url in sitemap_urls:
        filter_keyword = "/product/"
        urls = gather_filtered_urls_from_sitemap(sitemap_url)
        for i in urls:
            ProductCode = i.split("/product/")[-1].split("/")[0]

            items = {
                "ProductURL" : i,
                "ProductCode": ProductCode,
                "Status": "Pending"
            }
            try:
                product_data.insert_one(items)
                print("Product Data Inserted...")

            except Exception as e:
                if 'duplicate key error' not in str(e):
                    print(e)
