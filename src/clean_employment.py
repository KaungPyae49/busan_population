
import pandas as pd
from pathlib import Path

# 1. File paths
input_file = Path("data/raw/부산_연령별_취업자_및_고용률__KOSIS.xlsx")
output_dir = Path("data/processed")

output_dir.mkdir(parents=True, exist_ok=True)

# 2. Read Excel
df = pd.read_excel(input_file, sheet_name="데이터")

# 3. Clean column names
df.columns = df.columns.astype(str).str.strip()

# 4. Fill hierarchical labels
label_columns = [
    "행정구역별",
    "항목",
    "연령별"
]

for col in label_columns:
    df[col] = df[col].ffill()

# 5. Identify period columns
period_columns = [
    col for col in df.columns
    if col not in label_columns
]

# 6. Convert values to numeric
for col in period_columns:
    df[col] = pd.to_numeric(
        df[col].astype(str).str.replace(",", "", regex=False),
        errors="coerce"
    )

# 7. Save processed CSV
output_file = output_dir / "employment.csv"

df.to_csv(output_file, index=False, encoding="utf-8-sig")

# 8. Validation
print("\n===== CLEANING RESULT =====")
print(df.to_string(index=False))

print("\n===== DATA TYPES =====")
print(df.dtypes)

print("\n===== MISSING VALUES =====")
print(df.isnull().sum())

print("\n===== DATA SHAPE =====")
print(df.shape)

print("\nSaved to:", output_file)
