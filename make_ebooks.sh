#!/bin/sh



title=$(grep "pdftitle=" layout/hp-header.tex | awk -F '[{}]' '{print $2}')
author=$(grep "pdfauthor=" layout/hp-header.tex | awk -F '[{}]' '{print $2}')
# TODO: Deutsche Version
title="$title - Deutsche Fan-Übersetzung"

# script_dir=$(cd `dirname $0` && pwd)
# cd $script_dir/..

# TODO:images

# prepare .tex file for html

# insert files to load
# sed '3i\\\input{layout/hp-format}\n\\input{layout/hp-markup}\n\\usepackage{polyglossia}\n\\setmainlanguage{german}\n\\setdefaultlanguage[spelling = new]{german}' hpmor.tex > hpmor_epub.tex
sed '3i\\\usepackage{polyglossia}\n\\setmainlanguage{german}\n\\setdefaultlanguage[spelling = new]{german}\n' hpmor.tex > hpmor_epub.tex
sed -i '8i\\\input{layout/hp-format}\n\\input{layout/hp-markup}\n' hpmor_epub.tex
# remove loading of hp-contents file
sed -i '/\\\input{hp-contents}/d' hpmor_epub.tex

# overwrite the headlines env, since it makes problems in pandoc
sed -i '10i\\\renewenvironment{headlines}{\\begin{scshape}\\scshape}{\\end{scshape}}\n' hpmor_epub.tex
# sed -i '/\\begin{headlines}/d ; /\\end{headlines}/d' hpmor_flatten.tex		# TODO: \headlines (can't generate epub)

# exit


# # flatten the .tex files to one file
latexpand hpmor_epub.tex -o hpmor_flatten.tex



sed -i 's/\\parsela{#1}/\\parselb{#1}/' hpmor_flatten.tex

# # Cant find a way to add directly font or class name in span… ⇒ hack: add color → class
sed -i 's/{Parseltongue.ttf}#1}/{Parseltongue.ttf}\\textcolor{YellowOrange}{#1}}/g' hpmor_flatten.tex
sed -i 's/{gabriele-bad.ttf}#1}/{gabriele-bad.ttf}\\textcolor{YellowGreen}{#1}}/g' hpmor_flatten.tex
sed -i 's/\\textcolor{blue}{\\Huge{\\underline{\\textcolor{red}{#1}}}}/\\textcolor{red}{#1}/g' hpmor_flatten.tex

sed -i 's/\\vskip .1\\baselineskip plus .1\\baselineskip minus .1\\baselineskip//g' hpmor_flatten.tex
sed -i 's/\\vskip 1\\baselineskip plus 1\\baselineskip minus 1\\baselineskip//g' hpmor_flatten.tex
sed -i 's/\\vskip 0pt plus 2//g' hpmor_flatten.tex

sed -i 's/\\begin{align\*}//g ; s/\\end{align\*}//g ; s/ }&\\hbox{/ }\\hbox{/g' hpmor_flatten.tex

sed -i 's/\\hplettrineextrapara//g' hpmor_flatten.tex

sed -i '/^\\def{\\ifnum\\prevgraf/,/^\\fi}/d;' hpmor_flatten.tex 


# LaTeX -> HTML
# TODO: hpmor_flatten.tex 
pandoc --standalone --from=latex+latex_macros hpmor_flatten.tex -o hpmor.html --metadata title="$title" --metadata author="$author"

# # modifications
sed -i 's/<span style=\"color: YellowOrange\">/<span class=\"parsel\">/g' hpmor.html
sed -i 's/<span style=\"color: YellowGreen\">/<span class=\"headline\">/g' hpmor.html
sed -i 's/<span style=\"color: red\">/<span class=\"mcgonagallboard\">/g' hpmor.html

# TODO: this causes trouble
# sed -i '/<p>‘ ‘ ‘ ‘ ‘̇ ‘  ‘ ‘ ‘ ‘<\/p>/,/bubble.png/d' hpmor.html

# remove pdf graphics
grep -v ".pdf" hpmor.html > hpmor-tmp.html
cp hpmor-tmp.html hpmor.html
rm hpmor-tmp.html

# alternatively via -c and css file
# add css format for \emph in \emph 
sed -i 's/\s*<\/style>/    em { font-style: italic;}\n    em em { font-style: normal;}\n    em em em { font-style: italic;}\n  <\/style>/' hpmor.html

# pandoc --standalone --from=html hpmor.html -o hpmor.epub 

pandoc --standalone --from=html hpmor.html -o hpmor.epub --epub-embed-font="./fonts/automobile_contest/Automobile Contest.ttf" --epub-embed-font="./fonts/graphe/Graphe_Alpha_alt.ttf" --epub-embed-font="./fonts/Parseltongue/Parseltongue.ttf" --epub-embed-font="./fonts/graphe/Graphe_Alpha_alt.ttf" --epub-embed-font="./fonts/gabriele_bad_ah/gabriele-bad.ttf" --css "./ebook/2epub.css"

pandoc --standalone hpmor.epub -o hpmor.docx


# # TODO
# # cd ebook
# # ./1_latex2html.py && ./2_html2epub.sh

# rm -f hpmor_epub.tex hpmor_flatten.tex
