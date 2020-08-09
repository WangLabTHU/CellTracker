# -*- coding: UTF-8 -*-

from __future__ import print_function, absolute_import

import os.path as osp
import numpy as np
from ..utils import read_json, mkdir
from cell_tracker.utils import logger


def _pluck(images, labels):
    ret = []
    for image, label in zip(images, labels):
        ret.append((image, label))
    return ret


class DatasetWrapper(object):
    def __init__(self, data, mean, std):
        self._data = data
        self.mean = mean
        self.std = std

    def __len__(self):
        return len(self._data)

    def __getitem__(self, index):
        return self._data[index]


class Benchmark(object):
    def __init__(self, log_root):
        self.log_root = log_root
        self.train, self.val = [], []

        if not osp.isdir(self.log_root):
            mkdir(self.log_root)

    @property
    def train_log_dir(self):
        self.log_root

    def load(self,  verbose=True):
        self.train_val_splits = read_json(
            osp.join(self.log_root, 'train_val_splits.json'))
        train_images = self.train_val_splits['train_images']
        train_labels = self.train_val_splits['train_labels']
        validate_images = self.train_val_splits['validate_images']
        validate_labels = self.train_val_splits['validate_labels']
        mean = self.train_val_splits['dataset_mean']
        std = self.train_val_splits['dataset_std']

        self.train = DatasetWrapper(
            _pluck(train_images, train_labels), mean, std)
        self.val = DatasetWrapper(
            _pluck(validate_images, validate_labels), mean, std)

        num_train = len(self.train)
        num_val = len(self.val)

        if verbose:
            print(self.__class__.__name__, "dataset loaded")
            print("  subset   | # images")
            print("  ---------------------------")
            print("  train    | {:8d}"
                  .format(num_train))
            print("  val      | {:8d}"
                  .format(num_val))

            logger.info("%s dataset loaded" % self.__class__.__name__)
            logger.info("  subset   | # images")
            logger.info("  ---------------------------")
            logger.info("  train    | {:8d}"
                        .format(num_train))
            logger.info("  val      | {:8d}"
                        .format(num_val))

    def _check_integrity(self):
        return osp.isfile(osp.join(self.log_root, 'train_val_splits.json'))
