# -*- coding: utf-8 -*-
"""
Tukey‑IQR 地球化学数据质控标记脚本
QC script for geochemical dataset, Tukey 1.5*IQR outlier flag
Only flag candidates, NOT auto‑delete any data
Paper: A geochemical dataset of Early Precambrian rocks from the Eastern Hebei region
"""

import pandas as pd
import numpy as np

# ===================== 配置参数 =====================
INPUT_EXCEL = r"D:\PyProject\daxiongketang\chapter_1\EastHebei_Precambrian_Geochem_Dataset_1.xlsx"
TARGET_SHEET = "Major_Elements"
OUTPUT_FLAGGED = "qc_output_flagged.xlsx"
OUTPUT_SUMMARY = "qc_outlier_summary.xlsx"

ELEMENT_COLS = [
    "SiO2", "TiO2", "Al2O3", "FeOT", "FeO", "Fe2O3T",
    "Fe2O3", "MnO", "MgO", "CaO", "Na2O", "K2O"
]
# 使用实际sheet内的表头
GROUP_COL1 = "Rock name"          # 岩性列
GROUP_COL2 = "Analytical object"  # 分析对象列
MIN_GROUP_N = 5

# ===================== 加载数据 =====================
df_raw = pd.read_excel(INPUT_EXCEL, sheet_name=TARGET_SHEET)

# 生成Excel行号列（表头行1，数据从第2行开始）
df_raw["Excel_Row_Num"] = df_raw.index + 2

# -------- 打印全部列名 --------
print(f"==== 工作表【{TARGET_SHEET}】所有列名 ====")
for col in df_raw.columns:
    print(repr(col))

# 列存在性校验
missing_cols = []
for check_col in [GROUP_COL1, GROUP_COL2]:
    if check_col not in df_raw.columns:
        missing_cols.append(check_col)
if len(missing_cols) > 0:
    raise SystemExit(f"\n❌错误：下列分组列在Major_Elements中不存在：{missing_cols}")


df_out = df_raw.copy()

# 新增输出标记列
flag_cols = []
for elem in ELEMENT_COLS:
    df_out[f"{elem}_IQR_flag"] = ""
    df_out[f"{elem}_group_name"] = ""
    df_out[f"{elem}_group_N"] = np.nan
    df_out[f"{elem}_lower_fence"] = np.nan
    df_out[f"{elem}_upper_fence"] = np.nan
    flag_cols.append(f"{elem}_IQR_flag")

outlier_records = []

# ===================== 逐元素循环质控 =====================
for elem in ELEMENT_COLS:
    print(f"\n==== Processing element: {elem} ====")
    mask_valid = (~df_raw[elem].isna()) & (df_raw[elem] != "<DOL")
    df_valid = df_raw.loc[mask_valid, [GROUP_COL1, GROUP_COL2, elem, "Excel_Row_Num"]].copy()
    df_valid[elem] = pd.to_numeric(df_valid[elem], errors="coerce")
    df_valid = df_valid.dropna(subset=[elem])

    groupobj = df_valid.groupby([GROUP_COL1, GROUP_COL2])

    for (litho, ana_obj), group_df in groupobj:
        group_name = f"{litho} | {ana_obj}"
        n_group = len(group_df)
        idx_origin = group_df.index

        if n_group < MIN_GROUP_N:
            df_out.loc[idx_origin, f"{elem}_IQR_flag"] = "SmallGroup"
            df_out.loc[idx_origin, f"{elem}_group_name"] = group_name
            df_out.loc[idx_origin, f"{elem}_group_N"] = n_group
            continue

        q1 = np.percentile(group_df[elem], 25)
        q3 = np.percentile(group_df[elem], 75)
        iqr = q3 - q1
        lower_fence = q1 - 1.5 * iqr
        upper_fence = q3 + 1.5 * iqr

        df_out.loc[idx_origin, f"{elem}_group_name"] = group_name
        df_out.loc[idx_origin, f"{elem}_group_N"] = n_group
        df_out.loc[idx_origin, f"{elem}_lower_fence"] = np.round(lower_fence, 4)
        df_out.loc[idx_origin, f"{elem}_upper_fence"] = np.round(upper_fence, 4)

        is_out = (group_df[elem] < lower_fence) | (group_df[elem] > upper_fence)
        df_out.loc[idx_origin, f"{elem}_IQR_flag"] = np.where(is_out, "CandidateOutlier", "Normal")

        for idx in group_df.loc[is_out].index:
            row_info = {
                "element": elem,
                "group_name": group_name,
                "group_N": n_group,
                "lower_fence": np.round(lower_fence,4),
                "upper_fence": np.round(upper_fence,4),
                "value": df_raw.loc[idx, elem],
                "excel_row_num": df_raw.loc[idx, "Excel_Row_Num"]
            }
            for c in ["Sample_ID","Reference_No", GROUP_COL1, GROUP_COL2]:
                if c in df_raw.columns:
                    row_info[c] = df_raw.loc[idx, c]
            outlier_records.append(row_info)

# ===================== 输出结果 =====================
df_out.to_excel(OUTPUT_FLAGGED, index=False)
print(f"\n✅ 全量标记结果已保存: {OUTPUT_FLAGGED}")

df_summary = pd.DataFrame(outlier_records)
df_summary.to_excel(OUTPUT_SUMMARY, index=False)
print(f"✅ 异常值候选汇总已保存: {OUTPUT_SUMMARY}")
print(f"总异常候选记录数: {len(df_summary)}")
print("\n注意：所有候选异常值必须对照原始文献人工核查，脚本不会自动删除任何数据。")
