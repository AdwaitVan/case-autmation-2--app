import logging
import os
import sys
import traceback
import datetime
import xlwings as xw
from case_type_map import resolve_case_type
from fetching_cnr import process_case

# -------------------------
# Logging setup
# -------------------------
LOG_FILE = os.path.join(os.path.dirname(__file__), "automation_log.txt")
logging.basicConfig(
    filename=LOG_FILE,
    filemode="a",
    format="%(asctime)s [%(levelname)s] %(message)s",
    level=logging.INFO
)

# -------------------------
# Helpers
# -------------------------
def clean(val):
    """Convert Excel float values like 1999.0 to '1999' and trim strings."""
    if val is None:
        return ""
    if isinstance(val, float) and val.is_integer():
        return str(int(val))
    return str(val).strip()

def normalize_header_map(headers):
    """
    Normalize headers by stripping whitespace and dots.
    Maps variants like 'Case No.' and 'Case No' to the same key 'Case No'.
    """
    norm = {}
    for idx, name in enumerate(headers, start=1):
        key = str(name or "").strip()
        key = key.replace(".", "")  # remove trailing dots
        norm[key] = idx
    return norm

# -------------------------
# Main Excel workflow
# -------------------------
def fetch_and_update_excel():
    logging.info("Connecting to running Excel instance...")

    app = xw.apps.active
    if app is None:
        raise RuntimeError("No active Excel app found. Open the workbook and run the macro again.")

    wb = app.books.active
    sheet = wb.sheets["Cases"]
    logging.info(f"Attached to workbook: {wb.name}")

    # Read and normalize headers
    headers = sheet.range("A1").expand("right").value
    header_map = normalize_header_map(headers)

    # Ensure Notes column exists
    if "Notes" not in header_map:
        sheet.range(1, len(headers) + 1).value = "Notes"
        header_map["Notes"] = len(headers) + 1
        logging.info("Created Notes column")

    # Resolve required columns (support minor header variations)
    required = {
        "Case Type": header_map.get("Case Type"),
        "Case No": header_map.get("Case No"),
        "Year": header_map.get("Year"),
        "CNR": header_map.get("CNR"),
        "Status": header_map.get("Status"),
        "Notes": header_map.get("Notes"),
    }

    missing = [k for k, v in required.items() if v is None]
    if missing:
        raise KeyError(f"Missing required headers: {missing}. "
                       f"Headers present: {headers}")

    case_type_col = required["Case Type"]
    case_no_col = required["Case No"]
    year_col = required["Year"]
    cnr_col = required["CNR"]
    status_col = required["Status"]
    notes_col = required["Notes"]

    last_row = sheet.range("A1").expand("down").last_cell.row
    logging.info(f"Found {last_row - 1} data rows")

    for row in range(2, last_row + 1):
        try:
            status_val = sheet.range(row, status_col).value
            status = str(status_val or "").strip().lower()
        except Exception:
            status = ""

        if status == "pending":
            case_type_excel = clean(sheet.range(row, case_type_col).value)
            case_no = clean(sheet.range(row, case_no_col).value)
            year = clean(sheet.range(row, year_col).value)

            try:
                # Decide Civil/Criminal from case type text
                side_choice = "Criminal" if case_type_excel.startswith("Cr") else "Civil"

                # Map to site’s exact/near-exact dropdown text
                dropdown_text = resolve_case_type(case_type_excel)

                logging.info(
                    f"Row {row}: {case_type_excel} {case_no}/{year} "
                    f"→ Side={side_choice}, Dropdown='{dropdown_text}'"
                )

                cnr = process_case(side_choice, dropdown_text, case_no, year)

                sheet.range(row, cnr_col).value = cnr if cnr else "Not Found"
                sheet.range(row, status_col).value = "Fetched" if cnr else "Error"
                sheet.range(row, notes_col).value = "" if cnr else "No CNR found"

            except ValueError as ve:
                msg = f"Unknown case type: {ve}"
                logging.warning(f"Row {row}: {msg}")
                sheet.range(row, cnr_col).value = "Error"
                sheet.range(row, status_col).value = "Error"
                sheet.range(row, notes_col).value = msg

            except Exception as e:
                msg = f"Error: {e}"
                logging.error(f"Row {row}: {msg}")
                logging.error(traceback.format_exc())
                sheet.range(row, cnr_col).value = "Error"
                sheet.range(row, status_col).value = "Error"
                sheet.range(row, notes_col).value = msg

    wb.save()
    logging.info("Workbook saved successfully")

# -------------------------
# Entrypoint
# -------------------------
def main():
    logging.info("=" * 80)
    logging.info("🚀 New run started")
    logging.info(f"Python executable: {sys.executable}")
    logging.info(f"Script arguments: {sys.argv}")
    logging.info(f"Timestamp: {datetime.datetime.now().isoformat()}")

    try:
        fetch_and_update_excel()
        logging.info("✅ Run finished successfully")
    except Exception as e:
        logging.error("❌ Run failed with exception")
        logging.error(str(e))
        logging.error(traceback.format_exc())
    finally:
        logging.info("🏁 End of run")
        logging.info("=" * 80 + "\n\n")

if __name__ == "__main__":
    main()
