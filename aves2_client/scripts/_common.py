#!/usr/bin/env python


import signal
import shutil

from aves2_client import utils
from aves2_client import logger


def handler(signal, frame):
    raise KeyboardInterrupt

signal.signal(signal.SIGTERM, handler)


def aves2_main():
    utils.prep_folders()
    utils.init_config()

    from aves2_client.args.job_args import aves2_parser as  parser

    args = parser.parse_args()
    logger.log2console(lvl='INFO')
    if not hasattr(args, 'func'):
        parser.print_help()
        return
    return args.func(args)

