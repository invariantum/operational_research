"""Small wrappers around `in_class_test_code.py`.

This file is useful in Google Colab when you want short, question-by-question
function calls rather than running the whole script at once.

Colab quick start:
    !pip install pyomo simpy ortools openpyxl highspy

Then:
    import worked_solution_snippets as ws
    ws.q1_results()
    ws.q6_results()
"""

from __future__ import annotations

import in_class_test_code as exam


def q1_results():
    """Question 1: LP / integer production results."""
    return exam.question_1_results()


def q2_results():
    """Question 2: set-covering results."""
    return exam.question_2_results()


def q3_results():
    """Question 3: transhipment results."""
    return exam.question_3_results()


def q4_results():
    """Question 4: simulation results."""
    return exam.question_4_results()


def q5_results():
    """Question 5: forecasting results without exporting the workbook."""
    return exam.question_5_results(export_workbook=False)


def q6_results():
    """Question 6: scheduling results."""
    return exam.question_6_results()


def all_results(export_workbook=False):
    """Run the full worked solution pack."""
    return exam.run_all_solutions(export_workbook=export_workbook)


def main():
    """Print every question result in sequence."""
    exam.print_all_solutions(all_results(export_workbook=False))


if __name__ == "__main__":
    main()
