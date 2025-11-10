# Kepler Exoplanet Dataset (Enhanced)

This repository contains the Kepler exoplanet dataset, enriched with habitability indices to facilitate analysis and visualization of potentially habitable worlds.

## Contents

- `kepler_data_enriched.csv`: Main dataset with 53 variables (50 original + 3 habitability indices) and 9,564 observations of potential exoplanets. The enrichment of
- this dataset is intended solely for academic purposes related to data science analysis and visualization, and not for commercial or operational use.

## Dataset Description

The original dataset comes from NASA and contains information about exoplanets detected via the transit method. 
Three new variables have been added to evaluate planetary habitability:

- `HZ_bin`: Indicates if the planet is in the habitable zone.
- `Temp_habitable_bin`: Indicates if the equilibrium temperature is compatible with life.
- `H_index`: Combined habitability index.

## Main Variables

| Variable             | Description                                      |
|----------------------|--------------------------------------------------|
| koi_disposition      | Planet confirmation status                       |
| koi_prad             | Planetary radius (Earth radii)                   |
| koi_teq              | Equilibrium temperature (K)                      |
| koi_insol            | Insolation received (Earth units)                |
| koi_steff            | Effective stellar temperature (K)                |
| koi_smass            | Stellar mass (solar masses)                      |
| HZ_bin               | Binary habitable zone index                      |
| Temp_habitable_bin   | Binary temperature habitability index            |
| H_index              | Combined habitability index                      |

## Usage and License

The original dataset is released under the CC0: Public Domain license
[CC0 Public Domain Dedication](https://creativecommons.org/publicdomain/zero/1.0/).

## Credits

- Original source: [NASA Kepler Exoplanet Search Results (CC0: Public Domain)](https://www.kaggle.com/datasets/nasa/kepler-exoplanet-search-results)
- Enrichment and documentation: mfcabero
