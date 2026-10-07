# 各章の tex/ で latexmk を実行することを想定する。
# Workshop 側の -auxdir=../build -outdir=../pdf が優先される。
$pdf_mode = 4;
$lualatex = 'lualatex -interaction=nonstopmode -file-line-error %O %S';
$aux_dir = 'build';
$out_dir = 'pdf';
$clean_ext = 'synctex.gz nav snm vrb';
