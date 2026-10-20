"""実験: α=1 固定、σ=t を [0, 1] で動かす（スライドの単純な選び方）。"""
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from common import load_x0, mix, save_clip_grid, save_png, stem_float
import numpy as np

HERE = Path(__file__).resolve().parent
OUT = HERE / "outputs"
T_VALUES = [0.0, 0.02, 0.05, 0.1, 0.2, 0.35, 0.5, 0.8, 1.0]


def main() -> None:
    x0 = load_x0()
    eps = np.random.default_rng(0).normal(0.0, 1.0, size=x0.shape)
    images, titles = [], []
    for t in T_VALUES:
        xt = mix(x0, alpha=1.0, sigma=t, eps=eps)
        images.append(xt)
        titles.append(f"t={t:g}\nα=1, σ={t:g}")
        save_png(OUT / f"{stem_float('linear', 't', t)}.png", xt)
    save_clip_grid(
        images,
        titles,
        OUT / "grid.png",
        r"vary-t-linear: $\alpha=1,\ \sigma=t$",
    )
    print(OUT / "grid.png")


if __name__ == "__main__":
    main()
