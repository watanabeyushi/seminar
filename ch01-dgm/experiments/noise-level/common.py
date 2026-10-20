"""x_t = α x_0 + σ ε の実験で共通する処理。"""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parent
IMAGE_DIR = ROOT / "images"

plt.rcParams["font.family"] = ["Yu Gothic", "Meiryo", "MS Gothic", "sans-serif"]
plt.rcParams["axes.unicode_minus"] = False


def make_demo_image(size: int = 256) -> np.ndarray:
    y, x = np.mgrid[0:size, 0:size]
    img = np.zeros((size, size, 3), dtype=np.float64)
    img[..., 0] = x / (size - 1)
    img[..., 1] = y / (size - 1)
    img[..., 2] = 1.0 - 0.5 * img[..., 0] - 0.5 * img[..., 1]

    cy, cx = size // 2, size // 2
    rr = ((y - cy) ** 2 + (x - cx) ** 2) < (size * 0.18) ** 2
    img[rr] = np.array([0.95, 0.85, 0.15])

    square = (x > size * 0.12) & (x < size * 0.32) & (y > size * 0.12) & (y < size * 0.32)
    img[square] = np.array([0.15, 0.35, 0.90])

    stripe = (np.abs((x + y) % 40 - 20) < 4) & (y > size * 0.62)
    img[stripe] = np.array([0.05, 0.05, 0.05])
    return np.clip(img, 0.0, 1.0)


def load_x0(path: Path | None = None) -> np.ndarray:
    IMAGE_DIR.mkdir(parents=True, exist_ok=True)
    if path is None:
        path = IMAGE_DIR / "demo.png"
    if path.exists():
        return np.asarray(Image.open(path).convert("RGB"), dtype=np.float64) / 255.0
    x0 = make_demo_image()
    Image.fromarray((x0 * 255).astype(np.uint8)).save(IMAGE_DIR / "demo.png")
    return x0


def mix(x0: np.ndarray, alpha: float, sigma: float, eps: np.ndarray) -> np.ndarray:
    return alpha * x0 + sigma * eps


def save_png(path: Path, img: np.ndarray) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    Image.fromarray((np.clip(img, 0.0, 1.0) * 255).astype(np.uint8)).save(path)


def stem_float(prefix: str, name: str, value: float) -> str:
    return f"{prefix}_{name}{str(value).replace('.', 'p')}"


def save_clip_grid(
    images: list[np.ndarray],
    titles: list[str],
    out_path: Path,
    suptitle: str,
) -> None:
    n = len(images)
    cols = min(5, n)
    rows = int(np.ceil(n / cols))
    fig, axes = plt.subplots(rows, cols, figsize=(3.2 * cols, 3.4 * rows))
    axes = np.atleast_1d(axes).ravel()
    for ax, img, title in zip(axes, images, titles):
        ax.imshow(np.clip(img, 0.0, 1.0))
        ax.set_title(title, fontsize=10)
        ax.axis("off")
    for ax in axes[n:]:
        ax.axis("off")
    fig.suptitle(suptitle, fontsize=13)
    fig.tight_layout()
    out_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out_path, dpi=150, bbox_inches="tight")
    plt.close(fig)


def save_clip_stretch_grid(
    images: list[np.ndarray],
    titles: list[str],
    out_path: Path,
    suptitle: str,
) -> None:
    n = len(images)
    fig, axes = plt.subplots(2, n, figsize=(3.0 * n, 6.4))
    if n == 1:
        axes = np.array(axes).reshape(2, 1)
    for col, (img, title) in enumerate(zip(images, titles)):
        axes[0, col].imshow(np.clip(img, 0.0, 1.0))
        axes[0, col].set_title(f"clip  {title}")
        axes[0, col].axis("off")
        lo, hi = img.min(), img.max()
        axes[1, col].imshow((img - lo) / (hi - lo + 1e-12))
        axes[1, col].set_title(f"stretch  [{lo:.1f},{hi:.1f}]")
        axes[1, col].axis("off")
    fig.suptitle(suptitle)
    fig.tight_layout()
    out_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out_path, dpi=150, bbox_inches="tight")
    plt.close(fig)
