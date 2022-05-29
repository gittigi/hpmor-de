#!/bin/sh

# based on work by yeKcim
# https://github.com/yeKcim/hpmor/tree/master/ebook

echo === 7. HTML -\> epub,mobi, doc ===

source_file="hpmor.html"
target_file="hpmor.epub"

# echo ==== 7.1 pandoc: html -\> epub====
# for some reason pandoc looses the css style of the html, so so trying calibre instead...

# pandoc --standalone --from=html $source_file -o $target_file

# pandoc --standalone --from=html $source_file -o $target_file --epub-embed-font="./fonts/automobile_contest/Automobile Contest.ttf" --epub-embed-font="./fonts/graphe/Graphe_Alpha_alt.ttf" --epub-embed-font="./fonts/Parseltongue/Parseltongue.ttf" --epub-embed-font="./fonts/graphe/Graphe_Alpha_alt.ttf" --epub-embed-font="./fonts/gabriele_bad_ah/gabriele-bad.ttf" 
#--css "./ebook/epub.css"


echo ==== 7.2 calibre: html -\> epub ====
ebook-convert $source_file $target_file --language de-DE --no-default-epub-cover --cover "ebook/tmp/title.jpg" --book-producer "Torben Menke"
# --no-default-epub-cover --cover tmp/title-en.jpg --authors "Eliezer Yudkowsky" --title "Harry Potter and the Methods of Rationality" --book-producer "Torben Menke" --pubdate 2015-03-14 --language en-US


source_file="hpmor.epub"
echo ==== 7.3 calibre: epub -\> mobi ====
target_file="hpmor.mobi"
ebook-convert $source_file $target_file

echo ==== 7.4 epub -\> docx ====
target_file="hpmor.docx"
ebook-convert $source_file $target_file
# pandoc --standalone $source_file -o $target_file
