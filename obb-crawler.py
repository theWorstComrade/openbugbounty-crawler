#!/usr/bin/python3.7

from src.list import ProgramList
from time import sleep


def run():
    lst = ProgramList()
    offset = 0
    total = 1

    while offset < total:
        lst_model = lst.get(offset)
        total = int(lst_model.recordsTotal)
        offset += 50
        sleep(15)


if __name__ == "__main__":
    run()
