
import pandas as pd
from pathlib import Path

# 1. Set project paths
BASE_DIR = Path(__file__).resolve().parents[1]
RAW_DIR = BASE_DIR / "data" / "raw"
REPORT_DIR = BASE_DIR / "data" / "processed"

REPORT_DIR.mkdir(parents=True, exist_ok=True)

report_file = REPORT_DIR / "inspection_report.txt"

# 2. Find Excel files
excel_files = sorted(RAW_DIR.glob("*.xlsx"))

report = []

def log(message=""):
    print(message)
    report.append(str(message))


log("=" * 70)
log("BUSAN POPULATION DASHBOARD")
log("DATA INSPECTION REPORT")
log("=" * 70)

log(f"Total Excel files found: {len(excel_files)}")

if not excel_files:
    log("ERROR: No Excel files found in data/raw!")
    raise SystemExit

# 3. Inspect each Excel file
for file in excel_files:

    log("\n" + "=" * 70)
    log(f"FILE NAME: {file.name}")
    log("=" * 70)

    try:
        xls = pd.ExcelFile(file)

        log(f"Sheet names: {xls.sheet_names}")

        for sheet in xls.sheet_names:

            df = pd.read_excel(
                file,
                sheet_name=sheet,
                header=None
            )

            log("\n" + "-" * 50)
            log(f"SHEET: {sheet}")

            # Data dimensions
            log("\n[1] DATA SIZE")
            log(f"Rows: {df.shape[0]}")
            log(f"Columns: {df.shape[1]}")

            # Missing values
            log("\n[2] MISSING VALUES")
            log(df.isnull().sum().to_string())

            # Duplicate rows
            log("\n[3] DUPLICATE ROWS")
            log(str(df.duplicated().sum()))

            # Data types
            log("\n[4] DATA TYPES")
            log(df.dtypes.to_string())

            # Preview
            log("\n[5] FIRST 10 ROWS")
            log(df.head(10).to_string(index=False))

    except Exception as e:
        log(f"ERROR: {e}")

# 4. Save report
report_file.write_text(
    "\n".join(report),
    encoding="utf-8-sig"
)

log("\n" + "=" * 70)
log("DATA INSPECTION COMPLETED")
log(f"Report saved: {report_file}")
log("=" * 70)
