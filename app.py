import streamlit as st
import subprocess
import re
import time
from playwright.sync_api import sync_playwright

# ==============================================================================
# 1. CLOUD SETUP: AUTOMATIC BROWSER INSTALLER
# ==============================================================================
def install_playwright():
    """
    This runs only once to install the Chromium browser on the Streamlit Cloud server.
    """
    if "playwright_installed" not in st.session_state:
        try:
            with st.spinner("🔧 Installing Browser for Cloud (First Run Only)..."):
                subprocess.run(["playwright", "install", "chromium"], check=True)
            st.session_state["playwright_installed"] = True
        except Exception as e:
            st.error(f"Browser installation failed: {e}")

# ==============================================================================
# 2. HELPER: CASE TYPE MAPPER (Simplified)
# ==============================================================================
def resolve_case_type_name(short_code):
    """
    Maps short codes (WP, SA) to the exact text expected by the High Court dropdown.
    """
    code = short_code.strip().upper().replace(".", "")
    
    # Common mappings (You can add more from your original file if needed)
    mapping = {
        "WP": "Civil Writ Petition",
        "PIL": "Public Interest Litigation",
        "SA": "Second Appeal",
        "FA": "First Appeal",
        "CA": "Civil Application",
        "MCA": "Misc.Civil Application",
        "CRA": "Civil Revision Application",
        "CP": "Contempt Petition",
        "LPA": "Letter Patent Appeal",
        "BA": "Bail Application",
        "ABA": "Anticipatory Bail Application",
        "APEAL": "Criminal Appeal",
        "APPLN": "Criminal Application",
        "CRWP": "Criminal Writ Petition"
    }
    
    # Return the mapped name if found, otherwise return the input as-is
    return mapping.get(code, short_code)

# ==============================================================================
# 3. CORE LOGIC: PLAYWRIGHT ROBOT
# ==============================================================================
def fetch_cnr_data(side, case_type_text, case_no, case_year):
    url = "https://bombayhighcourt.nic.in/case_query.php"
    
    with sync_playwright() as p:
        # Launch Headless Chrome
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        )
        page = context.new_page()
        
        try:
            # 1. Load Page
            page.goto(url, timeout=30000)
            
            # 2. Select Side (Civil/Criminal/Original)
            side_select = page.locator("select[name='m_sideflg']")
            if side.startswith("Crim"):
                side_select.select_option(label="Criminal")
            elif side.startswith("Orig"):
                side_select.select_option(label="Original")
            else:
                side_select.select_option(label="Civil")
                
            # Wait for reload
            page.wait_for_timeout(1000)

            # 3. Select Case Type
            # XPath for Case Type Dropdown
            ctype_xpath = "/html/body/div[3]/div/div[2]/form/table/tbody/tr[2]/td/div[6]/div[2]/select"
            # Try to select by label
            try:
                page.locator(ctype_xpath).select_option(label=case_type_text)
            except:
                return {"status": "Error", "message": f"Could not find Case Type '{case_type_text}' in dropdown."}

            # 4. Enter Case Number
            cno_xpath = "/html/body/div[3]/div/div[2]/form/table/tbody/tr[2]/td/div[8]/div[2]/input"
            page.locator(cno_xpath).fill(str(case_no))

            # 5. Select Year
            cyear_xpath = "/html/body/div[3]/div/div[2]/form/table/tbody/tr[2]/td/div[9]/div[2]/select"
            page.locator(cyear_xpath).select_option(label=str(case_year))

            # 6. Solve Captcha (The URL Trick)
            captcha_img = page.locator("//img[contains(@src,'captcha')]")
            src_url = captcha_img.get_attribute("src")
            
            code = "12345" # Fallback
            if src_url:
                match = re.search(r"[?&]rand=([A-Za-z0-9]+)", src_url)
                if match:
                    code = match.group(1)
            
            # Input the code
            captcha_input_xpath = "/html/body/div[3]/div/div[2]/form/table/tbody/tr[2]/td/div[13]/div[2]/input[2]"
            page.locator(captcha_input_xpath).fill(code)

            # 7. Click Go
            go_btn = "/html/body/div[3]/div/div[2]/form/table/tbody/tr[2]/td/div[14]/input"
            page.locator(go_btn).click()
            
            # 8. Wait for results
            page.wait_for_timeout(2000)

            # 9. Extract CNR
            # This is the cell where CNR usually appears
            result_cell = page.locator("/html/body/div[3]/div/div[2]/form/table/tbody/tr[3]/td[2]")
            
            if result_cell.is_visible():
                cnr_text = result_cell.inner_text().strip()
                return {"status": "Success", "cnr": cnr_text}
            else:
                # Check for "Invalid Captcha" error text
                body_text = page.inner_text("body")
                if "Invalid Code" in body_text:
                    return {"status": "Failed", "message": "Captcha Failed (Try again)"}
                return {"status": "Failed", "message": "Case not found or inputs incorrect."}

        except Exception as e:
            return {"status": "Error", "message": str(e)}
        finally:
            browser.close()

# ==============================================================================
# 4. STREAMLIT UI
# ==============================================================================

st.set_page_config(page_title="High Court Fetcher", page_icon="⚖️")

# Run the installer once
install_playwright()

st.title("⚖️ Bombay HC - Case Fetcher")
st.markdown("Automated lookup using **Playwright** on the Cloud.")

# --- Inputs ---
col1, col2 = st.columns(2)
with col1:
    side_input = st.selectbox("Side", ["Civil", "Criminal", "Original"])
    type_code = st.text_input("Case Type (e.g. WP, SA, BA)", value="WP")
with col2:
    num_input = st.text_input("Case Number", value="")
    year_input = st.selectbox("Year", range(2026, 1990, -1), index=1)

# --- Action ---
if st.button("🔍 Get CNR Number", type="primary"):
    if not num_input:
        st.warning("Please enter a Case Number!")
    else:
        # 1. Resolve Name
        full_type_name = resolve_case_type_name(type_code)
        
        st.info(f"🤖 Searching for: **{side_input}** / **{full_type_name}** / **{num_input}/{year_input}**")
        
        # 2. Run Robot
        with st.spinner("Connecting to High Court website..."):
            result = fetch_cnr_data(side_input, full_type_name, num_input, year_input)
        
        # 3. Display
        if result["status"] == "Success":
            st.success("✅ Case Found!")
            st.metric("CNR Number", result["cnr"])
            st.caption("You can now use this CNR to fetch orders via API.")
        else:
            st.error(f"❌ {result['message']}")
