import pandas as pd
import os

def load_excel():
    print("===== Column Value Frequency Count =====")
    while True:
        path = input('Please enter Excel file path: ').strip().strip('"\'')
        if os.path.exists(path):
            try:
                df = pd.read_excel(path)
                print(f"✅ Loaded successfully.")
                return df
            except Exception as e:
                print(f"❌ Read failed: {e}")
        else:
            print("❌ File not found.")

def freq_count():
    df = load_excel()
    print("\n===== Value Frequency =====")
    start = int(input("Start column index: "))
    end = int(input("End column index: "))
    subset = df.iloc[:, start:end+1]
    all_freq = []

    for col in subset.columns:
        freq = subset[col].value_counts(dropna=False).reset_index()
        freq.columns = ["Value", "Count"]
        freq["Column"] = col
        all_freq.append(freq)

    if all_freq:
        pd.concat(all_freq, ignore_index=True).to_excel("Value_Frequency_Result.xlsx", index=False)
        print("✅ Frequency result saved to Value_Frequency_Result.xlsx")
    else:
        print("✅ No data to count.")

if __name__ == "__main__":
    freq_count()