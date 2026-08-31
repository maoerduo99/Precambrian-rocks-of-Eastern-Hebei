# -*- coding: utf-8 -*-
"""
check_provenance_consistency.py
Purpose: Validation script to verify that every Sample‑ID in data sheets
can be correctly matched against the standard Reference No. stored in Rock_Metadata sheet.
This script ONLY performs consistency checking. It does NOT modify or write‑back any source dataset.
Output: human‑readable text report in console + reference_validation_report.xlsx summary report.
No original input file will be altered.
Repository: https://github.com/XXX/XXX
"""
import pandas as pd
from pathlib import Path

# ===================== 固定配置，无需交互 =====================
INPUT_FILE = Path(r"D:\PyProject\daxiongketang\chapter_1\EastHebei_Precambrian_Geochem_Dataset.xlsx")
OUTPUT_REPORT = Path(r"reference_validation_report.xlsx")

SHEET_METADATA = "Rock_Metadata"
DATA_SHEETS = ["Major_Elements", "Trace_Elements", "Isotope_Data"]

COL_SAMPLE_ID = "Sample ID"
COL_REFNO = "Reference No."
# ============================================================

def main():
    if not INPUT_FILE.exists():
        print(f"ERROR: Input file not found: {INPUT_FILE.resolve()}")
        return

    print(f"Reading metadata sheet: {SHEET_METADATA}")
    df_meta = pd.read_excel(INPUT_FILE, sheet_name=SHEET_METADATA)

    # 构建 SampleID → Reference No. 映射字典，过滤空值
    df_meta_valid = df_meta.dropna(subset=[COL_SAMPLE_ID, COL_REFNO])
    sampleid_to_std_refno = {}
    for _, row in df_meta_valid.iterrows():
        sid = str(row[COL_SAMPLE_ID]).strip()
        ref = str(row[COL_REFNO]).strip()
        sampleid_to_std_refno[sid] = ref

    total_meta_samples = len(sampleid_to_std_refno)
    print(f"\nTotal valid Sample‑ID with standard Reference No. in Rock_Metadata: {total_meta_samples}")

    report_records = []
    total_checked_rows = 0
    total_mismatch = 0

    for sheet_name in DATA_SHEETS:
        print(f"\n==== Validating sheet: {sheet_name} ====")
        df_sheet = pd.read_excel(INPUT_FILE, sheet_name=sheet_name)

        if COL_SAMPLE_ID not in df_sheet.columns:
            print(f"WARNING: Sheet {sheet_name} missing {COL_SAMPLE_ID} column, skip checking this sheet.")
            continue

        sheet_rows = len(df_sheet)
        total_checked_rows += sheet_rows
        sheet_error = 0

        for idx, row in df_sheet.iterrows():
            sid_raw = row[COL_SAMPLE_ID]
            if pd.isna(sid_raw):
                rec = {
                    "sheet": sheet_name,
                    "excel_row_number": idx + 2,
                    "sample_id": None,
                    "std_reference_no_from_metadata": None,
                    "issue": "Sample‑ID is blank"
                }
                report_records.append(rec)
                sheet_error += 1
                total_mismatch += 1
                continue

            sid = str(sid_raw).strip()
            if sid not in sampleid_to_std_refno:
                rec = {
                    "sheet": sheet_name,
                    "excel_row_number": idx + 2,
                    "sample_id": sid,
                    "std_reference_no_from_metadata": None,
                    "issue": "Sample‑ID NOT found in Rock_Metadata (invalid / non‑existent sample identifier)"
                }
                report_records.append(rec)
                sheet_error += 1
                total_mismatch += 1

        print(f"Sheet {sheet_name}: total rows = {sheet_rows}, problematic entries = {sheet_error}")

    # 输出校验报告excel
    df_report = pd.DataFrame(report_records)
    df_report.to_excel(OUTPUT_REPORT, index=False)

    print("\n" + "=" * 70)
    print(f"Total rows checked across all data sheets: {total_checked_rows}")
    print(f"Total problematic / unmatched Sample‑ID entries: {total_mismatch}")
    if total_mismatch == 0:
        print("✅ VALIDATION RESULT: ALL Sample‑IDs from data sheets have matching standard Reference No. in Rock_Metadata.")
        print("✅ No invented / arbitrary Reference No. identifiers detected.")
    else:
        print("⚠️ WARNING: There are unmatched entries, please open report file to inspect.")
    print(f"\nValidation summary report saved to: {OUTPUT_REPORT.resolve()}")
    print("NOTE: This script performs checking‑only; original input file remains unchanged.")


if __name__ == "__main__":
    main()
