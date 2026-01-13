import json
import time
import urllib.parse
from urllib.parse import urlparse
from pathlib import Path

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    NoSuchElementException,
    TimeoutException,
    ElementClickInterceptedException,
    StaleElementReferenceException,
)

# ---------- CONFIG ----------
REGIONS_FILE = "regions_cookies.json"            # input (existing cookies/headers)
OUTPUT_FILE = "regions_cookies_updated.json"     # merged output
PER_REGION_OUTPUT = "cookies_and_headers_{}.txt" # per-region human readable
HEADLESS = False
WAIT_TIMEOUT = 12
SCROLL_PAUSE = 1.0
# If you prefer to use a chromedriver Service, set CHROMEDRIVER_PATH
CHROMEDRIVER_PATH = None  # e.g. "/usr/local/bin/chromedriver" or None to let selenium manage
# ----------------------------

def start_driver():
    opts = Options()
    if HEADLESS:
        opts.add_argument("--headless=new")
    opts.add_argument("--window-size=1920,1080")
    opts.add_argument("--disable-gpu")
    opts.add_argument("--no-sandbox")
    opts.add_argument("--disable-dev-shm-usage")
    # avoid automation flags if you want
    opts.add_experimental_option("excludeSwitches", ["enable-automation"])
    opts.add_experimental_option('useAutomationExtension', False)
    if CHROMEDRIVER_PATH:
        from selenium.webdriver.chrome.service import Service
        service = Service(CHROMEDRIVER_PATH)
        driver = webdriver.Chrome(service=service, options=opts)
    else:
        driver = webdriver.Chrome(options=opts)
    driver.set_page_load_timeout(60)
    return driver

def build_cookie_dict(raw_cookies):
    cookies = {}
    for c in raw_cookies:
        name = c.get("name")
        value = c.get("value", "")
        try:
            value_decoded = urllib.parse.unquote(value)
        except Exception:
            value_decoded = value
        cookies[name] = value_decoded
    return cookies

def build_cookie_header_string(cookie_dict):
    return "; ".join(f"{k}={v}" for k, v in cookie_dict.items())

def try_click_element(driver, element):
    try:
        element.click()
        return True
    except (ElementClickInterceptedException, StaleElementReferenceException):
        try:
            driver.execute_script("arguments[0].click();", element)
            return True
        except Exception:
            return False

def navigate_to_page2(driver):
    wait = WebDriverWait(driver, WAIT_TIMEOUT)

    # Strategy A: look for a pagination link for page 2
    xpaths_for_page2 = [
        "//a[normalize-space(text())='2']",
        "//a[contains(@aria-label,'page 2') or contains(@aria-label,'Page 2')]",
        "//a[contains(@href,'page=2') or contains(@href,'/page/2') or contains(@href,'/2')]",
    ]
    for xp in xpaths_for_page2:
        try:
            el = wait.until(EC.element_to_be_clickable((By.XPATH, xp)))
            if try_click_element(driver, el):
                time.sleep(1)
                return True
        except TimeoutException:
            continue
        except Exception:
            continue

    # Strategy B: click a Next link/button
    xpaths_for_next = [
        "//a[contains(translate(text(),'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),'next')]",
        "//button[contains(translate(text(),'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),'next')]",
        "//a[contains(text(),'>') or contains(text(),'›') or contains(text(),'→')]",
        "//button[contains(text(),'>') or contains(text(),'›') or contains(text(),'→')]",
    ]
    for xp in xpaths_for_next:
        try:
            el = driver.find_element(By.XPATH, xp)
            if try_click_element(driver, el):
                time.sleep(1)
                return True
        except NoSuchElementException:
            continue
        except Exception:
            continue

    # Strategy C: click "load more" style buttons
    load_more_selectors = [
        "//button[contains(translate(.,'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),'load more')]",
        "//button[contains(translate(.,'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),'lihat lainnya')]",
        "//button[contains(@class,'load-more') or contains(@class,'loadmore') or contains(@class,'more-button')]",
        "//a[contains(@class,'load-more') or contains(@class,'loadmore') or contains(@class,'more-button')]",
    ]
    for xp in load_more_selectors:
        try:
            el = driver.find_element(By.XPATH, xp)
            if try_click_element(driver, el):
                time.sleep(1.5)
                return True
        except NoSuchElementException:
            continue
        except Exception:
            continue

    # Strategy D: scroll to bottom repeatedly and wait for new items to appear
    product_selectors = [
        "//div[contains(@class,'product') or contains(@class,'item') or contains(@class,'product-item')]",
        "//li[contains(@class,'product') or contains(@class,'item')]",
        "//div[contains(@class,'prd') or contains(@class,'product-list')]",
        "//article",
    ]
    initial_count = 0
    for sel in product_selectors:
        try:
            elems = driver.find_elements(By.XPATH, sel)
            if len(elems) > initial_count:
                initial_count = len(elems)
        except Exception:
            continue

    max_scrolls = 10
    for i in range(max_scrolls):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(SCROLL_PAUSE)
        driver.execute_script("window.scrollBy(0, 300);")
        time.sleep(SCROLL_PAUSE)
        new_count = 0
        for sel in product_selectors:
            try:
                elems = driver.find_elements(By.XPATH, sel)
                if len(elems) > new_count:
                    new_count = len(elems)
            except Exception:
                continue
        if new_count > initial_count:
            return True
    return False

def dict_to_python_literal(d):
    parts = []
    for k, v in d.items():
        if isinstance(v, str):
            escaped = v.replace("'", "\\'")
            parts.append(f"    '{k}': '{escaped}',")
        else:
            parts.append(f"    '{k}': {json.dumps(v)},")
    body = "\n".join(parts)
    return "{\n" + body + "\n}"

def domain_from_url(url):
    parsed = urlparse(url)
    return parsed.hostname

def process_region(region_key, region_conf):
    base_url = region_conf.get("base_url")
    if not base_url:
        print(f"[!] Region {region_key} missing base_url, skipping.")
        return None

    driver = start_driver()
    try:
        # initial navigation to establish domain context
        driver.get(base_url)
        try:
            WebDriverWait(driver, WAIT_TIMEOUT).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        except TimeoutException:
            pass

        # attempt to reach page 2 (optional)
        try:
            ok = navigate_to_page2(driver)
            if not ok:
                # fallback: try to append page=2
                cur = driver.current_url
                if "?" in cur:
                    new = cur + "&page=2"
                else:
                    new = cur + ("&page=2" if "page=" in cur else "?page=2")
                try:
                    driver.get(new)
                    time.sleep(1.2)
                except Exception:
                    pass
        except Exception:
            pass

        time.sleep(1.2)

        # extract cookies
        raw_cookies = driver.get_cookies()
        cookie_dict = build_cookie_dict(raw_cookies)

        # user-agent
        try:
            user_agent = driver.execute_script("return navigator.userAgent")
        except Exception:
            user_agent = region_conf.get("headers", {}).get("user-agent", "Mozilla/5.0")

        # origin + referer
        parsed = urlparse(driver.current_url)
        origin = f"{parsed.scheme}://{parsed.netloc}"
        referer = driver.current_url

        # xsrf token from cookie if present
        xsrf_value = cookie_dict.get("XSRF-TOKEN") or cookie_dict.get("x-xsrf-token") or cookie_dict.get("_tb_token_") or ""

        # build headers (merge existing headers if present)
        existing_headers = region_conf.get("headers", {})
        headers = {
            "accept": existing_headers.get("accept", "application/json, text/plain, */*"),
            "accept-language": existing_headers.get("accept-language", "en-GB,en-US;q=0.9,en;q=0.8"),
            "content-type": existing_headers.get("content-type", "application/json;charset=UTF-8"),
            "origin": origin,
            "priority": existing_headers.get("priority", "u=1, i"),
            "referer": referer,
            "sec-ch-ua": existing_headers.get("sec-ch-ua", '"Chromium";v="142", "Google Chrome";v="142", "Not_A Brand";v="99"'),
            "sec-ch-ua-mobile": existing_headers.get("sec-ch-ua-mobile", "?0"),
            "sec-ch-ua-platform": existing_headers.get("sec-ch-ua-platform", '"Windows"'),
            "sec-fetch-dest": existing_headers.get("sec-fetch-dest", "empty"),
            "sec-fetch-mode": existing_headers.get("sec-fetch-mode", "cors"),
            "sec-fetch-site": existing_headers.get("sec-fetch-site", "same-origin"),
            "user-agent": user_agent,
            "x-csrf-token": existing_headers.get("x-csrf-token", ""),
            "x-requested-with": existing_headers.get("x-requested-with", "XMLHttpRequest"),
            "x-xsrf-token": xsrf_value,
        }

        cookie_header_str = build_cookie_header_string(cookie_dict)
        headers_with_cookie = dict(headers)
        headers_with_cookie["cookie"] = cookie_header_str

        # prepare updated region conf
        updated_conf = {
            "base_url": base_url,
            "headers": headers,
            "cookies": cookie_dict,
        }

        # write per-region human readable file
        per_out = PER_REGION_OUTPUT.format(region_key)
        cookies_literal = dict_to_python_literal(cookie_dict)
        headers_literal = dict_to_python_literal(headers_with_cookie)
        output_text = f"cookies = {cookies_literal}\n\nheaders = {headers_literal}\n"
        Path(per_out).write_text(output_text, encoding="utf-8")
        print(f"[+] Saved per-region file: {per_out}")

        return updated_conf

    finally:
        driver.quit()

def main():
    # load regions
    if not Path(REGIONS_FILE).exists():
        print(f"[!] Regions file not found: {REGIONS_FILE}")
        return

    regions = json.loads(Path(REGIONS_FILE).read_text(encoding="utf-8"))
    updated = {}

    for region_key, region_conf in regions.items():
        print(f"[*] Processing region: {region_key}")
        try:
            updated_conf = process_region(region_key, region_conf)
            if updated_conf is not None:
                updated[region_key] = updated_conf
        except Exception as e:
            print(f"[!] Error processing {region_key}: {e}")

    # write merged output
    Path(OUTPUT_FILE).write_text(json.dumps(updated, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"[+] Wrote updated regions to: {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
