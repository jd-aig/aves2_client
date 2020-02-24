# -*- coding:utf-8 -*-

import sys
import logging


def add_handler(stream, lvl, formatter):
    logger = logging.getLogger("")
    handler = logging.StreamHandler(stream)
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(lvl)
    return handler

def log2console(lvl=logging.INFO):
    # formatter = logging.Formatter(fmt="%(levelname)-8s: %(message)s")
    formatter = logging.Formatter(
        fmt='%(asctime)s %(levelname)-8s: %(name)s: %(message)s',
        datefmt='%H:%M:%S'
        )
    add_handler(sys.stdout, lvl, formatter)

def log2file(logfile, lvl=logging.DEBUG):
    formatter = logging.Formatter(
        fmt='%(asctime)s %(levelname)-8s: %(name)s: %(message)s',
        datefmt='%H:%M:%S'
        )
    add_handler(sys.stdout, lvl, formatter)
    add_handler(open(logfile, "w"), lvl, formatter)

def add_file_handler(logger, logfile, fmt="%(message)s"):
    handler = logging.FileHandler(logfile)
    formatter = logging.Formatter(fmt=fmt)
    handler.setFormatter(formatter)
    logger.addHandler(handler)

