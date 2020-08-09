# -*- coding: UTF-8 -*-

from __future__ import absolute_import

from .writer import Writer


def get_writer(**kwargs):
    """
    :return: writer
    """
    writer = Writer(**kwargs)
    return writer
