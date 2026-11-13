
import pandas as pd
from pathlib import Path

RAW_DIR = Path("data/raw")

for file in RAW_DIR.glob("*.xlsx"):

    print("\n" + "=" * 70)
    print("FILE:", file.name)
    print("=" * 70)

    excel = pd.ExcelFile(file)

    for sheet in excel.sheet_names:

        if sheet != "데이터":
            continue

        df = pd.read_excel(file, sheet_name=sheet, header=None)

        print(f"\nSHEET: {sheet}")
        print("\n--- FIRST 15 ROWS ---")
        print(df.head(15).to_string(index=False))

        print("\n--- NON-EMPTY COUNTS ---")
        print(df.notna().sum())

        print("\n--- UNIQUE VALUES (FIRST 3 COLUMNS) ---")
        for col in df.columns[:3]:
            print(f"Column {col}:")
            print(df[col].dropna().unique()[:15])
