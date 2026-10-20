"""実験: 制限なし。α=1 固定、σ=t を 1 より大きくする。"""
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from common import load_x0, mix, save_clip_stretch_grid, save_png, stem_float
import numpy as np

HERE = Path(__file__).resolve().parent
OUT = HERE / "outputs"
T_VALUES = [0.0, 0.2, 0.5, 1.0, 2.0, 5.0, 10.0]


def main() -> None:
    x0 = load_x0()
    eps = np.random.default_rng(0).normal(0.0, 1.0, size=x0.shape)
    images, titles = [], []
    print(f"{'t':>6} {'α':>6} {'σ':>6} {'min':>8} {'max':>8} {'std':>8}")
    for t in T_VALUES:
        xt = mix(x0, alpha=1.0, sigma=t, eps=eps)
        images.append(xt)
        titles.append(f"t={t:g}")
        print(f"{t:6.1f} {1.0:6.1f} {t:6.1f} {xt.min():8.2f} {xt.max():8.2f} {xt.std():8.2f}")
        save_png(OUT / f"{stem_float('unrestricted', 't', t)}.png", xt)
    save_clip_stretch_grid(
        images,
        titles,
        OUT / "grid.png",
        r"unrestricted-t: $\alpha=1,\ \sigma=t$（上: clip / 下: stretch）",
    )
    print(OUT / "grid.png")


if __name__ == "__main__":
    main()
