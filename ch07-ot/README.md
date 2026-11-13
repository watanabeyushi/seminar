# 第7章 (Optional) Diffusion Models and Optimal Transport

論文 *The Principles of Diffusion Models* (arXiv:2510.21890) の第7章。
節ごとに `tex/` `slides/` `images/` `build/` を分け、完成PDFは章直下の `pdf/` にまとめます。

| フォルダ | 節 |
|----------|------|
| `7-1/` | 7.1 Prologue of Distribution-to-Distribution Translation |
| `7-2/` | 7.2 Taxonomy of the Problem Setups |
| `7-3/` | 7.3 Relationship of Variant Optimal Transport Formulations |
| `7-4/` | 7.4 Is Diffusion Model’s SDE Optimal Solution to SB Problem? |
| `7-5/` | 7.5 Is Diffusion Model’s ODE an Optimal Map to OT Problem? |
| `7-6/` | 7.6 Closing Remarks |

コンパイル例（`7-1/tex/` で）:

```powershell
latexmk -lualatex -interaction=nonstopmode "-auxdir=..\build" "-outdir=..\..\pdf" "7-1.tex"
```
