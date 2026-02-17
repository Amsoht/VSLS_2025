# taunus-medusa baseline data parameterization
We used the [IAU_baseline filter](https://doi.org/10.5281/zenodo.18668744) to create parameterizations for ground-based measurements of the following compounds:
- CH2Cl2
- CHCl3
- C2Cl4
- CH3Cl
- CFC-11
- HCFC-22
- SF6
- HFC-125
- CFC-12
- H-1211
- HFC-32

## Usage:
1. Clone this repository to your local compouter.
2. In a terminal go to the local repositoy path and type run `pixi install` (obviously you need to have [pixi](https://pixi.prefix.dev/latest/installation/) installed on your computer). This will install python and all packages needed for reproducing the results.
3. Open the [`VSLS_2025/results/load_results.ipynb`](https://github.com/Amsoht/VSLS_2025/blob/main/results/load_results.ipynb) jupyter notebook e.g. in vscode and start exploring!

## Disclaimer: 
- The parameterization is valid for the timerange 2024-2025
- The raw data is stored in a dvc repository on next.hessenbox. Contact the author to get access.
