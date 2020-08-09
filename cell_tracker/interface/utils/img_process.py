# -*- coding: UTF-8 -*-

from __future__ import absolute_import

import cv2
import numpy as np
import os.path as osp
from cell_tracker.utils import logger
from ..components.frame import Frame


def unit16b2uint8(img):
    if img.dtype == 'uint8':
        return img
    elif img.dtype == 'uint16':
        img = img.astype(np.float32) / 65535.0 * 255.0
        return img.astype(np.uint8)
    else:
        logger.error(
            'No such of image transfer type: {} for image/'.format(img.dtype))
        raise TypeError(
            'No such of image transfer type: {} for image/'.format(img.dtype))


def img_standardization(img):
    img = cv2.convertScaleAbs(img)
    if len(img.shape) == 2:
        img = np.expand_dims(img, 2)
        img = np.tile(img, (1, 1, 3))
        return img
    elif len(img.shape) == 3:
        return img
    else:
        logger.error('The image shape dimension is not equal to 2 or 3.')
        raise TypeError('The image shape dimension is not equal to 2 or 3.')


def load_images(file_names):
    extentions = file_names[0].split('.')[-1].lower()
    frames = {}

    if extentions in ['png', 'jpg', 'jpeg', 'tif']:
        for idx, file_name in enumerate(file_names):
            img = cv2.imread(file_name, -1)
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            img = img_standardization(img)
            frame = Frame(file_name=file_name, frame_id=idx, raw_img=img)
            frames[idx] = frame

    elif extentions in ['mp4', 'avi', 'mpg']:
        if len(file_names) > 1:
            logger.error('The number of selected video ({}) file larger than one.'.format(
                ';'.join(file_names)))
            raise ValueError('The number of selected video ({}) file larger than one.'.format(
                ';'.join(file_names)))
        capture = cv2.VideoCapture(file_names[0])
        dirname = osp.dirname(file_names[0])
        idx = 0
        while True:
            ret, img = capture.read()
            if ret:
                img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                img = img_standardization(img)
                file_name = osp.join(dirname, '{:0>6d}.jpg'.format(idx))
                try:
                    cv2.imwrite(file_name, img)
                except:
                    pass
                frame = Frame(file_name=file_name, frame_id=idx, raw_img=img)
                frames[idx] = frame
                idx += 1
            else:
                break
        capture.release()

    else:
        logger.error(
            'No supported images format with extentions: {}.'.format(extentions))
        raise TypeError(
            'No supported images format with extentions: {}.'.format(extentions))

    if not len(frames) >= 1:
        logger.error('Load images failure, image number less than 1.')
        raise ValueError('Load images failure, image number less than 1.')

    return frames
