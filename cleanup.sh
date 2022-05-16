#!/bin/sh

latexmk -C
rm -rf chapters/*.aux
rm -rf chapters/*-autofix.tex
rm -rf ebook/tmp
