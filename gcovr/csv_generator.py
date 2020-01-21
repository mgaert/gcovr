# -*- coding:utf-8 -*-

# This file is part of gcovr <http://gcovr.com/>.
#
# Copyright 2020 Michael Gärtner

import sys
import csv
from .utils import calculate_coverage, sort_coverage, presentable_filename


def print_csv_report(covdata, output_file, options):
    """produce the classic gcovr text report"""

    csv.register_dialect("gcover_dialect", delimiter=options.csvdelim)

    if output_file:
        with open(output_file, 'w', newline='') as fh:
            writer = csv.writer(fh, dialect="gcover_dialect")
            _real_print_csv_report(covdata, writer, options)
    else:
        _real_print_csv_report(covdata, sys.stdout, options)


def _real_print_csv_report(covdata, OUTPUT, options):
    total_lines = 0
    total_covered = 0

    # Header
    OUTPUT.writerow([""]*5)
    OUTPUT.writerow(["GCC Code Coverage Report", "", "", "", ""])
    OUTPUT.writerow(["Directory: " + options.root, "", "", "", ""])

    OUTPUT.writerow([""]*5)
    a = options.show_branch and "Branches" or "Lines"
    b = options.show_branch and "Taken" or "Exec"
    c = "Missing"
    OUTPUT.writerow(["File", a, b, "Cover", c])
    OUTPUT.writerow([""]*5)

    # Data
    keys = sort_coverage(
        covdata, show_branch=options.show_branch,
        by_num_uncovered=options.sort_uncovered,
        by_percent_uncovered=options.sort_percent)

    def _summarize_file_coverage(coverage):
        filename = presentable_filename(
            coverage.filename, root_filter=options.root_filter)

        if options.show_branch:
            total, cover, percent = coverage.branch_coverage()
            uncovered_lines = coverage.uncovered_branches_str()
        else:
            total, cover, percent = coverage.line_coverage()
            uncovered_lines = coverage.uncovered_lines_str()
        percent = '--' if percent is None else str(int(percent))
        return (total, cover,
                (filename, str(total), str(cover), percent + "%", uncovered_lines))

    for key in keys:
        (t, n, txt) = _summarize_file_coverage(covdata[key])
        total_lines += t
        total_covered += n
        OUTPUT.writerow(txt)

    # Footer & summary
    OUTPUT.writerow([""]*5)
    percent = calculate_coverage(total_covered, total_lines, nan_value=None)
    percent = "--" if percent is None else str(int(percent))
    OUTPUT.writerow(("TOTAL", str(total_lines), str(
        total_covered), str(percent) + "%"))
    OUTPUT.writerow([""]*5)
