# -*- coding: UTF-8 -*-

import sys
import os.path as osp

CURRENT_DIR = osp.dirname(__file__)
ABS_DIR = osp.dirname(osp.abspath(__file__))
sys.path.append(CURRENT_DIR)
sys.path.append(osp.join(CURRENT_DIR, '..'))

from cell_tracker.segmenters.unet import TrainParameters
from cell_tracker.segmenters.unet import TrainerWrapper


if __name__ == "__main__":

    source_img_root = osp.join(ABS_DIR, 'source_img')
    label_img_root = osp.join(ABS_DIR, 'label_img')
    log_root = osp.join(ABS_DIR, 'log')
    validation_ratio = 0.2
    scale_img = 1.0
    weighted_type = 'edge_weighted'  # 'edge_weighted'，'sample_balance' and 'None'
    aug_list = ['Flip', 'Rotate', 'GaussianNoise', 'GaussianBlur']
    batch_size = 2
    workers = 4  # wait modify
    gpu_num = 1
    resume = False
    epochs = 500
    lr = 0.001
    weight_decay = 0.0005
    loss_type = 'WBCELoss'

    train_parameters = TrainParameters(source_img_root=source_img_root,
                                       label_img_root=label_img_root,
                                       log_root=log_root,
                                       validation_ratio=validation_ratio,
                                       scale_img=scale_img,
                                       weighted_type=weighted_type,
                                       aug_list=aug_list,
                                       batch_size=batch_size,
                                       workers=workers,
                                       gpu_num=gpu_num,
                                       resume=resume,
                                       epochs=epochs,
                                       lr=lr,
                                       weight_decay=weight_decay,
                                       loss_type=loss_type)
    train_wrapper = TrainerWrapper(train_parameters)
    start_epoch = train_wrapper.start_epoch
    for epoch in range(start_epoch, train_parameters.epochs):
        train_wrapper.train_epoch(epoch)
