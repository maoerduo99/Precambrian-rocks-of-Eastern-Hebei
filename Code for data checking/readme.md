1. Overview

This toolkit contains 4 independent Python scripts for data quality control of Excel-based geochemical/geological datasets. All scripts run independently.
All functions are designed for:(1)Non‑numeric cell detection; (2)Null value checking (with row location); (3)Full‑column min/max statistics;(4)Column value frequency counting.

2. File List & Functions

| Script Name | Function | Output File |
|-------------|----------|-------------|
| check_non_numeric_cells.py | Detect non-numeric cells in specified column range | Non_numeric_Check_Result.xlsx |
| check_null_values.py | Count null values and locate exact row numbers of nulls | Null_Check_Report.xlsx<br>Null_Value_Locations.xlsx |
| column_min_max_stats.py | Calculate min/max values for all columns | Min_Max_Statistics.xlsx |
| column_value_frequency.py | Count value frequency in specified column range | Value_Frequency_Result.xlsx |
| major_check.py | geochemical quality control, applying Tukey 1.5×IQR rule | qc_output_flagged.xlsx |
