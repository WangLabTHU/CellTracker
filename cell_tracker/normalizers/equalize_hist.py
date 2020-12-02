# -*- coding: UTF-8 -*-

from __future__ import absolute_import

import cv2
import numpy as np


class EqualizeHist:
    def __init__(self):
        pass

    def __call__(self, img):
        img = cv2.cvtColor(img, cv2.COLOR_RGB2YUV)
        # equalize the histogram of the Y channel
        img[:, :, 0] = cv2.equalizeHist(img[:, :, 0])
        # convert the YUV image back to RGB format
        img = cv2.cvtColor(img, cv2.COLOR_YUV2RGB)
        return img


# Contrast limited adaptive histogram equalization
class CLAHE:
    def __init__(self, clip_limit=2.0, grid_width=8, grid_height=8):
        self.clahe = cv2.createCLAHE(clipLimit=clip_limit,
                                     tileGridSize=(int(grid_height), int(grid_width)))

    def __call__(self, img):
        # Converting image to LAB Color model
        img = cv2.cvtColor(img, cv2.COLOR_RGB2LAB)
        # Splitting the LAB image to different channels
        l, a, b = cv2.split(img)
        # Applying CLAHE to L-channel
        cl = self.clahe.apply(l)
        limg = cv2.merge((cl, a, b))
        # Converting image from LAB Color model to RGB model
        img = cv2.cvtColor(limg, cv2.COLOR_LAB2RGB)
        return img