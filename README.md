# Does AI Break the Case for Broad Index Investing? Rent Decay, Private Capital, and Deflation

[![Zenodo](https://img.shields.io/badge/Zenodo-10.5281%2Fzenodo.24240516-007ec6)](https://doi.org/10.5281/zenodo.24240516)
[![SSRN](https://img.shields.io/badge/SSRN-10.2139%2Fssrn.6058896-1f4e79)](https://doi.org/10.2139/ssrn.6058896)
[![replication](https://github.com/apapadogiannis/ai-broad-index-investing/actions/workflows/replicate.yml/badge.svg)](https://github.com/apapadogiannis/ai-broad-index-investing/actions/workflows/replicate.yml)

Replication package for the article by Agisilaos Papadogiannis, forthcoming in *The Journal of Beta Investment Strategies* (2027).
Title and abstract: `paper/abstract.pdf`; also on SSRN: [doi:10.2139/ssrn.6058896](https://doi.org/10.2139/ssrn.6058896).
Archived on Zenodo: [doi:10.5281/zenodo.24240516](https://doi.org/10.5281/zenodo.24240516) (v1.0).
The article is copyright PMR and its text is not distributed here; this repository holds the code and the data behind its empirical exhibits, so that every reported number can be reproduced.

## What this is

Does AI break the case for holding a broad capitalization-weighted index? A common claim
says it does: AI shortens competitive advantage, lets firms grow without listing, and
causes deflation that rewards fixed-supply assets such as Bitcoin. We examine each claim
with a model in which equity value is capital plus the scarcity rents, profits above the
normal return, that listed firms hold, and with data on index returns, market composition
by region, index membership, real yields, and inflation regimes. Since the release of
ChatGPT, capitalization-weighted indices have beaten equal-weighted and most AI-themed
funds, as the model predicts: the index follows rents as they migrate, without a forecast.
A smaller listed market does not lower the index return; what does is value capitalized in
private hands before listing. Deflation strengthens fiat: cash earned 7% a year in real
terms in deflation years, and since its price was freed from the dollar in 1971, gold has
not seen one. The rents AI attacks are listed mainly in the US; the results favor breadth,
with a global all-cap index as its fullest form.

## Layout

```
scripts/    the code (see below)
data/       all input data, with sources and terms in data/README.md
outputs/    results.json: every number reported in Exhibits 5 to 10
paper/      title and abstract of the article (PDF and LaTeX source); the full text is not included
```

## Reproducing

Requirements: Python 3.11+, `pip install -r requirements.txt` (pandas, numpy,
statsmodels, matplotlib). `requirements-lock.txt` lists the exact versions under which
`outputs/results.json` was generated.

```bash
git clone https://github.com/apapadogiannis/ai-broad-index-investing
cd ai-broad-index-investing
pip install -r requirements.txt
./run_all.sh    # a few seconds
```

The scripts are deterministic. Re-running them reproduces `outputs/results.json` and
writes the LaTeX table bodies (`outputs/exhibit5.tex` to `exhibit10.tex`) and the two
figures (`figures/`), which are generated locally and not tracked. A GitHub Actions
workflow re-runs the pipeline on every push and once a month and fails if a stored result is not reproduced
(see "How the check works").

| Script | What it produces | Where it appears |
|---|---|---|
| `build_etf_monthly.py` | `data/etf_monthly.csv`, merged from the raw exports in `data/pv/` | input to Exhibits 7 and 9 |
| `make_exhibits.py` | Return on invested capital by scarcity layer | Exhibit 5 |
| | Sector composition of the US, developed ex-US, emerging and world markets | Exhibit 6 |
| | Return, volatility and drawdown of 15 funds, AI period and since 2018 | Exhibit 7 |
| | S&P 500 replacements, survival of past members, concentration | Exhibit 8 |
| | Fund return per one-point rise in the 10-year real yield (OLS, Newey-West, 3 lags) | Exhibit 9 |
| | Real returns on stocks, bills, bonds and gold by inflation regime, 1928 to 2025 | Exhibit 10 |
| `fig1_five_layers.py` | The five layers of scarcity (schematic) | Figure 1 |
| `fig2_rent_value.py` | Value of a dollar of rent by decay rate (illustrative) | Figure 2 |

Exhibits 1 to 4 and 11 of the article are qualitative tables and have no code.

The keys of `outputs/results.json` are named after the exhibits
(`exhibit5_roic_by_layer`, ..., `exhibit10_inflation_regimes`). The AI period is
December 2022 to September 2026 (46 months); fund data run from January 2018 to
September 2026.

## How the check works

```bash
python3 check_outputs.py --also data/etf_monthly.csv    # reruns ./run_all.sh, then compares
```

1. `outputs/results.json` and `data/etf_monthly.csv` are stored in this repository exactly as they were when the
   article's numbers were taken from them.
2. `check_outputs.py` sets the stored copies aside, reruns `./run_all.sh` on the files in `data/`,
   and compares the fresh files with the stored ones, number by number.
3. A number counts as reproduced if it agrees with the stored one to nine significant digits
   (relative tolerance 1e-9). Text, labels and whole numbers must match exactly. Any other
   difference is listed and the check fails.

Why a tolerance and not a character-by-character match: the last digits of a floating-point
result depend on the processor and on the build of the numerical libraries, so two correct runs
on different machines can differ in the 12th to 16th significant digit. The check reports
how many numbers differed in this way and by how much. For the same reason, a value printed with
a fixed number of decimals may differ by one unit in its last printed place; such cases are listed.

The workflow behind the badge runs the pipeline on a new machine with the pinned package
versions, on every push and once a month, and applies the same comparison. The stored results
are also frozen in the Zenodo archive, which cannot be altered after release.

Two limits. The comparison is between regenerated and stored results, not with the article's
PDF: to connect the two, use the script table above, which says where each output appears in
the article. And the figures and LaTeX table bodies are written locally from the same values but are not
stored here, so they are not part of the comparison.

## Data and licensing

All input files are in `data/`; `data/README.md` lists, for each file, the source, the
retrieval date and the terms under which the source makes it available. In short:

- Return on capital by industry and annual asset returns since 1928: Aswath Damodaran, NYU Stern.
- Monthly fund total returns: Portfolio Visualizer.
- Consumer prices: US Bureau of Labor Statistics, via the `datasets/cpi-us` data package (ODC-PDDL 1.0).
- 10-year real yields: US Department of the Treasury (public domain).
- S&P 500 membership history: `fja05680/sp500` (MIT License).
- Index weights, sector weights and largest holdings: Slickcharts, iShares (BlackRock), Stock Analysis.

Third-party data remain the property of their sources and are included for replication
only, with attribution; they are not covered by the license of this repository.
Code: MIT License. `outputs/results.json`: CC BY 4.0, cite the article.

## Citation

> Papadogiannis, A. (2027). "Does AI break the case for broad index investing? Rent decay,
> private capital, and deflation." *The Journal of Beta Investment Strategies*, forthcoming.
> SSRN: https://doi.org/10.2139/ssrn.6058896

Code and data:

> Papadogiannis, A. (2026). "Does AI break the case for broad index investing? Replication package." Zenodo.
> https://doi.org/10.5281/zenodo.24240516

## Disclaimer

Independent research; no funding, no institutional position. Not investment advice.
