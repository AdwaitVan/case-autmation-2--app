import streamlit as st
import logging
from datetime import datetime
from case_type_map import resolve_case_type
from fetching_cnr import process_case

# -------------------------
# Logging setup
# -------------------------
logging.basicConfig(
    format="%(asctime)s [%(levelname)s] %(message)s",
    level=logging.INFO
)

# -------------------------
# Page config
# -------------------------
st.set_page_config(
    page_title="Case CNR Fetcher",
    page_icon="⚖️",
    layout="wide"
)

st.title("⚖️ Case CNR Fetcher")
st.markdown("Fetch CNR numbers from Bombay High Court")

# Initialize session state for results
if 'results' not in st.session_state:
    st.session_state.results = []

# -------------------------
# Input Form
# -------------------------
st.subheader("Enter Case Details")

col1, col2 = st.columns(2)

with col1:
    side_choice = st.selectbox(
        "Case Side:",
        ["Civil", "Criminal", "Original"],
        key="side"
    )

with col2:
    case_type_input = st.text_input(
        "Case Type (e.g., 'SA', 'WP', 'Cr.ABA'):",
        placeholder="Enter case type",
        key="case_type"
    )

col1, col2 = st.columns(2)

with col1:
    case_number = st.number_input(
        "Case Number:",
        min_value=1,
        value=1,
        key="case_no"
    )

with col2:
    case_year = st.number_input(
        "Case Year:",
        min_value=1950,
        max_value=datetime.now().year,
        value=datetime.now().year,
        key="year"
    )

# Fetch button
if st.button("🔍 Fetch CNR", type="primary"):
    if not case_type_input.strip():
        st.error("❌ Please enter a case type")
    else:
        with st.spinner("Fetching CNR from Bombay High Court..."):
            try:
                # Resolve case type
                dropdown_text = resolve_case_type(case_type_input)
                st.info(f"📋 Resolved case type: **{dropdown_text}**")
                
                # Fetch CNR
                cnr = process_case(side_choice, dropdown_text, str(case_number), str(case_year))
                
                if cnr:
                    st.success(f"✅ CNR Found: **{cnr}**")
                    st.session_state.results.append({
                        "Case Type": case_type_input,
                        "Case No": case_number,
                        "Year": case_year,
                        "Side": side_choice,
                        "CNR": cnr,
                        "Status": "Fetched"
                    })
                else:
                    st.warning("⚠️ No CNR found for this case")
                    st.session_state.results.append({
                        "Case Type": case_type_input,
                        "Case No": case_number,
                        "Year": case_year,
                        "Side": side_choice,
                        "CNR": "Not Found",
                        "Status": "Not Found"
                    })
            
            except ValueError as ve:
                st.error(f"❌ Unknown case type: {ve}")
                st.session_state.results.append({
                    "Case Type": case_type_input,
                    "Case No": case_number,
                    "Year": case_year,
                    "Side": side_choice,
                    "CNR": "Error",
                    "Status": "Error"
                })
            
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
                st.session_state.results.append({
                    "Case Type": case_type_input,
                    "Case No": case_number,
                    "Year": case_year,
                    "Side": side_choice,
                    "CNR": "Error",
                    "Status": "Error"
                })

# -------------------------
# Display Results
# -------------------------
if st.session_state.results:
    st.divider()
    st.subheader("Fetched Cases")
    
    # Display as table
    for idx, result in enumerate(st.session_state.results):
        with st.container(border=True):
            col1, col2, col3, col4, col5 = st.columns(5)
            with col1:
                st.write(f"**Case Type:** {result['Case Type']}")
            with col2:
                st.write(f"**Case No:** {result['Case No']}/{result['Year']}")
            with col3:
                st.write(f"**Side:** {result['Side']}")
            with col4:
                st.write(f"**CNR:** {result['CNR']}")
            with col5:
                status_color = "🟢" if result['Status'] == 'Fetched' else "🔴"
                st.write(f"**Status:** {status_color} {result['Status']}")
    
    # Statistics
    st.divider()
    st.subheader("Statistics")
    col1, col2, col3 = st.columns(3)
    
    total = len(st.session_state.results)
    fetched = len([r for r in st.session_state.results if r['Status'] == 'Fetched'])
    errors = total - fetched
    
    with col1:
        st.metric("Total Cases", total)
    
    with col2:
        st.metric("CNR Fetched", fetched)
    
    with col3:
        st.metric("Errors", errors)
    
    # Clear results button
    if st.button("🗑️ Clear Results"):
        st.session_state.results = []
        st.rerun()
