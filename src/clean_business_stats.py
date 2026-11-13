
import pandas as pd
from pathlib import Path

# 1. Load original Excel
input_path = Path("data/raw/사업체수__종사자수_KOSIS.xlsx")
output_path = Path("data/processed/사업체수__종사자수.csv")

df = pd.read_excel(
    input_path,
    sheet_name="데이터",
    header=None
)

# 2. Remove 3 header rows
clean = df.iloc[3:, :10].copy()

# 3. Fill business type
clean[0] = clean[0].ffill()

# 4. Rename columns
clean.columns = [
    "business_type",
    "industry",
    "2020_establishments",
    "2020_employees",
    "2021_establishments",
    "2021_employees",
    "2022_establishments",
    "2022_employees",
    "2023_establishments",
    "2023_employees"
]

# 5. Preserve X and convert numeric values
for col in clean.columns[2:]:
    clean[col] = clean[col].apply(
        lambda x: int(x) if pd.notna(x) and str(x).isdigit() else x
    )

# 6. Reset index
clean = clean.reset_index(drop=True)

# 7. Save CSV
output_path.parent.mkdir(parents=True, exist_ok=True)

clean.to_csv(
    output_path,
    index=False,
    encoding="utf-8-sig"
)

print("===== CLEANING RESULT =====")
print("Shape:", clean.shape)
print("Missing Values:", clean.isna().sum().sum())
print("Duplicate Rows:", clean.duplicated().sum())
print("Suppressed Values (X):", clean.eq("X").sum().sum())
print(clean.head(10).to_string(index=False))
print("Saved:", output_path)
