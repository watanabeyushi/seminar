# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.patches import FancyBboxPatch, Circle
from pathlib import Path

out = Path(__file__).resolve().parent

# Prefer Windows JP fonts
candidates = [
    r"C:\Windows\Fonts\YuGothM.ttc",
    r"C:\Windows\Fonts\meiryo.ttc",
    r"C:\Windows\Fonts\msgothic.ttc",
    r"C:\Windows\Fonts\segoeui.ttf",
]
font_path = next((p for p in candidates if Path(p).exists()), None)
if font_path:
    font_manager.fontManager.addfont(font_path)
    prop = font_manager.FontProperties(fname=font_path)
    plt.rcParams["font.family"] = prop.get_name()
plt.rcParams["axes.unicode_minus"] = False

# ---------- 1) magnitude ----------
fig, axes = plt.subplots(1, 2, figsize=(10.5, 4.2))
x = np.linspace(-3.2, 3.2, 400)
p = np.exp(-0.5 * x**2) / np.sqrt(2 * np.pi)
s2 = 0.8 + 0.15 * x**2
weighted = p * s2

ax = axes[0]
ax.fill_between(x, p, color="#4C78A8", alpha=0.35)
ax.plot(x, p, color="#4C78A8", lw=2)
ax.set_title(r"データ密度 $p_{\mathrm{data}}(x)$", fontsize=12)
ax.set_xlabel(r"$x$")
ax.set_ylabel("密度")
ax.set_ylim(0, p.max() * 1.15)
ax.annotate(
    "ここが重い\n（サンプルが多い）",
    xy=(0, p.max()),
    xytext=(1.2, p.max() * 0.85),
    arrowprops=dict(arrowstyle="->", color="#333"),
    fontsize=10,
)

ax = axes[1]
ax.fill_between(x, weighted, color="#F58518", alpha=0.35)
ax.plot(x, weighted, color="#F58518", lw=2, label=r"$p\,\|s\|^2$")
ax.plot(x, 0.35 * s2, color="#999", lw=1.5, ls="--", label=r"$\|s\|^2$（参考）")
ax.set_title(r"大きさの項の実効寄与 $p_{\mathrm{data}}\|s\|^2$", fontsize=12)
ax.set_xlabel(r"$x$")
ax.set_ylabel("重み付き寄与")
ax.legend(loc="upper right", fontsize=9)
ax.annotate(
    "同じ $\|s\|^2$ でも\n山の下ほど損失に効く",
    xy=(0, weighted.max()),
    xytext=(1.1, weighted.max() * 0.7),
    arrowprops=dict(arrowstyle="->", color="#333"),
    fontsize=10,
)

fig.suptitle(
    r"大きさの項：期待値は $p_{\mathrm{data}}$ で取るので高密度ほど強く罰する",
    fontsize=13,
    y=1.02,
)
fig.tight_layout()
fig.savefig(out / "esm-magnitude.png", dpi=180, bbox_inches="tight", facecolor="white")
plt.close()

# ---------- 2) divergence ----------
fig, axes = plt.subplots(1, 2, figsize=(10.5, 4.4))
xs = np.linspace(-2.2, 2.2, 11)
ys = np.linspace(-2.2, 2.2, 11)
X, Y = np.meshgrid(xs, ys)
Ux_sink, Uy_sink = -X, -Y
Ux_src, Uy_src = X, Y

for ax, Ux, Uy, title, note, color in [
    (axes[0], Ux_sink, Uy_sink, "吸い込み（収縮）", r"$\mathrm{div}\,s < 0$", "#2E7D32"),
    (axes[1], Ux_src, Uy_src, "湧き出し（膨張）", r"$\mathrm{div}\,s > 0$", "#C62828"),
]:
    ax.quiver(X, Y, Ux, Uy, color=color, angles="xy", scale_units="xy", scale=4.5, width=0.006)
    ax.add_patch(Circle((0, 0), 0.35, fill=False, ec=color, lw=2, ls="--"))
    ax.set_aspect("equal")
    ax.set_xlim(-2.4, 2.4)
    ax.set_ylim(-2.4, 2.4)
    ax.set_title(title, fontsize=13, color=color)
    ax.text(
        0,
        -2.05,
        note,
        ha="center",
        fontsize=12,
        color=color,
        bbox=dict(boxstyle="round,pad=0.3", fc="white", ec=color, alpha=0.9),
    )
    ax.set_xticks([])
    ax.set_yticks([])
    for spine in ax.spines.values():
        spine.set_alpha(0.3)

fig.suptitle(
    r"発散項：損失に $+\mathrm{Tr}(\nabla s)$ が入るので、最小化は左（収縮）を好む",
    fontsize=13,
    y=1.02,
)
fig.tight_layout()
fig.savefig(out / "esm-divergence.png", dpi=180, bbox_inches="tight", facecolor="white")
plt.close()

# ---------- 3) why optimal ----------
fig, ax = plt.subplots(figsize=(10.8, 3.6))
ax.set_xlim(0, 10)
ax.set_ylim(0, 3.2)
ax.axis("off")
boxes = [
    (0.3, 1.1, 2.8, 1.4, "真の目的\nSM: E∥sφ−s∥²\ns=∇log p_data", "#1565C0"),
    (3.6, 1.1, 2.8, 1.4, "命題より\nL_SM = L_eSM + C\nC は φ 無関係", "#6A1B9A"),
    (6.9, 1.1, 2.8, 1.4, "同じ最小化子\ns★ = ∇log p_data", "#2E7D32"),
]
for x0, y0, w, h, text, c in boxes:
    ax.add_patch(
        FancyBboxPatch(
            (x0, y0),
            w,
            h,
            boxstyle="round,pad=0.05,rounding_size=0.15",
            facecolor=c,
            edgecolor="none",
            alpha=0.9,
        )
    )
    ax.text(x0 + w / 2, y0 + h / 2, text, ha="center", va="center", color="white", fontsize=11)

for x in [3.15, 6.45]:
    ax.annotate(
        "",
        xy=(x + 0.4, 1.8),
        xytext=(x, 1.8),
        arrowprops=dict(arrowstyle="->", lw=2.2, color="#333"),
    )

ax.text(
    5,
    0.45,
    "だから eSM だけ見えても、最小化すれば真のスコアに到達する",
    ha="center",
    fontsize=12,
    bbox=dict(boxstyle="round,pad=0.4", fc="#FFF8E1", ec="#F9A825"),
)
fig.tight_layout()
fig.savefig(out / "esm-why-optimal.png", dpi=180, bbox_inches="tight", facecolor="white")
plt.close()
print("OK", list(out.glob("esm-*.png")))
