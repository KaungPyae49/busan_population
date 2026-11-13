
import pandas as pd
import os

# =====================================
# 1. FILE PATH
# =====================================

input_file = "data/raw/사업체수__종사자수_KOSIS.xlsx"

# =====================================
# 2. CHECK FILE
# =====================================

if not os.path.exists(input_file):
    raise FileNotFoundError(f"File not found: {input_file}")

print("=" * 60)
print("BUSINESS & EMPLOYMENT DATA INSPECTION")
print("=" * 60)

# =====================================
# 3. EXCEL SHEET INSPECTION
# =====================================

excel = pd.ExcelFile(input_file)

print("\n[1] SHEET NAMES")
print(excel.sheet_names)

# =====================================
# 4. INSPECT EACH SHEET
# =====================================

for sheet in excel.sheet_names:

    print("\n" + "=" * 60)
    print(f"SHEET: {sheet}")
    print("=" * 60)

    df = pd.read_excel(input_file, sheet_name=sheet)

    # Shape
    print("\n[2] DATA SIZE")
    print("Rows:", df.shape[0])
    print("Columns:", df.shape[1])

    # Column names
    print("\n[3] COLUMN NAMES")
    print(df.columns.tolist())

    # Data types
    print("\n[4] DATA TYPES")
    print(df.dtypes)

    # Missing values
    print("\n[5] MISSING VALUES")
    print(df.isnull().sum())

    # Duplicate rows
    print("\n[6] DUPLICATE ROWS")
    print(df.duplicated().sum())

    # First 10 rows
    print("\n[7] FIRST 10 ROWS")
    print(df.head(10).to_string())

    # Last 5 rows
    print("\n[8] LAST 5 ROWS")
    print(df.tail(5).to_string())

print("\n" + "=" * 60)
print("INSPECTION COMPLETED")
print("=" * 60)

