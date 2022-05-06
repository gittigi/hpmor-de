#!/usr/bin/env python3

# read hpmor.tex for list of uncommented (=translated) chapters
# check and autofix the chapter tex files for known issues
# skip all lines starting with '%'
# if findings, write proposal to *-autofix.tex


import re

# TODO:
# auto-fix quotations?
# in EN the quotations “...”
# in DE the quotations are „...“ so this needs to be removed: “...
# in DE "..." should be fixed

# - ->  —


def process_file(f: str) -> list:
    changed = False
    with open(f, mode="r", encoding="utf-8") as fh:
        cont = fh.read()

    # more than 1 empty line
    if "\n\n\n" in cont:
        changed = True
        cont = re.sub(r"\n\n\n+", r"\n\n", cont, flags=re.DOTALL)

    l_cont = cont.split("\n")
    del cont
    l_cont_2 = []
    for line in l_cont:
        lineOrig = line
        # do not modify commented out lines
        if not re.match("^\s*%", line):
            line = fix_line(s=line)
            if changed == False and lineOrig != line:
                changed = True
        l_cont_2.append(line)
    if changed:
        fileOut = f.replace(".tex", "-autofix.tex")
        with open(fileOut, mode="w", encoding="utf-8", newline="\n") as fh:
            fh.write("\n".join(l_cont_2))


def fix_line(s: str) -> str:
    s1 = s
    # multiple spaces
    s = re.sub(r"[ \t][ \t]+", " ", s)
    # remove spaces from empty lines
    s = re.sub(r"^\s+$", "", s)

    # simple
    # ...
    s = s.replace("...", "…")
    s = s.replace(" … ", "…")
    # … at end of quotation ' …"' -> '…"'
    s = s.replace(' …"', '…"')

    s = s.replace("Mr. H. Potter", "Mr~H.~Potter")
    s = s.replace("Mr. Potter", "Mr~Potter")

    # Mr / Mrs
    s = re.sub(r"\b(Mrs?)\.~?\s*", r"\1~", s, flags=re.DOTALL)

    # Word…"Word -> Word…" Word
    s = re.sub(r"(\w…\")(\w)", r"\1 \2", s, flags=re.DOTALL)

    # if s != s1:
    #     print(s1 + "\n" + s)

    return s


if __name__ == "__main__":
    with open("../hpmor.tex", mode="r", encoding="utf-8") as fh:
        l = fh.readlines()
    l = [elem for elem in l if elem.startswith("\include{chapters/hpmor-chapter-")]
    for i in l:
        fileName = re.search("^.*\{.+/(.+?)\}.*$", i).group(1)
        fileIn = fileName + ".tex"
        print(fileName)
        process_file(f=fileIn)
