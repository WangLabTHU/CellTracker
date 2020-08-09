# -*- coding: UTF-8 -*-

from __future__ import absolute_import

import os.path as osp
import cv2
import numpy as np
import torch
from torchvision.transforms import Compose
from torchvision.transforms import Normalize
from torchvision.transforms import ToTensor
from .backbone import get_backbone
from .utils import mkdir
from .utils import load_params
from .dataset.utils import image_norm
from ..utils import bgr_to_gray
from ..utils import gray_to_bgr
from ..utils import instance_filtering


class Unet:
    def __init__(self, model_path, minimal_size=0, threshold=0.5, scale_img=0.5, device='cpu'):
        if torch.cuda.is_available() and device == 'gpu':
            self._device = 'cuda'
        else:
            self._device = 'cpu'
        self._scale_img = scale_img
        self._model_path = model_path
        self._threshold = threshold
        self._minimal_size = minimal_size
        self._model, self.dataset_info = self._load_model(device=self._device)
        self._load_mean_std()
        self.height, self.width = None, None

    def _load_model(self, device):
        # Create the model
        model = get_backbone(name='unet', n_channels=3,
                             n_classes=1).to(device).eval()
        model, dataset_info = load_params(model, self._model_path)
        return model, dataset_info

    def _load_mean_std(self):
        self.mean = self.dataset_info['dataset_mean']
        self.std = self.dataset_info['dataset_std']

    def _scaling_img(self, img, scale_img):
        self.height, self.width = img.shape[0:2]
        size = (int(self.width*scale_img), int(self.height*scale_img))
        img = cv2.resize(img, size, interpolation=cv2.INTER_NEAREST)
        return img

    def _scaling_img_recover(self, img):
        size = (self.width , self.height)
        img = cv2.resize(img, size, interpolation=cv2.INTER_NEAREST)
        return img
        
    def _pre_process(self, img):
        img = self._scaling_img(img, scale_img=self._scale_img)
        img = image_norm(img)
        img = (img - self.mean) / self.std
        img = img.astype(np.float32)
        img = torch.from_numpy(img.copy())
        return img.permute(2, 0, 1).unsqueeze(0)

    def __call__(self, img):
        with torch.no_grad():
            img = self._pre_process(img)
            img = img.to(self._device)
            binary_mask = torch.sigmoid(self._model(img)).squeeze(
                dim=0).permute(dims=[1, 2, 0]).cpu().numpy()
            binary_mask = cv2.medianBlur(
                (255 * binary_mask).astype(np.uint8), 3)
            binary_mask = binary_mask.astype(np.float) / 255
            binary_mask[binary_mask < self._threshold] = 0
            binary_mask[binary_mask >= self._threshold] = 1
            binary_mask = (255 * binary_mask).astype(np.uint8)
            binary_mask = self._scaling_img_recover(binary_mask)
            # binary_mask = cv2.dilate(binary_mask, np.ones((3, 3), np.uint8))
            binary_mask = np.expand_dims(binary_mask, 2)
            _, label_img, _, _ = cv2.connectedComponentsWithStats(
                binary_mask, connectivity=4, ltype=cv2.CV_32S)
            label_img = np.expand_dims(label_img, axis=2)
            label_img = instance_filtering(
                label_img, minimal_size=self._minimal_size)
        return label_img
