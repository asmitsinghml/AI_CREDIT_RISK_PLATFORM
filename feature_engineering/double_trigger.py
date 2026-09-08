from pathlib import Path
import pandas as pd

# 1. PROJECT PATHS

PROJECT_ROOT = Path(__file__).resolve().parents[1]

CACHE_FILE = (
    PROJECT_ROOT
    / "data"
    / "interim"
    / "behavioral"
    / "apc"
    / "apc_base_data.pkl"
)

OUTPUT_DIR = (
    PROJECT_ROOT
    / "data"
    / "interim"
    / "behavioral"
    / "double_trigger"
)

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


# 2. LOAD CACHED DATA

print("=" * 70)
print("DOUBLE TRIGGER")
print("=" * 70)

print("\nLoading cached data...")

df = pd.read_pickle(CACHE_FILE)

print(f"Rows    : {len(df):,}")
print(f"Columns : {len(df.columns)}")


# 3. REQUIRED VARIABLES

print("\n" + "=" * 70)
print("STEP 1 - REQUIRED VARIABLES")
print("=" * 70)

required_columns = [
    "id",
    "time",
    "orig_time",
    "balance_time",
    "balance_orig_time",
    "LTV_time"
]

missing_columns = [
    col for col in required_columns
    if col not in df.columns
]

if missing_columns:

    print("\nMissing columns:")

    for col in missing_columns:
        print(" -", col)

    raise ValueError(
        "Required variables are missing from cached data."
    )

print("\nAll required variables found.")

for col in required_columns:
    print(" -", col)


# 4. EQUITY

print("\n" + "=" * 70)
print("STEP 2 - EQUITY")
print("=" * 70)

# Equity = 1 - LTV / 100

df["Equity"] = 1 - (
    df["LTV_time"] / 100
)

print("\nEquity created.")

print("\nEquity summary:")

print(
    df["Equity"].describe().to_string()
)


# 5. CEP / LIQUIDITY

print("\n" + "=" * 70)
print("STEP 3 - CEP / LIQUIDITY")
print("=" * 70)

# CEP:
# (Scheduled Balance - Actual Balance)
# -------------------------------------
# Scheduled Balance
#
# Using available balance variables:
# balance_orig_time = scheduled/original balance
# balance_time      = actual balance

df["CEP"] = (
    (df["balance_orig_time"] - df["balance_time"])
    / df["balance_orig_time"]
)

# Handle division by zero

df.loc[
    df["balance_orig_time"] == 0,
    "CEP"
] = pd.NA

print("\nCEP created.")

print("\nCEP summary:")

print(
    df["CEP"].describe().to_string()
)


# 6. LIQUIDITY TRIGGER

print("\n" + "=" * 70)
print("STEP 4 - LIQUIDITY TRIGGER")
print("=" * 70)

# Negative CEP = low liquidity

df["Liquidity_Trigger"] = (
    df["CEP"] < 0
).astype(int)

print("\nLiquidity Trigger counts:")

print(
    df["Liquidity_Trigger"]
    .value_counts()
    .sort_index()
)

# 7. EQUITY TRIGGER

print("\n" + "=" * 70)
print("STEP 5 - EQUITY TRIGGER")
print("=" * 70)

# Negative Equity = LTV > 100%

df["Equity_Trigger"] = (
    df["Equity"] < 0
).astype(int)

print("\nEquity Trigger counts:")

print(
    df["Equity_Trigger"]
    .value_counts()
    .sort_index()
)

# 8. DOUBLE TRIGGER

print("\n" + "=" * 70)
print("STEP 6 - DOUBLE TRIGGER")
print("=" * 70)

# Both conditions must be adverse:
#
# 1. Low liquidity
# 2. Negative equity

df["Double_Trigger"] = (
    (df["Liquidity_Trigger"] == 1)
    &
    (df["Equity_Trigger"] == 1)
).astype(int)

print("\nDouble Trigger counts:")

print(
    df["Double_Trigger"]
    .value_counts()
    .sort_index()
)


# 9. TRIGGER COMBINATION SUMMARY

print("\n" + "=" * 70)
print("STEP 7 - TRIGGER COMBINATION SUMMARY")
print("=" * 70)

trigger_summary = (
    df.groupby(
        [
            "Liquidity_Trigger",
            "Equity_Trigger",
            "Double_Trigger"
        ]
    )
    .agg(
        observations=("id", "count"),
        unique_loans=("id", "nunique")
    )
    .reset_index()
)

print("\n")
print(
    trigger_summary.to_string(index=False)
)

# 10. SAVE FEATURES

print("\n" + "=" * 70)
print("STEP 8 - SAVE DOUBLE TRIGGER FEATURES")
print("=" * 70)

output_columns = [
    "id",
    "time",
    "orig_time",
    "balance_time",
    "balance_orig_time",
    "LTV_time",
    "Equity",
    "CEP",
    "Liquidity_Trigger",
    "Equity_Trigger",
    "Double_Trigger"
]

double_trigger_df = df[
    output_columns
].copy()

OUTPUT_FILE = (
    OUTPUT_DIR / "double_trigger_features.csv"
)

double_trigger_df.to_csv(
    OUTPUT_FILE,
    index=False
)

print("\nFeature file saved:")
print(OUTPUT_FILE)


# 11. SAVE SUMMARY

SUMMARY_FILE = (
    OUTPUT_DIR / "double_trigger_summary.csv"
)

trigger_summary.to_csv(
    SUMMARY_FILE,
    index=False
)

print("\nSummary file saved:")
print(SUMMARY_FILE)


# 12. FINAL

print("\n" + "=" * 70)
print("DOUBLE TRIGGER COMPLETED")
print("=" * 70)

print(f"Rows         : {len(double_trigger_df):,}")
print(f"Unique Loans : {double_trigger_df['id'].nunique():,}")

print("=" * 70)