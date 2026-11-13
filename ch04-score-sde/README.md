# 第4章 Diffusion Models Today: Score SDE Framework

論文 *The Principles of Diffusion Models* (arXiv:2510.21890) の第4章。
節ごとに `tex/` `slides/` `images/` `build/` を分け、完成PDFは章直下の `pdf/` にまとめます。

フォルダ番号は既存構成に合わせています（論文の 4.2 Matching Marginals は 4-1 に含める）。

| フォルダ | スライド題 | 論文の節 |
|----------|------------|----------|
| `4-1/` | 4.1 Score SDE: Its Principles | 4.1 +（要点）4.2 |
| `4-2/` | 4.2 Score SDE: Its Training and Sampling | 4.3 |
| `4-3/` | 4.3 Instantiations of SDEs | 4.4 |
| `4-4/` | 4.4 (Optional) Forward Kernels | 4.5 |
| `4-5/` | 4.5 (Optional) Fokker–Planck and Reverse SDE | 4.6 |
| `4-6/` | 4.6 Closing Remarks | 4.7 |

完成PDFの場所: `ch04-score-sde/pdf/`（例: `pdf/4-1.pdf`）。

コンパイル例（`4-1/tex/` で）:

```powershell
latexmk -lualatex -interaction=nonstopmode "-auxdir=..\build" "-outdir=..\..\pdf" "4-1.tex"
```

Cursor / LaTeX Workshop ではレシピ **latexmk (section)** が既定です（第1・2章のフラット構成は `% !LW recipe = latexmk (flat)`）。
