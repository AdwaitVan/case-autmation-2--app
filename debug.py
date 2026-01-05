import logging
import os
import sys
import traceback
import datetime
import fetchingcntintoexcel as main_script

LOG_FILE = os.path.join(os.path.dirname(__file__), "automation_log.txt")
logging.basicConfig(
    filename=LOG_FILE,
    filemode="a",
    format="%(asctime)s [%(levelname)s] %(message)s",
    level=logging.INFO
)

def main():
    logging.info("=" * 80)
    logging.info("🚀 New run started")
    logging.info(f"Python executable: {sys.executable}")
    logging.info(f"Script arguments: {sys.argv}")
    logging.info(f"Timestamp: {datetime.datetime.now().isoformat()}")

    try:
        main_script.fetch_and_update_excel()
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
