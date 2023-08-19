#!/usr/bin/env python3

import os.path
import pathlib
import calendar
import datetime
from dateutil.relativedelta import relativedelta
import sys


def mkjournals(dt, journal_dir, month_offsets):
    months = [
        dt + relativedelta(months=int(month_offset)) for month_offset in month_offsets
    ]

    journals = [
        month.date().strftime(f"{journal_dir}/%Y/%02m.journal") for month in months
    ]

    for journal, month in zip(journals, months, strict=True):
        if not os.path.exists(journal) or os.path.getsize(journal) == 0:
            pathlib.Path(os.path.join(journal_dir, str(month.year))).mkdir(
                exist_ok=True, parents=True
            )
            with open(journal, "w") as journal:
                journal.write(f"{calendar.month(month.year, month.month)}\n# week \n")

    return journals


def main():
    if len(sys.argv) < 3:
        print(f"{os.path.basename(sys.argv[0])}: missing operands", file=sys.stderr)

        return 1

    journals = " ".join(
        mkjournals(datetime.datetime.today(), sys.argv[1], sys.argv[2:])
    )

    if not journals:
        print(
            f"{os.path.basename(sys.argv[0])}: could not make journals", file=sys.stderr
        )

        return 2

    print(journals)

    return 0


if __name__ == "__main__":
    sys.exit(main())
