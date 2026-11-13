
import pandas as pd
from pathlib import Path

# 1. File paths
input_file = Path("data/raw/부산_인구이동률_KOSIS.xlsx")
output_dir = Path("data/processed")

output_dir.mkdir(parents=True, exist_ok=True)

# 2. Read Excel
df = pd.read_excel(input_file, sheet_name="데이터")

# 3. Clean column names
df.columns = df.columns.astype(str).str.strip()

# 4. Fill administrative region
df["행정구역(시도)별"] = (
    df["행정구역(시도)별"].ffill()
)

# 5. Convert data types
df["시점"] = pd.to_numeric(df["시점"], errors="coerce")

rate_columns = [
    "총전입률(%)",
    "총전출률(%)",
    "순이동률(%)"
]

for col in rate_columns:
    df[col] = pd.to_numeric(df[col], errors="coerce")

# 6. Remove invalid rows if any
df = df.dropna(subset=["시점"])

df["시점"] = df["시점"].astype(int)

# 7. Save processed CSV
output_file = output_dir / "migration_rate.csv"

df.to_csv(output_file, index=False, encoding="utf-8-sig")

# 8. Validation
print("\n===== CLEANING RESULT =====")
print(df.to_string(index=False))

print("\n===== DATA TYPES =====")
print(df.dtypes)

print("\n===== MISSING VALUES =====")
print(df.isnull().sum())

print("\nSaved to:", output_file)

