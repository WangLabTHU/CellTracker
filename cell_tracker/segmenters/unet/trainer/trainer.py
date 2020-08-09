# -*- coding: UTF-8 -*-

from __future__ import print_function, absolute_import

import time
import torch
from ..utils import AverageMeter


class BaseTrainer(object):
    def __init__(self, model, criterion):
        super(BaseTrainer, self).__init__()
        self.model = model
        self.criterion = criterion

    def train(self, epoch, data_loader, optimizer, device, log, print_freq=1):

        self.model.train()
        batch_time = AverageMeter()
        data_time = AverageMeter()
        losses = AverageMeter()

        end = time.time()
        for i, inputs in enumerate(data_loader):
            data_time.update(time.time() - end)

            loss, batch_size = self._forward(inputs, device)

            losses.update(loss.item(), batch_size)

            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

            batch_time.update(time.time() - end)
            end = time.time()

            if (i + 1) % print_freq == 0:
                print('train: \t'
                      'Epoch: [{}][{}/{}]\t'
                      'Time {:.3f} ({:.3f})\t'
                      'Data {:.3f} ({:.3f})\t'
                      'Loss {:.5f} ({:.5f})\t'
                      .format(epoch, i + 1, len(data_loader),
                              batch_time.val, batch_time.avg,
                              data_time.val, data_time.avg,
                              losses.val, losses.avg), file=log)
        return losses.avg

    def eval(self, epoch, data_loader, device, log, print_freq=1):

        self.model.eval()

        batch_time = AverageMeter()
        data_time = AverageMeter()
        losses = AverageMeter()

        end = time.time()
        with torch.no_grad():
            for i, inputs in enumerate(data_loader):
                data_time.update(time.time() - end)

                loss, batch_size = self._forward(inputs, device)

                losses.update(loss.item(), batch_size)

                batch_time.update(time.time() - end)
                end = time.time()

                if 0 == (i + 1) % print_freq:
                    print('validation: \t'
                          'Epoch: [{}][{}/{}]\t'
                          'Time {:.3f} ({:.3f})\t'
                          'Data {:.3f} ({:.3f})\t'
                          'Loss {:.5f} ({:.5f})\t'
                          .format(epoch, i + 1, len(data_loader),
                                  batch_time.val, batch_time.avg,
                                  data_time.val, data_time.avg,
                                  losses.val, losses.avg), file=log)

        return losses.avg

    def _forward(self, inputs, device):
        raise NotImplementedError


class UnetTrainer(BaseTrainer):

    def _parse_data(self, inputs, device):
        data, label, weight = inputs["image"], inputs["label"], inputs["weight"]
        data, label = data.to(device), label.to(device)
        if len(weight.shape) > 3:
            weight = weight.to(device)
        return {"data": data,
                "label": label,
                "weight": weight}

    def _forward(self, inputs, device):
        inputs = self._parse_data(inputs, device)
        batch_size = inputs["label"].size(0)
        predictions = self.model(inputs["data"])
        loss = self.criterion(y_pred=predictions,
                              y_true=inputs["label"], weights=inputs["weight"])
        return loss, batch_size
