import time
import random
import re
import traceback
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC

FORM_URL = "https://bombayhighcourt.nic.in/case_query.php"
CNR_XPATH = "/html/body/div[3]/div/div[2]/form/table/tbody/tr[3]/td[2]"

# Stealth JS to mask Selenium automation
STEALTH_JS = r"""
Object.defineProperty(navigator, 'webdriver', { get: () => undefined });
if (!navigator.languages || !navigator.languages.length) {
  Object.defineProperty(navigator, 'languages', { get: () => ['en-US', 'en'] });
}
Object.defineProperty(navigator, 'plugins', { get: () => [1, 2, 3, 4, 5] });
window.chrome = window.chrome || { runtime: {} };
"""

def type_slow(el, text, per_key=0.12):
    """Type text into an element with a human‑like delay."""
    el.clear()
    for ch in text:
        el.send_keys(ch)
        time.sleep(per_key)

def process_case(side_choice, case_type, case_number, case_year):
    """
    Fetch the CNR number for a given case from the Bombay High Court site.

    Args:
        side_choice (str): "Civil", "Criminal", or "Original"
        case_type (str): Dropdown text for case type (e.g. "SA - Second Appeal")
        case_number (str|int): Case number
        case_year (str|int): Case year

    Returns:
        str | None: CNR value if found, else None
    """
    print(f"\n=== Starting CNR fetch for {side_choice} → {case_type} {case_number}/{case_year} ===")

    opts = Options()
    opts.add_argument(f'--window-size={random.randint(1280, 1366)},{random.randint(720, 900)}')
    driver = webdriver.Chrome(options=opts)
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {"source": STEALTH_JS})
    wait = WebDriverWait(driver, 15)

    try:
        # Warm‑up load
        driver.get(FORM_URL)
        time.sleep(0.5)

        # Load form
        driver.get(FORM_URL)
        wait.until(EC.presence_of_element_located((By.XPATH, "//form")))
        wait.until(EC.presence_of_element_located((By.XPATH, "//input[@name='CSRFToken']")))
        wait.until(EC.presence_of_element_located((By.XPATH, "//img[contains(@src,'captcha')]")))

        # --- Side dropdown ---
        side_xpath = "//select[@name='m_sideflg']"
        side_select = Select(driver.find_element(By.XPATH, side_xpath))
        # Always explicitly select, even if Civil is default
        if side_choice.lower().startswith("crim"):
            side_select.select_by_visible_text("Criminal")
        elif side_choice.lower().startswith("orig"):
            side_select.select_by_visible_text("Original")
        else:
            side_select.select_by_visible_text("Civil")
        time.sleep(0.2)

        ctype_xpath = "/html/body/div[3]/div/div[2]/form/table/tbody/tr[2]/td/div[6]/div[2]/select"
        ctype_select = Select(driver.find_element(By.XPATH, ctype_xpath))
        print("Available case types:", [o.text for o in ctype_select.options])


        # --- Case type ---
        ctype_xpath = "/html/body/div[3]/div/div[2]/form/table/tbody/tr[2]/td/div[6]/div[2]/select"
        wait.until(EC.text_to_be_present_in_element((By.XPATH, ctype_xpath), case_type))
        Select(driver.find_element(By.XPATH, ctype_xpath)).select_by_visible_text(case_type)
        time.sleep(0.2)

        # --- Case number ---
        cno_xpath = "/html/body/div[3]/div/div[2]/form/table/tbody/tr[2]/td/div[8]/div[2]/input"
        driver.find_element(By.XPATH, cno_xpath).send_keys(str(case_number))
        time.sleep(0.2)

        # --- Year ---
        cyear_xpath = "/html/body/div[3]/div/div[2]/form/table/tbody/tr[2]/td/div[9]/div[2]/select"
        Select(driver.find_element(By.XPATH, cyear_xpath)).select_by_visible_text(str(case_year))
        time.sleep(0.2)

        # --- CAPTCHA (rand trick) ---
        captcha_img = driver.find_element(By.XPATH, "//img[contains(@src,'captcha')]")
        src = captcha_img.get_attribute("src") or ""
        m = re.search(r"[?&]rand=([A-Za-z0-9]+)", src)
        code = m.group(1) if m else ""
        captcha_input_xpath = "/html/body/div[3]/div/div[2]/form/table/tbody/tr[2]/td/div[13]/div[2]/input[2]"
        type_slow(driver.find_element(By.XPATH, captcha_input_xpath), code, per_key=0.10)

        # --- Submit ---
        driver.find_element(By.XPATH, "/html/body/div[3]/div/div[2]/form/table/tbody/tr[2]/td/div[14]/input").click()
        time.sleep(2.2)

        # --- Check invalid session ---
        if "invalidinputerror" in driver.current_url:
            print("❌ Invalid session or input error after submission.")
            return None

        # --- Extract CNR ---
        wait.until(EC.presence_of_element_located((By.XPATH, CNR_XPATH)))
        cnr_value = driver.find_element(By.XPATH, CNR_XPATH).text.strip()
        print(f"✅ CNR fetched: {cnr_value}")
        return cnr_value

    except Exception as e:
        print("⚠️ Error during CNR fetch:", repr(e))
        traceback.print_exc()
        return None

    finally:
        print("[END] Closing browser...")
        driver.quit()

# Example usage
if __name__ == "__main__":
    result = process_case("Civil", "SA - Second Appeal", "508", "1999")
    print("Result:", result)
