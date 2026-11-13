# 第5章 Flow-Based Perspective: From NFs to Flow Matching

論文 *The Principles of Diffusion Models* (arXiv:2510.21890) の第5章。
節ごとに `tex/` `slides/` `images/` `build/` を分け、完成PDFは章直下の `pdf/` にまとめます。

| フォルダ | 節 |
|----------|------|
| `5-1/` | 5.1 Flow-Based Models: Normalizing Flows and Neural ODEs |
| `5-2/` | 5.2 Flow Matching Framework |
| `5-3/` | 5.3 Constructing Probability Paths and Velocities |
| `5-4/` | 5.4 (Optional) Properties of the Canonical Affine Flow |
| `5-5/` | 5.5 Closing Remarks |

コンパイル例（`5-1/tex/` で）:

```powershell
latexmk -lualatex -interaction=nonstopmode "-auxdir=..\build" "-outdir=..\..\pdf" "5-1.tex"
```
