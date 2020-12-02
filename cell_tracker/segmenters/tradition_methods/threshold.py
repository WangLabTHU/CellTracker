# -*- coding: UTF-8 -*-

from __future__ import absolute_import

import cv2
import numpy as np
from ..utils import bgr_to_gray
from ..utils import gray_to_bgr
from ..utils import instance_filtering


class BinaryThresholding:
    def __init__(self, threshold, minimal_size=0):
        self.threshold = threshold
        self._minimal_size = minimal_size

    def __call__(self, img):
        gray = bgr_to_gray(img)
        (_, binary_mask) = cv2.threshold(
            gray, self.threshold, 255, cv2.THRESH_BINARY)
        binary_mask = np.expand_dims(binary_mask, 2)
        _, label_img, _, _ = cv2.connectedComponentsWithStats(
            binary_mask, connectivity=4, ltype=cv2.CV_32S)
        label_img = np.expand_dims(label_img, axis=2)
        label_img = instance_filtering(
            label_img, minimal_size=self._minimal_size)
        return label_img


class OtsuThresholding:
    def __init__(self, minimal_size=0):
        self.threshold = 0.0
        self._minimal_size = minimal_size

    def __call__(self, img):
        gray = bgr_to_gray(img)
        (_, binary_mask) = cv2.threshold(
            gray, self.threshold, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        binary_mask = np.expand_dims(binary_mask, 2)
        _, label_img, _, _ = cv2.connectedComponentsWithStats(
            binary_mask, connectivity=4, ltype=cv2.CV_32S)
        label_img = np.expand_dims(label_img, axis=2)
        label_img = instance_filtering(
            label_img, minimal_size=self._minimal_size)
        return label_img 