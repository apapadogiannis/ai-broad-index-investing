"""Merges the Portfolio Visualizer exports in data/pv/ into data/etf_monthly.csv.

Each batch file holds monthly total returns (%) for up to three funds. A fund that
appears in more than one batch (BITO) is taken from the first batch that has a value.
Usage: python3 build_etf_monthly.py
"""
import os, glob
import pandas as pd
B = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
out = None
for f in sorted(glob.glob(os.path.join(B, "data", "pv", "batch*.csv"))):
    d = pd.read_csv(f).set_index(["Year", "Month"])
    out = d if out is None else out.combine_first(d)
order = ["SPY","RSP","VT","BOTZ","ROBO","SMH","XLU","GLD","URA","VUG","VTV","TLT","AIQ","GRID","PAVE","BITO","IBIT","IAU"]
out = out[order].sort_index().reset_index()
out.to_csv(os.path.join(B, "data", "etf_monthly.csv"), index=False)
print("wrote data/etf_monthly.csv", out.shape)
