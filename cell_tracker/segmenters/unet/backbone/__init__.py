# -*- coding: UTF-8 -*-

from __future__ import absolute_import

import os.path as osp
import torch.nn as nn
from .unet import UNet


__BACKBONES = {
    'unet': UNet,
}


def init_weights(model):
    for m in model.modules():
        if isinstance(m, nn.Conv2d):
            nn.init.kaiming_normal_(m.weight, mode='fan_out')
            if m.bias is not None:
                nn.init.constant_(m.bias, 0)
        elif isinstance(m, nn.BatchNorm2d):
            nn.init.constant_(m.weight, 1)
            nn.init.constant_(m.bias, 0)
        elif isinstance(m, nn.Linear):
            nn.init.normal_(m.weight, std=0.001)
            if m.bias is not None:
                nn.init.constant_(m.bias, 0)
    return model


def get_backbone(name, **kwargs):
    """
    :param name: (str): model name
    :param kwargs: other parameters
    :return:
    """
    if name not in __BACKBONES:
        raise KeyError("Unknown backbone structure:", name)
    backbone = __BACKBONES[name](**kwargs)
    backbone = init_weights(backbone)
    return backbone
