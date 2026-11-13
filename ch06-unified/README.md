# 第6章 A Unified and Systematic Lens on Diffusion Models

論文 *The Principles of Diffusion Models* (arXiv:2510.21890) の第6章。
節ごとに `tex/` `slides/` `images/` `build/` を分け、完成PDFは章直下の `pdf/` にまとめます。

| フォルダ | 節 |
|----------|------|
| `6-1/` | 6.1 Conditional Tricks: The Secret Sauce of Diffusion Models |
| `6-2/` | 6.2 A Roadmap for Elucidating Training Losses in Diffusion Models |
| `6-3/` | 6.3 Equivalence in Diffusion Models |
| `6-4/` | 6.4 Beneath It All: The Fokker–Planck Equation |
| `6-5/` | 6.5 Closing Remarks |

コンパイル例（`6-1/tex/` で）:

```powershell
latexmk -lualatex -interaction=nonstopmode "-auxdir=..\build" "-outdir=..\..\pdf" "6-1.tex"
```
