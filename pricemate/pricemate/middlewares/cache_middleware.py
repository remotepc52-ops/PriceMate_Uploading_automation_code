import os, time
import urllib.parse
from scrapy import Selector
from scrapy.http import HtmlResponse
import requests


crawlera_key = "2c6ea6e6d8c14216a62781b8f850cd5b"
scraper_api_key = "f8f2ef6134be4c604d89eb084196f7bd"
scrape_do_api_key = "35c437e734644778b5884af53c186c27a226f186962"
zenrows_apikey = '21ed11ef5c872bc7727680a52233027db4578a0e'


class HtmlCacheMiddleware:
    def __init__(self, cache_dir, retailer, region, max_retry=3):
        self.cache_dir = cache_dir
        self.retailer = retailer
        self.region = region
        self.max_retry = max_retry
        os.makedirs(cache_dir, exist_ok=True)

    @classmethod
    def from_crawler(cls, crawler):
        spider = crawler.spider
        return cls(
            cache_dir=cls.get_cache_path(spider),
            retailer=getattr(spider, 'retailer', 'default'),
            region=getattr(spider, 'region', 'unknown'),
            max_retry=getattr(spider, 'max_retry', 3)
        )

    @staticmethod
    def get_cache_path(spider):
        today = getattr(spider, 'today', 'default')
        spider_name = getattr(spider, 'name', 'default')
        retailer = getattr(spider, 'retailer', 'default')
        region = getattr(spider, 'region', 'unknown')
        if spider_name == 'lazada_shop':
            return f"E:\\Data\\Crawl_Data_Collection\\PriceMate\\{today}\\Lazada\\HTMLs"

        elif 'shopee' in spider_name:
            return f"E:\\Data\\Crawl_Data_Collection\\PriceMate\\{today}\\shopee\\HTMLs"
        else:
            base_path = f"E:\\Data\\Crawl_Data_Collection\\PriceMate\\{today}\\{retailer}"
            return os.path.join(base_path, "HTMLs")

    def validate_response(self, response_text, should_be=None, not_should_be=None,
                          xpath_should_be=None, xpath_not_should_be=None):

        selector_response = Selector(text=response_text)
        if should_be:
            for val in should_be:
                if '|' in val:
                    if not any(sub_val in response_text for sub_val in val.split('|')):
                        return False
                else:
                    if val not in response_text:
                        return False
        if xpath_should_be:
            if isinstance(xpath_should_be, str):
                xpath_should_be = [xpath_should_be]
            if not all(selector_response.xpath(val) for val in xpath_should_be):
                return False
        if xpath_not_should_be:
            if isinstance(xpath_not_should_be, str):
                xpath_not_should_be = [xpath_not_should_be]
            if not all(not selector_response.xpath(val) for val in xpath_not_should_be):
                return False
        if not_should_be:
            if isinstance(not_should_be, str):
                not_should_be = [not_should_be]
            if not all(val not in response_text for val in not_should_be):
                return False
        return True

    @staticmethod
    def get_scrapy_proxy_url(proxy_name):
        if proxy_name == 'zyte':
            proxy_host = "api.zyte.com"
            proxy_port = "8011"
            proxy_auth = f"{crawlera_key}:"
            return "https://{}@{}:{}/".format(proxy_auth, proxy_host, proxy_port)

        elif proxy_name == 'zenrows_superproxy':
            proxi = 'http://3dbxcTLYpHGv:3dbxcTLYpHGv_country-sg@superproxy.zenrows.com:1337'
            return proxi

        elif proxy_name == 'zenrows_api':
            proxy = "http://21ed11ef5c872bc7727680a52233027db4578a0e:@api.zenrows.com:8001"
            return proxy

        return None

    def resolve_proxy(self, proxy_name, request_url=None, method='GET', headers=None):
        proxies = None
        modified_url = request_url
        modified_headers = headers or {}

        if proxy_name == 'zyte':
            proxy_host = "api.zyte.com"
            proxy_port = "8011"
            proxy_auth = f"{crawlera_key}:"
            proxies = {
                "http": "https://{}@{}:{}/".format(proxy_auth, proxy_host, proxy_port),
                "https": "http://{}@{}:{}/".format(proxy_auth, proxy_host, proxy_port)
            }

        elif proxy_name == 'scraper_api':
            modified_url = f"http://api.scraperapi.com?api_key={scraper_api_key}&url={request_url}&keep_headers=true"

        elif proxy_name == 'scrape_do':
            token = "2192d06a19b74b23884d257fcffee6f696674f8e128"
            proxyModeUrl = "http://{}:@proxy.scrape.do:8080".format(token)
            proxies = {
                "http": proxyModeUrl,
                "https": proxyModeUrl,
            }

        elif proxy_name == 'apify':
            token = 'apify_token_here'
            if request_url:
                connector = '&' if '?' in request_url else '?'
                modified_url = f"{request_url}{connector}proxy=apify&token={token}"
            proxies = None

        elif proxy_name == 'zenrows_superproxy':
            proxies = {
                'http': 'http://3dbxcTLYpHGv:3dbxcTLYpHGv_country-sg@superproxy.zenrows.com:1337',
                'https': 'http://3dbxcTLYpHGv:3dbxcTLYpHGv_country-sg@superproxy.zenrows.com:1337',
            }

        elif proxy_name == 'zenrows_universal':
            base = "https://api.zenrows.com/v1/"
            query = {
                'url': request_url,
                'apikey': zenrows_apikey,
                'custom_headers': 'true'
            }
            modified_url = f"{base}?{urllib.parse.urlencode(query)}"

        elif proxy_name == 'zenrows_api':
            proxy = "http://21ed11ef5c872bc7727680a52233027db4578a0e:@api.zenrows.com:8001"
            proxies = {"http": proxy, "https": proxy}

        elif proxy_name == 'custom_residential':
            proxy_url = 'http://user:pass@res-proxy.com:8888'
            proxies = {'http': proxy_url, 'https': proxy_url}

        elif proxy_name == 'custom_header_proxy':
            proxy_url = 'http://my-header-proxy.local'
            modified_headers['X-Proxy-Token'] = 'secure-token'
            proxies = {'http': proxy_url, 'https': proxy_url}

        return proxies, modified_url, modified_headers

    def make_direct_request(self, request, spider):
        """
        Make direct requests call bypassing Scrapy's URL encoding
        """
        # Use original URL without Scrapy's encoding
        original_url = request.url
        method = request.method.upper()
        filename = request.meta['filename']
        cache_file = os.path.join(self.cache_dir, filename)

        should_be = request.meta.get('should_be')
        not_should_be = request.meta.get('not_should_be')
        xpath_should_be = request.meta.get('xpath_should_be')
        xpath_not_should_be = request.meta.get('xpath_not_should_be')

        # ✅ Check cache first
        if os.path.exists(cache_file):
            spider.logger.info(f"[Direct Request Cache Hit] Returning from file: {cache_file}")
            with open(cache_file, "r", encoding="utf-8") as f:
                cached_content = f.read()

            # Validate cached content
            if self.validate_response(cached_content, should_be, not_should_be, xpath_should_be, xpath_not_should_be):
                response = HtmlResponse(url=original_url, body=cached_content, encoding='utf-8', request=request)
                response.meta['cache_file_path'] = cache_file
                response.meta['from_cache'] = True
                return response
            else:
                spider.logger.warning(f"[Direct Request] Cached content invalid, removing cache: {cache_file}")
                os.remove(cache_file)

        # Prepare request parameters
        headers = request.headers.to_unicode_dict()
        cookies = request.cookies
        timeout = request.meta.get('timeout', 51)
        verify = request.meta.get('verify', False)
        params = request.meta.get('params', None)

        # Handle proxy settings
        proxy_name = request.meta.get('proxy_name')
        proxies, final_url, final_headers = self.resolve_proxy(
            proxy_name=proxy_name,
            request_url=original_url,
            method=method,
            headers=headers
        )
        final_url = urllib.parse.unquote(final_url)

        # Retry logic for direct requests
        retry_count = 0
        while retry_count < self.max_retry:
            retry_count += 1
            try:
                spider.logger.info(f"[Direct Request] Attempt {retry_count} for: {final_url}")

                if method == 'GET':
                    r = requests.get(
                        final_url,
                        headers=final_headers,
                        cookies=cookies,
                        params=params,
                        timeout=timeout,
                        verify=verify,
                        proxies=proxies
                    )
                elif method == 'POST':
                    r = requests.post(
                        final_url,
                        headers=final_headers,
                        data=request.body,
                        cookies=cookies,
                        timeout=timeout,
                        verify=verify,
                        proxies=proxies
                    )
                else:
                    # Handle other HTTP methods
                    r = requests.request(
                        method,
                        final_url,
                        headers=final_headers,
                        data=request.body,
                        cookies=cookies,
                        timeout=timeout,
                        verify=verify,
                        proxies=proxies
                    )

                # Validate response
                if r.status_code == 200 and self.validate_response(r.text, should_be, not_should_be, xpath_should_be, xpath_not_should_be):
                    # Cache the valid response
                    with open(cache_file, "w", encoding="utf-8") as f:
                        f.write(r.text)

                    spider.logger.info(f"✅ [Direct Request] Valid response on attempt {retry_count}")
                    response = HtmlResponse(url=original_url, body=r.text, encoding='utf-8', request=request)
                    response.meta['cache_file_path'] = cache_file
                    response.meta['from_cache'] = False
                    response.meta['status_code'] = r.status_code
                    return response
                else:
                    spider.logger.warning(
                        f"[Direct Request] Invalid response on attempt {retry_count}: "
                        f"Status {r.status_code}, validation failed"
                    )

            except Exception as e:
                spider.logger.error(f"[Direct Request] Attempt {retry_count} failed for {original_url}: {e}")
                if retry_count < self.max_retry:
                    time.sleep(2 ** retry_count)  # Exponential backoff

        # All retries failed
        spider.logger.error(f"❌ [Direct Request] All attempts failed for {original_url}")
        # Return empty response with error status
        response = HtmlResponse(url=original_url, body="", encoding='utf-8', request=request, status=500)
        response.meta['direct_request_failed'] = True
        return response

    def make_direct_cach(self, request, spider):
        """
        Make direct requests call bypassing any requests process
        """
        # Use original URL without Scrapy's encoding
        original_url = request.url
        filename = request.meta['filename']
        cache_file = os.path.join(self.cache_dir, filename)

        # ✅ Check cache first
        if os.path.exists(cache_file):
            spider.logger.info(f"[Direct Request Cache Hit] Returning from file: {cache_file}")
            with open(cache_file, "r", encoding="utf-8") as f:
                cached_content = f.read()

            response = HtmlResponse(url=original_url, body=cached_content, encoding='utf-8', request=request)
            response.meta['cache_file_path'] = cache_file
            response.meta['from_cache'] = True
            return response

        # Cach File Not Found....
        spider.logger.error(f"❌ [Direct Cach] Failed to fetch data from direct cach file {cache_file}")
        # Return empty response with error status
        response = HtmlResponse(url=original_url, body="", encoding='utf-8', request=request, status=404)
        response.meta['direct_cach_failed'] = True
        return response

    def process_response(self, request, response, spider):
        # ✅ Check if direct_requests mode is enabled
        if request.meta.get('direct_requests', False):
            spider.logger.info(f"[Direct Request Mode] Processing: {request.url}")
            return self.make_direct_request(request, spider)

        elif request.meta.get('direct_cach', False):
            spider.logger.info(f"[Direct Cach Mode] Processing: {request.url}")
            return self.make_direct_cach(request, spider)

        # Original logic for normal Scrapy processing
        url = request.url
        method = request.method.upper()
        filename = request.meta['filename']
        cache_file = os.path.join(self.cache_dir, filename)

        should_be = request.meta['should_be']
        not_should_be = request.meta.get('not_should_be')
        xpath_should_be = request.meta.get('xpath_should_be')
        xpath_not_should_be = request.meta.get('xpath_not_should_be')

        # Skip retry for 4xx errors except 429 and 403
        if 400 <= response.status < 500 and response.status != 429 and response.status != 403:
            spider.logger.warning(f"❌ Skipping retry for HTTP {response.status} {url}")
            return response

        # ✅ Return cached file if exists
        if os.path.exists(cache_file):
            spider.logger.info(f"[Cache Hit] Returning from file: {cache_file}")
            with open(cache_file, "r", encoding="utf-8") as f:
                cached_content = f.read()

            response = HtmlResponse(url=url, body=cached_content, encoding='utf-8', request=request)
            response.meta['cache_file_path'] = cache_file
            return response

        # ✅ Accept valid Scrapy response
        if response.status == 200 and self.validate_response(response.text, should_be, not_should_be,
                                                             xpath_should_be, xpath_not_should_be):
            with open(cache_file, "w", encoding="utf-8") as f:
                f.write(response.text)

            response = HtmlResponse(url=url, body=response.text, encoding='utf-8', request=request)
            response.meta['cache_file_path'] = cache_file
            return response

        # 🔁 Retry using Scrapy
        scrapy_retry_count = request.meta.get('scrapy_retry_count', 0)
        proxy_name = request.meta.get('proxy_name')

        if scrapy_retry_count < self.max_retry and not proxy_name:
            new_meta = request.meta.copy()
            new_meta['scrapy_retry_count'] = scrapy_retry_count + 1
            spider.logger.info(f"🔌 [Scrapy retry] Using proxy '{proxy_name}'")
            spider.logger.warning(f"🔁 Retrying via Scrapy: attempt {scrapy_retry_count + 1} for {url}")
            return request.replace(url=url, dont_filter=True, meta=new_meta)

        # 🔁 Final fallback: retry using requests
        spider.logger.warning(f"🔄 Scrapy retries exhausted. Fallback to requests for: {url}")

        headers = request.headers.to_unicode_dict()
        cookies = request.cookies
        timeout = request.meta.get('timeout', 51)
        verify = request.meta.get('verify', False)

        # ⛓️ Proxy logic
        proxy_name = request.meta.get('proxy_name')
        proxies, final_url, final_headers = self.resolve_proxy(
            proxy_name=proxy_name,
            request_url=url,
            method=method,
            headers=headers
        )

        retry_count = 0
        while retry_count < self.max_retry:
            retry_count += 1
            try:
                print("Requesting for: ", final_url)
                if method == 'GET':
                    r = requests.get(final_url, headers=final_headers, cookies=cookies,
                                     timeout=timeout, verify=verify, proxies=proxies)
                else:
                    r = requests.post(final_url, headers=final_headers, data=request.body, cookies=cookies,
                                      timeout=timeout, verify=verify, proxies=proxies)

                if r.status_code == 200 and self.validate_response(r.text, should_be, not_should_be,
                                                                   xpath_should_be, xpath_not_should_be):
                    with open(cache_file, "w", encoding="utf-8") as f:
                        f.write(r.text)
                    spider.logger.info(f"✅ Valid response from requests after retry {retry_count}")

                    response = HtmlResponse(url=url, body=r.text, encoding='utf-8', request=request)
                    response.meta['cache_file_path'] = cache_file
                    return response

            except Exception as e:
                spider.logger.error(f"Retry {retry_count} via requests failed for {url}: {e}")
                time.sleep(3)

        spider.logger.error(f"❌ Final failure after fallback retries for {url}")
        return response  # return original invalid response if all retries fail