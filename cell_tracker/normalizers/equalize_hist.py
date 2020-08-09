# -*- coding: UTF-8 -*-

from __future__ import absolute_import

import cv2
import numpy as np


class EqualizeHist:
    def __init__(self):
        pass

    def __call__(self, img):
        img = cv2.cvtColor(img, cv2.COLOR_BGR2YUV)
        # equalize the histogram of the Y channel
        img[:, :, 0] = cv2.equalizeHist(img[:, :, 0])
        # convert the YUV image back to RGB format
        img = cv2.cvtColor(img, cv2.COLOR_YUV2BGR)
        return img
