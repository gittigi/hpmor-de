import os
import re
import glob

from bs4 import BeautifulSoup  # pip install beautifulsoup4

# my helper
# import helper

translators = ["Schneefl0cke", "Jost", "DieFuechsin", "Patneu", "TralexHPMOR"]
lang = "de"

# make output dirs
os.makedirs("output", exist_ok=True)
for translator in translators:
    for dir in (
        # f"1-download/{translator}/",
        f"2-extract/{translator}/",
        # f"3-clean/{translator}/",
    ):
        os.makedirs(dir, exist_ok=True)


def extract_chapter_text():
    """
    extract chapter text from html and writes result into 2-extracted/
    2 modifications are done: removal of comments and removal of javascript
    """
    for translator in translators:
        print("===" + translator + "===")
        for fileIn in sorted(glob.glob(f"1-download/{translator}/*.html")):
            (filePath, fileName) = os.path.split(fileIn)
            fileOut = f"2-extract/{translator}/{fileName}"
            with open(fileIn, mode="r", encoding="utf-8", newline="\n") as fh:
                cont = fh.read()

            # cleanup comments and scripts
            cont = re.sub("<!--.*?-->", "", cont, flags=re.DOTALL)
            cont = re.sub(
                "<script.*?</script>", "", cont, flags=re.DOTALL | re.IGNORECASE
            )

            soup = BeautifulSoup(cont, features="html.parser")

            myTitle = ""
            myBody = ""

            # find chapter name from dropdown
            myElement = soup.find("select", {"id": "kA"})
            myElement = myElement.find("option", {"selected": "selected"})
            myTitle = myElement.text  # chars only, no tags

            # find body text
            myElement = soup.find("div", {"class": "user-formatted-inner"})
            # myBody = myElement.prettify()
            # myBody = myElement.encode()
            myBody = str(myElement)
            del myElement

            # remove linebreaks and multiple spaces
            myTitle = re.sub("\s+", " ", myTitle, flags=re.DOTALL | re.IGNORECASE)
            print(myTitle)
            # remove outer encapsolating div start and end
            myBody = re.sub("^<div[^>]*>", "", myBody, flags=re.DOTALL | re.IGNORECASE)
            myBody = re.sub("</div>[^>]*$", "", myBody, flags=re.DOTALL | re.IGNORECASE)

            out = f"<h1>{myTitle}</h1>\n{myBody}\n"

            with open(fileOut, mode="w", encoding="utf-8", newline="\n") as fh:
                fh.write(out)


def html_modify():
    for lang in languages:
        html_start = helper.get_html_start(lang=lang)
        html_end = "</body></html>"

        fhAll = open(
            f"output/hpmor-{lang}.html", mode="w", encoding="utf-8", newline="\n"
        )
        fhAll.write(html_start)

        for fileIn in sorted(glob.glob(f"2-extracted/{lang}/*.html")):
            (filePath, fileName) = os.path.split(fileIn)
            fileOut = f"3-cleaned/{lang}/{fileName}"
            with open(fileIn, mode="r", encoding="utf-8", newline="\n") as fh:
                cont = fh.read()
            soup = BeautifulSoup(cont, features="html.parser")

            # find header
            myElement = soup.find("h1")
            myTitle = myElement.text  # chars only, no tags
            myElement.replace_with("")
            del myElement
            if lang == "de" and myTitle == "1. Einführung":
                myTitle = "1. Vorwort zur Übersetzung"
            print(myTitle)

            # find body text
            myElement = soup
            s = str(myElement)
            # s = myElement.prettify()

            s = html_tuning(s, lang=lang)
            myElement = BeautifulSoup(s, features="html.parser")
            # myBody = myElement.prettify()
            # myBody = myElement.encode()
            myBody = str(myElement)
            del myElement

            out = f"<h1>{myTitle}</h1>\n{myBody}\n"

            with open(fileOut, mode="w", encoding="utf-8", newline="\n") as fh:
                fh.write(html_start)
                fh.write(out)
                fh.write(html_end)
            fhAll.write(out)
            # break
        fhAll.write(html_end)
        fhAll.close()


def html_tuning(s: str, lang: str) -> str:
    """
    cleanup spans and divs
    fix small typos
    fix "
    TODO: add unit tests!
    """
    # whitespace at start of line
    s = re.sub("\n\s+", "\n", s)
    #
    # cleanup divs and spans
    # alternatively define them via
    # <style>
    # div.user_center {	text-align: center; }
    # </style>
    #
    # cleanup spans
    s = re.sub(
        '<span class="user_normal">(.*?)</span>',
        r"\1",
        s,
        flags=re.DOTALL | re.IGNORECASE,
    )
    s = re.sub(
        '<span class="user_underlined">(.*?)</span>',
        r"<u>\1</u>",
        s,
        flags=re.DOTALL | re.IGNORECASE,
    )
    s = re.sub(
        '<span style="text-decoration:underline;">(.*?)</span>',
        r"<u>\1</u>",
        s,
        flags=re.DOTALL | re.IGNORECASE,
    )

    s = re.sub(
        '<span class="user_italic">(.*?)</span>',
        r"<em>\1</em>",
        s,
        flags=re.DOTALL | re.IGNORECASE,
    )
    s = re.sub(
        '<span class="user_bold">(.*?)</span>',
        r"<b>\1</b>",
        s,
        flags=re.DOTALL | re.IGNORECASE,
    )
    # need to repeat b and em
    s = re.sub(
        '<span class="user_italic">(.*?)</span>',
        r"<em>\1</em>",
        s,
        flags=re.DOTALL | re.IGNORECASE,
    )
    s = re.sub(
        '<span class="user_bold">(.*?)</span>',
        r"<b>\1</b>",
        s,
        flags=re.DOTALL | re.IGNORECASE,
    )

    # cleanup divs
    s = re.sub(
        '<div class="user_center">(.*?)</div>',
        r"<center>\1</center>",
        s,
        flags=re.DOTALL | re.IGNORECASE,
    )
    s = re.sub(
        '<div class="user_right">(.*?)</div>',
        r"<right>\1</right>",
        s,
        flags=re.DOTALL | re.IGNORECASE,
    )
    s = re.sub(
        '<div class="user_left">(.*?)</div>',
        r"<left>\1</left>",
        s,
        flags=re.DOTALL | re.IGNORECASE,
    )

    # 4x br -> 2x br
    s = re.sub(
        "<br/>\s*<br/>\s*<br/>\s*<br/>",
        "<br/><br/>",
        s,
        flags=re.DOTALL | re.IGNORECASE,
    )
    # 3x br -> 2x br
    s = re.sub(
        "<br/>\s*<br/>\s*<br/>", "<br/><br/>", s, flags=re.DOTALL | re.IGNORECASE
    )
    # drop empty tags 3x
    s = re.sub(r"<(\w+)>\s*</\1>", "", s, flags=re.DOTALL | re.IGNORECASE)
    s = re.sub(r"<(\w+)>\s*</\1>", "", s, flags=re.DOTALL | re.IGNORECASE)
    s = re.sub(r"<(\w+)>\s*</\1>", "", s, flags=re.DOTALL | re.IGNORECASE)

    # double br: remove spaces
    s = re.sub("<br/>\s+<br/>", "<br/><br/>", s, flags=re.DOTALL | re.IGNORECASE)
    # if more than 300 char -> use p instead of br
    s = re.sub("<br/>\n(.{200,})\n", r"<p>\n\1\n</p>", s, flags=re.IGNORECASE)
    s = re.sub("<br/>\s*<p>", "<p>", s, flags=re.DOTALL | re.IGNORECASE)
    s = re.sub("</p>\s*<br/>", "</p>", s, flags=re.DOTALL | re.IGNORECASE)

    # remove space before puctuation
    s = re.sub(" ([\.,:;])", r"\1", s)
    # add space after puctuation
    s = re.sub("([a-zA-Z][\.,:;])([a-zA-Z])", r"\1 \2", s)
    # multiple spaces
    s = re.sub("  +", " ", s)

    # spaces before " at lineend
    s = re.sub('\s+"\n', '"\n', s, flags=re.DOTALL | re.IGNORECASE)
    # empty lines
    s = re.sub("\n\n+", "\n", s)
    # remove linebreaks from sentences containing quotation marks
    # 3x
    s = re.sub(
        r'("\w[^"]+)\s+<br/>\s+([^"]+)\s+<br/>\s+([^"]+)\s+<br/>\s+([^"]+")',
        r"\1 \2 \3 \4",
        s,
        flags=re.DOTALL | re.IGNORECASE,
    )
    # 2x
    s = re.sub(
        r'("\w[^"]+)\s+<br/>\s+([^"]+)\s+<br/>\s+([^"]+")',
        r"\1 \2 \3",
        s,
        flags=re.DOTALL | re.IGNORECASE,
    )
    # 1x
    s = re.sub(
        r'("\w[^"]+)\s+<br/>\s+([^"]+")', r"\1 \2", s, flags=re.DOTALL | re.IGNORECASE
    )

    if lang == "en":
        s = s.replace('<hr noshade="noshade" size="1"/>', "<hr/>")
    elif lang == "de":
        # br -> p
        s = "<p>" + s + "</p>"
        s = re.sub("<br/><br/>", "</p><p>", s, flags=re.DOTALL | re.IGNORECASE)

        s = s.replace('."Wie kannst du das', '. "Wie kannst du das')
        s = s.replace('Mannes erstickte."Peter hatte', 'Mannes erstickte. "Peter hatte')
        s = s.replace(
            'begann zu gehen."Und pass auf, dass',
            'begann zu gehen. "Und pass auf, dass',
        )
        s = s.replace('Auroren,"ist der Grund', 'Auroren, "ist der Grund')
        s = s.replace('Draco?"sagte', 'Draco?" sagte')
        s = s.replace('Blick zu."Hör mal', 'Blick zu. "Hör mal')
        s = s.replace('Kopf."Ich', 'Kopf. "Ich')
        s = s.replace('Bäume."Halte', 'Bäume. "Halte')
        s = s.replace('Quirrell."Ich denke', 'Quirrell. "Ich denke')
        s = s.replace('Verteidigungsprofessor."Wir', 'Verteidigungsprofessor. "Wir')
        s = s.replace('Glück."Also', 'Glück. "Also')

    # nice looking quotation signs
    # en &ldquo;example&rdquo;
    # de &bdquo;Beispiel&ldquo;
    if lang == "de":
        q_left = "&bdquo;"
        q_right = "&ldquo;"
    else:
        q_left = "&ldquo;"
        q_right = "&rdquo;"
    # left
    s = re.sub('([\s\(]+)"', rf"\1{q_left}", s)
    s = re.sub('(\.\.\.)"(\w)', rf"\1{q_left}\2", s)
    # right
    s = re.sub('"([\s,\.!\?\)\-]+)', rf"{q_right}\1", s)
    s = re.sub('([\w])"([;])', rf"\1{q_right}\2", s)

    return s


if __name__ == "__main__":
    extract_chapter_text()
    # html_modify()
