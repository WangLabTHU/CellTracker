# -*- coding: UTF-8 -*-

from __future__ import absolute_import

import cv2
import numpy as np


class CustomizedSegmentor:
    """
    Parameters
    ----------
    img : numpy array
        Input array or original image.

    Returns
    -------
    res : label_image
        Instance Id numpy array. same shape as image. zeros for background
    """

    def __init__(self):
        pass

    def __call__(self, img):
        raise NotImplementedError
