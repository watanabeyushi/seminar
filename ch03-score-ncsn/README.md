# 第3章 Score-Based Perspective: From EBMs to NCSN

論文 *The Principles of Diffusion Models* (arXiv:2510.21890) の第3章。
節ごとに `tex/` `slides/` `images/` `build/` を分け、完成PDFは章直下の `pdf/` にまとめます。

| フォルダ | 節 |
|----------|------|
| `3-1/` | 3.1 Energy-Based Models（現行スライド） |
| `3-2/` | 3.2 From Energy-Based to Score-Based Generative Models |
| `3-3/` | 3.3 Denoising Score Matching |
| `3-4/` | 3.4 Multi-Noise Levels of Denoising Score Matching (NCSN) |
| `3-5/` | 3.5 Summary: A Comparative View of NCSN and DDPM |
| `3-6/` | 3.6 Closing Remarks |

完成PDFの場所: `ch03-score-ncsn/pdf/`（例: `pdf/3-1.pdf`）。

コンパイル例（`3-1/tex/` で）:

```powershell
latexmk -lualatex -interaction=nonstopmode "-auxdir=..\build" "-outdir=..\..\pdf" "3-1.tex"
```

Cursor / LaTeX Workshop ではレシピ **latexmk (section)** が既定です（第1・2章のフラット構成は各 `tex/*.tex` 先頭の `% !LW recipe = latexmk (flat)`）。
