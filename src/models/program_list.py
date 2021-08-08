#!/usr/bin/python3.7


class ProgramListModel:

    programs = list()

    recordsTotal = 0

    def __str__(self):
        return "Total: " + str(self.recordsTotal) + "\n" \
               "Programs count: " + str(len(self.programs))
