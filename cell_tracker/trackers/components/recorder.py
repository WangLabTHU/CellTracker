
# -*- coding: UTF-8 -*-

from __future__ import absolute_import

import numpy as np
from ..utils import InferenceUtil


class Recorder:
    '''
    Record features and boxes every frame
    '''

    def __init__(self, max_record_frame=5000):
        self.max_record_frame = max_record_frame
        self.all_frame_index = np.array([], dtype=int)
        self.all_regions = {}
        self.all_boxes = {}
        self.all_iou = {}

    def update(self, frame_index, features, boxes):
        # if the coming frame in the new frame
        if frame_index not in self.all_frame_index:
            # if the recorder have reached the max_record_frame.
            if len(self.all_frame_index) == self.max_record_frame:
                del_frame = self.all_frame_index[0]
                del self.all_regions[del_frame]
                del self.all_boxes[del_frame]
                del self.all_iou[del_frame]
                self.all_frame_index = self.all_frame_index[1:]

            # add new item for all_frame_index, all_regions and all_boxes. Besides, also add new similarity
            self.all_frame_index = np.append(self.all_frame_index, frame_index)
            self.all_regions[frame_index] = features
            self.all_boxes[frame_index] = boxes

            self.all_iou[frame_index] = {}
            for pre_index in self.all_frame_index[:-1]:
                iou = InferenceUtil.get_iou(self.all_boxes[pre_index], boxes)
                self.all_iou[frame_index][pre_index] = iou

    def get_region(self, frame_index, detection_index):
        '''
        get the feature by the specified frame index and detection index
        :param frame_index: start from 0
        :param detection_index: start from 0
        :return: the corresponding feature at frame index and detection index
        '''
        if frame_index in self.all_frame_index:
            regions = self.all_regions[frame_index]
            if detection_index is None:
                return regions
            if len(regions) == 0:
                return None
            if detection_index < len(regions):
                return regions[detection_index]
        return None

    def get_box(self, frame_index, detection_index):
        if frame_index in self.all_frame_index:
            boxes = self.all_boxes[frame_index]
            if len(boxes) == 0:
                return None
            if detection_index < len(boxes):
                return boxes[detection_index]
        return None

    def get_regions(self, frame_index):
        if frame_index in self.all_frame_index:
            regions = self.all_regions[frame_index]
        else:
            return None
        if len(regions) == 0:
            return None
        return regions

    def get_boxes(self, frame_index):
        if frame_index in self.all_frame_index:
            boxes = self.all_boxes[frame_index]
        else:
            return None
        if len(boxes) == 0:
            return None

        return boxes
