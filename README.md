# Kepler Exoplanet Dataset (Enhanced)

This repository contains the enhanced Kepler exoplanet dataset, which includes information about exoplanets discovered via the transit method and enriched with habitability indices. These indices help to identify potentially habitable worlds for further analysis and visualization.

The repository also provides Python code to generate additional CSV files, offering various visualization and analytical capabilities. These enhancements aim to support academic research in data science and exoplanet habitability studies.

## Dataset Overview

The dataset is derived from NASA's Kepler Exoplanet Search Results and contains detailed information about exoplanets, including variables related to the planet’s size, temperature, and the insolation received from its host star. Additionally, three new habitability indices have been added to evaluate the potential for life on these planets:

- **HZ_bin**: Indicates whether the planet is located within the habitable zone.
- **Temp_habitable_bin**: Indicates whether the equilibrium temperature of the planet is compatible with life.
- **H_index**: A combined habitability index based on multiple factors.

### Main Variables

| Variable                | Description                                                                 |
|-------------------------|-----------------------------------------------------------------------------|
| `koi_disposition`        | Planet confirmation status (e.g., confirmed, candidate, etc.)               |
| `koi_prad`               | Planetary radius in Earth radii                                             |
| `koi_teq`                | Equilibrium temperature in Kelvin                                           |
| `koi_insol`              | Insolation received by the planet (in Earth units)                          |
| `koi_steff`              | Effective stellar temperature (in Kelvin)                                   |
| `koi_smass`              | Stellar mass (in solar masses)                                              |
| `HZ_bin`                 | Binary habitable zone index (1 if inside habitable zone, 0 otherwise)       |
| `Temp_habitable_bin`     | Binary temperature habitability index (1 if suitable for life, 0 otherwise) |
| `H_index`                | Combined habitability index (ranges from 0 to 1)                            |

## Usage and License

This dataset is released under the **CC0: Public Domain** license and is free to use for academic, research, and non-commercial purposes.

- **Original source**: NASA Kepler Exoplanet Search Results (CC0 Public Domain)
- **Dataset enrichment and documentation**: mfcabero (2025)

## Code License
All Python code and related scripts in this repository are licensed under the MIT License.

This means you are free to use, copy, modify, merge, publish, and distribute the software as long as the original copyright notice and permission statement are included.

## Repository Contents

1. **datasets/kepler_data_enriched.csv**: Main dataset with 53 variables and 9,564 observations of potential exoplanets, enriched with habitability indices.
2. **Python Code**: Scripts for generating derived datasets and performing analysis.
3. **Generated CSVs**:
   - `HZ_bin_count.csv`: Count of exoplanets categorized by their HZ_bin status.
   - `kepler_hz_bin1.csv`: Data for exoplanets located inside the habitable zone (HZ_bin = 1).
   - `kepler_hz_bin1_histogram.csv`: Histogram data for equilibrium temperatures of exoplanets in the habitable zone, in Celsius.
   - `koi_disposition_by_HZ_bin.csv`: Count of planets grouped by their disposition and HZ_bin status.
   - `koi_disposition_hz_pivot.csv`: Pivoted data showing the distribution of planets in and out of the habitable zone by disposition.
   - `koi_disposition_hz_percentage.csv`: Percentage-normalized data showing the proportion of planets in the habitable zone for each disposition.
   - `kepler_combined_habitability_top15.csv`: Top 15 planets ranked by the combined habitability index.

## How to Run the Code

### 1. **Install Dependencies**

To run the code, you need to have Python 3.x installed. You also need to install the required Python libraries:

```bash
pip install pandas numpy
```

This will install pandas (for data manipulation) and numpy (for numerical operations), both of which are essential to process the Kepler exoplanet dataset.

### 2. **Download or Prepare the Dataset*

Make sure you have the original dataset kepler_exoplanet_search_results_enhanced.csv from the repository. Place the dataset in a folder, preferably the datasets/ directory.

Ensure the SRC_PATH variable in the Python script points to this dataset file. You can modify the path if needed:

```bash
SRC_PATH = "../datasets/kepler_exoplanet_search_results_enhanced.csv"
```

If your project structure differs, adjust `SRC_PATH` so it correctly references the CSV file relative to the script.

3. Run the Python Script

Once you have the dependencies installed and the dataset in place, run the Python script to generate the additional CSV files and perform the analysis:

```bash
python generate_kepler_datasets.py
```

Use `python3` instead if your system distinguishes between Python 2 and Python 3

This will execute the Python script, and the related CSV files will be generated in the datasets/ directory.