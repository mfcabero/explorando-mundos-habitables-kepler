"""
Generation of required datasets for Kepler Visualization
Author: mfcabero (2025)
"""

import pandas as pd
import numpy as np

# Paths
SRC_PATH = "../datasets/kepler_exoplanet_search_results_enhanced.csv"
OUT_HZ_BIN_COUNT = "../datasets/HZ_bin_count.csv"
OUT_HZ_BIN1 = "../datasets/kepler_hz_bin1.csv"
OUT_HZ_BIN1_HIST = "../datasets/kepler_hz_bin1_histogram.csv"
OUT_KOI_DISPOSITION_HZ = "../datasets/koi_disposition_by_HZ_bin.csv"
OUT_KOI_DISPOSITION_PIVOT = "../datasets/koi_disposition_hz_pivot.csv"
OUT_KOI_DISPOSITION_PCT = "../datasets/koi_disposition_hz_percentage.csv"
OUT_H_INDEX_TOP15 = "../datasets/kepler_combined_habitability_top15.csv"


# Load original dataset
df = pd.read_csv(SRC_PATH)

# Count per HZ_bin
hz_bin_count = (
    df["HZ_bin"]
    .value_counts()
    .sort_index()
    .reset_index()
)
hz_bin_count.columns = ["HZ_bin", "count"]

hz_bin_count.to_csv(OUT_HZ_BIN_COUNT, index=False)
print(f"HZ_bin count saved to {OUT_HZ_BIN_COUNT}")

# Filter dataset for HZ_bin = 1
df_hz_bin1 = df[df["HZ_bin"] == 1]
print(f"Filtered {len(df_hz_bin1)} entries with HZ_bin = 1")
df_hz_bin1.to_csv(OUT_HZ_BIN1, index=False)

# Prepare histogram data (convert to Celsius)
df_hz_bin1_hist = df_hz_bin1.dropna(subset=["koi_teq"])
values_C = df_hz_bin1_hist["koi_teq"] - 273.15
# Compute optimal bin edges in C
bin_edges_C = np.histogram_bin_edges(values_C, bins="fd")

# Compute bins and counts
counts_C, edges_C = np.histogram(values_C, bins=bin_edges_C)
bin_left_C = edges_C[:-1].round(1)
bin_right_C = edges_C[1:].round(1)
bin_center_C = ((bin_left_C + bin_right_C) / 2).round(1)

# Create binned dataset in Celsius
df_histogram_C = pd.DataFrame({
    "temp_C_bin_left": bin_left_C,
    "temp_C_bin_right": bin_right_C,
    "temp_C_bin_center": bin_center_C,
    "frequency": counts_C
})

df_histogram_C.to_csv(OUT_HZ_BIN1_HIST, index=False)
print(f"Binned Celsius data saved: {len(df_histogram_C)} bins")

# koi_disposition × HZ_bin
df_koi_hz = (
    df
    .groupby(["koi_disposition", "HZ_bin"])
    .size()
    .reset_index(name="count")
    .sort_values(["koi_disposition", "HZ_bin"])
)

df_koi_hz.to_csv(OUT_KOI_DISPOSITION_HZ, index=False)
print(f"koi_disposition by HZ_bin saved to {OUT_KOI_DISPOSITION_HZ}")

# Group and pivot
df_koi_pivot = (
    df
    .groupby(["koi_disposition", "HZ_bin"])
    .size()
    .unstack(fill_value=0)
    .reset_index()
)

# Rename columns
df_koi_pivot = df_koi_pivot.rename(columns={
    0: "Outside_HZ",
    1: "Inside_HZ"
})

df_koi_pivot.to_csv(OUT_KOI_DISPOSITION_PIVOT, index=False)
print(f"Pivoted koi_disposition dataset saved to {OUT_KOI_DISPOSITION_PIVOT}")

# Percentage-normalized version
df_pct = df_koi_pivot.copy()

# Compute row-wise percentages
row_sum = df_pct[["Outside_HZ", "Inside_HZ"]].sum(axis=1)

df_pct["Outside_HZ_pct"] = (df_pct["Outside_HZ"] / row_sum * 100).round(1)
df_pct["Inside_HZ_pct"] = (df_pct["Inside_HZ"] / row_sum * 100).round(1)

# Keep only percentage columns
df_pct = df_pct[[
    "koi_disposition",
    "Outside_HZ_pct",
    "Inside_HZ_pct"
]]

df_pct.to_csv(OUT_KOI_DISPOSITION_PCT, index=False)
print(f"Percentage-normalized dataset saved to {OUT_KOI_DISPOSITION_PCT}")

df_hz_bin1 = df[df["HZ_bin"] == 1].copy()


def score_insolation(s):
    """
    Score in [0,1], maximum at koi_insol = 1.
    Goes to 0 at 0.1 and 10 (clipped range).
    """
    if pd.isna(s):
        return np.nan
    s = max(min(s, 10), 0.1)
    if s <= 1:
        # 0.1 -> 0 ; 1 -> 1
        return (s - 0.1) / (1 - 0.1)
    else:
        # 1 -> 1 ; 10 -> 0
        return (10 - s) / (10 - 1)


def score_teq(t):
    """
    Score in [0,1], maximum in 240–320 K.
    0 at 150 K and 400 K.
    """
    if pd.isna(t):
        return np.nan
    if t <= 150 or t >= 400:
        return 0.0
    if 240 <= t <= 320:
        return 1.0
    if t < 240:
        # 150 -> 0 ; 240 -> 1
        return (t - 150) / (240 - 150)
    else:  # t > 320
        # 320 -> 1 ; 400 -> 0
        return (400 - t) / (400 - 320)


def score_radius(r):
    """
    Score in [0,1], maximum for 1–2 Earth radii.
    0 at 0.5 and 4 Earth radii.
    """
    if pd.isna(r):
        return np.nan
    if r <= 0.5 or r >= 4:
        return 0.0
    if 1 <= r <= 2:
        return 1.0
    if r < 1:
        # 0.5 -> 0 ; 1 -> 1
        return (r - 0.5) / (1 - 0.5)
    else:  # r > 2
        # 2 -> 1 ; 4 -> 0
        return (4 - r) / (4 - 2)


df_hz_bin1["score_insol"] = df_hz_bin1["koi_insol"].apply(score_insolation)
df_hz_bin1["score_teq"] = df_hz_bin1["koi_teq"].apply(score_teq)
df_hz_bin1["score_prad"] = df_hz_bin1["koi_prad"].apply(score_radius)

# Combined habitability index (geometric mean to reduce saturation)
df_hz_bin1["H_index_combined"] = (
    df_hz_bin1["score_insol"]
    * df_hz_bin1["score_teq"]
    * df_hz_bin1["score_prad"]
) ** (1 / 3)

# Distance to maximum habitability (for visualization)
df_hz_bin1["H_delta"] = 1.0 - df_hz_bin1["H_index_combined"]

# Visualization-friendly rescaling (opens values near 1)
ALPHA = 0.4  # tweak between 0.3–0.5 if needed
df_hz_bin1["H_vis"] = 1.0 - (1.0 - df_hz_bin1["H_index_combined"]) ** ALPHA

# Sort by combined index and take Top 15
df_ranked = (
    df_hz_bin1
    .dropna(subset=["H_index_combined"])
    .sort_values("H_index_combined", ascending=False)
)

top15 = df_ranked.head(15)

# Dataset for combined habitability index
cols_Hcombined_dataset = [
    "kepoi_name",
    "H_index_combined",
    "H_vis",
    "H_delta",
    "koi_insol",
    "koi_teq",
    "koi_prad",
    "H_index",
    "HZ_bin"
]
top15_Hcombined = top15[cols_Hcombined_dataset]

top15_Hcombined.to_csv(OUT_H_INDEX_TOP15, index=False)
print(f"Top 15 combined habitability saved to {OUT_H_INDEX_TOP15}")

# N Planets with H_index > 0.7
N = (df["H_index"] > 0.7).sum()
print("Planets greater than 0.7:", N)

N_confirmed = (
    (df["H_index"] > 0.7) & (df["koi_disposition"] == "CONFIRMED")).sum()
print("Confirmed planets with H_index > 0.7:", N_confirmed)