# -*- coding: UTF-8 -*-

from __future__ import print_function, absolute_import

import os
import sys
import random
import os.path as osp
import numpy as np
import torch
from torch import nn
from torch.backends import cudnn

from .backbone import get_backbone
from .trainer import get_trainer
from .loss import build_loss
from .dataset import build_dataloader
from .utils import Logger, load_checkpoint, save_checkpoint, export_history


class TrainerWrapper(object):
    def __init__(self, train_parameters):
        self.train_parameters = train_parameters
        self._init()

    def _init(self):
        if self.train_parameters.gpu_num:
            os.environ['CUDA_VISIBLE_DEVICES'] = ','.join(
                [str(x) for x in range(self.train_parameters.gpu_num)])
        random.seed(self.train_parameters.train_seed)
        np.random.seed(self.train_parameters.train_seed)
        torch.manual_seed(self.train_parameters.train_seed)
        cudnn.benchmark = True

        # Redirect print to both console and log file
        self.train_log = Logger(
            osp.join(self.train_parameters.log_root, 'train.log'))
        self.train_loader, self.val_loader, self.dataset_info = build_dataloader(
            name='cells', **self.train_parameters.dataloader_params)
        self.model = get_backbone(name='unet').to(self.train_parameters.device)
        if self.train_parameters.gpu_num > 1:
            self.model = nn.DataParallel(self.model).to(
                self.train_parameters.device)
        else:
            self.model = self.model.to(self.train_parameters.device)

        self.criterion = build_loss(name=self.train_parameters.loss_type).to(
            self.train_parameters.device)

        self.optimizer = torch.optim.Adam(
            self.model.parameters(), **self.train_parameters.optimizer_params)

        # Load from checkpoint
        self.start_epoch = 0
        self.best_loss = 1e8

        # Trainer
        self.trainer = get_trainer(
            name='unet_trainer', model=self.model, criterion=self.criterion)

        if self.train_parameters.resume:
            try:
                print("load previous checkpoint file from {} \n".format(
                    self.train_parameters.resume), file=self.train_log)
                checkpoint = load_checkpoint(self.train_parameters.resume)
                self.model.load_state_dict(checkpoint['state_dict'])
                self.best_loss = checkpoint['best_loss']
                self.start_epoch = checkpoint['epoch']
                print("=> Start epoch {}  best_loss {:.3%}".format(
                    self.start_epoch, self.best_loss), file=self.train_log)
            except:
                raise ValueError(
                    'Load previous checkpoint file {} failed.".format(train_parameters.resume)')

    # Start training
    def train_epoch(self, epoch):

        train_loss = self.trainer.train(epoch, self.train_loader, self.optimizer,
                                        device=self.train_parameters.device, log=self.train_log)
        val_loss = self.trainer.eval(epoch, self.val_loader,
                                     device=self.train_parameters.device, log=self.train_log)

        values = [epoch + 1, train_loss, val_loss]
        header = ['epoch', 'train_loss', 'val_loss']
        export_history(header=header, value=values, file_path=osp.join(
            self.train_parameters.log_root, "loss_per_epoch.csv"))

        is_best = val_loss < self.best_loss
        self.best_loss = min(val_loss, self.best_loss)
        save_checkpoint({
            'state_dict': self.model.state_dict(),
            'epoch': epoch + 1,
            'best_loss': self.best_loss,
            'dataset_info' : self.dataset_info,
        }, is_best, fpath=osp.join(self.train_parameters.log_root, 'checkpoint.pth.tar'))

        print('\n * Finished epoch {:3d}  train_loss: {:.3f}  val_loss: {:.3f}  best: {:.3f}{}\n'.
              format(epoch, train_loss, val_loss, self.best_loss, ' *' if is_best else ''), file=self.train_log)
