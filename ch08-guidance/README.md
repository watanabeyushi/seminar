# 第8章 Guidance and Controllable Generation

論文 *The Principles of Diffusion Models* (arXiv:2510.21890) の第8章。
節ごとに `tex/` `slides/` `images/` `build/` を分け、完成PDFは章直下の `pdf/` にまとめます。

| フォルダ | 節 |
|----------|------|
| `8-1/` | 8.1 Prologue |
| `8-2/` | 8.2 Classifier Guidance |
| `8-3/` | 8.3 Classifier-Free Guidance |
| `8-4/` | 8.4 (Optional) Training-Free Guidance |
| `8-5/` | 8.5 From RL to DPO for Model Alignment |
| `8-6/` | 8.6 Closing Remarks |

コンパイル例（`8-1/tex/` で）:

```powershell
latexmk -lualatex -interaction=nonstopmode "-auxdir=..\build" "-outdir=..\..\pdf" "8-1.tex"
```
