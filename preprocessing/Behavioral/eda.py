from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]

import pandas as pd
import os
import pandas as pd
import os

# EDA - STEP 1 : BASIC DATASET PROFILING

print("\n" + "=" * 70)
print("BEHAVIORAL SCORECARD - EDA")
print("STEP 1: BASIC DATASET PROFILING")
print("=" * 70)

# PATH

file_path = r"data/raw/Behavioral/Final_scorecard_1_Data check.xlsm"

output_dir = r"data/interim/behavioral/eda"

os.makedirs(output_dir, exist_ok=True)

# LOAD DATA

print("\nLoading dataset...")
print("Please wait...\n")

df = pd.read_excel(
    file_path,
    sheet_name="Reconciliation",
    engine="openpyxl"
)

print("Dataset loaded successfully.")

# 1. DATASET SHAPE

print("\n" + "=" * 70)
print("1. DATASET SHAPE")
print("=" * 70)

print("Rows    :", df.shape[0])
print("Columns :", df.shape[1])

# 2. COLUMN NAMES

print("\n" + "=" * 70)
print("2. COLUMN NAMES")
print("=" * 70)

for i, column in enumerate(df.columns, start=1):
    print(f"{i:2}. {column}")

# 3. DATA TYPES

print("\n" + "=" * 70)
print("3. DATA TYPES")
print("=" * 70)

print(df.dtypes)

# 4. MISSING VALUES

print("\n" + "=" * 70)
print("4. MISSING VALUES")
print("=" * 70)

missing = pd.DataFrame({
    "Column": df.columns,
    "Missing_Count": df.isnull().sum().values,
    "Missing_Percentage": (
        df.isnull().sum().values / len(df) * 100
    )
})

missing = missing.sort_values(
    by="Missing_Count",
    ascending=False
)

print(missing.to_string(index=False))


# Save missing-value report
missing.to_csv(
    os.path.join(output_dir, "missing_values.csv"),
    index=False
)


# 5. UNIQUE IDS

print("\n" + "=" * 70)
print("5. UNIQUE IDS")
print("=" * 70)

print("Unique IDs:", df["id"].nunique())

# 6. DUPLICATE ROWS

print("\n" + "=" * 70)
print("6. DUPLICATE ROWS")
print("=" * 70)

duplicate_count = df.duplicated().sum()

print("Duplicate rows:", duplicate_count)


# 7. NUMERICAL SUMMARY

print("\n" + "=" * 70)
print("7. NUMERICAL SUMMARY")
print("=" * 70)

numeric_df = df.select_dtypes(
    include="number"
)

summary = numeric_df.describe().T

summary["missing"] = numeric_df.isnull().sum()

print(summary.to_string())


# Save descriptive statistics
summary.to_csv(
    os.path.join(output_dir, "descriptive_statistics.csv")
)

# 8. FIRST 5 RECORDS

print("\n" + "=" * 70)
print("8. FIRST 5 RECORDS")
print("=" * 70)

print(df.head().to_string())

# 9. LAST 5 RECORDS
print("\n" + "=" * 70)
print("9. LAST 5 RECORDS")
print("=" * 70)

print(df.tail().to_string())

# 10. BASIC ID OBSERVATION

print("\n" + "=" * 70)
print("10. OBSERVATIONS PER ID")
print("=" * 70)

observations_per_id = df.groupby("id").size()

print(
    observations_per_id.describe().to_string()
)


# Save ID observation summary
id_summary = observations_per_id.describe()

id_summary.to_csv(
    os.path.join(output_dir, "observations_per_id.csv")
)

# FINAL

print("\n" + "=" * 70)
print("EDA STEP 1 COMPLETED")
print("=" * 70)

print("\nReports saved in:")
print(output_dir)

print("\nGenerated files:")
print("- missing_values.csv")
print("- descriptive_statistics.csv")
print("- observations_per_id.csv")

print("\n" + "=" * 70)
print("BEHAVIORAL SCORECARD - EDA")
print("STEP 1: BASIC DATASET PROFILING")
print("=" * 70)

# PATH

file_path = r"data/raw/Behavioral/Final_scorecard_1_Data check.xlsm"

output_dir = r"data/interim/behavioral/eda"

os.makedirs(output_dir, exist_ok=True)

# LOAD DATA

print("\nLoading dataset...")
print("Please wait...\n")

df = pd.read_excel(
    file_path,
    sheet_name="Reconciliation",
    engine="openpyxl"
)

print("Dataset loaded successfully.")

# 1. DATASET SHAPE

print("\n" + "=" * 70)
print("1. DATASET SHAPE")
print("=" * 70)

print("Rows    :", df.shape[0])
print("Columns :", df.shape[1])

# 2. COLUMN NAMES

print("\n" + "=" * 70)
print("2. COLUMN NAMES")
print("=" * 70)

for i, column in enumerate(df.columns, start=1):
    print(f"{i:2}. {column}")

# 3. DATA TYPES

print("\n" + "=" * 70)
print("3. DATA TYPES")
print("=" * 70)

print(df.dtypes)

# 4. MISSING VALUES

print("\n" + "=" * 70)
print("4. MISSING VALUES")
print("=" * 70)

missing = pd.DataFrame({
    "Column": df.columns,
    "Missing_Count": df.isnull().sum().values,
    "Missing_Percentage": (
        df.isnull().sum().values / len(df) * 100
    )
})

missing = missing.sort_values(
    by="Missing_Count",
    ascending=False
)

print(missing.to_string(index=False))


# Save missing-value report
missing.to_csv(
    os.path.join(output_dir, "missing_values.csv"),
    index=False
)

# 5. UNIQUE IDS

print("\n" + "=" * 70)
print("5. UNIQUE IDS")
print("=" * 70)

print("Unique IDs:", df["id"].nunique())


# 6. DUPLICATE ROWS

print("\n" + "=" * 70)
print("6. DUPLICATE ROWS")
print("=" * 70)

duplicate_count = df.duplicated().sum()

print("Duplicate rows:", duplicate_count)

# 7. NUMERICAL SUMMARY

print("\n" + "=" * 70)
print("7. NUMERICAL SUMMARY")
print("=" * 70)

numeric_df = df.select_dtypes(
    include="number"
)

summary = numeric_df.describe().T

summary["missing"] = numeric_df.isnull().sum()

print(summary.to_string())


# Save descriptive statistics
summary.to_csv(
    os.path.join(output_dir, "descriptive_statistics.csv")
)

# 8. FIRST 5 RECORDS

print("\n" + "=" * 70)
print("8. FIRST 5 RECORDS")
print("=" * 70)

print(df.head().to_string())

# 9. LAST 5 RECORDS

print("\n" + "=" * 70)
print("9. LAST 5 RECORDS")
print("=" * 70)

print(df.tail().to_string())


# 10. BASIC ID OBSERVATION

print("\n" + "=" * 70)
print("10. OBSERVATIONS PER ID")
print("=" * 70)

observations_per_id = df.groupby("id").size()

print(
    observations_per_id.describe().to_string()
)


# Save ID observation summary
id_summary = observations_per_id.describe()

id_summary.to_csv(
    os.path.join(output_dir, "observations_per_id.csv")
)

# FINAL

print("\n" + "=" * 70)
print("EDA STEP 1 COMPLETED")
print("=" * 70)

print("\nReports saved in:")
print(output_dir)

print("\nGenerated files:")
print("- missing_values.csv")
print("- descriptive_statistics.csv")
print("- observations_per_id.csv")


# EDA - STEP 2 : DETAILED DESCRIPTIVE STATISTICS

print("\n" + "=" * 70)
print("EDA STEP 2: DETAILED DESCRIPTIVE STATISTICS")
print("=" * 70)

# SELECT IMPORTANT MODEL VARIABLES

eda_columns = [
    "time",
    "orig_time",
    "first_time",
    "mat_time",
    "balance_time",
    "LTV_time",
    "interest_rate_time",
    "rate_time",
    "hpi_time",
    "gdp_time",
    "uer_time",
    "balance_orig_time",
    "FICO_orig_time",
    "LTV_orig_time",
    "Interest_Rate_orig_time",
    "default_time",
    "payoff_time",
    "status_time",
    "lgd_time",
    "recovery_res"
]


# Only use columns that actually exist
eda_columns = [
    col for col in eda_columns
    if col in df.columns
]

print("\nVariables selected for detailed EDA:")
print(eda_columns)

# DESCRIPTIVE STATISTICS

stats = df[eda_columns].describe().T

stats["missing"] = df[eda_columns].isnull().sum()

stats["missing_pct"] = (
    df[eda_columns].isnull().sum()
    / len(df)
    * 100
)

stats["unique"] = [
    df[col].nunique()
    for col in eda_columns
]

stats = stats[
    [
        "count",
        "missing",
        "missing_pct",
        "unique",
        "mean",
        "std",
        "min",
        "25%",
        "50%",
        "75%",
        "max"
    ]
]

print("\n")
print(stats.to_string())

# SAVE REPORT


stats_path = os.path.join(
    output_dir,
    "detailed_descriptive_statistics.csv"
)

stats.to_csv(stats_path)

print("\nDetailed statistics saved:")
print(stats_path)

# MINIMUM / MAXIMUM CHECK

print("\n" + "=" * 70)
print("MINIMUM / MAXIMUM CHECK")
print("=" * 70)

for col in eda_columns:

    print(
        f"{col:25} "
        f"Min = {df[col].min()}    "
        f"Max = {df[col].max()}"
    )
# EDA STEP 2 COMPLETED

print("\n" + "=" * 70)
print("EDA STEP 2 COMPLETED")
print("=" * 70)


# EDA - STEP 3 : OUTLIER ANALYSIS

print("\n" + "=" * 70)
print("EDA STEP 3: OUTLIER ANALYSIS")
print("=" * 70)

# VARIABLES FOR OUTLIER ANALYSIS

outlier_columns = [
    "interest_rate_time",
    "LTV_time",
    "LTV_orig_time",
    "balance_time",
    "balance_orig_time",
    "FICO_orig_time",
    "Interest_Rate_orig_time",
    "lgd_time",
    "recovery_res"
]

# Keep only columns that exist
outlier_columns = [
    col for col in outlier_columns
    if col in df.columns
]

# IQR OUTLIER CALCULATION

outlier_results = []


for col in outlier_columns:

    # Remove missing values for calculation
    series = df[col].dropna()

    Q1 = series.quantile(0.25)
    Q3 = series.quantile(0.75)

    IQR = Q3 - Q1

    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR

    outliers = series[
        (series < lower_bound) |
        (series > upper_bound)
    ]

    outlier_count = len(outliers)

    outlier_percentage = (
        outlier_count / len(series) * 100
    )

    outlier_results.append({
        "Variable": col,
        "Q1": Q1,
        "Q3": Q3,
        "IQR": IQR,
        "Lower_Bound": lower_bound,
        "Upper_Bound": upper_bound,
        "Min": series.min(),
        "Max": series.max(),
        "Outlier_Count": outlier_count,
        "Outlier_Percentage": outlier_percentage
    })


# Convert to DataFrame
outlier_summary = pd.DataFrame(
    outlier_results
)

# DISPLAY RESULTS

print("\n")
print(
    outlier_summary.to_string(index=False)
)

# SAVE OUTLIER REPORT

outlier_path = os.path.join(
    output_dir,
    "outlier_analysis.csv"
)

outlier_summary.to_csv(
    outlier_path,
    index=False
)

print("\nOutlier report saved:")
print(outlier_path)

# EXTREME VALUES

print("\n" + "=" * 70)
print("EXTREME VALUE CHECK")
print("=" * 70)


for col in outlier_columns:

    series = df[col].dropna()

    print(f"\n{col}")

    print("Lowest 5 values:")
    print(
        series.nsmallest(5).to_list()
    )

    print("Highest 5 values:")
    print(
        series.nlargest(5).to_list()
    )


# INTEREST RATE SPECIFIC CHECK

print("\n" + "=" * 70)
print("INTEREST RATE SPECIFIC CHECK")
print("=" * 70)


interest_col = "interest_rate_time"

interest_zero = (
    df[interest_col] == 0
).sum()

interest_above_20 = (
    df[interest_col] > 20
).sum()

interest_above_30 = (
    df[interest_col] > 30
).sum()

interest_37_5 = (
    df[interest_col] == 37.5
).sum()


print("Interest rate = 0      :", interest_zero)
print("Interest rate > 20%    :", interest_above_20)
print("Interest rate > 30%    :", interest_above_30)
print("Interest rate = 37.5%  :", interest_37_5)

# LTV SPECIFIC CHECK


print("\n" + "=" * 70)
print("LTV SPECIFIC CHECK")
print("=" * 70)


print(
    "LTV_time > 100% :",
    (df["LTV_time"] > 100).sum()
)

print(
    "LTV_time > 150% :",
    (df["LTV_time"] > 150).sum()
)

print(
    "LTV_time > 200% :",
    (df["LTV_time"] > 200).sum()
)

print(
    "LTV_orig_time > 100% :",
    (df["LTV_orig_time"] > 100).sum()
)

print(
    "LTV_orig_time > 150% :",
    (df["LTV_orig_time"] > 150).sum()
)

print(
    "LTV_orig_time > 200% :",
    (df["LTV_orig_time"] > 200).sum()
)

# EDA STEP 3 COMPLETED

print("\n" + "=" * 70)
print("EDA STEP 3 COMPLETED")
print("=" * 70)

# EDA STEP 4: MACRO / TIME TREND ANALYSIS

print("\n" + "=" * 70)
print("EDA STEP 4: MACRO / TIME TREND ANALYSIS")
print("=" * 70)

# Macro / time based variables
macro_variables = [
    "hpi_time",
    "gdp_time",
    "uer_time",
    "rate_time",
    "interest_rate_time"
]

# Check that columns exist
available_macro = [col for col in macro_variables if col in df.columns]

print("\nMacro variables found:")
print(available_macro)

# 1. Average value for each time period

macro_by_time = (
    df.groupby("time")[available_macro]
      .mean()
      .reset_index()
)

print("\n" + "=" * 70)
print("AVERAGE MACRO VALUES BY TIME")
print("=" * 70)

print(macro_by_time.head(10))

# Save result
macro_by_time.to_csv(
    "data/interim/behavioral/eda/macro_trend_by_time.csv",
    index=False
)

# 2. Minimum and Maximum for each time period


macro_summary_by_time = (
    df.groupby("time")[available_macro]
      .agg(["min", "max", "mean"])
)

print("\n" + "=" * 70)
print("MACRO MIN / MAX / MEAN BY TIME")
print("=" * 70)

print(macro_summary_by_time.head(10))

# Save result
macro_summary_by_time.to_csv(
    "data/interim/behavioral/eda/macro_summary_by_time.csv"
)

# 3. Overall change from first time to last time

first_time = df["time"].min()
last_time = df["time"].max()

first_values = (
    df[df["time"] == first_time][available_macro]
    .mean()
)

last_values = (
    df[df["time"] == last_time][available_macro]
    .mean()
)

comparison = pd.DataFrame({
    "First_Time": first_values,
    "Last_Time": last_values
})

comparison["Absolute_Change"] = (
    comparison["Last_Time"] - comparison["First_Time"]
)

comparison["Percentage_Change"] = (
    comparison["Absolute_Change"]
    / comparison["First_Time"].replace(0, pd.NA)
) * 100

print("\n" + "=" * 70)
print("FIRST TIME vs LAST TIME")
print("=" * 70)

print(comparison)

# Save result
comparison.to_csv(
    "data/interim/behavioral/eda/macro_first_vs_last.csv"
)

print("\n" + "=" * 70)
print("EDA STEP 4 COMPLETED")
print("=" * 70)

# EDA STEP 5: VINTAGE / COHORT ANALYSIS

print("\n" + "=" * 70)
print("EDA STEP 5: VINTAGE / COHORT ANALYSIS")
print("=" * 70)

# orig_time ka distribution
vintage_summary = (
    df.groupby("orig_time")
      .agg(
          total_observations=("id", "size"),
          unique_loans=("id", "nunique")
      )
      .reset_index()
      .sort_values("orig_time")
)

print("\nOrigination time distribution:")
print(vintage_summary.to_string(index=False))

# Save result
vintage_summary.to_csv(
    "data/interim/behavioral/eda/vintage_orig_time_summary.csv",
    index=False
)

print("\n" + "=" * 70)
print("EDA STEP 5 - ORIG_TIME ANALYSIS COMPLETED")
print("=" * 70)

# STEP 5: VINTAGE ANALYSIS

print("\n" + "=" * 60)
print("STEP 5: VINTAGE ANALYSIS")
print("=" * 60)

# Create Vintage / Cohort
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

# Check vintage distribution
vintage_summary = (
    df.groupby("Vintage")
      .agg(
          total_observations=("id", "count"),
          unique_loans=("id", "nunique"),
          min_orig_time=("orig_time", "min"),
          max_orig_time=("orig_time", "max")
      )
      .reset_index()
)

print("\nVintage Summary:")
print(vintage_summary)

# Observation count by Vintage and Time
vintage_time_summary = (
    df.groupby(["Vintage", "time"])
      .agg(
          observations=("id", "count"),
          unique_loans=("id", "nunique")
      )
      .reset_index()
)

print("\nVintage-Time Summary:")
print(vintage_time_summary.head(20))

# Save outputs
output_file = (
    PROJECT_ROOT
    / "data"
    / "interim"
    / "behavioral"
    / "eda"
    / "vintage_analysis.csv"
)

vintage_summary.to_csv(output_file, index=False)

print(f"\nVintage analysis saved to: {output_file}")

# ============================================================
# STEP 5B: VINTAGE-WISE BEHAVIOUR ANALYSIS
# ============================================================

print("\n" + "=" * 60)
print("STEP 5B: VINTAGE-WISE BEHAVIOUR ANALYSIS")
print("=" * 60)

# ------------------------------------------------------------
# 1. Vintage vs Time - observations and loans
# ------------------------------------------------------------

vintage_time_behavior = (
    df.groupby(["Vintage", "time"])
      .agg(
          observations=("id", "count"),
          unique_loans=("id", "nunique"),
          avg_LTV=("LTV_time", "mean"),
          avg_balance=("balance_time", "mean"),
          default_rate=("default_time", "mean")
      )
      .reset_index()
)

print("\nVintage-wise behaviour:")
print(vintage_time_behavior.head(30))


# ------------------------------------------------------------
# 2. Default rate by Vintage
# ------------------------------------------------------------

vintage_default = (
    df.groupby("Vintage")
      .agg(
          observations=("id", "count"),
          unique_loans=("id", "nunique"),
          defaults=("default_time", "sum"),
          default_rate=("default_time", "mean")
      )
      .reset_index()
)

vintage_default["default_rate_pct"] = (
    vintage_default["default_rate"] * 100
)

print("\nDefault rate by Vintage:")
print(vintage_default)


# ------------------------------------------------------------
# 3. Average LTV by Vintage
# ------------------------------------------------------------

vintage_ltv = (
    df.groupby("Vintage")
      .agg(
          avg_LTV=("LTV_time", "mean"),
          median_LTV=("LTV_time", "median")
      )
      .reset_index()
)

print("\nLTV by Vintage:")
print(vintage_ltv)


# ------------------------------------------------------------
# 4. Average Balance by Vintage
# ------------------------------------------------------------

vintage_balance = (
    df.groupby("Vintage")
      .agg(
          avg_balance=("balance_time", "mean"),
          median_balance=("balance_time", "median")
      )
      .reset_index()
)

print("\nBalance by Vintage:")
print(vintage_balance)

# SAVE OUTPUTS

eda_output = (
    PROJECT_ROOT
    / "data"
    / "interim"
    / "behavioral"
    / "eda"
)

vintage_time_behavior.to_csv(
    eda_output / "vintage_time_behavior.csv",
    index=False
)

vintage_default.to_csv(
    eda_output / "vintage_default_analysis.csv",
    index=False
)

vintage_ltv.to_csv(
    eda_output / "vintage_ltv_analysis.csv",
    index=False
)

vintage_balance.to_csv(
    eda_output / "vintage_balance_analysis.csv",
    index=False
)

print("\nStep 5B outputs saved successfully.")