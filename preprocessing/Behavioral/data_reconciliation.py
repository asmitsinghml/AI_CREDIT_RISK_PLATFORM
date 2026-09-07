import pandas as pd
import os

# ============================================================
# PATHS
# ============================================================

file_path = r"data/raw/Behavioral/Final_scorecard_1_Data check.xlsm"

output_dir = r"data/interim/behavioral"

os.makedirs(output_dir, exist_ok=True)


# ============================================================
# LOAD RAW DATA - ONLY ONCE
# ============================================================

print("\nLoading original Excel file...")
print("This may take some time because the file is very large.\n")

df = pd.read_excel(
    file_path,
    sheet_name="Reconciliation",
    engine="openpyxl"
)

print("Raw data loaded successfully.")
print("Raw rows:", len(df))


# ============================================================
# KEEP ONLY REQUIRED SOURCE COLUMNS
# ============================================================

required_columns = [
    "id",
    "time",
    "orig_time",
    "first_time",
    "mat_time",
    "balance_time",
    "balance_orig_time",
    "LTV_time",
    "default_time",
    "payoff_time",
    "status_time",
    "status_check"
]

df = df[required_columns].copy()

print("Columns selected successfully.")


# ============================================================
# CHECK 1
# time >= first_time
# ============================================================

print("\n" + "=" * 60)
print("CHECK 1: time >= first_time")
print("=" * 60)

failed_rows_1 = df[
    df["time"] < df["first_time"]
]

failed_ids_1 = failed_rows_1["id"].unique()

print("CHECK 1 failed IDs:", len(failed_ids_1))

# Remove ALL rows belonging to failed IDs
df_check1_clean = df[
    ~df["id"].isin(failed_ids_1)
].copy()

print("Rows before CHECK 1:", len(df))
print("Rows after CHECK 1:", len(df_check1_clean))
print("Rows removed:", len(df) - len(df_check1_clean))

if len(failed_ids_1) == 0:
    print("CHECK 1 PASSED.")
else:
    print("CHECK 1 FAILED - Failed IDs removed.")

# Save Check 1 output
check1_path = os.path.join(
    output_dir,
    "check1_clean.csv"
)

df_check1_clean.to_csv(
    check1_path,
    index=False
)

print("CHECK 1 output saved:", check1_path)


# ============================================================
# CHECK 2
# first_time >= orig_time
# ============================================================

print("\n" + "=" * 60)
print("CHECK 2: first_time >= orig_time")
print("=" * 60)

# IMPORTANT:
# Check 2 runs on Check 1 cleaned data

df_check2 = df_check1_clean.copy()

failed_rows_2 = df_check2[
    df_check2["first_time"] < df_check2["orig_time"]
]

failed_ids_2 = failed_rows_2["id"].unique()

print("CHECK 2 failed IDs:", len(failed_ids_2))

# Remove ALL rows belonging to failed IDs
df_check2_clean = df_check2[
    ~df_check2["id"].isin(failed_ids_2)
].copy()

print("Rows before CHECK 2:", len(df_check2))
print("Rows after CHECK 2:", len(df_check2_clean))
print("Rows removed:", len(df_check2) - len(df_check2_clean))

if len(failed_ids_2) == 0:
    print("CHECK 2 PASSED.")
else:
    print("CHECK 2 FAILED - Failed IDs removed.")

# Save Check 2 output
check2_path = os.path.join(
    output_dir,
    "check2_clean.csv"
)

df_check2_clean.to_csv(
    check2_path,
    index=False
)

print("CHECK 2 output saved:", check2_path)


# ============================================================
# CHECK 3
# orig_time < mat_time
# ============================================================

print("\n" + "=" * 60)
print("CHECK 3: orig_time < mat_time")
print("=" * 60)

# IMPORTANT:
# Check 3 runs on Check 2 cleaned data

df_check3 = df_check2_clean.copy()

failed_rows_3 = df_check3[
    df_check3["orig_time"] >= df_check3["mat_time"]
]

failed_ids_3 = failed_rows_3["id"].unique()

print("CHECK 3 failed IDs:", len(failed_ids_3))

# Remove ALL rows belonging to failed IDs
df_check3_clean = df_check3[
    ~df_check3["id"].isin(failed_ids_3)
].copy()

print("Rows before CHECK 3:", len(df_check3))
print("Rows after CHECK 3:", len(df_check3_clean))
print("Rows removed:", len(df_check3) - len(df_check3_clean))

if len(failed_ids_3) == 0:
    print("CHECK 3 PASSED.")
else:
    print("CHECK 3 FAILED - Failed IDs removed.")

# Save Check 3 output
check3_path = os.path.join(
    output_dir,
    "check3_clean.csv"
)

df_check3_clean.to_csv(
    check3_path,
    index=False
)

print("CHECK 3 output saved:", check3_path)


# ============================================================
# CHECK 4
# balance_time <= balance_orig_time
# ============================================================

print("\n" + "=" * 60)
print("CHECK 4: balance_time <= balance_orig_time")
print("=" * 60)

# IMPORTANT:
# Check 4 runs on Check 3 cleaned data

df_check4 = df_check3_clean.copy()

failed_rows_4 = df_check4[
    df_check4["balance_time"] > df_check4["balance_orig_time"]
]

failed_ids_4 = failed_rows_4["id"].unique()

print("CHECK 4 failed IDs:", len(failed_ids_4))

# Remove ALL rows belonging to failed IDs
df_check4_clean = df_check4[
    ~df_check4["id"].isin(failed_ids_4)
].copy()

print("Rows before CHECK 4:", len(df_check4))
print("Rows after CHECK 4:", len(df_check4_clean))
print("Rows removed:", len(df_check4) - len(df_check4_clean))

if len(failed_ids_4) == 0:
    print("CHECK 4 PASSED.")
else:
    print("CHECK 4 FAILED - Failed IDs removed.")

# Save Check 4 output
check4_path = os.path.join(
    output_dir,
    "check4_clean.csv"
)

df_check4_clean.to_csv(
    check4_path,
    index=False
)

print("CHECK 4 output saved:", check4_path)


# ============================================================
# FINAL SUMMARY
# ============================================================

print("\n" + "=" * 60)
print("DATA RECONCILIATION SUMMARY")
print("=" * 60)

print("Original rows :", len(df))
print("After Check 1 :", len(df_check1_clean))
print("After Check 2 :", len(df_check2_clean))
print("After Check 3 :", len(df_check3_clean))
print("After Check 4 :", len(df_check4_clean))

print("\nIDs removed:")
print("Check 1:", len(failed_ids_1))
print("Check 2:", len(failed_ids_2))
print("Check 3:", len(failed_ids_3))
print("Check 4:", len(failed_ids_4))

print("\nFinal cleaned dataset:")
print(check4_path)

print("\nCHECK 1-4 COMPLETED SUCCESSFULLY.")
print("CHECK 5 will be implemented after verifying its exact Excel logic.")



# ============================================================
# CHECK 4 VERIFICATION AGAINST EXCEL
# ============================================================

print("\n" + "=" * 60)
print("CHECK 4 VERIFICATION AGAINST EXCEL")
print("=" * 60)

# Read only the columns required for verification
df_excel_check4 = pd.read_excel(
    file_path,
    sheet_name="Reconciliation",
    engine="openpyxl",
    usecols=[
        "id",
        "balance_time",
        "balance_orig_time",
        "CHECK 4"
    ]
)

# ------------------------------------------------------------
# Python CHECK 4
# ------------------------------------------------------------

df_excel_check4["python_check4"] = (
    df_excel_check4["balance_time"]
    <= df_excel_check4["balance_orig_time"]
).astype(int)

# ------------------------------------------------------------
# Compare Excel CHECK 4 with Python CHECK 4
# ------------------------------------------------------------

comparison = (
    df_excel_check4["CHECK 4"]
    == df_excel_check4["python_check4"]
)

mismatch_count = (~comparison).sum()

print("Total rows checked:", len(df_excel_check4))
print("CHECK 4 mismatched rows:", mismatch_count)

if mismatch_count == 0:
    print("\nCHECK 4 VERIFICATION PASSED.")
    print("Excel CHECK 4 and Python CHECK 4 are exactly matching.")
else:
    print("\nCHECK 4 VERIFICATION FAILED.")
    print("Excel and Python CHECK 4 are different.")

    print("\nFirst 20 mismatched rows:")
    print(
        df_excel_check4.loc[
            ~comparison
        ].head(20)
    )


# ------------------------------------------------------------
# Compare failed IDs
# ------------------------------------------------------------

excel_failed_ids = set(
    df_excel_check4.loc[
        df_excel_check4["CHECK 4"] == 0,
        "id"
    ].unique()
)

python_failed_ids = set(
    df_excel_check4.loc[
        df_excel_check4["python_check4"] == 0,
        "id"
    ].unique()
)

print("\nExcel failed IDs :", len(excel_failed_ids))
print("Python failed IDs:", len(python_failed_ids))

if excel_failed_ids == python_failed_ids:
    print("FAILED ID VERIFICATION PASSED.")
    print("Excel and Python have the same failed IDs.")
else:
    print("FAILED ID VERIFICATION FAILED.")

    print(
        "IDs only in Excel:",
        len(excel_failed_ids - python_failed_ids)
    )

    print(
        "IDs only in Python:",
        len(python_failed_ids - excel_failed_ids)
    )
    
    
    # ============================================================
# CHECK 5: STATUS TIME PROPERLY GENERATED
# ============================================================

print("\n" + "=" * 60)
print("CHECK 5: status_time properly generated")
print("=" * 60)

# Check 5 runs on Check 4 cleaned data
df_check5 = df_check4_clean.copy()

# ------------------------------------------------------------
# Generate expected status
# ------------------------------------------------------------

df_check5["status_check_python"] = 0

# Default = 1
df_check5.loc[
    df_check5["default_time"] > 0,
    "status_check_python"
] = 1

# Paid off = 2
df_check5.loc[
    df_check5["payoff_time"] > 0,
    "status_check_python"
] = 2

# ------------------------------------------------------------
# Compare with actual status_time
# ------------------------------------------------------------

df_check5["check5_result"] = (
    df_check5["status_time"]
    == df_check5["status_check_python"]
).astype(int)

failed_rows_5 = df_check5[
    df_check5["check5_result"] == 0
]

failed_ids_5 = failed_rows_5["id"].unique()

print("CHECK 5 failed IDs:", len(failed_ids_5))
print("CHECK 5 failed rows:", len(failed_rows_5))

# ------------------------------------------------------------
# IMPORTANT
# Do NOT remove IDs yet.
# First verify against Excel.
# ------------------------------------------------------------

print("\nCHECK 5 calculation completed.")

# Save Check 5 verification file
check5_path = os.path.join(
    output_dir,
    "check5_verification.csv"
)

df_check5.to_csv(
    check5_path,
    index=False
)

print("CHECK 5 verification saved:", check5_path)


# ============================================================
# CHECK 5 VERIFICATION AGAINST EXCEL
# ============================================================

print("\n" + "=" * 60)
print("CHECK 5 VERIFICATION AGAINST EXCEL")
print("=" * 60)

df_excel_check5 = pd.read_excel(
    file_path,
    sheet_name="Reconciliation",
    engine="openpyxl",
    usecols=[
        "id",
        "status_time",
        "status_check",
        "CHECK 5"
    ]
)

# Excel CHECK 5 should be 1 when status_time = status_check
df_excel_check5["python_check5"] = (
    df_excel_check5["status_time"]
    == df_excel_check5["status_check"]
).astype(int)

# Compare Excel CHECK 5 with Python
comparison_5 = (
    df_excel_check5["CHECK 5"]
    == df_excel_check5["python_check5"]
)

mismatch_count_5 = (~comparison_5).sum()

print("Total rows checked:", len(df_excel_check5))
print("CHECK 5 mismatched rows:", mismatch_count_5)

if mismatch_count_5 == 0:
    print("\nCHECK 5 VERIFICATION PASSED.")
    print("Excel CHECK 5 and Python CHECK 5 match exactly.")
else:
    print("\nCHECK 5 VERIFICATION FAILED.")

    print("\nFirst 20 mismatched rows:")
    print(
        df_excel_check5.loc[
            ~comparison_5
        ].head(20)
    )


# ============================================================
# FAILED ID COMPARISON
# ============================================================

excel_failed_ids_5 = set(
    df_excel_check5.loc[
        df_excel_check5["CHECK 5"] == 0,
        "id"
    ].unique()
)

python_failed_ids_5 = set(
    df_excel_check5.loc[
        df_excel_check5["python_check5"] == 0,
        "id"
    ].unique()
)

print("\nExcel failed IDs :", len(excel_failed_ids_5))
print("Python failed IDs:", len(python_failed_ids_5))

if excel_failed_ids_5 == python_failed_ids_5:
    print("FAILED ID VERIFICATION PASSED.")
    print("Excel and Python have the same failed IDs.")
else:
    print("FAILED ID VERIFICATION FAILED.")

    print(
        "IDs only in Excel:",
        len(excel_failed_ids_5 - python_failed_ids_5)
    )

    print(
        "IDs only in Python:",
        len(python_failed_ids_5 - excel_failed_ids_5)
    )