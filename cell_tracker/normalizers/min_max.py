# -*- coding: UTF-8 -*-

from __future__ import absolute_import

import cv2
import numpy as np


class MinMax:
    def __init__(self):
        pass

    def __call__(self, img):
        img = img.astype(np.float32)
        min_value = np.min(img, axis=(0, 1))
        max_value = np.max(img, axis=(0, 1))
        img = (img - min_value) / (max_value - min_value)
        return np.uint8(255 * img)
