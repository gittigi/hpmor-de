import os
import requests

# import re
# import glob
# import requests
# from bs4 import BeautifulSoup  # pip install beautifulsoup4

# # my helper
# import helper

translations = {
    "Schneefl0cke": {"id": "60044849000ccc541aef297e", "chStart": 0, "numFiles": 121},
    "Jost": {"id": "4cb8beb50000203e067007d0", "chStart": 1, "numFiles": 21},
    "DieFuechsin": {
        "id": "5c793dfe000a402030774dc7",
        "chStart": 34 - 1,
        "numFiles": 46,
    },
    "Patneu": {"id": "55610c610004dede273a3811", "chStart": 1, "numFiles": 38},
    "TralexHPMOR": {"id": "59a29b7f000813c22ec1454b", "chStart": 22, "numFiles": 6},
}

# make output dirs
os.makedirs("output", exist_ok=True)
for translator in translations.keys():
    for dir in (
        f"1-download/{translator}/",
        # f"2-extract/{translator}/",
        # f"3-clean/{translator}/",
    ):
        os.makedirs(dir, exist_ok=True)


def download_file(url: str, filepath: str):
    """download file from url to filepath"""
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:75.0) Gecko/20100101 Firefox/75.0 ",
    }
    cont = requests.get(url, headers=headers, verify=True).content
    # verify=False -> skip SSL cert verification: CERTIFICATE_VERIFY_FAILED
    with open(filepath, mode="bw") as fh:
        fh.write(cont)


def download_all_chapters():
    """Downloads into chapters-1-download/<lang>/ only if fileOut does not exist"""
    url_base = "https://www.fanfiktion.de/s/<---id--->/<---fileNum--->/"
    for translator, trans in translations.items():
        # chapter_last = trans["chStart"] + trans["numFiles"]
        chapter = trans["chStart"]
        for fileNum in range(1, trans["numFiles"] + 1):
            fileOut = f"chapters-1-download/{translator}/%03d.html" % chapter
            if not os.path.exists(fileOut):
                print(f"downloading chapter %03d" % chapter)
                url = url_base.replace("<---id--->", trans["id"]).replace(
                    "<---fileNum--->", str(fileNum)
                )
                download_file(url=url, filepath=fileOut)
            chapter += 1


if __name__ == "__main__":
    download_all_chapters()
