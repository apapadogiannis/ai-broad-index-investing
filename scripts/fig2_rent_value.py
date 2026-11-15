import os; OUT=os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),"figures"); os.makedirs(OUT,exist_ok=True)
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

plt.rcParams.update({"font.family": "serif", "font.serif": ["Latin Modern Roman", "DejaVu Serif"],
                     "mathtext.fontset": "cm", "font.size": 10})
rg = 0.03
d = np.linspace(0.02, 0.60, 400)
v = 1.0 / (rg + d)

fig, ax = plt.subplots(figsize=(6.3, 3.3))
ax.plot(d * 100, v, color="0.55", lw=1.6)
pools = [("Slow pool", 0.05, "#1f5fbf", (8, 4)),
         ("Fast pool", 0.22, "0.45", (6, 8)),
         ("Fast pool after AI", 0.47, "0.45", (4, 9))]
for name, dd, col, off in pools:
    val = 1.0 / (rg + dd)
    ax.plot([dd * 100, dd * 100], [0, val], color="0.8", lw=0.8, ls=(0, (3, 3)))
    ax.plot(dd * 100, val, "o", color=col, ms=7, zorder=3)
    ax.annotate(f"{name}: \\${val:.2f}", (dd * 100, val), xytext=off, textcoords="offset points",
                ha="left", va="bottom")
ax.text(11.5, 9.6, r"$\leftarrow$ A3: rents migrate toward slow pools", color="0.3", fontsize=9)
ax.text(27.0, 7.3, r"A1: AI raises decay in fast pools $\rightarrow$", color="0.3", fontsize=9)
ax.set_xlim(0, 60); ax.set_ylim(0, 21)
ax.set_xticks(range(0, 61, 10)); ax.set_xticklabels([f"{t}%" for t in range(0, 61, 10)])
ax.set_yticks([0, 5, 10, 15, 20]); ax.set_yticklabels([f"\\${t}" for t in [0, 5, 10, 15, 20]])
ax.set_xlabel("Decay rate per year"); ax.set_ylabel("Value today of \\$1 per year of rent")
for s in ("top", "right"):
    ax.spines[s].set_visible(False)
fig.tight_layout()
fig.savefig(os.path.join(OUT,"figure2_rent_value.pdf"))
fig.savefig(os.path.join(OUT,"figure2_rent_value.png"), dpi=150)
