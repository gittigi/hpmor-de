import os
import glob
import re

translators = ["Schneefl0cke", "Jost", "DieFuechsin", "Patneu", "TralexHPMOR"]


for translator in translators:
    for dir in (
        # f"1-download/{translator}/",
        # f"2-extract/{translator}/",
        # f"3-clean/{translator}/",
        # f"4-latex/{translator}/",
        f"5-latex-clean/{translator}/",
    ):
        os.makedirs(dir, exist_ok=True)


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
    s = s.replace("``", "“")
    s = s.replace("{}", "")
    s = s.replace("\maketitle", "")
    # empty lines
    s = re.sub(r"\n\n\n+", "\n\n", s)
    return s


if __name__ == "__main__":
    loop_files_for_cleanup()
