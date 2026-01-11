import streamlit as st
import pandas as pd
import requests
from datetime import datetime
from case_type_map import resolve_case_type

# --------------------------------------------------------------------------------
# COURT CODES
# --------------------------------------------------------------------------------

COURT_MAP = {
    "Bombay (Principal Seat)": {"state": 24, "dist": 0, "court": 1},
    "Nagpur Bench": {"state": 24, "dist": 0, "court": 2},
    "Aurangabad Bench": {"state": 24, "dist": 0, "court": 3},
    "Goa Bench": {"state": 24, "dist": 0, "court": 4},
}

# --------------------------------------------------------------------------------
# API HELPERS
# --------------------------------------------------------------------------------

def fetch_by_cnr(cnr: str):
    """Fetch case details (including type/number/year) using CNR."""
    url = "https://hcservices.ecourts.gov.in/ecourtindiaHC/services/caseDetailsByCnr.php"
    resp = requests.get(url, params={"cnr_number": cnr}, timeout=15)

    data = resp.json() if resp.ok else None
    if not data or "case_details" not in data:
        return None

    details = data["case_details"][0]

    return {
        "case_type": details.get("case_type", ""),
        "case_no": details.get("case_number", ""),
        "year": details.get("case_year", ""),
        "state": details.get("state_code", ""),
        "dist": details.get("dist_code", ""),
        "court": details.get("court_code", ""),
    }


def fetch_latest_order(state, dist, court, case_type, case_no, year):
    """Fetch latest order using the official API."""
    url = "https://hcservices.ecourts.gov.in/ecourtindiaHC/services/getOrderDetails.php"

    params = {
        "state_code": state,
        "dist_code": dist,
        "court_code": court,
        "case_type": case_type,
        "case_no": case_no,
        "case_year": year,
    }

    resp = requests.get(url, params=params, timeout=15)
    data = resp.json() if resp.ok else None

    if not data or "order_details" not in data:
        return None

    orders = data["order_details"]
    if not orders:
        return None

    # Sort by date to get the latest
    for o in orders:
        try:
            o["parsed_date"] = datetime.strptime(o["order_date"], "%Y-%m-%d")
        except:
            o["parsed_date"] = datetime.min

    latest = sorted(orders, key=lambda x: x["parsed_date"], reverse=True)[0]

    return {
        "date": latest.get("order_date", ""),
        "judge": latest.get("order_judge", ""),
        "link": latest.get("order_link", "")
    }


# --------------------------------------------------------------------------------
# STREAMLIT UI
# --------------------------------------------------------------------------------

st.set_page_config(page_title="Latest High Court Order Fetcher", layout="wide")
st.title("📄 High Court – Latest Order Fetcher")

# Court Selection
selected_court = st.selectbox(
    "Select High Court Bench",
    list(COURT_MAP.keys()),
    index=0
)

court_info = COURT_MAP[selected_court]

# Initialize table in session_state
if "table" not in st.session_state:
    st.session_state.table = pd.DataFrame({
        "Case Type": [""],
        "Case No": [""],
        "Case Year": [""],
        "CNR": [""],
        "Status": [""],
        "Latest Order Date": [""],
        "Judge": [""],
        "PDF Link": [""],
    })

st.subheader("Enter Case Details")

edited_df = st.data_editor(
    st.session_state.table,
    num_rows="dynamic",
    use_container_width=True
)

# Save edited table back
st.session_state.table = edited_df

# --------------------------------------------------------------------------------
# FETCH BUTTON
# --------------------------------------------------------------------------------

if st.button("🔍 Fetch Latest Orders"):
    df = st.session_state.table.copy()

    for idx, row in df.iterrows():
        case_type_input = str(row["Case Type"]).strip()
        case_no = str(row["Case No"]).strip()
        case_year = str(row["Case Year"]).strip()
        cnr = str(row["CNR"]).strip()

        latest_order = None

        try:
            # ──────────────────────────────
            # Case 1: Use CNR directly
            # ──────────────────────────────
            if cnr:
                base = fetch_by_cnr(cnr)
                if not base:
                    df.at[idx, "Status"] = "❌ Invalid CNR"
                    continue

                latest_order = fetch_latest_order(
                    base["state"], base["dist"], base["court"],
                    base["case_type"], base["case_no"], base["year"]
                )

            # ──────────────────────────────
            # Case 2: Use Case Type + Number + Year
            # ──────────────────────────────
            else:
                if not (case_type_input and case_no and case_year):
                    df.at[idx, "Status"] = "❌ Missing Case Info"
                    continue

                # Resolve the exact case type text (your function!)
