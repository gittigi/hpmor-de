#!/bin/sh

echo === 1. prepare .tex file, based on hpmor.tex===

# ensure we are in the hpmor root dir
script_dir=$(cd `dirname $0` && pwd)
cd $script_dir/..

source_file="hpmor.tex"
# source_file="layout/test.tex"

target_file="hpmor-epub-1.tex"
cp $source_file $target_file

# insert packages to load
# sed '3i\\\input{layout/hp-format}\n\\input{layout/hp-markup}\n\\usepackage{polyglossia}\n\\setmainlanguage{german}\n\\setdefaultlanguage[spelling = new]{german}' $source_file > $target_file
sed -i '3i\\\usepackage{polyglossia}\n\\setdefaultlanguage[variant = german, spelling = new, babelshorthands = true, script = latin]{german}\n\\enablehyphenation\n' $target_file
sed -i '8i\\\input{layout/hp-format}\n\\input{layout/hp-markup}\n' $target_file

# remove loading of hp-contents file
sed -i '/\\\input{layout\/hp-contents}/d' $target_file

# overwrite the headlines env, since it makes problems in pandoc
sed -i '10i\\\renewenvironment{headlines}{}{}\n' $target_file
sed -i '11i\\\renewenvironment{writtenNote}{}{}\n' $target_file
# sed -i '/\\begin{headlines}/d ; /\\end{headlines}/d' $target_file # TODO: \headlines (can't generate epub)

sed -i '12i\\\newcommand\{\\writtenNoteA}[1]{\\par\\textcolor{YellowBlue}{#1}}\n' $target_file
