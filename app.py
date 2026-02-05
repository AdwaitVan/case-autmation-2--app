import os
import subprocess
import sys

# --- CRITICAL: AUTO-INSTALL PLAYWRIGHT BROWSER ---
# This forces Streamlit Cloud to download the browser binary on startup.
try:
    print("⬇️ Installing Playwright Chromium...")
    subprocess.check_call([sys.executable, "-m", "playwright", "install", "chromium"])
    print("✅ Browser installed!")
except Exception as e:
    print(f"❌ Error installing browser: {e}")
# ------------------------------------------------
import streamlit as st
import time
import base64
from datetime import datetime
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
import PIL.Image
import ddddocr

# --- PATCH FOR PILLOW/DDDDOCR CONFLICT ---
if not hasattr(PIL.Image, 'ANTIALIAS'):
    PIL.Image.ANTIALIAS = PIL.Image.LANCZOS

# --- CONFIG ---
URL = "https://hcservices.ecourts.gov.in/hcservices/main.php"
MAX_RETRIES = 5

CASES_TO_CHECK = [
    {"name": "Second Appeal", "value": "4", "no": "508", "year": "1999"},
    {"name": "Writ Petition", "value": "1", "no": "11311", "year": "2025"}
]

# --- SESSION STATE ---
if 'results' not in st.session_state:
    st.session_state.results = [] 
if 'logs' not in st.session_state:
    st.session_state.logs = []

# --- HELPER FUNCTIONS ---
def update_terminal(message, placeholder):
    now = datetime.now().strftime("%H:%M:%S")
    st.session_state.logs.append(f"[{now}] {message}")
    placeholder.code("\n".join(st.session_state.logs), language="bash")

def solve_captcha(page):
    try:
        page.wait_for_selector("#captcha_image", state="visible", timeout=3000)
        time.sleep(1)
        captcha_img = page.locator("#captcha_image")
        captcha_bytes = captcha_img.screenshot()
        ocr = ddddocr.DdddOcr(show_ad=False)
        code = ocr.classification(captcha_bytes)
        return code if len(code) == 6 else ""
    except: return ""

def get_latest_order_link(html_content):
    soup = BeautifulSoup(html_content, "html.parser")
    table = soup.find("table", class_="order_table")
    if not table: return None, None
    orders = []
    for row in table.find_all("tr")[1:]:
        cols = row.find_all("td")
        if len(cols) < 5: continue
        date_text = cols[3].get_text(strip=True)
        link_tag = cols[4].find("a")
        if date_text and link_tag:
            try:
                dt_obj = datetime.strptime(date_text, "%d-%m-%Y")
                orders.append((dt_obj, link_tag.get("href")))
            except: continue
    if not orders: return None, None
    orders.sort(key=lambda x: x[0], reverse=True)
    return orders[0][0].strftime("%d-%m-%Y"), orders[0][1]

def run_batch_process(cases, terminal_placeholder):
    st.session_state.results = []
    st.session_state.logs = []
    
    with sync_playwright() as p:
        update_terminal("🚀 Starting Robot...", terminal_placeholder)
        
        # --- FIX 1: MEMORY OPTIMIZATION ARGS ---
        # These flags prevent the browser from crashing on Streamlit Cloud
        browser = p.chromium.launch(
            headless=True,
            args=[
                '--no-sandbox',
                '--disable-dev-shm-usage',  # Crucial for Cloud
                '--disable-gpu'
            ]
        )
        context = browser.new_context(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
        page = context.new_page()

        for case in cases:
            case_label = f"{case['name']} {case['no']}/{case['year']}"
            update_terminal(f"\n📂 PROCESSING: {case_label}", terminal_placeholder)
            
            success = False
            for attempt in range(1, MAX_RETRIES + 1):
                try:
                    # ... (Navigation and Form Filling code remains the same) ...
                    # COPY YOUR EXISTING NAVIGATION/FORM FILLING LOGIC HERE
                    # OR USE THE FULL SCRIPT BELOW
                    
                    try: page.goto(URL, timeout=60000)
                    except: continue

                    page.locator("#leftPaneMenuCS").click()
                    try:
                        page.wait_for_timeout(1000)
                        if page.locator("button[data-bs-dismiss='modal']").is_visible():
                            page.locator("button[data-bs-dismiss='modal']").click()
                    except: pass

                    page.select_option("#sess_state_code", value="1")
                    page.wait_for_timeout(1000)
                    page.select_option("#court_complex_code", value="1")
                    page.wait_for_timeout(1000)

                    if page.locator("#CScaseNumber").is_visible():
                        page.locator("#CScaseNumber").click()

                    page.select_option("#case_type", value=case['value'])
                    page.locator("#search_case_no").fill(case['no'])
                    page.locator("#rgyear").fill(case['year'])

                    # Captcha Logic
                    code = solve_captcha(page)
                    if not code:
                        update_terminal("⚠️ Captcha blurry. Reloading...", terminal_placeholder)
                        continue
                    
                    page.locator("#captcha").fill(code)
                    page.locator("#goResetDiv input[value='Go']").click()
                    
                    try: page.wait_for_selector("#dispTable, text=Invalid Captcha", timeout=15000)
                    except: continue

                    if page.locator("text=Invalid Captcha").is_visible():
                        update_terminal("❌ Invalid Captcha. Retrying...", terminal_placeholder)
                        time.sleep(2)
                        continue
                    
                    # Extract Result
                    page.locator("#dispTable a[onclick*='viewHistory']").first.click()
                    page.wait_for_selector(".order_table", state="visible", timeout=20000)
                    
                    date_str, rel_link = get_latest_order_link(page.content())
                    
                    if date_str:
                        full_url = f"https://hcservices.ecourts.gov.in/hcservices/{rel_link}"
                        update_terminal(f"📄 Found Link: {date_str}", terminal_placeholder)
                        
                        # --- FIX 2: VALIDATE PDF ---
                        response = page.request.get(full_url)
                        
                        # Check if it is actually a PDF
                        content_type = response.headers.get("content-type", "")
                        
                        if response.status == 200 and "application/pdf" in content_type:
                            st.session_state.results.append({
                                "label": f"{case['no']}/{case['year']}",
                                "desc": f"{case['name']} (Order: {date_str})",
                                "data": response.body()
                            })
                            update_terminal("✅ PDF Downloaded Successfully!", terminal_placeholder)
                            success = True
                            break
                        else:
                            # It is an error page
                            update_terminal("⚠️ Website Error: Order listed but file is missing/not uploaded.", terminal_placeholder)
                            success = True # Stop retrying, the file just isn't there
                            break
                    else:
                        update_terminal("⚠️ No orders found in history.", terminal_placeholder)
                        success = True
                        break

                except Exception as e:
                    update_terminal(f"❌ Error: {e}", terminal_placeholder)
                    time.sleep(2)
            
            if not success: update_terminal(f"❌ Failed all retries for {case_label}", terminal_placeholder)
            time.sleep(2)

        browser.close()
        update_terminal("\n🏁 Batch Complete!", terminal_placeholder)

# --- UI LAYOUT ---
st.set_page_config(page_title="High Court Bot", page_icon="⚖️", layout="wide")
st.title("⚖️ High Court Viewer")

col1, col2 = st.columns([1, 1])
with col1:
    if st.button("🚀 Fetch & View Orders", type="primary"):
        run_batch_process(CASES_TO_CHECK, st.empty())

with col2:
    st.markdown("### 📋 Live Logs")
    terminal_placeholder = st.empty()

# --- PDF VIEWER SECTION ---
if st.session_state.results:
    st.markdown("---")
    st.subheader("📑 View Orders")

    # Create Tabs for each result
    tabs = st.tabs([res['label'] for res in st.session_state.results])

    for i, tab in enumerate(tabs):
        result = st.session_state.results[i]
        
        with tab:
            st.info(f"**Viewing:** {result['desc']}")
            
            # Convert PDF bytes to Base64 for embedding
            base64_pdf = base64.b64encode(result['data']).decode('utf-8')
            
            # Embed PDF using HTML <iframe>
            pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="100%" height="800" type="application/pdf"></iframe>'
            st.markdown(pdf_display, unsafe_allow_html=True)


