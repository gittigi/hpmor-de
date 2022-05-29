#!/bin/sh

# based on work by yeKcim
# https://github.com/yeKcim/hpmor/tree/master/ebook

echo === 5. HTML modifications ===

# ensure we are in the hpmor root dir
script_dir=$(cd `dirname $0` && pwd)
cd $script_dir/..

source_file="hpmor-epub-4-html-1.html"
target_file="hpmor-epub-5-html-2.html"
cp $source_file $target_file

# cleanup of title/header leftovers: # <p>‘ ‘ ‘ ‘ ‘̇ ‘  ‘ ‘ ‘ ‘</p>
# -z changes the delimiter to null characters (\0)
sed -i -z 's/<\/header>.*<p>HARRY POTTER<\/p>/<\/header>\n<p>HARRY POTTER<\/p>/' $target_file

# TODO: this causes trouble
# sed -i '/<p>‘ ‘ ‘ ‘ ‘̇ ‘  ‘ ‘ ‘ ‘<\/p>/,/bubble.png/d' hpmor.html

sed -i 's/<div style=\"color: YellowBlue\">/<div class=\"writtenNote\">/g' $target_file
sed -i 's/<span style=\"color: YellowBlue\">/<span class=\"writtenNote\">/g' $target_file
sed -i 's/<span style=\"color: YellowOrange\">/<span class=\"parsel\">/g' $target_file
sed -i 's/<div style=\"color: YellowOrange\">/<div class=\"parsel\">/g' $target_file
sed -i 's/<span style=\"color: YellowGreen\">/<span class=\"headline\">/g' $target_file
sed -i 's/<span style=\"color: YellowRed\">/<span class=\"mcgonagallboard\">/g' $target_file

# add css format for \emph in \emph 
# alternatively via -c and css file

sed -i -e '/<style/r ebook/epub.css' $target_file

# remove pdf graphics
grep -v ".pdf" $target_file > "$target_file.tmp"
cp "$target_file.tmp" $target_file
rm "$target_file.tmp"


cp $target_file hpmor.html