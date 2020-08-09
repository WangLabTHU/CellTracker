# -*- coding: UTF-8 -*-

from __future__ import absolute_import
from .equalize_hist import EqualizeHist
from .retinex import RetinexMSRCP
from .retinex import RetinexMSRCR
from .min_max import MinMax


__all__ = [
    'EqualizeHist',
    'RetinexMSRCR',
    'RetinexMSRCP',
    'MinMax'
]


__NORMALIZER = {
    'equalize_hist': EqualizeHist,
    'retinex_MSRCP': RetinexMSRCP,
    'retinex_MSRCR': RetinexMSRCR,
    'min_max': MinMax
}


def get_normalizer(name, **kwargs):
    """
    :param name: normalizer name
    :return: normalizer
    """
    if name not in __NORMALIZER:
        raise KeyError("Unknown normalizer:", name)
    normalizer = __NORMALIZER[name](**kwargs)
    return normalizer
