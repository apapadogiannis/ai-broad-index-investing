# Does AI Break the Case for Broad Index Investing? Rent Decay, Private Capital, and Deflation

[![SSRN](https://img.shields.io/badge/SSRN-10.2139%2Fssrn.6058896-1f4e79)](https://doi.org/10.2139/ssrn.6058896)
[![replication](https://github.com/apapadogiannis/ai-broad-index-investing/actions/workflows/replicate.yml/badge.svg)](https://github.com/apapadogiannis/ai-broad-index-investing/actions/workflows/replicate.yml)

Replication package for the article by Agisilaos Papadogiannis, forthcoming in *The Journal of Beta Investment Strategies* (2027).
Title and abstract: `paper/abstract.pdf`; also on SSRN: [doi:10.2139/ssrn.6058896](https://doi.org/10.2139/ssrn.6058896).
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
workflow re-runs the pipeline on every push and fails if `results.json` differs from the
committed file.

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

## Disclaimer

Independent research; no funding, no institutional position. Not investment advice.
