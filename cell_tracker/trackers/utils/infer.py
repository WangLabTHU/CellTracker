
# -*- coding: UTF-8 -*-

import cv2
import numpy as np
import copy
from collections import Counter
from .bbox import overlap_ratio

class InferenceUtil:

    @staticmethod
    def get_iou(pre_boxes, next_boxes):

        h = len(next_boxes)
        w = len(pre_boxes)
        if h == 0 or w == 0:
            return []
        iou = np.zeros((h, w), dtype=float)
        for i in range(h):
            rect1 = np.expand_dims(next_boxes[i, :], 0)
            rect1 = np.repeat(rect1, pre_boxes.shape[0], axis=0)
            iou[i,:] = overlap_ratio(rect1, pre_boxes)
        return iou


class MergeUtils:

    @staticmethod
    def merge(tracks, min_merge_threshold=0.5):
        tracks_num = len(tracks)
        res = np.zeros((tracks_num, tracks_num), dtype=float)
        # get track similarity matrix
        for i in range(tracks_num):
            t1 = tracks[i]
            for j in range(i+1, tracks_num):
                t2 = tracks[j]
                s = MergeUtils.get_merge_similarity(copy.deepcopy(t1), copy.deepcopy(t2))
                if s is not None:
                    res[i, j] = s
                    res[j, i] = s

        # get the track pair which needs merged
        used_indexes = []
        merge_pair = []
        for i in range(tracks_num):
            if i in used_indexes:
                continue
            max_track_index = np.argmax(res[i, :])
            if i != max_track_index and res[i, max_track_index] > min_merge_threshold:
                used_indexes += [max_track_index]
                merge_pair += [(i, max_track_index)]

        # start merge
        merge_pair = sorted(merge_pair, key=lambda x: x[1], reverse=True)
        for i, j in merge_pair:

            tracks[i] = MergeUtils.merge_pair(copy.deepcopy(tracks[i]),
                                              copy.deepcopy(tracks[j]))
        for _, j in merge_pair:
            del tracks[j]

        # remove dupicate
        all_id = [t.track_id for t in tracks]
        id_count = dict()
        for idx, t_id in enumerate(all_id):
            if t_id not in id_count.keys():
                id_count[t_id] = [idx]
            else:
                id_count[t_id].append(idx)
        merge_pair = []
        for v in id_count.values():
            assert len(v) <= 2
            if len(v) == 2:
                merge_pair.append(tuple(v))
        merge_pair = sorted(merge_pair, key=lambda x: x[1], reverse=True)
        for i, j in merge_pair:

            tracks[i] = MergeUtils.merge_pair(copy.deepcopy(tracks[i]),
                                              copy.deepcopy(tracks[j]))
        for _, j in merge_pair:
            del tracks[j]
        

        return tracks

    @staticmethod
    def get_merge_similarity(t1, t2):
        '''
        Get the similarity between two tracks
        :param t1: track 1
        :param t2: track 2
        :return: the similairty (float value).
        '''

        if len(t1.nodes) < len(t2.nodes):
            t1, t2 = t2, t1

        t1_d, t2_d = dict(), dict()
        for n in t1.nodes:
            t1_d[n.frame_index] = n.bbox
        for n in t2.nodes:
            t2_d[n.frame_index] = n.bbox

        t1_b, t2_b = [], []
        for k in t1_d.keys():
            if k in t2_d.keys():
                t1_b.append(t1_d[k])
                t2_b.append(t2_d[k])
        if len(t1_b) > 0:
            iou = overlap_ratio(np.array(t1_b), np.array(t2_b))
            return np.mean(iou)
        else:
            return 0.0

    @staticmethod
    def merge_pair(t1, t2):
        '''
        merge t2 to t1, after that delete t2
        :param t1: track 1
        :param t2: track 2
        :return: None
        '''
        if len(t1.nodes) < len(t2.nodes):
            t1, t2 = t2, t1

        all_f1 = [n.frame_index for n in t1.nodes]
        all_f2 = [n.frame_index for n in t2.nodes]

        for i, f2 in enumerate(all_f2):
            if f2 not in all_f1:
                insert_pos = 0
                for j, f1 in enumerate(all_f1):
                    if f2 < f1:
                        break
                    insert_pos += 1
                t1.nodes.insert(insert_pos, t2.nodes[i])
        t1.missed_frame = min(t1.missed_frame, t2.missed_frame)
        return t1






