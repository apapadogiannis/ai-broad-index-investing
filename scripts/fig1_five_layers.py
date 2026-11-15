import os; OUT=os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),"figures"); os.makedirs(OUT,exist_ok=True)
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

plt.rcParams.update({"font.family": "serif", "font.serif": ["Latin Modern Roman", "DejaVu Serif"],
                     "mathtext.fontset": "cm", "font.size": 10})
layers = [("5. Jurisdictional", "High-capacity states, legal systems, fiscal regimes", "Slow pool", False),
          ("4. Institutional", "Regulation, licenses, data and model rights", "Slow pool", False),
          ("3. Capabilities: tacit", "Know-how, trust, brands, frontier talent", "Slow pool", False),
          ("3. Capabilities: codified", "Standard software, routine analysis", "Fast pool", True),
          ("2. Infrastructural", "Compute, chip plants, grids, data centers", "Slow pool", False),
          ("1. Physical", "Land, energy, water, critical minerals", "Slow pool", False)]

fig, ax = plt.subplots(figsize=(6.3, 2.9))
h, gap = 0.8, 0.14
for i, (name, ex, pool, fast) in enumerate(layers):
    y = (len(layers) - 1 - i) * (h + gap)
    face = "0.80" if fast else "#dbe6f6"
    ax.add_patch(FancyBboxPatch((0, y), 10, h, boxstyle="round,pad=0,rounding_size=0.08",
                                facecolor=face, edgecolor="none"))
    ax.text(0.2, y + h / 2, name, va="center", ha="left", fontsize=9.5, fontweight="bold")
    ax.text(4.25, y + h / 2, ex, va="center", ha="left", fontsize=9, color="0.25")
    ax.text(9.8, y + h / 2, pool, va="center", ha="right", fontsize=9.5)
ax.set_xlim(0, 10)
ax.set_ylim(-0.05, len(layers) * (h + gap) - gap + 0.05)
ax.axis("off")
fig.tight_layout(pad=0.2)
fig.savefig(os.path.join(OUT,"figure1_five_layers.pdf"))
fig.savefig(os.path.join(OUT,"figure1_five_layers.png"), dpi=150)
