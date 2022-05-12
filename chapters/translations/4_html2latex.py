import os
import glob
import re
import subprocess

translators = ["Schneefl0cke", "Jost", "DieFuechsin", "Patneu", "TralexHPMOR"]


for translator in translators:
    for dir in (
        # f"1-download/{translator}/",
        # f"2-extract/{translator}/",
        # f"3-clean/{translator}/",
        f"4-latex/{translator}/",
        # f"5-latex-clean/{translator}/",
    ):
        os.makedirs(dir, exist_ok=True)


def html2latex():
    for translator in translators:
        print("===" + translator + "===")
        for fileIn in sorted(glob.glob(f"3-clean/{translator}/*.html")):
            print(fileIn)
            fileOut = fileIn.replace("3-clean/", "4-latex/").replace(".html", ".tex")
            # pandoc -s fileIn -o fileOut
            process = subprocess.run(
                ["pandoc", "-s", fileIn, "-o", fileOut], capture_output=True, text=True
            )
            print(process.stdout)


if __name__ == "__main__":
    html2latex()
