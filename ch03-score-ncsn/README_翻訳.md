# 第3章 日本語訳

`翻訳/` 直下は **PDF のみ**です。原稿・TeX・図・英語原文は各節フォルダ内にあります。

## 配置

```
翻訳/
  3-1.pdf ... 3-6.pdf          ← 閲覧用
  3-1/
    3-1.md / 3-1.tex / 3-1.en.txt / images/ / build/
  ...
```

## 再生成（ワークスペース直下）

```powershell
python _md_to_tex.py
python _compile_translation_pdfs.py 3-2
```
