# -*- coding:utf-8 -*-

import sys
import os
import tempfile
from datetime import datetime
import shutil
import itertools
import time
from pkg_resources import Requirement, resource_filename

if os.name == 'nt':
    # TODO: This is no pwd module on Win OS
    pass
else:
    import pwd

def dotdir():
    return os.path.expanduser("~/.aves2")

def makedirs(d):
    if os.path.isdir(d):
        return
    elif os.path.lexists(d):
        os.unlink(d)

    if sys.version_info.major > 2:
        os.makedirs(d, 0o700)
    else:
        os.makedirs(d, 448)

def our_path():
    return os.path.dirname(os.path.realpath(__file__))

def cfg_files():
    expect_cfgs = [
        os.path.join(os.path.dirname(os.path.realpath(__file__)), "../../etc/aves2/aves2.cfg"),
        "/etc/aves2/aves2.cfg",
        os.path.join(dotdir(), "aves2.cfg"),
        "aves2.cfg"
    ]
    cfgs = []
    for f in expect_cfgs:
        if os.path.isfile(f):
            cfgs.append(f)
    return cfgs

def prep_folders():
    makedirs(dotdir())

def print_warning(message):
    print("\033[1;31m" + message + "\033[0m")

def print_success(message):
    print("\033[1;32m" + message + "\033[0m")


def _print_tree(tree, buff, prefix, level):
    count = len(tree)
    for k, v in tree.items():
        count -= 1
        if v:
            buff.append('%s +- %s/' % (prefix, k))
            if count > 0:
                _print_tree(v, buff, prefix + ' |  ', level + 1)
            else:
                _print_tree(v, buff, prefix + '    ', level + 1)
        elif v == {}:
            buff.append('%s +- %s/' % (prefix, k))
        else:
            buff.append('%s +- %s' % (prefix, k))

def print_tree(tree, buff):
    _print_tree(tree, buff, '', 0)
    print('\n'.join(buff))

def sleep_and_print(sec, sign='.', count=6):
    duration = float(sec)/count
    for i in range(count):
        print("%s" % sign * (i+1), end="\r")
        time.sleep(duration)
    print("%s" % ' ' * (count+1), end="\r")

def init_config():
    path = resource_filename(
            Requirement.parse("aves2_client"),
            "etc/aves2/aves2.cfg.example"
           )
    target = os.path.join(dotdir(), 'aves2.cfg')
    if not os.path.exists(target):
        shutil.copy(path, target)


class DfInfo:
    def __init__(self):
        self._df_list = self._exec_cmd_parse_output_as_dict_list('df -h')

    def _exec_cmd_parse_output_as_dict_list(self, cmd):
        f = os.popen(cmd)
        splited = [line.split() for line in f.readlines()]
        keys = splited[0]
        values_list = splited[1:]
        l = []
        for values in values_list:
            l.append(dict(zip(keys,values)))
        f.close()
        return l

    def find_match(self, path):
        longest_match_size = 0
        longest_match = None
        for df in self._df_list:
            if path.startswith(df['Mounted']):
                if len(df['Mounted']) > longest_match_size:
                    longest_match_size = len(df['Mounted'])
                    longest_match = df
        return longest_match

df_info = DfInfo()

