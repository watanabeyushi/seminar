"""実験: 分散一定 α²+σ²=1。σ=t、α=√(1-t²)。"""
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from common import load_x0, mix, save_clip_grid, save_png, stem_float
import numpy as np

HERE = Path(__file__).resolve().parent
OUT = HERE / "outputs"
T_VALUES = [0.0, 0.1, 0.2, 0.4, 0.6, 0.8, 0.95, 1.0]


def main() -> None:
    x0 = load_x0()
    eps = np.random.default_rng(0).normal(0.0, 1.0, size=x0.shape)
    images, titles = [], []
    for t in T_VALUES:
        alpha = float(np.sqrt(1.0 - t * t))
        xt = mix(x0, alpha=alpha, sigma=t, eps=eps)
        images.append(xt)
        titles.append(f"t={t:g}\nα={alpha:.3f}, σ={t:g}")
        save_png(OUT / f"{stem_float('vp', 't', t)}.png", xt)
    save_clip_grid(
        images,
        titles,
        OUT / "grid.png",
        r"vary-t-vp: $\alpha^2+\sigma^2=1$",
    )
    print(OUT / "grid.png")


if __name__ == "__main__":
    main()
