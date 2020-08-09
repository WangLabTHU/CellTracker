# -*- coding: UTF-8 -*-

import torch
import numpy as np


class BboxTransfer(object):

    @staticmethod
    def xyxy2xywh(bbox, as_int=False):
        if len(bbox.shape) == 1:
            bbox = np.array([bbox[0],
                             bbox[1],
                             (bbox[2] - bbox[0]),
                             (bbox[3] - bbox[1])]).astype(np.float32)
        else:
            bbox = np.stack((bbox[:, 0],
                             bbox[:, 1],
                             bbox[:, 2] - bbox[:, 0],
                             bbox[:, 3] - bbox[:, 1]), axis=1).astype(np.float32)
        if as_int:
            return bbox.astype(np.int32)
        return bbox

    @staticmethod
    def xyxy2ccwh(bbox, as_int=False):
        if len(bbox.shape) == 1:
            bbox = np.array([(bbox[0] + bbox[2]) / 2.,
                             (bbox[1] + bbox[3]) / 2.,
                             (bbox[2] - bbox[0]),
                             (bbox[3] - bbox[1])]).astype(np.float32)
        else:
            bbox = np.stack(((bbox[:, 0] + bbox[:, 2]) / 2.,
                             (bbox[:, 1] + bbox[:, 3]) / 2.,
                             bbox[:, 2] - bbox[:, 0],
                             bbox[:, 3] - bbox[:, 1]), axis=1).astype(np.float32)
        if as_int:
            return bbox.astype(np.int32)
        return bbox

    @staticmethod
    def ccwh2xyxy(bbox, as_int=False):
        if len(bbox.shape) == 1:
            bbox = np.expand_dims(bbox, axis=0)
            bbox = np.array([bbox[:, 0] - bbox[:, 2] / 2.,
                           bbox[:, 1] - bbox[:, 3] / 2.,
                           bbox[:, 0] + bbox[:, 2] / 2.,
                           bbox[:, 1] + bbox[:, 3] / 2.]).astype(np.float32)
            bbox = bbox.squeeze()
        else:
            bbox = np.stack((bbox[:, 0] - bbox[:, 2] / 2.,
                           bbox[:, 1] - bbox[:, 3] / 2.,
                           bbox[:, 0] + bbox[:, 2] / 2.,
                           bbox[:, 1] + bbox[:, 3] / 2.), axis=1).astype(np.float32)
        if as_int:
            return bbox.astype(np.int32)
        return bbox


def bbox_aug(bbox, ratio=10):
    th_w = (bbox[2] - bbox[0]) / ratio / 2.
    th_h = (bbox[3] - bbox[1]) / ratio / 2.
    return np.array([bbox[0] + np.random.uniform(-th_w, th_w, 1).astype(np.int32)[0],
                     bbox[1] + np.random.uniform(-th_w, th_h, 1).astype(np.int32)[0],
                     bbox[2] + np.random.uniform(-th_w, th_w, 1).astype(np.int32)[0],
                     bbox[3] + np.random.uniform(-th_w, th_h, 1).astype(np.int32)[0]])


def overlap_ratio(rect1, rect2):
    '''
    Compute overlap ratio between two rects
    - rect: 1d array of [x,y,x,y] or
          2d array of N x [x,y,x,y]
    '''

    if rect1.ndim == 1:
        rect1 = rect1[None, :]
    if rect2.ndim == 1:
        rect2 = rect2[None, :]

    left = np.maximum(rect1[:, 0], rect2[:, 0])
    right = np.minimum(rect1[:, 2], rect2[:, 2])
    top = np.maximum(rect1[:, 1], rect2[:, 1])
    bottom = np.minimum(rect1[:, 3], rect2[:, 3])
    intersect = np.maximum(0, right - left) * np.maximum(0, bottom - top)
    union = (rect1[:, 2] - rect1[:, 0]) * (rect1[:, 3] - rect1[:, 1]) + \
          (rect2[:, 2] - rect2[:, 0]) * (rect2[:, 3] - rect2[:, 1]) - intersect
    iou = np.clip(intersect / union, 0, 1)
    return iou

def overlap_ratio_area(rect1, rect2):
    '''
    Compute overlap ratio between two rects
    - rect: 1d array of [x,y,x,y] or
          2d array of N x [x,y,x,y]
    '''

    if rect1.ndim == 1:
        rect1 = rect1[None, :]
    if rect2.ndim == 1:
        rect2 = rect2[None, :]

    left = np.maximum(rect1[:, 0], rect2[:, 0])
    right = np.minimum(rect1[:, 2], rect2[:, 2])
    top = np.maximum(rect1[:, 1], rect2[:, 1])
    bottom = np.minimum(rect1[:, 3], rect2[:, 3])
    intersect = np.maximum(0, right - left) * np.maximum(0, bottom - top)
    area = (rect1[:, 2] - rect1[:, 0]) * (rect1[:, 3] - rect1[:, 1])
    iou = np.clip(intersect / area, 0, 1)
    return iou


def area_ratio(rect1, rect2):
    '''
    Compute overlap ratio between two rects
    - rect: 1d array of [x,y,x,y] or
          2d array of N x [x,y,x,y]
    '''

    if rect1.ndim == 1:
        rect1 = rect1[None, :]
    if rect2.ndim == 1:
        rect2 = rect2[None, :]

    width_rect1 = rect1[:, 2] - rect1[:, 0]
    height_rect1 = rect1[:, 3] - rect1[:, 1]
    width_rect2 = rect2[:, 2] - rect2[:, 0]
    height_rect2 = rect2[:, 3] - rect2[:, 1]
    area_ratio = (width_rect1 * height_rect1) / (width_rect2 * height_rect2)
    area_ratio = np.maximum(area_ratio, 1.0 / area_ratio)
    return area_ratio


def distance_ratio(rect1, rect2):
    '''
    Compute overlap ratio between two rects
    - rect: 1d array of [x,y,x,y] or
          2d array of N x [x,y,x,y]
    '''

    if rect1.ndim == 1:
        rect1 = rect1[None, :]
    if rect2.ndim == 1:
        rect2 = rect2[None, :]

    width_rect1 = rect1[:, 2] - rect1[:, 0]
    height_rect1 = rect1[:, 3] - rect1[:, 1]
    # width_rect2 = rect2[:, 2] - rect2[:, 0]
    # height_rect2 = rect2[:, 3] - rect2[:, 1]
    centerx_rect1 = (rect1[:, 0] + rect1[:, 2]) / 2.0
    centery_rect1 = (rect1[:, 1] + rect1[:, 3]) / 2.0
    centerx_rect2 = (rect2[:, 0] + rect2[:, 2]) / 2.0
    centery_rect2 = (rect2[:, 1] + rect2[:, 3]) / 2.0
    dis = np.sqrt(np.power((centerx_rect1 - centerx_rect2), 2) + np.power((centery_rect1 - centery_rect2), 2))
    radis1 = np.sqrt(np.power(width_rect1, 2) + np.power(height_rect1, 2)) / 2.0
    dis_ratio = dis / radis1
    return dis_ratio


def overlap_ratio_wh(rect1, rect2):
    '''
    Compute overlap ratio between two rects
    - rect: 1d array of [x,y,w,h] or
          2d array of N x [x,y,w,h]
    '''

    if rect1.ndim == 1:
        rect1 = rect1[None, :]
    if rect2.ndim == 1:
        rect2 = rect2[None, :]
    left = np.maximum(rect1[:, 0], rect2[:, 0])
    right = np.minimum(rect1[:, 0] + rect1[:, 2], rect2[:, 0] + rect2[:, 2])
    top = np.maximum(rect1[:, 1], rect2[:, 1])
    bottom = np.minimum(rect1[:, 1] + rect1[:, 3], rect2[:, 1] + rect2[:, 3])

    intersect = np.maximum(0, right - left) * np.maximum(0, bottom - top)
    union = rect1[:, 2] * rect1[:, 3] + rect2[:, 2] * rect2[:, 3] - intersect
    iou = np.clip(intersect / union, 0, 1)
    return iou


def clip_bbox(bbox, imgsize):
    """
    bbox is in [x,y,x,y]
    imgsize is in [h, w]
    """
    bbox_cliq = np.zeros(4)
    bbox_cliq[0] = max(0, bbox[0])
    bbox_cliq[1] = max(0, bbox[1])
    bbox_cliq[2] = min(imgsize[1] - 1, bbox[2])
    bbox_cliq[3] = min(imgsize[0] - 1, bbox[3])
    return bbox_cliq.astype(np.int16)


def non_max_suppression(boxes, max_bbox_overlap, scores=None):
    """Suppress overlapping detections.

        Original code from [1]_ has been adapted to include confidence score.

        .. [1] http://www.pyimagesearch.com/2015/02/16/
            faster-non-maximum-suppression-python/

        Examples
        --------
        >>> boxes = [d.roi for d in detections]
        >>> scores = [d.confidence for d in detections]
        >>> indices = non_max_suppression(boxes, max_bbox_overlap, scores)
        >>> detections = [detections[i] for i in indices]

        Parameters
        ----------
        boxes : ndarray
            Array of ROIs (x, y, width, height).
        max_bbox_overlap : float
            ROIs that overlap more than this values are suppressed.
        scores : Optional[array_like]
            Detector confidence score.

        Returns
        -------
        List[int]
            Returns indices of detections that have survived non-maxima suppression.
    """
    if len(boxes) == 0:
        return []
    boxes = boxes.astype(np.float)
    pick = []
    x1 = boxes[:, 0]
    y1 = boxes[:, 1]
    x2 = boxes[:, 2] + boxes[:, 0]
    y2 = boxes[:, 3] + boxes[:, 1]

    area = (x2 - x1 + 1) * (y2 - y1 + 1)
    if scores is not None:
        idxs = np.argsort(scores)
    else:
        # idxs = np.argsort(y2)
        # idxs = np.arange(len(boxes))[::-1]
        idxs = np.arange(len(boxes))

    while len(idxs) > 0:
        last = len(idxs) - 1
        i = idxs[last]
        pick.append(i)

        xx1 = np.maximum(x1[i], x1[idxs[:last]])
        yy1 = np.maximum(y1[i], y1[idxs[:last]])
        xx2 = np.minimum(x2[i], x2[idxs[:last]])
        yy2 = np.minimum(y2[i], y2[idxs[:last]])
        w = np.maximum(0, xx2 - xx1 + 1)
        h = np.maximum(0, yy2 - yy1 + 1)

        overlap = (w * h) / area[idxs[:last]]
        idxs = np.delete(idxs, np.concatenate(([last], np.where(overlap > max_bbox_overlap)[0])))

    return pick


def soft_nms(boxes, scores, Nt=0.5, sigma=0.5, thresh=0.001, method='nms'):
    """Soft Suppress overlapping detections.
            Parameters
            ----------
            boxes : ndarray
                Array of ROIs (x, y, width, height).
            scores : array_like
                Detector confidence score.
            Nt : float
                ROIs that overlap more than this values are suppressed.
            sigma : float
                constant parameter of soft-gaussian
            thresh : float
                minimal score of pick detection
            method: str
                one of soft-gaussian, soft-linear, nms

            Returns
            -------
            List[int]
                Returns indices of detections that have survived soft non-maxima suppression.
        """
    if len(boxes) == 0:
        return []
    boxes = boxes.astype(np.float)

    # indexes concatenate boxes with the last column
    N = boxes.shape[0]
    indexes = np.array([np.arange(N)])
    boxes = np.concatenate((boxes, indexes.T), axis=1)

    x1 = boxes[:, 0]
    y1 = boxes[:, 1]
    x2 = boxes[:, 2] + boxes[:, 0]
    y2 = boxes[:, 3] + boxes[:, 1]
    areas = (x2 - x1 + 1) * (y2 - y1 + 1)

    for i in range(N):
        # intermediate parameters for later parameters exchange
        t_bbox = boxes[i, :].copy()
        t_score = scores[i].copy()
        t_area = areas[i].copy()
        pos = i + 1

        if i != N - 1:
            max_score = np.max(scores[pos:], axis=0)
            max_pos = np.argmax(scores[pos:], axis=0)
        else:
            max_score = scores[-1]
            max_pos = 0
        if t_score < max_score:
            boxes[i, :] = boxes[max_pos + i + 1, :]
            boxes[max_pos + i + 1, :] = t_bbox
            # t_bbox = boxes[i, :]

            scores[i] = scores[max_pos + i + 1]
            scores[max_pos + i + 1] = t_score
            # t_score = scores[i]

            areas[i] = areas[max_pos + i + 1]
            areas[max_pos + i + 1] = t_area
            # t_area = areas[i]

        # IoU calculate
        xx1 = np.maximum(x1[i], x1[pos:])
        yy1 = np.maximum(y1[i], y1[pos:])
        xx2 = np.minimum(x2[i], x2[pos:])
        yy2 = np.minimum(y2[i], y2[pos:])

        w = np.maximum(0.0, xx2 - xx1 + 1)
        h = np.maximum(0.0, yy2 - yy1 + 1)
        inter = w * h
        ovr = inter / (areas[i] + areas[pos:] - inter)

        if method == 'soft-linear':
            weight = np.ones(ovr.shape)
            weight[ovr > Nt] = weight[ovr > Nt] - ovr[ovr > Nt]
        elif method == 'soft-gaussian':
            weight = np.exp(-(ovr * ovr) / sigma)
        elif method == 'nms':
            weight = np.ones(ovr.shape)
            weight[ovr > Nt] = 0
        else:
            raise ValueError('No such of methods {} for soft nms'.format(method))
        scores[pos:] = weight * scores[pos:]

    indexes = boxes[:, 4][scores > thresh]
    pick = indexes.astype(int)
    return pick



