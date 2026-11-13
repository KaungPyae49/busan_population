
import pandas as pd
from pathlib import Path

# 1. File paths
input_file = Path("data/raw/전입사유별_이동자수_KOSIS.xlsx")
output_dir = Path("data/processed")

output_dir.mkdir(parents=True, exist_ok=True)

# 2. Read Excel
df = pd.read_excel(input_file, sheet_name="데이터")

# 3. Clean column names
df.columns = df.columns.astype(str).str.strip()

# 4. Fill hierarchical labels
label_columns = [
    "행정구역(시군구)별",
    "전입사유별",
    "항목"
]

for col in label_columns:
    df[col] = df[col].ffill()

# 5. Convert year columns to numeric
year_columns = [
    col for col in df.columns
    if str(col).isdigit()
]

for col in year_columns:
    df[col] = pd.to_numeric(df[col], errors="coerce")

# 6. Save processed CSV
output_file = output_dir / "migration_reason.csv"

df.to_csv(output_file, index=False, encoding="utf-8-sig")

# 7. Validation
print("\n===== CLEANING RESULT =====")
print(df.to_string(index=False))

print("\n===== DATA TYPES =====")
print(df.dtypes)

print("\n===== MISSING VALUES =====")
print(df.isnull().sum())

print("\nSaved to:", output_file)
