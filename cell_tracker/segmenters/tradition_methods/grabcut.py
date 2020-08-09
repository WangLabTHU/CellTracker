# -*- coding: UTF-8 -*-

from __future__ import absolute_import

import cv2
import numpy as np


class GrabCut:
    def __init__(self, iteration=3):
        self.iteration = iteration
        self.label_img = None

    @staticmethod
    def bbox_verify(rect, img_sz):
        height, width = img_sz
        xmin = max(rect[0], 0)
        ymin = max(rect[1], 0)
        xmax = min(rect[2], width)
        ymax = min(rect[3], height)
        return (xmin, ymin, ymax - ymin, xmax - xmin)

    def __call__(self, img, rect, obj_idx):
        img_sz = img.shape[0:2]
        rect = self.bbox_verify(rect, img_sz)
        mask = np.zeros(img.shape[:2], np.uint8)
        bgdModel = np.zeros((1, 65), np.float64)
        fgdModel = np.zeros((1, 65), np.float64)
        # Grabcut
        cv2.grabCut(img, mask, rect, bgdModel, fgdModel,
                    self.iteration, cv2.GC_INIT_WITH_RECT)
        binary_mask = np.where((mask == 2) | (
            mask == 0), 0, obj_idx).astype('uint8')
        binary_mask = np.expand_dims(binary_mask, axis=2)  # 0 and obj_idx
        return binary_mask
