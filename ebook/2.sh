#!/bin/sh

echo === 2. flatten .tex files ===

# ensure we are in the hpmor root dir
script_dir=$(cd `dirname $0` && pwd)
cd $script_dir/..

source_file="hpmor-epub-1.tex"
target_file="hpmor-epub-2-flatten.tex"

# flatten the .tex files to one file
latexpand $source_file -o $target_file