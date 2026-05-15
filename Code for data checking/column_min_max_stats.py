import pandas as pd
import os
import numpy as np

def load_excel():
    print("===== Column Min/Max Statistics =====")
    while True:
        path = input('Please enter Excel file path: ').strip().strip('"\'')
        if os.path.exists(path):
            try:
                df = pd.read_excel(path)
                print(f"✅ Loaded successfully. Total columns: {len(df.columns)}")
                return df
            except Exception as e:
                print(f"❌ Read failed: {e}")
        else:
            print("❌ File not found.")

def min_max_stats():
    df = load_excel()
    out = []

    # 遍历所有列，而不是只取数值列（修复核心问题）
    for col in df.columns:
        col_data = pd.to_numeric(df[col], errors='coerce')  # 强制转数字，无法转的变为NaN
        min_val = col_data.min()
        max_val = col_data.max()
        valid_count = col_data.dropna().shape[0]

        out.append({
            "Column": col,
            "Min": min_val,
            "Max": max_val,
            "Valid Numeric Values": valid_count,
            "Dtype": str(df[col].dtype)
        })

    # 导出所有列的最大最小值
    pd.DataFrame(out).to_excel("Min_Max_Statistics.xlsx", index=False)
    print(f"\n✅ All columns' min/max calculated successfully!")
    print(f"✅ Result saved to Min_Max_Statistics.xlsx")
    print(f"📊 Total columns processed: {len(out)}")

if __name__ == "__main__":
    min_max_stats()