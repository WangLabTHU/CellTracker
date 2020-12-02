# -*- coding: UTF-8 -*-

from __future__ import absolute_import

import cv2
import numpy as np
from ..utils import instance_filtering


def bgr_to_gray(img):
    img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    return img


class WaterShed:
    def __init__(self, minimal_size=0, noise_amplitude=5, dist_thresh=0.5):
        self.noise_amplitude = noise_amplitude
        self.dist_thresh = 1 - dist_thresh
        self._minimal_size = minimal_size

    def __call__(self, img, makers=None):
        gray = bgr_to_gray(img)
        if makers is None:
            _, thresh_img = cv2.threshold(
                gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
            # remove noise foreground with opening
            kernel = np.ones((3, 3), np.uint8)
            opening = cv2.morphologyEx(
                thresh_img, cv2.MORPH_OPEN, kernel, iterations=self.noise_amplitude)
            # dilate foreground to get sure background area
            sure_bg = cv2.dilate(opening, kernel, iterations=3)
            # Finding sure foreground area according to the distance to background
            dist_transform = cv2.distanceTransform(opening, cv2.DIST_L2, 5)
            _, sure_fg = cv2.threshold(
                dist_transform, self.dist_thresh * dist_transform.max(),  255, 0)
            # Finding border region
            sure_fg = np.uint8(sure_fg)
            border = cv2.subtract(sure_bg, sure_fg)
            # Marker labelling
            ret, markers = cv2.connectedComponents(sure_fg)
            # Add one to all labels so that sure background is not 0, but 1
            markers = markers+1
            # Now, mark the region of border with zero
            markers[border == 255] = 0
            label_img = cv2.watershed(img, markers)  # -1 for edge
            label_img[label_img == -1] = 0  # edge
            label_img[label_img == 1] = 0  # background
            label_img = np.maximum(label_img - 1, 0)
            label_img = np.expand_dims(label_img, axis=2)
            label_img = instance_filtering(
                label_img, minimal_size=self._minimal_size)
            return label_img
