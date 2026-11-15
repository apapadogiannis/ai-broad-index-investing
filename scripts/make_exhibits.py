"""Builds every empirical exhibit of the paper (Exhibits 5 to 10) from the files in data/.

Usage: python3 make_exhibits.py
Writes outputs/results.json (every number reported in the exhibits) and
outputs/exhibit5.tex ... exhibit10.tex (LaTeX table bodies; not tracked in the repository).
"""
import pandas as pd, numpy as np, statsmodels.api as sm, json
import os; B=os.path.dirname(os.path.dirname(os.path.abspath(__file__))); D=B+'/data/'; OUT=B+'/outputs/'; os.makedirs(OUT,exist_ok=True)
res={}
# ---------- Exhibit 5: ROIC by layer ----------
d=pd.read_csv(D+'damodaran/roc_jan2026.csv'); d=d[~d.industry.str.startswith('Total')].dropna()
layer={
'Codified capabilities':['Software (System & Application)','Software (Internet)','Software (Entertainment)','Computer Services','Computers/Peripherals','Telecom. Equipment','Information Services','Electronics (General)','Heathcare Information and Technology','Business & Consumer Services','Advertising','Education'],
'Institutional':['Drugs (Pharmaceutical)','Drugs (Biotechnology)','Tobacco','Aerospace/Defense','Insurance (General)','Insurance (Life)','Insurance (Prop/Cas.)','Reinsurance','Hospitals/Healthcare Facilities','Healthcare Support Services','Healthcare Products'],
'Physical':['Coal & Related Energy','Oil/Gas (Integrated)','Oil/Gas (Production and Exploration)','Oilfield Svcs/Equip.','Metals & Mining','Precious Metals','Steel','Chemical (Basic)','Paper/Forest Products','Farming/Agriculture'],
'Infrastructural':['Power','Utility (General)','Utility (Water)','Transportation (Railroads)','Telecom. Services','Telecom (Wireless)','Cable TV','R.E.I.T.','Real Estate (Development)','Real Estate (General/Diversified)','Real Estate (Operations & Services)','Retail (REITs)','Green & Renewable Energy','Oil/Gas Distribution','Air Transport','Trucking','Transportation','Shipbuilding & Marine','Semiconductor','Semiconductor Equip'],
}
inv={i:l for l,v in layer.items() for i in v}
d['layer']=d.industry.map(inv).fillna('Other (consumer, industrial, retail)')
def wmed(g,c):
    g=g.sort_values(c); cw=g.nfirms.cumsum(); return g[c][cw>=g.nfirms.sum()/2].iloc[0]
rows=[]
for l in ['Codified capabilities','Institutional','Other (consumer, industrial, retail)','Physical','Infrastructural']:
    g=d[d.layer==l]; rows.append((l,len(g),int(g.nfirms.sum()),wmed(g,'aftertax_roic_unadj'),wmed(g,'aftertax_roic_lease_rd_adj'),wmed(g,'normalized_roic_10y')))
e3=pd.DataFrame(rows,columns=['layer','industries','firms','roic','roic_adj','roic10']); res['e3']=e3.round(1).to_dict('records')
with open(OUT+'exhibit5.tex','w') as f:
    pool={'Codified capabilities':'Fast','Institutional':'Slow','Other (consumer, industrial, retail)':'Mixed','Physical':'Slow','Infrastructural':'Slow'}
    f.write("\\begin{tabular}{@{}llrrrr@{}}\n\\toprule\nLayer & Pool & Industries & Firms & ROIC, 2025 & ROIC, 10-year \\\\\n\\midrule\n")
    for r in rows: f.write(f"{r[0]} & {pool[r[0]]} & {r[1]} & {r[2]:,} & {r[3]:.1f}\\% & {r[5]:.1f}\\% \\\\\n")
    f.write("\\bottomrule\n\\end{tabular}\n")
# ---------- Exhibit 7: index strategies ----------
e=pd.read_csv(D+'etf_monthly.csv')
def stats(dd,c):
    r=dd[c].dropna()/100; n=len(r); cum=(1+r).prod()-1; ann=(1+cum)**(12/n)-1; vol=r.std()*np.sqrt(12); w=(1+r).cumprod(); dd_=(w/w.cummax()-1).min()
    return n,cum*100,ann*100,vol*100,ann/vol,dd_*100
groups=[('Broad capitalization-weighted indices',[('SPY','S\\&P 500 (SPY)'),('VT','Global all-cap (VT)')]),
 ('Alternative weightings and styles',[('RSP','S\\&P 500, equal-weighted (RSP)'),('VUG','US growth (VUG)'),('VTV','US value (VTV)')]),
 ('AI-themed funds',[('BOTZ','AI and robotics (BOTZ)'),('ROBO','Robotics and automation (ROBO)'),('AIQ','AI and technology (AIQ)')]),
 ('Bottleneck sleeves',[('SMH','Semiconductors (SMH)'),('XLU','US utilities (XLU)'),('GRID','Grid infrastructure (GRID)'),('URA','Uranium (URA)')]),
 ('Other assets',[('GLD','Gold (GLD)'),('TLT','Long Treasuries (TLT)'),('BITO','Bitcoin (BITO)')])]
post=e[(e.Year>2022)|((e.Year==2022)&(e.Month>=12))]
full=e
res['e5']={}
with open(OUT+'exhibit7.tex','w') as f:
    f.write("\\begin{tabular}{@{}lrrrrrrr@{}}\n\\toprule\n & \\multicolumn{4}{c}{AI period: Dec 2022 to Sep 2026} & \\multicolumn{3}{c}{Full period: Jan 2018 to Sep 2026} \\\\\n\\cmidrule(lr){2-5}\\cmidrule(lr){6-8}\nFund & Return & Vol. & Ret./vol. & Max DD & Return & Vol. & Max DD \\\\\n\\midrule\n")
    for gname,members in groups:
        f.write("\\multicolumn{8}{@{}l}{\\textit{"+gname+"}} \\\\\n")
        for t,lab in members:
            n1,c1,a1,v1,s1,d1=stats(post,t); n2,c2,a2,v2,s2,d2=stats(full,t)
            note='$^{a}$' if t=='BITO' else ('$^{b}$' if t in ('AIQ','GRID') else '')
            shade="\\rowcolor{gray!18}" if gname=='AI-themed funds' else ""
            f.write(f"{shade}\\quad {lab} & {a1:.1f}\\% & {v1:.1f}\\% & {s1:.2f} & {d1:.0f}\\% & {a2:.1f}\\%{note} & {v2:.1f}\\% & {d2:.0f}\\% \\\\\n")
            res['e5'][t]=dict(post_ann=a1,post_vol=v1,post_dd=d1,full_ann=a2,full_vol=v2,full_dd=d2,n_full=n2)
        f.write("\\addlinespace[2pt]\n")
    f.write("\\bottomrule\n\\end{tabular}\n")

# ---------- Exhibit 6: sector composition by region ----------
sw=pd.read_csv(D+'sectors/ishares_sector_weights_2026-10-20.csv').set_index('sector')
groups=[('Information technology and communication services','Codified capabilities','Fast$^{*}$',['Information Technology','Communication']),
        ('Financials and health care','Institutional','Slow',['Financials','Health Care']),
        ('Industrials','Infrastructural and other','Mixed',['Industrials']),
        ('Energy, materials, utilities, real estate','Physical and infrastructural','Slow',['Energy','Materials','Utilities','Real Estate']),
        ('Consumer discretionary and staples','Other','Mixed',['Consumer Discretionary','Consumer Staples'])]
cols=['IVV_US','IEFA_DMexUS','IEMG_EM','ACWI_World']
# region weights in the world index: US weight of ACWI; developed share = US weight of ACWI / US weight of MSCI World (URTH); both iShares, Oct 20, 2026
us_acwi=64.67; us_world=72.93; dev=us_acwi/us_world*100; devex=dev-us_acwi; em=100-dev
region=[us_acwi,devex,em,100.0]
res['e6_sectors']={'groups':{},'region':dict(zip(['US','DevexUS','EM','World'],[round(x,1) for x in region]))}
with open(OUT+'exhibit6.tex','w') as f:
    f.write("\\begin{tabularx}{\\textwidth}{@{}>{\\raggedright\\arraybackslash}p{0.24\\textwidth}>{\\raggedright\\arraybackslash}X>{\\raggedright\\arraybackslash}p{0.065\\textwidth}rrrr@{}}\n\\toprule\n")
    f.write("Sector group & Layer & Pool & US & Dev. ex-US & Emerging & World \\\\\n & & & S\\&P 500 & MSCI EAFE & MSCI EM & MSCI ACWI \\\\\n\\midrule\n")
    slow=np.zeros(4)
    for name,layer,pool,secs in groups:
        v=[sw.loc[secs,c].sum() for c in cols]; res['e6_sectors']['groups'][name]=[round(x,1) for x in v]
        if pool=='Slow' or name=='Industrials': slow+=np.array(v)
        f.write(f"{name} & {layer} & {pool} & "+" & ".join(f"{x:.0f}\\%" for x in v)+" \\\\\n")
    res['e6_sectors']['slow']=[round(x,1) for x in slow]
    f.write("\\midrule\n")
    f.write("Slow-pool groups (second to fourth rows) & & & "+" & ".join(f"{x:.0f}\\%" for x in slow)+" \\\\\n")
    f.write("Weight of the region in the world index & & & "+" & ".join(f"{x:.0f}\\%" for x in region)+" \\\\\n")
    f.write("\\addlinespace\n\\multicolumn{7}{@{}p{\\textwidth}@{}}{\\textit{Five largest holdings.} US: Nvidia, Apple, Microsoft, Amazon, Alphabet. Developed ex-US: ASML, HSBC, Roche, Shell, Novartis. Emerging: TSMC, Samsung Electronics, SK hynix, Tencent, Alibaba.} \\\\\n")
    f.write("\\multicolumn{7}{@{}p{\\textwidth}@{}}{$^{*}$In emerging markets, mostly chip fabrication and memory, a slow pool.} \\\\\n")
    f.write("\\bottomrule\n\\end{tabularx}\n")
# ---------- Exhibit 8: admission, mortality, concentration ----------
import csv, collections, bisect
rows_=list(csv.DictReader(open(D+'sp500/sp500_ticker_start_end.csv')))
adds=collections.Counter(); rem=collections.Counter()
for r in rows_:
    if r['start_date'] and r['start_date']>'1996-01-02': adds[r['start_date'][:4]]+=1
    if r['end_date']: rem[r['end_date'][:4]]+=1
hist=list(csv.reader(open(D+'sp500/SandP_500_Historical_Components_and_Changes.csv')))
dates=[r[0] for r in hist[1:]]
alive=set(r['ticker'] for r in rows_ if not r['end_date'])
surv={}
for y in [2000,2005,2010,2015]:
    i=bisect.bisect_right(dates,f'{y}-12-31')-1; m=set(hist[1+i][1].split(',')); surv[y]=(len(m),len(m&alive))
dec={}
for dcd,(y0,y1) in {'1996-2000':(1996,2000),'2001-2005':(2001,2005),'2006-2010':(2006,2010),'2011-2015':(2011,2015),'2016-2020':(2016,2020),'2021-2025':(2021,2025)}.items():
    dec[dcd]=sum(adds[str(y)] for y in range(y0,y1+1))/ (y1-y0+1)
w=[float(r['weight']) for r in csv.DictReader(open(D+'weights/sp500_top274_slickcharts_2026-10-20.csv'))]
res['e6']=dict(adds_per_year=dec,survival=surv,top10=sum(w[:10]),top50=sum(w[:50]),vt_top10=22.45,vt_holdings=10242)
with open(OUT+'exhibit8.tex','w') as f:
    f.write("\\begin{tabular}{@{}lr@{}}\n\\toprule\nMeasure & Value \\\\\n\\midrule\n")
    ai=sum(adds[str(y)] for y in range(2023,2026))+adds['2026']; ai_rate=ai/(3+8/12)
    res['e6']['ai_replacements_per_year']=ai_rate
    f.write("\\multicolumn{2}{@{}l}{\\textit{Replacements in the S\\&P 500 per year, average}} \\\\\n")
    for k,v in dec.items(): f.write(f"\\quad {k} & {v:.0f} \\\\\n")
    f.write(f"\\quad AI period, 2023 to August 2026 & {ai_rate:.0f} \\\\\n")
    f.write("\\addlinespace\n\\multicolumn{2}{@{}l}{\\textit{Members at year-end still members in August 2026}} \\\\\n")
    for y,(n,s) in surv.items(): f.write(f"\\quad End of {y} & {s} of {n} ({100*s/n:.0f}\\%) \\\\\n")
    f.write("\\addlinespace\n\\multicolumn{2}{@{}l}{\\textit{Concentration, October 2026}} \\\\\n")
    f.write(f"\\quad S\\&P 500: weight of the ten largest & {sum(w[:10]):.1f}\\% \\\\\n\\quad S\\&P 500: weight of the fifty largest & {sum(w[:50]):.1f}\\% \\\\\n\\quad Global all-cap (VT, 10,242 stocks): weight of the ten largest & 22.4\\% \\\\\n")
    f.write("\\bottomrule\n\\end{tabular}\n")
# ---------- Exhibit 9: rate sensitivity ----------
y=pd.read_csv(D+'real10y_monthend.csv'); y['Year']=y.month.str[:4].astype(int); y['Month']=y.month.str[5:].astype(int)
dd=e.merge(y[['Year','Month','real10y']],on=['Year','Month']); dd['dr']=dd.real10y.diff()
res['e7']={}
with open(OUT+'exhibit9.tex','w') as f:
    f.write("\\begin{tabular}{@{}lrrrr@{}}\n\\toprule\nFund & Months & \\multicolumn{1}{p{3.6cm}}{\\raggedleft Return change per one-point rise in the real yield (\\%)} & $t$-statistic & $R^2$ \\\\\n\\midrule\n")
    g7=[('Broad capitalization-weighted indices',[('VT','Global all-cap (VT)'),('SPY','S\\&P 500 (SPY)')]),
        ('Alternative weightings and styles',[('RSP','S\\&P 500, equal-weighted (RSP)'),('VUG','US growth (VUG)'),('VTV','US value (VTV)')]),
        ('Bottleneck sleeves',[('SMH','Semiconductors (SMH)'),('XLU','US utilities (XLU)'),('GRID','Grid infrastructure (GRID)')]),
        ('Other assets',[('GLD','Gold (GLD)'),('BITO','Bitcoin (BITO)'),('TLT','Long Treasuries (TLT), for reference')])]
    for gname,members in g7:
        f.write("\\multicolumn{5}{@{}l}{\\textit{"+gname+"}} \\\\\n")
        for t,lab in members:
            s_=dd[[t,'dr']].dropna(); X=sm.add_constant(s_.dr); m=sm.OLS(s_[t],X).fit(cov_type='HAC',cov_kwds={'maxlags':3})
            f.write(f"\\quad {lab} & {len(s_)} & {m.params.dr:.1f} & {m.tvalues.dr:.1f} & {m.rsquared:.2f} \\\\\n"); res['e7'][t]=dict(beta=float(m.params.dr),t=float(m.tvalues.dr),r2=float(m.rsquared),n=len(s_))
        f.write("\\addlinespace[2pt]\n")
    f.write("\\bottomrule\n\\end{tabular}\n")
# ---------- Exhibit 10: inflation regimes ----------
h=pd.read_csv(D+'damodaran/histret_1928_2025.csv'); cpi=pd.read_csv(D+'cpi_us_monthly.csv'); cpi['Date']=pd.to_datetime(cpi['Date'])
dcm=cpi[cpi.Date.dt.month==12]; decidx=dcm.set_index(dcm.Date.dt.year)['Index']; infl=(decidx/decidx.shift(1)-1)*100
h['infl']=h.year.map(infl)
for c in ['sp500_total','tbill','tbond10','gold']: h['r_'+c]=((1+h[c]/100)/(1+h['infl']/100)-1)*100
def reg(x): return 'Deflation (below 0\\%)' if x<0 else ('0 to 2\\%' if x<2 else ('2 to 4\\%' if x<4 else 'Above 4\\%'))
h['regime']=h.infl.apply(reg); order=['Deflation (below 0\\%)','0 to 2\\%','2 to 4\\%','Above 4\\%']
g=h.groupby('regime'); g2=h[h.year>=1972].groupby('regime')
res['e8']={}
with open(OUT+'exhibit10.tex','w') as f:
    f.write("\\begin{tabular}{@{}lrrrrrr@{}}\n\\toprule\n & \\multicolumn{4}{c}{1928 to 2025} & \\multicolumn{2}{c}{1972 to 2025} \\\\\n\\cmidrule(lr){2-5}\\cmidrule(lr){6-7}\nInflation regime & Years & Stocks & T-bills & T-bonds & Years & Gold \\\\\n\\midrule\n")
    for r_ in order:
        gg=g.get_group(r_); n2=len(g2.get_group(r_)) if r_ in g2.groups else 0; gold=g2.get_group(r_).r_gold.mean() if n2 else float('nan')
        f.write(f"{r_} & {len(gg)} & {gg.r_sp500_total.mean():.1f}\\% & {gg.r_tbill.mean():.1f}\\% & {gg.r_tbond10.mean():.1f}\\% & {n2} & {('%.1f\\%%'%gold) if n2 else '--'} \\\\\n")
        res['e8'][r_]=dict(n=len(gg),stocks=gg.r_sp500_total.mean(),tbill=gg.r_tbill.mean(),tbond=gg.r_tbond10.mean(),n72=n2,gold=gold if n2 else None)
    f.write("\\bottomrule\n\\end{tabular}\n")
def _round(o):
    if isinstance(o,dict): return {str(k).replace('\\',''):_round(v) for k,v in o.items()}
    if isinstance(o,(list,tuple)): return [_round(v) for v in o]
    if isinstance(o,(float,np.floating)): return None if o!=o else round(float(o),4)
    if isinstance(o,np.integer): return int(o)
    return o
names={'e3':'exhibit5_roic_by_layer','e6_sectors':'exhibit6_sector_composition','e5':'exhibit7_fund_returns','e6':'exhibit8_membership_concentration','e7':'exhibit9_real_yield_sensitivity','e8':'exhibit10_inflation_regimes'}
out={names[k]:_round(res[k]) for k in names}
json.dump(out,open(OUT+'results.json','w'),indent=1,sort_keys=True)
print('wrote',OUT+'results.json')
