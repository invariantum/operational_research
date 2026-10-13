"""Build a combined full revision booklet from Practice Papers A and B."""

from __future__ import annotations

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PAPER_A = ROOT / "practice-paper-a" / "practice-paper-a.tex"
PAPER_B = ROOT / "practice-paper-b" / "practice-paper-b.tex"
SOL_A = ROOT / "practice-paper-a" / "practice-paper-a-solutions.tex"
SOL_B = ROOT / "practice-paper-b" / "practice-paper-b-solutions.tex"

OUT_DIR = Path(__file__).resolve().parent
QUESTION_OUT = OUT_DIR / "full-revision-booklet.tex"
SOLUTION_OUT = OUT_DIR / "full-revision-booklet-solutions.tex"


PAPER_PREAMBLE = r"""\documentclass[11pt,a4paper]{article}

\usepackage[a4paper,margin=1in]{geometry}
\usepackage{amsmath}
\usepackage{amssymb}
\usepackage{array}
\usepackage{booktabs}
\usepackage{enumitem}
\usepackage{tabularx}
\usepackage{tikz}
\usepackage[T1]{fontenc}
\usepackage{lmodern}
\usepackage{xcolor}

\definecolor{bookletblue}{RGB}{30,70,120}
\definecolor{bookletgrey}{RGB}{90,90,90}

\newcommand{\markalloc}[1]{\nobreak\hfill\mbox{(#1 Marks)}}
\newcommand{\questiontotal}[1]{\begin{flushright}\textbf{Total #1 Marks}\end{flushright}}

\setlength{\parindent}{0pt}
\setlength{\parskip}{0.45em}
\setlist[enumerate,1]{label=(\alph*), leftmargin=1.1cm, itemsep=0.55em, topsep=0.4em}

\begin{document}

\begin{center}
{\Large\bfseries\color{bookletblue} Full Revision Booklet}\\[0.4em]
{\large 5CM522 Operational Research}\\[0.3em]
{\color{bookletgrey} Combined and renumbered from Practice Papers A and B}
\end{center}

\vspace{0.8em}
\hrule
\vspace{0.8em}

This booklet contains all questions from both current practice papers.
The questions have been renumbered so that the set reads as one continuous revision pack.

\begin{center}
\begin{tabular}{lll}
\toprule
Booklet Question & Source & Original Question \\
\midrule
1--6 & Practice Paper A & Questions 1--6 \\
7--12 & Practice Paper B & Questions 1--6 \\
\bottomrule
\end{tabular}
\end{center}

\newpage
"""


SOLUTION_PREAMBLE = r"""\documentclass[11pt,a4paper]{article}

\usepackage[a4paper,margin=1in]{geometry}
\usepackage{amsmath}
\usepackage{amssymb}
\usepackage{array}
\usepackage{booktabs}
\usepackage{enumitem}
\usepackage{tabularx}
\usepackage{tikz}
\usepackage[T1]{fontenc}
\usepackage{lmodern}
\usepackage{xcolor}

\definecolor{bookletblue}{RGB}{30,70,120}
\definecolor{bookletgrey}{RGB}{90,90,90}

\setlength{\parindent}{0pt}
\setlength{\parskip}{0.45em}
\setlist[enumerate,1]{label=(\alph*), leftmargin=1.1cm, itemsep=0.55em, topsep=0.4em}

\begin{document}

\begin{center}
{\Large\bfseries\color{bookletblue} Full Revision Booklet}\\[0.4em]
{\large Worked Solutions}\\[0.3em]
{\color{bookletgrey} Combined and renumbered from Practice Papers A and B}
\end{center}

\vspace{0.8em}
\hrule
\vspace{1em}
"""


def strip_document_wrappers(text: str) -> str:
    text = re.sub(r"\\documentclass.*?\\begin\{document\}", "", text, count=1, flags=re.S)
    text = re.sub(r"\\end\{document\}\s*$", "", text, flags=re.S)
    return text


def extract_question_blocks(text: str):
    pattern = re.compile(r"\\textbf\{(\d+)\.\}")
    matches = list(pattern.finditer(text))
    blocks = []
    for idx, match in enumerate(matches):
        start = match.start()
        search_from = match.end()
        total_match = re.search(r"\\questiontotal\{25\}", text[search_from:])
        if total_match is None:
            raise RuntimeError(f"Could not find question total after question {match.group(1)}")
        end = search_from + total_match.end()
        block = text[start:end]
        blocks.append((int(match.group(1)), block))
        text = text[end:]
        matches = list(pattern.finditer(text))
        if not matches:
            break
        return blocks + [(num, blk) for num, blk in extract_question_blocks(text)]
    return blocks


def clean_question_block(block: str, new_number: int, source_label: str, source_number: int) -> str:
    block = re.sub(r"\\continuednotice", "", block)
    block = re.sub(r"\\newpage", "", block)
    block = block.strip()
    block = re.sub(r"\\textbf\{\d+\.\}", rf"\\textbf{{{new_number}.}}", block, count=1)
    source_line = f"\\textit{{Source: {source_label}, original Question {source_number}.}}\n\n"
    block = re.sub(
        rf"(\\textbf\{{{new_number}\.\}})",
        lambda m: m.group(1) + "\n\n" + source_line,
        block,
        count=1,
    )
    return block.strip()


def extract_solution_blocks(text: str):
    pattern = re.compile(r"\\textbf\{(\d+)\.\s*([^}]*)\}")
    matches = list(pattern.finditer(text))
    blocks = []
    for idx, match in enumerate(matches):
        start = match.start()
        end = matches[idx + 1].start() if idx + 1 < len(matches) else len(text)
        blocks.append((int(match.group(1)), match.group(2).strip(), text[start:end].strip()))
    return blocks


def clean_solution_block(block: str, new_number: int, title: str, source_label: str, source_number: int) -> str:
    block = re.sub(r"\\newpage", "", block)
    block = re.sub(r"\\textbf\{\d+\.\s*([^}]*)\}", rf"\\textbf{{{new_number}. {title}}}", block, count=1)
    source_line = f"\\textit{{Source: {source_label}, original Question {source_number}.}}\n\n"
    block = re.sub(
        rf"(\\textbf\{{{new_number}\.\s*{re.escape(title)}\}})",
        lambda m: m.group(1) + "\n\n" + source_line,
        block,
        count=1,
    )
    return block.strip()


def build_question_tex():
    parts = [PAPER_PREAMBLE]
    running = 1
    for source_label, path in [("Practice Paper A", PAPER_A), ("Practice Paper B", PAPER_B)]:
        text = strip_document_wrappers(path.read_text(encoding="utf-8"))
        for original_number, raw_block in extract_question_blocks(text):
            parts.append(clean_question_block(raw_block, running, source_label, original_number))
            if running < 12:
                parts.append("\n\n\\newpage\n\n")
            running += 1
    parts.append("\n\\end{document}\n")
    QUESTION_OUT.write_text("".join(parts), encoding="utf-8")


def build_solution_tex():
    parts = [SOLUTION_PREAMBLE]
    running = 1
    for source_label, path in [("Practice Paper A", SOL_A), ("Practice Paper B", SOL_B)]:
        text = strip_document_wrappers(path.read_text(encoding="utf-8"))
        for original_number, title, raw_block in extract_solution_blocks(text):
            parts.append(clean_solution_block(raw_block, running, title, source_label, original_number))
            if running < 12:
                parts.append("\n\n\\newpage\n\n")
            running += 1
    parts.append("\n\\end{document}\n")
    SOLUTION_OUT.write_text("".join(parts), encoding="utf-8")


def main():
    build_question_tex()
    build_solution_tex()
    print("Built:")
    print(QUESTION_OUT.name)
    print(SOLUTION_OUT.name)


if __name__ == "__main__":
    main()
