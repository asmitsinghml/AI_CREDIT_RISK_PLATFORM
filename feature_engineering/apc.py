from pathlib import Path
import pandas as pd

# 1. PROJECT PATHS

PROJECT_ROOT = Path(__file__).resolve().parents[1]

RAW_FILE = (
    PROJECT_ROOT
    / "data"
    / "raw"
    / "Behavioral"
    / "Final_scorecard_1_Data check.xlsm"
)

OUTPUT_DIR = (
    PROJECT_ROOT
    / "data"
    / "interim"
    / "behavioral"
    / "apc"
)

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

CACHE_FILE = OUTPUT_DIR / "apc_base_data.pkl"


# 2. REQUIRED RAW VARIABLES

usecols = [
    "id",
    "time",
    "orig_time",
    "first_time",
    "mat_time",
    "balance_time",
    "balance_orig_time",
    "LTV_time",
    "interest_rate_time",
    "rate_time",
    "hpi_time",
    "gdp_time",
    "uer_time",
    "default_time",
    "status_time"
]


# 3. LOAD DATA / CACHE

print("=" * 70)
print("APC FEATURE ENGINEERING")
print("=" * 70)

if CACHE_FILE.exists():

    print("\nChecking cached data...")

    df = pd.read_pickle(CACHE_FILE)

    required_cache_columns = [
        "balance_time",
        "balance_orig_time",
        "LTV_time"
    ]

    if all(col in df.columns for col in required_cache_columns):

        print("Updated cache found.")
        print("Loading cached data...")

    else:

        print("\nOld cache detected.")
        print("Reloading Excel with updated variables...")
        print("This may take some time...")

        df = pd.read_excel(
            RAW_FILE,
            sheet_name="Reconciliation",
            engine="openpyxl",
            usecols=usecols
        )

        df.to_pickle(CACHE_FILE)

        print("Updated cache saved.")

else:

    print("\nFirst run: Loading Excel...")
    print("This may take some time...")

    df = pd.read_excel(
        RAW_FILE,
        sheet_name="Reconciliation",
        engine="openpyxl",
        usecols=usecols
    )

    print("Excel loaded.")

    print("\nSaving cache...")

    df.to_pickle(CACHE_FILE)

    print("Cache saved.")


print(f"\nRows    : {len(df):,}")
print(f"Columns : {len(df.columns)}")

# 4. AGE / MOB

print("\n" + "=" * 70)
print("STEP 1 - AGE / MOB")
print("=" * 70)

df["MOB"] = df["time"] - df["orig_time"]

df["MOB_squared"] = df["MOB"] ** 2

print(f"Minimum MOB : {df['MOB'].min()}")
print(f"Maximum MOB : {df['MOB'].max()}")

negative_mob = (df["MOB"] < 0).sum()

print(f"Negative MOB records : {negative_mob:,}")


# 5. COHORT / VINTAGE

print("\n" + "=" * 70)
print("STEP 2 - COHORT / VINTAGE")
print("=" * 70)


def create_vintage(orig_time):

    if orig_time <= 0:
        return 0

    elif orig_time <= 12:
        return 1

    elif orig_time <= 24:
        return 2

    elif orig_time <= 36:
        return 3

    elif orig_time <= 48:
        return 4

    else:
        return 5


df["Vintage"] = df["orig_time"].apply(create_vintage)


vintage_summary = (
    df.groupby("Vintage")
    .agg(
        observations=("id", "count"),
        unique_loans=("id", "nunique"),
        min_orig_time=("orig_time", "min"),
        max_orig_time=("orig_time", "max")
    )
    .reset_index()
)

print("\nVintage Summary:")
print(vintage_summary.to_string(index=False))

vintage_summary.to_csv(
    OUTPUT_DIR / "vintage_summary.csv",
    index=False
)

# 6. PERIOD

print("\n" + "=" * 70)
print("STEP 3 - PERIOD")
print("=" * 70)

df["Period"] = df["time"]

print(f"Minimum Period : {df['Period'].min()}")
print(f"Maximum Period : {df['Period'].max()}")
print(f"Unique Periods : {df['Period'].nunique()}")


# 7. MACRO ECONOMIC VARIABLES

print("\n" + "=" * 70)
print("STEP 4 - MACRO ECONOMIC VARIABLES (MEVs)")
print("=" * 70)

mev_columns = [
    "hpi_time",
    "gdp_time",
    "uer_time",
    "rate_time",
    "interest_rate_time"
]

print("\nMEV Variables:")

for col in mev_columns:
    print("  -", col)

# 8. APC DATASET

apc_columns = [
    "id",
    "time",
    "orig_time",
    "MOB",
    "MOB_squared",
    "Vintage",
    "Period",
    "hpi_time",
    "gdp_time",
    "uer_time",
    "rate_time",
    "interest_rate_time",
    "default_time",
    "status_time",
    "balance_time",
    "balance_orig_time",
    "LTV_time"
]

apc_df = df[apc_columns].copy()


# 9. APC VALIDATION

print("\n" + "=" * 70)
print("STEP 5 - APC VALIDATION")
print("=" * 70)

validation_columns = [
    "MOB",
    "MOB_squared",
    "Vintage",
    "Period",
    "hpi_time",
    "gdp_time",
    "uer_time",
    "rate_time",
    "interest_rate_time",
    "balance_time",
    "balance_orig_time",
    "LTV_time"
]

print("\nMissing values:")

print(
    apc_df[validation_columns]
    .isna()
    .sum()
)

mob_check = (
    apc_df["MOB"]
    == apc_df["time"] - apc_df["orig_time"]
).all()

mob_squared_check = (
    apc_df["MOB_squared"]
    == apc_df["MOB"] ** 2
).all()

period_check = (
    apc_df["Period"]
    == apc_df["time"]
).all()

print(f"\nMOB calculation correct : {mob_check}")
print(f"MOB² calculation correct : {mob_squared_check}")
print(f"Period calculation correct : {period_check}")


# 10. SAVE APC DATA

print("\n" + "=" * 70)
print("STEP 6 - SAVE APC DATA")
print("=" * 70)

APC_OUTPUT = OUTPUT_DIR / "apc_features.csv"

apc_df.to_csv(
    APC_OUTPUT,
    index=False
)

print("\nAPC file saved:")
print(APC_OUTPUT)

# 11. APC SUMMARY ANALYSIS

print("\n" + "=" * 70)
print("STEP 7 - APC SUMMARY ANALYSIS")
print("=" * 70)


mob_analysis = (
    apc_df.groupby("MOB")
    .agg(
        observations=("id", "count"),
        unique_loans=("id", "nunique"),
        default_count=("default_time", "sum"),
        default_rate=("default_time", "mean")
    )
    .reset_index()
)

mob_analysis["default_rate_pct"] = (
    mob_analysis["default_rate"] * 100
)

mob_analysis.to_csv(
    OUTPUT_DIR / "mob_analysis.csv",
    index=False
)

print("\nMOB analysis saved.")


vintage_analysis = (
    apc_df.groupby("Vintage")
    .agg(
        observations=("id", "count"),
        unique_loans=("id", "nunique"),
        default_count=("default_time", "sum"),
        default_rate=("default_time", "mean")
    )
    .reset_index()
)

vintage_analysis["default_rate_pct"] = (
    vintage_analysis["default_rate"] * 100
)

vintage_analysis.to_csv(
    OUTPUT_DIR / "vintage_analysis.csv",
    index=False
)

print("Vintage analysis saved.")


period_mev_analysis = (
    apc_df.groupby("Period")
    .agg(
        observations=("id", "count"),
        unique_loans=("id", "nunique"),
        avg_HPI=("hpi_time", "mean"),
        avg_GDP=("gdp_time", "mean"),
        avg_UER=("uer_time", "mean"),
        avg_Rate=("rate_time", "mean"),
        avg_Interest_Rate=("interest_rate_time", "mean"),
        default_count=("default_time", "sum"),
        default_rate=("default_time", "mean")
    )
    .reset_index()
)

period_mev_analysis["default_rate_pct"] = (
    period_mev_analysis["default_rate"] * 100
)

period_mev_analysis.to_csv(
    OUTPUT_DIR / "period_mev_analysis.csv",
    index=False
)

print("Period / MEV analysis saved.")


# 12. APC DIMENSION ANALYSIS

print("\n" + "=" * 70)
print("STEP 8 - APC DIMENSION ANALYSIS")
print("=" * 70)


mob_vintage = (
    apc_df.groupby(["MOB", "Vintage"])
    .agg(
        observations=("id", "count"),
        unique_loans=("id", "nunique"),
        default_count=("default_time", "sum"),
        default_rate=("default_time", "mean")
    )
    .reset_index()
)

mob_vintage["default_rate_pct"] = (
    mob_vintage["default_rate"] * 100
)

mob_vintage.to_csv(
    OUTPUT_DIR / "mob_vintage_analysis.csv",
    index=False
)

print("\nMOB × Vintage analysis saved.")


vintage_period = (
    apc_df.groupby(["Vintage", "Period"])
    .agg(
        observations=("id", "count"),
        unique_loans=("id", "nunique"),
        default_count=("default_time", "sum"),
        default_rate=("default_time", "mean"),
        avg_HPI=("hpi_time", "mean"),
        avg_GDP=("gdp_time", "mean"),
        avg_UER=("uer_time", "mean"),
        avg_Rate=("rate_time", "mean"),
        avg_Interest_Rate=("interest_rate_time", "mean")
    )
    .reset_index()
)

vintage_period["default_rate_pct"] = (
    vintage_period["default_rate"] * 100
)

vintage_period.to_csv(
    OUTPUT_DIR / "vintage_period_analysis.csv",
    index=False
)

print("Vintage × Period analysis saved.")


mob_period = (
    apc_df.groupby(["MOB", "Period"])
    .agg(
        observations=("id", "count"),
        unique_loans=("id", "nunique"),
        default_count=("default_time", "sum"),
        default_rate=("default_time", "mean")
    )
    .reset_index()
)

mob_period["default_rate_pct"] = (
    mob_period["default_rate"] * 100
)

mob_period.to_csv(
    OUTPUT_DIR / "mob_period_analysis.csv",
    index=False
)

print("MOB × Period analysis saved.")


# 13. FINAL APC DATASET

print("\n" + "=" * 70)
print("STEP 9 - APC FINAL FEATURE DATASET")
print("=" * 70)

final_apc_columns = [
    "id",
    "time",
    "orig_time",
    "MOB",
    "MOB_squared",
    "Vintage",
    "Period",
    "hpi_time",
    "gdp_time",
    "uer_time",
    "rate_time",
    "interest_rate_time",
    "balance_time",
    "balance_orig_time",
    "LTV_time"
]

final_apc = apc_df[final_apc_columns].copy()

duplicate_rows = final_apc.duplicated().sum()

print(f"\nDuplicate APC rows : {duplicate_rows:,}")

mob_squared_errors = (
    final_apc["MOB_squared"]
    != final_apc["MOB"] ** 2
).sum()

period_errors = (
    final_apc["Period"]
    != final_apc["time"]
).sum()

print(f"MOB² calculation errors : {mob_squared_errors:,}")
print(f"Period calculation errors : {period_errors:,}")

print("\nMissing values in final APC dataset:")

print(
    final_apc.isna().sum()
)


FINAL_APC_OUTPUT = (
    OUTPUT_DIR / "apc_final_features.csv"
)

final_apc.to_csv(
    FINAL_APC_OUTPUT,
    index=False
)

# 14. FINAL SUMMARY

print("\n" + "=" * 70)
print("FINAL APC DATASET SUMMARY")
print("=" * 70)

print(f"Rows              : {len(final_apc):,}")
print(f"Columns           : {len(final_apc.columns)}")
print(f"Unique Loans      : {final_apc['id'].nunique():,}")
print(
    f"MOB Range         : "
    f"{final_apc['MOB'].min()} - {final_apc['MOB'].max()}"
)
print(f"Vintage Groups    : {final_apc['Vintage'].nunique()}")
print(
    f"Period Range      : "
    f"{final_apc['Period'].min()} - {final_apc['Period'].max()}"
)

print("\nFinal APC dataset saved:")
print(FINAL_APC_OUTPUT)

print("\nAPC STEP 9 COMPLETED.")
print("=" * 70)