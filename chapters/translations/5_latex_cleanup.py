import glob
import os
import re
import sys

# my helper
import helper

os.chdir(os.path.dirname(sys.argv[0]))

translations = helper.translations
translators = translations.keys()

# make output dirs
for translator in translations.keys():
    os.makedirs(f"5-latex-clean/{translator}/", exist_ok=True)


def loop_files_for_cleanup():
    for translator in translators:
        print("===" + translator + "===")
        for fileIn in sorted(glob.glob(f"4-latex/{translator}/*.tex")):
            fileOut = fileIn.replace("4-latex/", "5-latex-clean/")
            with open(fileIn, mode="r", encoding="utf-8") as fh:
                cont = fh.read()
            cont = cleanup_latex(s=cont)
            with open(fileOut, mode="w", encoding="utf-8", newline="\n") as fh:
                fh.write(cont)


def cleanup_latex(s):
    # end of line
    s = re.sub(r"\r\n", "\n", s)
    s = re.sub(r"^.*\\begin\{document\}", "", s, flags=re.DOTALL)
    s = re.sub(r"\\end\{document\}.*$", "", s, flags=re.DOTALL)

    # quotations
    s = s.replace("''", '"')
    s = s.replace("``", "“")
    # "...“ -> „...“
    s = re.sub(r"\"([^\"]+)“", r"„\1“", s)

    # latex stuff
    s = s.replace("{}", "")
    s = s.replace("\n\hfill\break ", "\n")
    s = s.replace("\maketitle", "")
    s = s.replace("\ldots", "…")

    # empty lines
    s = re.sub(r"\n\n\n+", "\n\n", s)

    # 1 line per paragraph
    s = re.sub(r"(?<!\s)\n(?!\s)", " ", s)

    return s


if __name__ == "__main__":
    loop_files_for_cleanup()
