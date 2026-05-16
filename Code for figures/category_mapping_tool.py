import pandas as pd
import warnings

warnings.filterwarnings("ignore")


def read_file(path):
    if path.lower().endswith(".csv"):
        return pd.read_csv(path)
    else:
        return pd.read_excel(path)


def main():
    print("===== Step 1: Enter path for reference table (contains small + large categories) =====")
    ref_path = input("Enter reference table file path: ").strip()
    print("\n===== Step 2: Enter path for target table (only small category needed) =====")
    target_path = input("Enter target table file path: ").strip()

    try:
        df_ref = read_file(ref_path)
        df_target = read_file(target_path)
        print(f"\n✅ Reference table loaded: {df_ref.shape[0]} rows")
        print(f"✅ Target table loaded: {df_target.shape[0]} rows")
    except Exception as e:
        print(f"❌ Failed to load file: {e}")
        return

    print("\n=====================================")
    print("📋 All columns in reference table:")
    print(list(df_ref.columns))

    print("\n📋 All columns in target table:")
    print(list(df_target.columns))
    print("=====================================\n")

    ref_small_col = input("Reference table - Small category column name: ").strip()
    ref_big_col = input("Reference table - Large category column name: ").strip()
    target_small_col = input("Target table - Small category column name: ").strip()

    if not all(c in df_ref.columns for c in [ref_small_col, ref_big_col]):
        print("❌ Specified columns not found in reference table!")
        return
    if target_small_col not in df_target.columns:
        print("❌ Specified small category column not found in target table!")
        return

    df_ref_valid = df_ref.dropna(subset=[ref_small_col])
    map_dict = dict(zip(df_ref_valid[ref_small_col].astype(str).str.strip(),
                        df_ref_valid[ref_big_col]))

    df_out = df_target.copy()
    target_small_series = df_out[target_small_col].astype(str).str.strip()
    df_out["Matched_Large_Category"] = target_small_series.map(map_dict)

    df_unmatch = df_out[df_out["Matched_Large_Category"].isna()].copy()
    df_unmatch["Original_Row_Number"] = df_unmatch.index + 2
    df_unmatch_res = pd.DataFrame({
        "Unmatched_Small_Category": df_unmatch[target_small_col],
        "Original_Row_Number": df_unmatch["Original_Row_Number"]
    })

    out1 = df_out[[target_small_col, "Matched_Large_Category"]].copy()
    out1.columns = ["Small_Category", "Large_Category"]
    out1.to_excel("Small_to_Large_Category_Mapping.xlsx", index=False)

    df_unmatch_res.to_excel("Unmatched_Small_Categories.xlsx", index=False)

    total = len(df_out)
    match_num = df_out["Matched_Large_Category"].notna().sum()
    unmatch_num = total - match_num

    print(f"\n===================== Statistics =====================")
    print(f"📊 Total small categories to match: {total}")
    print(f"✅ Successfully matched: {match_num} entries")
    print(f"❌ Unmatched: {unmatch_num} entries")
    print(f"\n📁 Two files generated:")
    print("1. Small_to_Large_Category_Mapping.xlsx (original order preserved)")
    print("2. Unmatched_Small_Categories.xlsx (includes name + original row number)")


if __name__ == "__main__":
    main()