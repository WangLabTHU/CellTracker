# -*- coding: UTF-8 -*-

from __future__ import absolute_import
import errno
import os
from os.path import join, isfile
from ..config import icon_path


def mkdir(path):
    """mimic the behavior of mkdir -p in bash"""
    try:
        os.makedirs(path)
    except OSError as exc:  # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise


def get_icon(name):
    icon = join(icon_path, name)
    if isfile(icon):
        return icon
    else:
        raise Exception("Invalid icon!", name)
