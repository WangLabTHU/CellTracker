# -*- coding: UTF-8 -*-

from __future__ import absolute_import

import os.path as osp
import cv2
import numpy as np
import torch
from torch.utils.data import DataLoader
from torchvision.transforms import Compose, ToTensor
from .cell import create
from .augmentation import Augmentation
from .weighted_label import make_balance_weight_map, make_weight_map_instance
from .utils import img_reader, label_reader, image_norm


class Preprocessor(Augmentation):
    def __init__(self, dataset, mode, source_img_root, label_img_root, scale_img, weighted_type, aug_list):
        super(Preprocessor, self).__init__(aug_list=aug_list)
        self.dataset = dataset
        self.mode = mode
        self.scale_img = scale_img
        self.source_img_root = source_img_root
        self.label_img_root = label_img_root
        self.weighted_type = weighted_type

        self.mean = self.dataset.mean
        self.std = self.dataset.std

    def __len__(self):
        return len(self.dataset)

    def __getitem__(self, indices):
        if isinstance(indices, (tuple, list)):
            return [self._get_single_item(index) for index in indices]
        return self._get_single_item(indices)

    def _scale_img(self, img, label, scale_img):
        try:
            assert img.shape[0:2] == label.shape[0:2]
        except:
            raise ValueError(
                'The size of source image is not equal to label image.')
        if scale_img != 1:
            height, width = img.shape[0:2]
            size = (int(width*scale_img), int(height*scale_img))
            img = cv2.resize(img, size, interpolation=cv2.INTER_NEAREST)
            label = cv2.resize(label, size, interpolation=cv2.INTER_NEAREST)
        return img, label

    def _get_single_item(self, index):
        image_path, label_path = self.dataset[index]

        image_path = osp.join(self.source_img_root, image_path)
        label_path = osp.join(self.label_img_root, label_path)

        image = img_reader(image_path)
        label = label_reader(label_path)

        image, label = self._scale_img(image, label, self.scale_img)
        if self.mode == 'train':
            image, label = self.augment(image, label)

        weight = 0
        # enlarge edges and added weight map
        if self.weighted_type == 'edge_weighted':
            weight, label = make_weight_map_instance(label, w0=10, sigma=5)
        # balance class
        if self.weighted_type == 'sample_balance':
            weight, label = make_balance_weight_map(label)

        label[label > 0] = 1.0
        label = label.astype(np.float32)
        image = image_norm(image)
        image = (image - self.mean) / self.std
        image = image.astype(np.float32)

        image = torch.from_numpy(image.copy())
        label = torch.from_numpy(label.copy())

        return {"image": image.permute(2, 0, 1),
                "label": label,
                "weight": weight}


def build_dataloader(name, source_img_root, label_img_root, log_root, validation_ratio, scale_img,
                     weighted_type, aug_list, batch_size, workers, **kwargs):

    dataset = create(name=name, source_img_root=source_img_root, label_img_root=label_img_root,
                     log_root=log_root, validation_ratio=validation_ratio)

    train_set = dataset.train
    val_set = dataset.val

    dataset_info = {
                    'dataset_mean': train_set.mean, 
                    'dataset_std': train_set.std
    }
    
    train_loader = DataLoader(
        Preprocessor(dataset=train_set, mode='train',
                     source_img_root=source_img_root,
                     label_img_root=label_img_root,
                     scale_img=scale_img,
                     weighted_type=weighted_type,
                     aug_list=aug_list),
        batch_size=batch_size,
        num_workers=workers,
        shuffle=True,
        pin_memory=True,
        drop_last=True)

    val_loader = DataLoader(
        Preprocessor(dataset=val_set, mode='val',
                     source_img_root=source_img_root,
                     label_img_root=label_img_root,
                     scale_img=scale_img,
                     weighted_type=weighted_type,
                     aug_list=None),
        batch_size=batch_size,
        num_workers=workers,
        shuffle=False,
        pin_memory=True)

    return train_loader, val_loader, dataset_info

