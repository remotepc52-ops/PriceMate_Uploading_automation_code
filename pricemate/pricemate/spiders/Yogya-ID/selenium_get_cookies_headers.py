import json
import time
import urllib.parse
from urllib.parse import urlparse

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
URL = "https://supermarket.yogyaonline.co.id/supermarket/fresh-daily-food-lainlain/category"
OUTPUT_FILE = "cookies_and_headers.txt"
HEADLESS = False   # set True to run headless
WAIT_TIMEOUT = 12  # seconds
SCROLL_PAUSE = 1.0
# ----------------------------

def start_driver():
    opts = Options()
    if HEADLESS:
        # modern headless flag
        opts.add_argument("--headless=new")
    opts.add_argument("--window-size=1920,1080")
    opts.add_argument("--disable-gpu")
    opts.add_argument("--no-sandbox")
    opts.add_argument("--disable-dev-shm-usage")
    # allow Selenium to auto-manage driver by not providing Service path
    driver = webdriver.Chrome(options=opts)
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
    """
    Try multiple strategies to reach 'page 2' / load next results:
    1) Click an 'a' element whose text is '2'
    2) Click a 'Next' button (text 'Next' or '>').
    3) Click a 'Load more' / 'Lihat Lainnya' button.
    4) If none found, scroll to bottom repeatedly and wait for more items (heuristic).
    """
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
                # wait for navigation or content change
                time.sleep(1)
                wait.until(lambda d: "page=2" in d.current_url or "page/2" in d.current_url or True)
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

    # Strategy C: click "load more" style buttons (common on infinite scroll)
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
                # wait for new content
                time.sleep(1.5)
                return True
        except NoSuchElementException:
            continue
        except Exception:
            continue

    # Strategy D: scroll to bottom repeatedly and wait for new items to appear
    # Heuristic: count product-like elements, then scroll, then wait for count to increase
    product_selectors = [
        "//div[contains(@class,'product') or contains(@class,'item') or contains(@class,'product-item')]",
        "//li[contains(@class,'product') or contains(@class,'item')]",
        "//div[contains(@class,'prd') or contains(@class,'product-list')]",
        "//article",  # fallback
    ]
    # get initial count
    initial_count = 0
    for sel in product_selectors:
        try:
            elems = driver.find_elements(By.XPATH, sel)
            if len(elems) > initial_count:
                initial_count = len(elems)
        except Exception:
            continue

    # perform incremental scrolls
    max_scrolls = 10
    for i in range(max_scrolls):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(SCROLL_PAUSE)
        # small extra scroll to trigger lazy loads
        driver.execute_script("window.scrollBy(0, 300);")
        time.sleep(SCROLL_PAUSE)
        # check new count
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
    # if nothing worked, return False
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

def main():
    driver = start_driver()
    try:
        driver.get(URL)

        # optional: wait until page loads body
        try:
            WebDriverWait(driver, WAIT_TIMEOUT).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        except TimeoutException:
            # continue anyway
            pass

        # try to navigate to page 2
        ok = navigate_to_page2(driver)
        if not ok:
            print("[!] Could not find explicit pagination or load-more. Falling back to constructing page=2 URL if possible.")
            # attempt to construct a page=2 query param if current url has recognizable structure
            cur = driver.current_url
            if "?" in cur:
                new = cur + "&page=2"
            else:
                # attempt to append ?page=2
                new = cur + ("&page=2" if "page=" in cur else "?page=2")
            try:
                driver.get(new)
                time.sleep(1.5)
            except Exception:
                print("[!] Fallback navigation failed; continuing with current page.")

        # wait briefly for the second page to load fully
        time.sleep(1.5)

        # 1) get cookies
        raw_cookies = driver.get_cookies()
        cookie_dict = build_cookie_dict(raw_cookies)

        # 2) get user-agent
        try:
            user_agent = driver.execute_script("return navigator.userAgent")
        except Exception:
            user_agent = "Mozilla/5.0"

        # 3) origin + referer
        parsed = urlparse(driver.current_url)
        origin = f"{parsed.scheme}://{parsed.netloc}"
        referer = driver.current_url

        # 4) xsrf token from cookie if present
        xsrf_value = cookie_dict.get("XSRF-TOKEN") or cookie_dict.get("x-xsrf-token") or ""

        headers = {
            "accept": "application/json, text/plain, */*",
            "accept-language": "en-GB,en-US;q=0.9,en;q=0.8",
            "content-type": "application/json;charset=UTF-8",
            "origin": origin,
            "priority": "u=1, i",
            "referer": referer,
            "sec-ch-ua": '"Chromium";v="142", "Google Chrome";v="142", "Not_A Brand";v="99"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "user-agent": user_agent,
            "x-csrf-token": "",
            "x-requested-with": "XMLHttpRequest",
            "x-xsrf-token": xsrf_value,
        }

        cookie_header_str = build_cookie_header_string(cookie_dict)
        headers_with_cookie = dict(headers)
        headers_with_cookie["cookie"] = cookie_header_str

        cookies_literal = dict_to_python_literal(cookie_dict)
        headers_literal = dict_to_python_literal(headers_with_cookie)

        output_text = f"cookies = {cookies_literal}\n\nheaders = {headers_literal}\n"
        with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
            f.write(output_text)

        print(f"[+] Saved cookies and headers (after navigating) to: {OUTPUT_FILE}")
        print(output_text)

    finally:
        driver.quit()

if __name__ == "__main__":
    main()