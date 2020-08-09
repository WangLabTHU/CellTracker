# -*- coding: UTF-8 -*-


from __future__ import absolute_import

import os.path as osp
import torch.nn as nn
from .trainer import UnetTrainer


__TRAINER = {
    'unet_trainer': UnetTrainer,
}


def get_trainer(name, **kwargs):
    """
    :param name: (str): trainer name
    :param kwargs: other parameters
    :return:
    """
    if name not in __TRAINER:
        raise KeyError("Unknown trainer structure:", name)
    trainer = __TRAINER[name](**kwargs)
    return trainer
