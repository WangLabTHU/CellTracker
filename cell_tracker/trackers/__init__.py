# -*- coding: UTF-8 -*-

from __future__ import absolute_import

from .bipartite import Bipartite

__all__ = [
    'Bipartite',
    'get_tracker'
]

__TRACKER = {
    'bipartite_tracker': Bipartite,
}


def get_tracker(name, **kwargs):
    """
    :param name: tracker name
    :return: tracker
    """
    if name not in __TRACKER:
        raise KeyError("Unknown tracker:", name)
    tracker = __TRACKER[name](**kwargs)
    return tracker
