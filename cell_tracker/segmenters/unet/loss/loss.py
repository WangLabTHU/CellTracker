# -*- coding: UTF-8 -*-

from __future__ import absolute_import
import torch.nn as nn
import torch
import torch.nn.functional as F


""" 
    Class that defines the Dice Loss function.
"""


class DiceLoss(nn.Module):

    def __init__(self, smooth=1):
        super(DiceLoss, self).__init__()
        self.smooth = smooth

    def dice_coef(self, y_pred, y_true):
        pred_probs = F.sigmoid(y_pred)
        y_true_f = y_true.view(-1)
        y_pred_f = pred_probs.view(-1)
        intersection = torch.sum(y_true_f * y_pred_f)
        return (2. * intersection + self.smooth) / (torch.sum(y_true_f) + torch.sum(y_pred_f) + self.smooth)

    def forward(self, y_pred, y_true, **kwargs):
        return 1 - self.dice_coef(y_pred, y_true)


class WeightedSoftDiceLoss(nn.Module):
    def __init__(self):
        super(WeightedSoftDiceLoss, self).__init__()

    def forward(self, y_pred, y_true, weights, **kwargs):
        try:
            assert weights is not None
        except:
            raise ValueError(
                'weight option should be selected for WeightedSoftDiceLoss.')
        probs = F.sigmoid(y_pred)
        num = y_true.size(0)
        w = weights.view(num, -1)
        w2 = w
        m1 = probs.view(num, -1)
        m2 = y_true.view(num, -1)
        intersection = (m1 * m2)
        score = 2. * ((w2 * intersection).sum(1) + 1) / (
            (w2 * m1).sum(1) + (w2 * m2).sum(1) + 1)
        score = 1 - score.sum() / num
        return score


"""
    Class that defines the Binary Cross Entropy Loss Function
"""


class BCELoss(nn.Module):
    def __init__(self):
        super(BCELoss, self).__init__()
        self.bce = nn.BCEWithLogitsLoss(reduction='mean')

    def forward(self, y_pred, y_true, **kwargs):
        batch_size = y_pred.size(0)
        return self.bce(y_pred.view(batch_size, -1), y_true.view(batch_size, -1))


"""
    Class that defines the Weighted Binary Cross Entropy Loss Function
"""


class WBCELoss(nn.Module):
    def __init__(self):
        super(WBCELoss, self).__init__()
        self.bce = nn.BCEWithLogitsLoss(reduction='none')

    def forward(self, y_pred, y_true, weights, **kwargs):
        try:
            assert weights is not None
        except:
            raise ValueError('weight option should be selected for WBCELoss.')
        batch_size = y_pred.size(0)
        loss = self.bce(y_pred.view(batch_size, -1),
                        y_true.view(batch_size, -1))
        return torch.mean(loss * weights.view(batch_size, -1))


class MSELoss(nn.Module):
    def __init__(self):
        super(MSELoss, self).__init__()
        self.mse = nn.MSELoss()

    def forward(self, y_pred, y_true, **kwargs):
        y_pred = F.sigmoid(y_pred)
        return self.mse(y_pred, y_true)


class MAELoss(nn.Module):
    def __init__(self):
        super(MAELoss, self).__init__()
        self.mae = nn.L1Loss()

    def forward(self, y_pred, y_true, **kwargs):
        y_pred = F.sigmoid(y_pred)
        return self.mae(y_pred, y_true)
