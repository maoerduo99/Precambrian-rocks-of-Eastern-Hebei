import pandas as pd
import os

def load_excel():
    print("===== Null Value Check Tool =====")
    while True:
        path = input('Please enter Excel file path: ').strip().strip('"\'')
        if os.path.exists(path):
            try:
                df = pd.read_excel(path)
                print(f"✅ Loaded successfully. Columns: {list(df.columns)}")
                return df
            except Exception as e:
                print(f"❌ Read failed: {e}")
        else:
            print("❌ File not found.")

def check_null():
    df = load_excel()
    print("\n===== Null Value Check =====")
    cols_input = input("Enter columns to check (split by comma): ")
    target_cols = [c.strip() for c in cols_input.split(",") if c.strip()]
    valid = [c for c in target_cols if c in df.columns]

    if not valid:
        print("❌ No valid columns.")
        return

    # ===================== 1. 空值统计（原功能保留）=====================
    res = []
    total = len(df)
    for col in valid:
        cnt = df[col].isnull().sum()
        pct = f"{cnt/total*100:.2f}%" if total>0 else "0%"
        has_null = "Yes" if cnt>0 else "No"
        res.append([col, total, cnt, pct, has_null])
        print(f"📌 {col}: total={total}, null={cnt}, %={pct}, has_null={has_null}")

    pd.DataFrame(res, columns=["Column", "TotalRows", "NullCount", "NullPercent", "HasNull"]).to_excel("Null_Check_Report.xlsx", index=False)

    # ===================== 2. 新增：定位所有空值的行号（核心改进）=====================
    null_locations = []
    for col in valid:
        null_rows = df[df[col].isnull()].index.tolist()
        for row_idx in null_rows:
            null_locations.append({
                "Column Name": col,
                "Row Number (Excel)": row_idx + 2,  # Excel真实行号（对应行+2）
                "Issue": "Null value"
            })

    if null_locations:
        pd.DataFrame(null_locations).to_excel("Null_Value_Locations.xlsx", index=False)
        print(f"\n✅ Total null positions found: {len(null_locations)}")
        print("✅ Null row locations saved to: Null_Value_Locations.xlsx")
    else:
        print("\n✅ No null values in selected columns.")

    print("\n🎉 All results saved successfully!")

if __name__ == "__main__":
    check_null()