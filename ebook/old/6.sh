#!/bin/sh

# based on work by yeKcim
# https://github.com/yeKcim/hpmor/tree/master/ebook

echo === 6. HTML modifications ===

# ensure we are in the hpmor root dir
script_dir=$(cd `dirname $0` && pwd)
cd $script_dir/..

source_file="hpmor-epub-5-html-1.html"
target_file="hpmor-epub-6-html-2.html"
# and hpmor.html : cp $target_file hpmor.html see below

cp $source_file $target_file

# remove strange leftovers between header and Disclaimer "Dies ist ein OpenSource Projekt..."
# -z changes the delimiter to null characters (\0)
# sed -i -z 's/<\/header>.*<p>HARRY POTTER<\/p>/<\/header>\n<p>HARRY POTTER<\/p>/' $target_file
# for some strange reason the "<" is lost and needs to be added manually
# sed -i -z 's|\(\<\header>\).*\(\<p>Dies ist ein\)|\1\n<\2|' $target_file
sed -i -z 's|\(\<\header>\).*\(\<p>Basierend\)|\1<p>Fanfiction basierend|' $target_file

# doc structure (not needed any more, using calibi --level1-toc flag instead)
# sed -i 's/<h1 /<h1 class="part"/g' $target_file
# sed -i 's/<h2 /<h2 class="chapter"/g' $target_file
# sed -i 's/<h3 /<h3 class="section"/g' $target_file

# remove ids from chapters since umlaute make problems here
sed -i 's/\<h2 id="[^"]+"/<h2/g' $target_file

# fix double rules
sed -i -z 's|<hr />\n<hr />|<hr />|g' $target_file

# fixing linebreak at author's comment
sed -i -z 's|<p>E. Y.: </p>\n<p>|E.Y.: |g' $target_file



# converting "color-marked" styles back to proper style classes
sed -i 's/<div style=\"color: ColorWrittenNote\">/<div class=\"writtenNote\">/g' $target_file
sed -i 's/<span style=\"color: ColorWrittenNote\">/<span class=\"writtenNote\">/g' $target_file
sed -i 's/<span style=\"color: ColorParsel\">/<span class=\"parsel\">/g' $target_file
sed -i 's/<div style=\"color: ColorParsel\">/<div class=\"parsel\">/g' $target_file
sed -i 's/<span style=\"color: ColorHeadline\">/<span class=\"headline\">/g' $target_file
sed -i 's/<span style=\"color: ColorMcGonagallWhiteBoard\">/<span class=\"McGonagallWhiteBoard\">/g' $target_file

# add css style file format for \emph in \emph 
sed -i -e '/<style/r ebook/html.css' $target_file

# remove pdf graphics
grep -v ".pdf" $target_file > "$target_file.tmp"
cp "$target_file.tmp" $target_file
rm "$target_file.tmp"


cp $target_file hpmor.html