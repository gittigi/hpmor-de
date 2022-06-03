#!/bin/sh

# based on work by yeKcim
# https://github.com/yeKcim/hpmor/tree/master/ebook

echo === 3. modify flattened file ===

# ensure we are in the hpmor root dir
script_dir=$(cd `dirname $0` && pwd)
cd $script_dir/..

source_file="hpmor-epub-2-flatten.tex"
target_file="hpmor-epub-3-flatten-mod1.tex"
cp $source_file $target_file

date=`date +"%d.%m.%Y"`

sed -i "s/\\\\today{}/$date/g" $target_file

# writtenNote env -> \writtenNoteA
# could not make sed ungreedy, using perl instead
# sed -i 's/\\begin{writtenNote}/\\begin{block}/g' $target_file
# sed -i 's/\\end{writtenNote}/\\end{block}/g' $target_file
# sed -i -z 's/\\begin{writtenNote}(.*)\\end{writtenNote}/mywrittenNote/g' $target_file
# writtenNote env -> \writtenNoteA (using "coler" writtenNote as defined in 1.sh
perl -pe '$/=undef;s/\\begin\{writtenNote\}\s*(.*?)\s*\\end\{writtenNote\}/\\writtenNoteA{\1}/sg' $target_file > "$target_file.tmp"
mv "$target_file.tmp" $target_file

sed -i 's/\\vskip .1\\baselineskip plus .1\\baselineskip minus .1\\baselineskip//g' $target_file
sed -i 's/\\vskip 1\\baselineskip plus 1\\baselineskip minus 1\\baselineskip//g' $target_file
sed -i 's/\\vskip 0pt plus 2//g' $target_file

sed -i 's/\\begin{align\*}//g ; s/\\end{align\*}//g ; s/ }&\\hbox{/ }\\hbox{/g' $target_file

sed -i 's/\\hplettrineextrapara//g' $target_file

sed -i '/^\\def{\\ifnum\\prevgraf/,/^\\fi}/d;' $target_file

# remove PDF files
sed -i 's/\\includegraphics[^}]\+pdf}//g' $target_file