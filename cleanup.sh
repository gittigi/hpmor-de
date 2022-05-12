#!/bin/sh

latexmk -C
rm -rf chapters/*.aux
rm -rf ebook/tmp
