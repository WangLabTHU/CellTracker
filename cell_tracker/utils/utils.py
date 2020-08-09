# -*- coding: UTF-8 -*-

from __future__ import absolute_import

import os
import errno


def mkdir(path):
    """mimic the behavior of mkdir -p in bash"""
    try:
        os.makedirs(path)
    except OSError as exc:  # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise


def format_out(target):
    if isinstance(target, str):
        return '%s' % target
    elif isinstance(target, float):
        return '%.2f' % target
    elif isinstance(target, int):
        return '%d' % target
    else:
        return target
