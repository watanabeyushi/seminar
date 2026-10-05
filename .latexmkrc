# LuaLaTeX で日本語文書をビルドし、生成物を pdf フォルダにまとめる。
$pdf_mode = 4;
$lualatex = 'lualatex -interaction=nonstopmode -file-line-error %O %S';
$aux_dir = 'build';
$out_dir = 'pdf';

# latexmk -c で SyncTeX などの補助ファイルも削除する。
$clean_ext = 'synctex.gz nav snm vrb';
