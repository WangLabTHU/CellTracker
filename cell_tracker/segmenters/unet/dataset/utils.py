
# -*- coding: UTF-8 -*-

from __future__ import absolute_import
import numpy as np
import cv2


def img_reader(image_path):
    def img_standardization(img):
        img = cv2.convertScaleAbs(img)
        if len(img.shape) == 2:
            img = np.expand_dims(img, 2)
            img = np.tile(img, (1, 1, 3))
            return img
        elif len(img.shape) == 3:
            return img
        else:
            raise TypeError('The Depth of image large than 3.')

    try:
        extentions = image_path.split('.')[-1].lower()
        if extentions in ['png', 'jpg', 'jpeg', 'tif']:
            img = cv2.imread(image_path, -1)
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            img = img_standardization(img)
            return img
        else:
            raise TypeError(
                'The image type of {} is not supported in training yet.'.format(extentions))
    except:
        raise ValueError('Load image {} failed.'.format(image_path))


def label_reader(label_path):
    def label_standardization(img):
        if len(img.shape) == 3:
            img = np.squeeze(img, 2)
            return img
        elif len(img.shape) == 2:
            return img
        else:
            raise TypeError(
                'The label image shape dimension is not equal to 2 or 3.')

    try:
        extentions = label_path.split('.')[-1].lower()
        if extentions in ['png', 'tif']:
            label = cv2.imread(label_path, -1)
            label = label_standardization(label)
            return label
        else:
            raise TypeError(
                'The label image type of {} is not supported in training yet.'.format(extentions))
    except:
        raise ValueError('Load label image {} failed.'.format(label_path))


def image_norm(img):
    img = 255 * img.astype(np.float32) / np.max(img, axis=(0, 1))
    img = np.clip(img, 0, 255)
    img = img / 255.
    return img.astype(np.float32)


def dataset_mean_std(image_path_list):
    images_array = []
    for image_path in image_path_list:
        image = img_reader(image_path)
        image = image_norm(image)
        images_array.append(image)
    images_array = np.stack(images_array, axis=0)
    return np.mean(images_array, (0, 1, 2)).astype(np.float32).tolist(), \
        np.std(images_array, (0, 1, 2)).astype(np.float32).tolist()

