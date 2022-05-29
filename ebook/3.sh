#!/bin/sh

echo === 3. modify flattened file ===

# ensure we are in the hpmor root dir
script_dir=$(cd `dirname $0` && pwd)
cd $script_dir/..

source_file="hpmor-epub-2-flatten.tex"
target_file="hpmor-epub-3-flatten-mod.tex"
cp $source_file $target_file

sed -i 's/\\parsela{#1}/\\parselb{#1}/' $target_file

# writtenNote env -> YellowBlue
# could not make sed ungreedy, using perl instead
# sed -i 's/\\begin{writtenNote}/\\begin{block}/g' $target_file
# sed -i 's/\\end{writtenNote}/\\end{block}/g' $target_file
# sed -i -z 's/\\begin{writtenNote}(.*)\\end{writtenNote}/mywrittenNote/g' $target_file

# writtenNote env -> \writtenNote (using YellowBlue as defined in 1.sh
perl -pe '$/=undef;s/\\begin\{writtenNote\}\s*(.*?)\s*\\end\{writtenNote\}/\\writtenNoteA{\1}/sg' $target_file > "$target_file.tmp"
mv "$target_file.tmp" $target_file

# # Cant find a way to add directly font or class name in span… ⇒ hack: add color → class
# \parsel -> YellowOrange
sed -i 's/{Parseltongue.ttf}#1}/{Parseltongue.ttf}\\textcolor{YellowOrange}{#1}}/g' $target_file
# \headline -> YellowGreen
sed -i 's/{gabriele-bad.ttf}#1}/{gabriele-bad.ttf}\\textcolor{YellowGreen}{#1}}/g' $target_file
# \McGonagallWhiteBoard -> YellowRed
sed -i 's/\\textcolor{blue}{\\Huge{\\underline{\\textcolor{red}{#1}}}}/\\textcolor{YellowRed}{#1}/g' $target_file

sed -i 's/\\vskip .1\\baselineskip plus .1\\baselineskip minus .1\\baselineskip//g' $target_file
sed -i 's/\\vskip 1\\baselineskip plus 1\\baselineskip minus 1\\baselineskip//g' $target_file
sed -i 's/\\vskip 0pt plus 2//g' $target_file

sed -i 's/\\begin{align\*}//g ; s/\\end{align\*}//g ; s/ }&\\hbox{/ }\\hbox{/g' $target_file

sed -i 's/\\hplettrineextrapara//g' $target_file

sed -i '/^\\def{\\ifnum\\prevgraf/,/^\\fi}/d;' $target_file