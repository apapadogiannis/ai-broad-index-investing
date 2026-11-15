# Data

Every file used by the scripts, with its source, retrieval date and the terms stated by
the source. Third-party data remain the property of their sources and are redistributed
here for replication only, with attribution.

| File | Content | Source | Retrieved | Terms |
|---|---|---|---|---|
| `damodaran/roc_jan2026.csv` | After-tax return on invested capital by US industry (94 groups), January 2026: number of firms, ROIC, ROIC adjusted for leases and R&D, ten-year normalized ROIC | Aswath Damodaran, NYU Stern, "Return on capital (ROIC) by industry", https://pages.stern.nyu.edu/~adamodar/New_Home_Page/datacurrent.html | October 2026 | Freely downloadable from the author's page; no license stated |
| `damodaran/histret_1928_2025.csv` | Annual returns (%) on the S&P 500 (total return), 3-month T-bills, 10-year T-bonds, Baa bonds, real estate and gold, 1928 to 2025 | Aswath Damodaran, NYU Stern, "Historical returns on stocks, bonds and bills: 1928-2025", same page | October 2026 | As above |
| `pv/batchA.csv` to `batchG.csv` | Monthly total returns (%) of exchange-traded funds, January 2018 (or fund inception) to September 2026, as exported | Portfolio Visualizer, https://www.portfoliovisualizer.com | October 21, 2026 | Site terms of service apply; no open license |
| `etf_monthly.csv` | The seven exports merged into one table (built by `scripts/build_etf_monthly.py`). Used: SPY, VT, RSP, VUG, VTV, BOTZ, ROBO, AIQ, SMH, XLU, GRID, URA, GLD, TLT, BITO. Not used in the article: PAVE, IBIT, IAU | Derived from `pv/` | | As `pv/` |
| `cpi_us_monthly.csv` | CPI-U, all items, not seasonally adjusted, monthly from 1913 | US Bureau of Labor Statistics, via the data package https://github.com/datasets/cpi-us | October 2026 | ODC Public Domain Dedication and License 1.0; BLS data are in the public domain |
| `real10y_monthend.csv` | Month-end 10-year Treasury par real yield (%), January 2018 to September 2026 | US Department of the Treasury, daily par real yield curve rates, https://home.treasury.gov | October 2026 | US government work, public domain |
| `sp500/SandP_500_Historical_Components_and_Changes.csv` | S&P 500 membership by date, 1996 to 2026 | Farrell Aultman, https://github.com/fja05680/sp500 | October 2026 | MIT License |
| `sp500/sp500_ticker_start_end.csv` | Start and end date of each ticker's membership | Same | October 2026 | MIT License |
| `weights/sp500_top274_slickcharts_2026-10-20.csv` | S&P 500 constituent weights (%), 274 largest, October 20, 2026 | Slickcharts, https://www.slickcharts.com/sp500 | October 20, 2026 | Site terms apply; no open license |
| `sectors/ishares_sector_weights_2026-10-20.csv` | GICS sector weights (% of market value) of the iShares funds IVV (S&P 500), IEFA (MSCI EAFE), IEMG (MSCI Emerging Markets), ACWX (MSCI ACWI ex US) and ACWI (MSCI ACWI), as of October 19 to 20, 2026; cash and derivative lines omitted | BlackRock, iShares fund pages, https://www.ishares.com | October 20, 2026 | Site terms apply; no open license. Figures transcribed by hand from the fund pages |
| `sectors/top_holdings.csv` | Five largest holdings and weights: S&P 500 (October 20, 2026; Alphabet is GOOGL plus GOOG), IEFA (September 29, 2026), IEMG (October 16, 2026) | Slickcharts; Stock Analysis, https://stockanalysis.com | October 20 to 22, 2026 | Site terms apply; no open license |

## Constants entered in the code

`scripts/make_exhibits.py` also uses four figures that are not in a data file:

- US weight of the iShares MSCI ACWI ETF, 64.67%, and of the iShares MSCI World ETF (URTH),
  72.93%, both as of October 20, 2026 (iShares fund pages). They give each region's weight
  in the world index: developed markets are 64.67 / 72.93 of it.
- Weight of the ten largest holdings of the Vanguard Total World Stock ETF (VT), 22.45%, and
  its number of holdings, 10,242, as of September 30, 2026 (Stock Analysis).

## Notes

- S&P 500 replacements and survival are computed at the ticker level, so a ticker change
  counts as an exit and survival is slightly understated.
- Inflation regimes use December-to-December CPI inflation; real returns deflate by the
  same rate. Gold enters from 1972, the first full year in which its dollar price floated.
