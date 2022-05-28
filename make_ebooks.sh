#!/bin/sh

# LaTeX -> HTML
pandoc --standalone --from=latex hpmor-pandoc.tex -o hpmor.html

# remove pdf graphics
grep -v ".pdf" hpmor.html > hpmor-tmp.html
cp hpmor-tmp.html hpmor.html
rm hpmor-tmp.html

# add css format for \emph in \emph 
sed -i 's/\s*<\/style>/    em { font-style: italic;}\n    em em { font-style: normal;}\n    em em em { font-style: italic;}\n  <\/style>/' hpmor.html

pandoc --standalone --from=html hpmor.html -o hpmor.epub
pandoc --standalone --from=html hpmor.html -o hpmor.docx


# TODO
# cd ebook
# ./1_latex2html.py && ./2_html2epub.sh
