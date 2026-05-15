import pandas as pd
import numpy as np
import os

def load_excel():
    print("===== Non-numeric Cell Check Tool =====")
    while True:
        path = input('Please enter Excel file path: ').strip().strip('"\'')
        if os.path.exists(path):
            try:
                df = pd.read_excel(path)
                print(f"✅ Loaded successfully. Rows: {df.shape[0]}, Columns: {df.shape[1]}")
                return df
            except Exception as e:
                print(f"❌ Read failed: {e}")
        else:
            print("❌ File not found.")

def check_non_numeric():
    df = load_excel()
    print("\n===== Start Checking Non-numeric Cells =====")
    try:
        start = int(input("Enter start column index: "))
        end = int(input("Enter end column index: "))
        subset = df.iloc[:, start:end+1]
        errors = []

        for col_idx, col in enumerate(subset.columns, start):
            for row_idx, val in enumerate(subset[col]):
                if pd.isna(val):
                    continue
                if not isinstance(val, (int, float, np.number)):
                    errors.append({
                        "Row": row_idx + 1,
                        "Column Index": col_idx,
                        "Column Name": col,
                        "Value": val,
                        "Issue": "Non-numeric"
                    })

        if errors:
            pd.DataFrame(errors).to_excel("Non_numeric_Check_Result.xlsx", index=False)
            print(f"✅ Found {len(errors)} issues. Saved to Non_numeric_Check_Result.xlsx")
        else:
            print("✅ No non-numeric cells found.")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    check_non_numeric()