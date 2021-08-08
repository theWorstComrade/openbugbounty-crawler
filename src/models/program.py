#!/usr/bin/python3.7


class ProgramModel:

    name = None

    url = None

    scope = list()

    checked_at = None

    def __str__(self):
        return "Name: " + str(self.name) + "\n" \
               "URL: " + str(self.url) + "\n" \
               "CheckedAt: " + str(self.checked_at) + "\n" \
               "Scope: " + str(self.scope)
