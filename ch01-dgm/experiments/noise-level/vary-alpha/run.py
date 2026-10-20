"""実験: ノイズ σ と ε を固定し、α だけを変える。"""
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from common import load_x0, mix, save_clip_stretch_grid, save_png, stem_float
import numpy as np

HERE = Path(__file__).resolve().parent
OUT = HERE / "outputs"
SIGMA = 0.3
ALPHAS = [0.0, 0.25, 0.5, 1.0, 1.5, 2.0, 3.0]


def main() -> None:
    x0 = load_x0()
    eps = np.random.default_rng(0).normal(0.0, 1.0, size=x0.shape)
    images, titles = [], []
    print(f"{'α':>6} {'σ':>6} {'min':>8} {'max':>8} {'std':>8}")
    for alpha in ALPHAS:
        xt = mix(x0, alpha=alpha, sigma=SIGMA, eps=eps)
        images.append(xt)
        titles.append(f"α={alpha:g}")
        print(f"{alpha:6.2f} {SIGMA:6.2f} {xt.min():8.2f} {xt.max():8.2f} {xt.std():8.2f}")
        save_png(OUT / f"{stem_float('alpha', 'a', alpha)}.png", xt)
    save_clip_stretch_grid(
        images,
        titles,
        OUT / "grid.png",
        rf"vary-alpha: $\sigma={SIGMA}$ 固定、$\varepsilon$ も固定（上: clip / 下: stretch）",
    )
    print(OUT / "grid.png")


if __name__ == "__main__":
    main()
