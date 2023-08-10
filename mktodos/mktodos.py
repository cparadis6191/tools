#!/usr/bin/env python3

import os.path
import pathlib
import calendar
import datetime
from dateutil.relativedelta import relativedelta
import sys


def mktodos(dt, todo_dir, month_offsets):
    months = [
        dt + relativedelta(months=int(month_offset)) for month_offset in month_offsets
    ]

    todos = [month.date().strftime(f"{todo_dir}/%Y/%02m.todo") for month in months]

    for todo, month in zip(todos, months, strict=True):
        if not os.path.exists(todo) or os.path.getsize(todo) == 0:
            pathlib.Path(os.path.join(todo_dir, str(month.year))).mkdir(
                exist_ok=True, parents=True
            )
            with open(todo, "w") as todo:
                todo.write(f"{calendar.month(month.year, month.month)}\n# week \n")

    return todos


def main():
    if len(sys.argv) < 3:
        print(f"{os.path.basename(sys.argv[0])}: missing operands", file=sys.stderr)

        return 1

    todos = " ".join(mktodos(datetime.datetime.today(), sys.argv[1], sys.argv[2:]))

    if not todos:
        print(f"{os.path.basename(sys.argv[0])}: could not make todos", file=sys.stderr)

        return 2

    print(todos)

    return 0


if __name__ == "__main__":
    sys.exit(main())
