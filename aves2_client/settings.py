# -*- coding:utf-8 -*-


import urllib
try:
    import ConfigParser as configparser
except ImportError:
    import configparser
from configobj import ConfigObj
from aves2_client.utils import cfg_files


def _aves2_cfg():
    """ Read aipctl config
    """
    config = ConfigObj()

    # The result is a merge of all the files as they appear in the list
    f_list = cfg_files()
    if not f_list:
        print("error: configuration file not found")
        exit(1)

    for f in cfg_files():
        _cfg = ConfigObj(f, encoding='UTF8')
        config.merge(_cfg)

    return config


aves2_cfg = _aves2_cfg()
