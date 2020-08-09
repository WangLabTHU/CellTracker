# -*- coding: UTF-8 -*-

from __future__ import print_function, absolute_import

import os.path as osp
from glob import glob
import numpy as np
from .benchmark import Benchmark
from .utils import dataset_mean_std
from ..utils import mkdir, write_json


class Cells(Benchmark):

    def __init__(self, source_img_root, label_img_root, log_root, validation_ratio):
        super(Cells, self).__init__(log_root)
        self.source_img_root = source_img_root
        self.label_img_root = label_img_root
        self.validation_ratio = validation_ratio

        self.make()
        if not self._check_integrity():
            raise RuntimeError("Dataset not found or corrupted. " +
                               "Please check it.")

        self.load()

    def make(self):

        images = []
        labels = []
        images += sorted(glob(osp.join(self.source_img_root, '*')))
        labels += sorted(glob(osp.join(self.label_img_root, '*')))
        try:
            assert len(images) == len(labels)
        except:
            raise ValueError(
                'The number of train image is not equal to the number of label image.')

        # Calculate dataset mean and std for every channels
        mean, std = dataset_mean_std(images)

        num = len(images)
        num_val = int(round(num * self.validation_ratio))
        ids = np.random.permutation(num).tolist()
        train_ids = sorted(ids[:-num_val])
        val_ids = sorted(ids[-num_val:])

        # Save meta information into a json file
        split = {
            'dataset_mean': mean,
            'dataset_std': std,
            'train_images': [images[idx] for idx in train_ids],
            'train_labels': [labels[idx] for idx in train_ids],
            'validate_images': [images[idx] for idx in val_ids],
            'validate_labels': [labels[idx] for idx in val_ids]
        }
        write_json(split, osp.join(self.log_root, 'train_val_splits.json'))


__factory = {
    'cells': Cells,
}


def create(name, *args, **kwargs):
    """
    Create a dataset instance.

    Parameters
    ----------
    name : str
        The dataset name.
    """
    if name not in __factory:
        raise KeyError("Unknown dataset:", name)
    return __factory[name](*args, **kwargs)
