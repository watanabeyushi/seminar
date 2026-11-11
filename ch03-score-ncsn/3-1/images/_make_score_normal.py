import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

plt.rcParams["font.family"] = "DejaVu Sans"
plt.rcParams["axes.unicode_minus"] = False
plt.rcParams["mathtext.fontset"] = "cm"

out = Path(__file__).with_name("score-standard-normal.png")

x = np.linspace(-3.5, 3.5, 500)
p = np.exp(-0.5 * x**2) / np.sqrt(2 * np.pi)
s = -x

fig, axes = plt.subplots(
    2,
    1,
    figsize=(7.6, 4.4),
    sharex=True,
    gridspec_kw={"height_ratios": [1.2, 1.0], "hspace": 0.18},
)

ax = axes[0]
ax.fill_between(x, p, color="#1e468c", alpha=0.18)
ax.plot(x, p, color="#1e468c", lw=2.5, label=r"$p(x)$")
pts = np.array([-2.0, -1.0, 0.0, 1.0, 2.0])
ax.scatter(pts, np.exp(-0.5 * pts**2) / np.sqrt(2 * np.pi), color="#1e468c", s=36, zorder=5)
ax.axvline(0, color="#1e468c", ls="--", lw=1.0, alpha=0.5)
ax.set_ylabel(r"$p(x)$", fontsize=12)
ax.set_ylim(0, 0.48)
ax.set_xlim(-3.5, 3.5)
ax.legend(loc="upper right", frameon=False, fontsize=11)
ax.set_title(r"Standard normal  $p(x)=\frac{1}{\sqrt{2\pi}}e^{-x^{2}/2}$", fontsize=12, pad=3)
ax.grid(True, alpha=0.25)

ax = axes[1]
ax.axhline(0, color="black", lw=1.0)
ax.plot(x, s, color="#1e7880", lw=2.3, label=r"$s(x)=-x$")
for xi in [-2.5, -1.5, -0.8, 0.8, 1.5, 2.5]:
    dx = -0.55 * np.sign(xi)
    ax.annotate(
        "",
        xy=(xi + dx, 0.0),
        xytext=(xi, 0.0),
        arrowprops=dict(arrowstyle="->", color="#c85028", lw=2.1, mutation_scale=15),
    )
ax.scatter([0], [0], color="#c85028", s=48, zorder=6)
ax.text(0.18, 0.7, r"$s(0)=0$", color="#c85028", fontsize=11)
ax.text(-2.9, 1.4, r"$s>0$ (right)", color="#c85028", fontsize=10)
ax.text(1.7, -1.6, r"$s<0$ (left)", color="#c85028", fontsize=10)
ax.set_ylabel(r"$s(x)$", fontsize=12)
ax.set_xlabel(r"$x$", fontsize=12)
ax.set_ylim(-3.0, 3.0)
ax.legend(loc="upper right", frameon=False, fontsize=11)
ax.set_title(r"Score $s(x)=-x$: arrows always point to the mode $x=0$", fontsize=12, pad=3)
ax.grid(True, alpha=0.25)

fig.savefig(out, dpi=220, bbox_inches="tight", facecolor="white")
print("saved", out)
