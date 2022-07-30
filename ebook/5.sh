#!/bin/sh

# based on work by yeKcim
# https://github.com/yeKcim/hpmor/tree/master/ebook

echo === 5. LaTeX -\> HTML via pandoc ===

# ensure we are in the hpmor root dir
script_dir=$(cd `dirname $0` && pwd)
cd $script_dir/..

source_file="hpmor-epub-4-flatten-mod2.tex"
target_file="hpmor-epub-5-html-1.html"

# LaTeX -> HTML
title=$(grep "pdftitle=" layout/hp-header.tex | awk -F '[{}]' '{print $2}')
author=$(grep "pdfauthor=" layout/hp-header.tex | awk -F '[{}]' '{print $2}')

pandoc --standalone --from=latex+latex_macros $source_file -o $target_file --metadata title="$title" --metadata author="$author"