
import pandas as pd

# 1. Load raw data
input_file = "data/raw/주간_아파트_매매가격지수_KOSIS.xlsx"

df = pd.read_excel(input_file, sheet_name="데이터", header=0)

# 2. Rename columns
df.columns = ["date", "busan_apartment_price_index"]

# 3. Clean date column
df["date"] = pd.to_datetime(
    df["date"].astype(str),
    format="%Y.%m.%d",
    errors="coerce"
)

# 4. Convert price index to numeric
df["busan_apartment_price_index"] = pd.to_numeric(
    df["busan_apartment_price_index"],
    errors="coerce"
)

# 5. Remove invalid rows
df = df.dropna()

# 6. Sort by date
df = df.sort_values("date")

# 7. Save cleaned CSV
output_file = "data/processed/apartment_price.csv"

df.to_csv(output_file, index=False, encoding="utf-8-sig")

# 8. Check result
print("===== CLEANING RESULT =====")
print("Shape:", df.shape)
print("Missing Values:", df.isnull().sum().sum())
print("Duplicate Rows:", df.duplicated().sum())
print(df.head())
print(df.tail())

print("\nSaved:", output_file)
