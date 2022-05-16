import glob
import os
import re
import sys

# my helper
import helper

os.chdir(os.path.dirname(sys.argv[0]))

translations = helper.translations
translators = translations.keys()

settings = {"lang": "DE"}

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
    s = re.sub(r"(?<=\n)\\hfill\\break *", r"", s)
    # s = re.sub(r"(?<=\n)\\hypertarget.*$", r"", s)
    s = s.replace("\maketitle", "")
    s = s.replace("\ldots", "…")
    s = s.replace("\\\\", "\n\n")

    # empty lines
    s = re.sub(r"\n\n\n+", "\n\n", s)

    # \later
    s = re.sub(r"\-\-\-\-+", r"\\later", s)
    s = re.sub(r"\* \* \*", r"\\later", s)

    # 1 line per paragraph
    s = re.sub(r"(?<!\s)\n(?!\s)", " ", s)

    lines = s.split("\n")
    lines2 = []
    # reuse code from check-chapters, per line
    for s in lines:
        # simple and safe
        s = fix_spaces(s)
        s = fix_latex(s)
        s = fix_dots(s)
        s = fix_MrMrs(s)
        s = fix_numbers(s)
        s = fix_common_typos(s)
        s = fix_spaces(s)

        # advanced stuff
        s = fix_quotations(s)
        s = fix_emph(s)
        s = fix_hyphens(s)
        s = fix_spaces(s)
        lines2.append(s)
    s = "\n".join(lines2)
    return s


def fix_spaces(s: str) -> str:
    # trailing spaces
    s = re.sub(r" +$", "", s)
    # remove spaces from empty lines
    s = re.sub(r"^\s+$", "", s)
    # multiple spaces (excluding start of new line)
    s = re.sub(r"(?<!^)[ \t][ \t]+", " ", s)
    return s


def fix_latex(s: str) -> str:
    # Latex: \begin and \end{...} at new line
    s = re.sub(r"([^\s+%])\s*\\(begin|end)\{", r"\1\n\\\2{", s)
    # Latex: \\ at new line
    s = re.sub(r"\\\\\s*(?!$)", r"\\\\\n", s)
    return s


def fix_dots(s: str) -> str:
    # ... -> …
    s = s.replace("...", "…")
    # ... with spaces around
    s = s.replace(" … ", "…")
    # NOT '… ' as in ', no… “I'
    # s = re.sub(r" *… *", r"…", s)

    # … at end of quotation ' …"' -> '…"'
    s = s.replace(' …"', '…"')
    # … at end of line
    s = re.sub(r" +…\n", r"…\n", s)
    # Word…"Word -> Word…" Word
    s = re.sub(r'(\w…")(\w)', r"\1 \2", s)
    # … after . or ,
    s = re.sub(r"([,\.])…", r"\1 …", s)
    return s


def fix_MrMrs(s: str) -> str:
    # Mr / Mrs
    s = s.replace("Mr. H. Potter", "Mr~H.~Potter")
    # s = s.replace("Mr. Potter", "Mr~Potter")
    s = re.sub(r"\b(Mr|Mrs|Miss|Dr)\b\.?\s+(?!”)", r"\1~", s)
    # Dr.~ -> Dr~Potter
    s = re.sub(r"\b(Mr|Mrs|Miss|Dr)\b\.~", r"\1~", s)
    # "Dr. " -> "Dr~"
    # s = re.sub(r"\b(Dr)\b\.?~?\s*", r"\1~", s)
    # s = s.replace("Mr~and Mrs~", "Mr and Mrs~")
    return s


def fix_numbers(s: str) -> str:
    if settings["lang"] == "DE":
        s = re.sub(r"(\d) +(Uhr)", r"\1~\2", s)
    return s


def fix_common_typos(s: str) -> str:
    if settings["lang"] == "DE":
        s = s.replace("ut mir Leid", "ut mir leid")
    return s


def fix_quotations(s: str) -> str:
    # in EN the quotations are “...” and ‘...’
    # in DE the quotations are „...“

    # "....." -> “.....”
    if settings["lang"] == "EN":
        s = re.sub(r'"([^"]+)"', r"“\1”", s)
    if settings["lang"] == "DE":
        s = re.sub(r'"([^"]+)"', r"„\1“", s)

    # fixing ' "Word..."' and ' "\command..."'
    if settings["lang"] == "EN":
        s = re.sub(r'(^|\s)"((\\|\w).*?)"', r"\1“\2”", s)
    if settings["lang"] == "DE":
        s = re.sub(r'(^|\s)"((\\|\w).*?)"', r"\1„\2“", s)

    # space between "…" and "“"
    if settings["lang"] == "EN":
        s = re.sub(r"…„", r"… “", s)
    if settings["lang"] == "DE":
        s = re.sub(r"…„", r"… „", s)

    # ” } -> ”}
    if settings["lang"] == "EN":
        s = s.replace("” }", "”} ")
    if settings["lang"] == "DE":
        s = s.replace("“ }", "“} ")
    # now fix possible new double spaces created by line above
    s = re.sub(r"(?<!^)[ \t][ \t]+", " ", s)
    s = re.sub(r" +$", r"", s)

    # quotation marks should go outside of emph:
    # \emph{“.....”} -> “\emph{.....}”
    if settings["lang"] == "EN":
        s = re.sub(r"\\(emph|shout)\{“([^”]+?)”\}", r"“\\\1{\2}”", s)
    if settings["lang"] == "DE":
        s = re.sub(r"\\(emph|shout)\{„([^“]+?)“\}", r"„\\\1{\2}“", s)

    # lone “ at end of \emph
    # “...\emph{.....”} -> “...\emph{.....}”
    if settings["lang"] == "EN":
        s = re.sub(r"(\\emph\{[^“]+?)”\}", r"\1}”", s)
    if settings["lang"] == "DE":
        s = re.sub(r"(\\emph\{[^„]+?)“\}", r"\1}“", s)

    if settings["lang"] == "DE":
        # migrate EN quotations
        s = re.sub(r"“([^“”]+?)”", r"„\1“", s)

        # migrate EN quotations at first word of chapter
        s = re.sub(r"\\(lettrine|lettrinepara)\[ante=“\]", r"\\\1[ante=„]", s)
    return s


def fix_emph(s: str) -> str:
    # space at start of emph
    s = re.sub(r"(\\emph{) +", " \1", s)

    # move punctuation out of 1-word-emph
    # ... \emph{WORD.} -> \emph{WORD}.
    # Note: only for , and .
    if settings["lang"] == "EN":
        s = re.sub(r"(?<!^)\\emph\{([^ …\}]+)([,\.])\}(?!”)", r"\\emph{\1}\2", s)
    if settings["lang"] == "DE":
        s = re.sub(r"(?<!^)\\emph\{([^ …\}]+)([,\.])\}(?!“)", r"\\emph{\1}\2", s)

    # Note: good, but MANY false positives
    # \emph{...} word \emph{...} -> \emph{... \emph{word} ...
    # s = re.sub(r"(\\emph\{[^\}]+)\} ([^ ]+) \\emph\{", r"\1 \\emph{\2} ", s)
    return s


def fix_hyphens(s: str) -> str:
    # --- -> em dash —
    s = s.replace("---", "—")
    s = s.replace("--", "—")
    # hyphens: (space-hyphen-space) should be "—" (em dash).
    # trim space around em-dash
    s = s.replace(" — ", "—")
    # NOT for '— ' as in ', no— “I'
    # s = re.sub(r"— ", r"—", s)

    # - at start of line
    s = re.sub(r"^[\-—] *", r"—", s)
    # - at start of line
    s = re.sub(r" [\-—]$", r"—", s)
    # - at end of emph
    s = re.sub(r"(\s*)\-\}", r"—}\1", s)
    # - at end of quote
    if settings["lang"] == "EN":
        s = re.sub(r"(\s*)\-”", r"—”\1", s)
    if settings["lang"] == "DE":
        s = re.sub(r"(\s*)\-“", r"—“\1", s)

    # there is a shorter dash as well:
    # 2-4 -> 2–4 using mid length hyphen
    s = re.sub(r"(\d)\-(?=\d)", r"\1–", s)
    # NOT: mid-length dash ->  em dash (caution: false positives!)
    # s = s.replace("–", "—")
    return s


if __name__ == "__main__":
    loop_files_for_cleanup()
