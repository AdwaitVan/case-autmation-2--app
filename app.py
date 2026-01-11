import streamlit as st
import pandas as pd
from ecourts.highcourt import HighCourt

st.set_page_config(page_title="Latest Orders Fetcher", layout="wide")
st.title("📄 High Court Latest Orders Fetcher")

# -------------------------------------------------------
# FULL CASE TYPE MAP (from your case_type_map.py)
# -------------------------------------------------------

CIVIL_CASE_MAP = {
    "AO": "Appeal from Order",
    "ARA": "Arbitration Appeal",
    "ARP": "Arbitration Petition",
    "CAO": "CA in Others(MCA/TXA/CA)",
    "CAP": "Civil Appl. in ARP",
    "CA": "Civil Application",
    "CAA": "Civil Application in AO",
    "CAE": "Civil Application in C.REF",
    "CAT": "Civil Application in CAPL",
    "CAN": "Civil Application in CP",
    "CAC": "Civil Application in CRA",
    "CAF": "Civil Application in FA",
    "CAM": "Civil Application in FCA",
    "CAFM": "Civil Application In FEMA",
    "CAY": "Civil Application in FERA",
    "CAL": "Civil Application in LPA",
    "CAI": "Civil Application in PIL",
    "CAS": "Civil Application in SA",
    "CAW": "Civil Application in WP",
    "CAR": "Civil Appln. in ARA",
    "CREF": "Civil References",
    "CRA": "Civil Revision Application",
    "SMCPC": "Civil Suo Motu Contempt Petition",
    "WP": "Civil Writ Petition",
    "COMAO": "Commercial AO",
    "COARA": "Commercial Arbitration Appeal",
    "COARP": "Commercial Arbitration Petition",
    "CCAPL": "Commercial Contempt Appeal",
    "COMCP": "Commercial Contempt Petition",
    "COMFA": "Commercial FA",
    "CP": "Contempt Petition",
    "CAPL": "Contempt Appeal",
    "CRR": "Court Receiver Report",
    "COXOB": "Cross Objection In Commercial FA/ARA/CO/ARP/CP/CA",
    "XOB": "Cross Objection Stamp",
    "FCA": "Family Court Appeal",
    "FEMA": "FEMA Appeal",
    "FERA": "FERA Appeal",
    "FA": "First Appeal",
    "IA": "INTERIM APPLICATION",
    "LPA": "Letter Patent Appeal",
    "MPA": "Marriage Petition (A)",
    "MCA": "Misc.Civil Application",
    "PIL": "Public Interest Litigation",
    "RC": "Rejected Case",
    "RPF": "Review Petition in FA",
    "RAP": "Review Petition in ARA",
    "COMRP": "Review Petition In Commercial FA/ARA/AO/ARP/CP/CA",
    "RPFM": "Review Petition In FEMA Appeal",
    "RPIA": "Review Petition in IA",
    "RPV": "Review Petition in MCA",
    "RPI": "Review Petition In PIL",
    "RPA": "Review Petition in AO",
    "RPR": "Review Petition in ARP",
    "RPT": "Review Petition in CAPL",
    "RPN": "Review Petition in CP",
    "RPC": "Review Petition in CRA",
    "RPM": "Review Petition in FCA",
    "RPL": "Review Petition in LPA",
    "RPS": "Review Petition in SA",
    "RPW": "Review Petition in WP",
    "SA": "Second Appeal",
    "SMP": "Suo Moto Petition",
    "SMWP": "Suo Motu Writ Petition",
    "SMPIL": "Suo Motu PIL",
    "TXA": "Tax Appeal",
    "XFER": "Transfer Case",
}

CRIMINAL_CASE_MAP = {
    "APPSC": "Application in Cr. Suo Moto CONP",
    "ALP": "Appln For Leave To Appeal(PVT.)",
    "ALS": "Appln For Leave to Appeal(STATE)",
    "ABA": "Anticipatory Bail Application",
    "APPA": "Application in Appeal",
    "APPP": "Application in Application",
    "APPCO": "Application in Confirmation",
    "APPCP": "Application in Contempt",
    "APPI": "Application in PIL",
    "APPCR": "Application in Reference",
    "APPR": "Application in Revision",
    "APPW": "Application in Writ Petition",
    "APL": "Application U/s 482",
    "BA": "Bail Application",
    "CRPIL": "Criminal Public Interest Litigation",
    "SMCP": "Suo-Motu Contempt Petition",
    "SOMO": "Suo-Motu Petition",
    "SMRN": "Suo-Motu Revision Application",
    "SMWP": "Suo-Motu Writ Petition",
    "APEAL": "Criminal Appeal",
    "APPLN": "Criminal Application",
    "CONF": "Criminal Confirmation Case",
    "CONP": "Criminal Contempt Petition",
    "REF": "Criminal Reference",
    "REVW": "Criminal Review",
    "REVN": "Criminal Revision Application",
    "SMAP": "Criminal Suo-Motu Application",
    "CRWP": "Criminal Writ Petition",
    "IA": "INTERIM APPLICATION",
    "SMP": "Suo-Motu Criminal PIL",
}

# Build dropdown list for Streamlit
case_type_options = []

for key, val in CIVIL_CASE_MAP.items():
    case_type_options.append(f"{key} – {val} (Civil)")

for key, val in CRIMINAL_CASE_MAP.items():
    case_type_options.append(f"{key} – {val} (Criminal)")


def parse_case_type(selected):
    """Extract 'SA' from 'SA – Second Appeal (Civil)'"""
    return selected.split("–")[0].strip() if "–" in selected else selected.strip()


# -------------------------------------------------------
# DEFAULT EMPTY TABLE SHOWN TO USER
# -------------------------------------------------------
default_df = pd.DataFrame({
    "State": ["MH"],
    "Bench": ["B"],
    "Case Type": [""],
    "Case Number": [""],
    "Year": [""],
    "CNR": [""],
    "Latest Order Date": [""],
    "Order Title": [""],
    "Judge": [""],
    "PDF URL": [""],
})

st.subheader("Enter Case Inputs Below")

df = st.data_editor(
    default_df,
    num_rows="dynamic",
    use_container_width=True,
    column_config={
        "Case Type": st.column_config.SelectboxColumn(
            label="Case Type",
            options=case_type_options,
            help="Select Civil/Criminal case type"
        ),
    }
)


# -------------------------------------------------------
# FETCH LATEST ORDER USING eCOURTS LIBRARY
# -------------------------------------------------------
def fetch_latest_order(row):
    try:
        hc = HighCourt(state_code=row["State"], bench_code=row["Bench"])

        # CASE A — CNR given
        if isinstance(row["CNR"], str) and row["CNR"].strip():
            orders = hc.orders(cnr=row["CNR"].strip())
            if len(orders) == 0:
                return None
            return orders[0]

        # CASE B — Case Type + Number + Year
        case_type_short = parse_case_type(row["Case Type"])

        case = hc.case(
            case_type=case_type_short,
            case_no=str(row["Case Number"]).strip(),
            case_year=str(row["Year"]).strip(),
        )

        if len(case.orders) == 0:
            return None
        return case.orders[0]

    except Exception:
        return None


# -------------------------------------------------------
# FETCH BUTTON
# -------------------------------------------------------
st.subheader("Run Fetch")

if st.button("🔍 Fetch Latest Orders"):
    progress = st.progress(0)
    total = len(df)

    for i, row in df.iterrows():
        progress.progress((i + 1) / total)
        latest = fetch_latest_order(row)

        if latest:
            df.at[i, "Latest Order Date"] = latest.order_date
            df.at[i, "Order Title"] = latest.order_title
            df.at[i, "Judge"] = getattr(latest, "judge_name", "")
            df.at[i, "PDF URL"] = latest.pdf_url
        else:
            df.at[i, "Latest Order Date"] = "Not Found"
            df.at[i, "Order Title"] = ""
            df.at[i, "Judge"] = ""
            df.at[i, "PDF URL"] = ""

    st.success("Fetch Completed!")
    st.dataframe(df, use_container_width=True)


# -------------------------------------------------------
# DOWNLOAD OPTION
# -------------------------------------------------------
st.subheader("Download Updated Table")

csv = df.to_csv(index=False).encode("utf-8")

st.download_button(
    label="⬇ Download CSV",
    data=csv,
    file_name="latest_orders.csv",
    mime="text/csv"
)
