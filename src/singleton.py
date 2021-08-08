#!/usr/bin/python3


class Singleton(object):

    _instance = None
    _initialized = False

    def __new__(cls, *args, **kwargs):
        """
        Function called, when new instance of Identity is requested
        """
        if isinstance(cls._instance, cls):
            cls.__init__ = lambda *args, **kwargs: None
        else:
            cls._instance = object.__new__(cls, *args, **kwargs)

        return cls._instance
