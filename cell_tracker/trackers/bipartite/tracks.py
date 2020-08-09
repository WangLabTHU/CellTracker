# -*- coding: UTF-8 -*-

from __future__ import absolute_import

import torch
import numpy as np
from ..components import chi2inv95
from ..utils import area_ratio
from ..utils import distance_ratio
from ..utils import overlap_ratio
from ..utils import MergeUtils
from ..utils import TrackerHyperParams


class Region():
    def __init__(self, bbox, mask):
        self._bbox = bbox
        self._mask = mask

    @property
    def bbox(self):
        return self._bbox

    @property
    def mask(self):
        return self._mask


class Node:
    """
    The Node is the basic element of a track. it contains the following information:
    1) frame index (frame index)
    2) box (a box (l, t, r, b)
    3) id, detection id for recorder indexing
    """

    def __init__(self, frame_index, id, region):
        self.frame_index = frame_index
        self._id = id
        self.region = region
        self.bbox = region.bbox

    def get_box(self, frame_index, recoder):
        if frame_index - self.frame_index >= TrackerHyperParams.max_record_frame:
            return None
        return recoder.all_boxes[self.frame_index][self._id, :]

    def get_iou(self, frame_index, recoder, box_id):
        return recoder.all_iou[frame_index][self.frame_index][box_id, self._id]


class Track:
    """
    Track is the class of track. it contains all the node and manages the node. it contains the following information:
    1) all the nodes
    2) track id. it is unique it identify each track
    3) track pool id. it is a number to give a new id to a new track
    4) age. age indicates how old is the track
    5) max_age. indicates the dead age of this track
    """
    _id_pool = 1

    def __init__(self, init_node, kf):
        self._nodes = list()
        self._nodes.append(init_node)

        self._age = 1
        self._missed_frame = 0
        # self._missed_detection_score = np.array(1e5)
        self._missed_detection_score = np.array(-1e5)

        self.parent = 0
        self.child = None

        self._id = Track._id_pool
        Track._id_pool += 1

        # kalman mean and covariance
        self._mean, self._covariance = kf.initiate(measurement=init_node.bbox)
        self.predicted_bbox = None

        self._valid = True  # indicate this track is merged
        self.color = tuple((np.random.rand(3) * 255).astype(int).tolist())

    def __del__(self):
        for n in self._nodes:
            del n

    @property
    def track_id(self):
        return self._id

    @track_id.setter
    def track_id(self, track_id):
        if track_id is not None:
            self._id = track_id
        else:
            raise ValueError('track id is None')

    @property
    def nodes(self):
        return self._nodes

    @nodes.setter
    def nodes(self, nodes):
        if isinstance(nodes, list):
            self._nodes = nodes
        else:
            raise ValueError('nodes should be a list')

    # TODO using kalman prediction or smooth
    def smooth_trajectory(self, max_missed_frame):
        nodes = []
        for index in range(len(self._nodes)-1):
            node_pre, node_post = self._nodes[index:index+2]
            frame_index_pre, frame_index_post = node_pre.frame_index, node_post.frame_index
            if frame_index_post == frame_index_pre + 1:
                nodes.append(node_pre)
                continue
            if frame_index_post - frame_index_pre >= max_missed_frame:
                nodes.append(node_pre)
                continue
            else:
                nodes.append(node_pre)
                num = frame_index_post - frame_index_pre + 1
                c_x_ref = (node_pre.bbox[0] + node_pre.bbox[2]) / 2.
                c_y_ref = (node_pre.bbox[1] + node_pre.bbox[3]) / 2.
                l = np.linspace(node_pre.bbox[0],
                                node_post.bbox[0], num=num)[1:-1]
                t = np.linspace(node_pre.bbox[1],
                                node_post.bbox[1], num=num)[1:-1]
                r = np.linspace(node_pre.bbox[2],
                                node_post.bbox[2], num=num)[1:-1]
                b = np.linspace(node_pre.bbox[3],
                                node_post.bbox[3], num=num)[1:-1]
                delta_c_x = (l + r) / 2. - c_x_ref
                delta_c_y = (t + b) / 2. - c_y_ref
                mask_ref = node_pre.region.mask
                height, width = mask_ref.shape
                coor_y_ref = np.where(mask_ref > 0)[0]
                coor_x_ref = np.where(mask_ref > 0)[1]
                for idx, (ll, tt, rr, bb, d_x, d_y) in enumerate(zip(l, t, r, b, delta_c_x, delta_c_y)):
                    coor_x = np.minimum(np.maximum(
                        0, (coor_x_ref + d_x).astype(np.int64)), width-1)
                    coor_y = np.minimum(np.maximum(
                        0, (coor_y_ref + d_y).astype(np.int64)), height-1)
                    mask = np.zeros_like(mask_ref)
                    mask[coor_y, coor_x] = 1
                    region = Region(np.array([ll, tt, rr, bb, 1.]), mask)
                    nodes.append(
                        Node(frame_index_pre + idx + 1, -1, region=region))
        nodes.append(self._nodes[-1])
        self._nodes = nodes

    def update_track(self, frame_index=None, det_id=None, region=None,
                     kalman_filter=None, visual_mode=False):
        if visual_mode:
            node = Node(frame_index, det_id, region=region)
            self._nodes.append(node)
            return True
        if region is not None:
            self._add_new_node(frame_index, det_id, region, kalman_filter)
            return True
        else:
            self._missed_frame += 1
            bbox = None
            self._update_kalman(bbox, kalman_filter)

    def _add_new_node(self, frame_index, det_id, region, kalman_filter):
        node = Node(frame_index, det_id, region=region)
        bbox = region.bbox
        self._age += 1
        self._missed_frame = 0
        self._nodes.append(node)
        self._update_kalman(bbox, kalman_filter)

    def _update_kalman(self, bbox, kalman_filter):
        if bbox is not None:
            if len(self._nodes) < 1:
                self._mean, self._covariance = kalman_filter.initiate(bbox)
            else:
                self._mean, self._covariance = kalman_filter.update(
                    self._mean, self._covariance, bbox)
            self._mean, self._covariance = kalman_filter.predict(
                self._mean, self._covariance)
            self.predicted_bbox = kalman_filter.predict_bbox(self._mean)
        else:
            self._mean, self._covariance = kalman_filter.predict(
                self._mean, self._covariance)
            self.predicted_bbox = kalman_filter.predict_bbox(self._mean)

    # fast
    def get_distance(self, frame_index, detections, regions,
                     kf=None, dis_th=1e6, using_kfgating=True):
        pick = []
        dis = np.zeros(len(detections)) + self._missed_detection_score
        ious = np.zeros(len(detections))
        for idx in range(len(detections)):
            bbox = detections[idx, :]
            if self._gate(frame_index, bbox, kf=kf, using_kfgating=using_kfgating):
                pick.append(idx)
        if len(pick) > 0:
            regs = [regions[idx] for idx in pick]
            seg_ious = self._get_seg_ious(regs)
            dets = detections[pick, :]
            distances = self._get_distance(dets, kf)
            for idx, val in enumerate(pick):
                dis[val] = distances[idx]
                ious[val] = seg_ious[idx]
            dis[dis > dis_th] = self._missed_detection_score
            ious[dis > dis_th] = self._missed_detection_score
        return dis, ious

    def _get_seg_ious(self, regs):
        ref_mask = self._nodes[-1].region.mask
        ref_mask_size = np.sum(ref_mask > 0)
        seg_ious = []
        for reg in regs:
            inter = ref_mask * reg.mask
            seg_iou = np.sum(inter > 0) / \
                (ref_mask_size + np.sum(reg.mask > 0))
            seg_ious.append(seg_iou)
        return np.array(seg_ious)

    def _get_distance(self, detections, kf):
        mean, covariance = kf.predict(self._mean, self._covariance)
        distances = kf.gating_distance(
            mean, covariance, detections, only_position=False)
        return distances

    def _gate(self, frame_index, bbox, history=1, kf=None, using_kfgating=True):
        if len(self._nodes) > 0:
            if not using_kfgating:  # only for dpm
                kf_gate = False
            else:
                kf_gate = kf.gating_distance(self._mean, self._covariance,
                                             bbox, only_position=False) > chi2inv95[4]
            node = self._nodes[-history:]
            history_bbox = np.array([n.bbox for n in node])
            history_delta_frame = [frame_index - n.frame_index for n in node]
            history_iou = overlap_ratio(history_bbox, bbox)
            history_area = area_ratio(history_bbox, bbox)
            history_dis = distance_ratio(history_bbox, bbox)
            index = np.argmax(history_iou)
            delta_frame = history_delta_frame[index]
            iou = float(history_iou[index])
            area_rto = float(history_area[index])
            dis_rto = float(history_dis[index])
            if delta_frame < TrackerHyperParams.max_frame_gap:
                # if iou < pow(TrackerHyperParams.iou_base, delta_frame) or area_rto > 2. or dis_rto > 1.0 or kf_gate:
                if iou < pow(TrackerHyperParams.iou_base, delta_frame):
                    return False
            else:
                return False
        return True

    def verify(self, frame_index, recorder, box_id):
        for n in self._nodes:
            delta_f = frame_index - n.frame_index
            if delta_f < TrackerHyperParams.max_frame_gap:
                iou = n.get_iou(frame_index, recorder, box_id)
                if iou is None:
                    continue
                if iou < pow(TrackerHyperParams.iou_base, delta_f):
                    return False
        return True

    @property
    def missed_frame(self):
        return self._missed_frame

    @missed_frame.setter
    def missed_frame(self, missed_frame):
        self._missed_frame = missed_frame


class Tracks:
    """
    Track set. It contains all the tracks and manage the tracks. it has the following information
    1) tracks. the set of tracks
    2) keep the previous tracks
    """

    def __init__(self, max_draw_track_node=20):
        self.tracks = list()  # the set of tracks
        self.saved_tracks = list()
        self.max_drawing_track = max_draw_track_node

    def __getitem__(self, item):
        return self.tracks[item]

    def add_new_track(self, frame_index, det_id, regions, kalman_filter, track_id=None, parent=None):
        node = Node(frame_index, det_id, region=regions)
        t = Track(init_node=node, kf=kalman_filter)
        if track_id is not None:
            t.track_id = track_id
        if parent is not None:
            t.parent = parent
        self.tracks.append(t)
        self.volatile_tracks()
        return t.track_id

    def get_track_by_id(self, id):
        for t in self.tracks:
            if t.track_id == id:
                return t
        return None

    def get_all_tracks(self, minimal_len=1):
        self.tracks = [t for t in self.tracks if len(t.nodes) >= minimal_len]
        self.saved_tracks = [
            t for t in self.saved_tracks if len(t.nodes) >= minimal_len]
        for t in self.tracks:
            t.smooth_trajectory(
                max_missed_frame=TrackerHyperParams.max_missed_frame)
        for t in self.saved_tracks:
            t.smooth_trajectory(
                max_missed_frame=TrackerHyperParams.max_missed_frame)
        tracks = self.tracks + self.saved_tracks
        # tracks = MergeUtils.merge(tracks,min_merge_threshold=TrackerHyperParams.min_merge_threshold)
        return tracks

    def volatile_tracks(self):  # delete the most oldest tracks acclerate
        if len(self.tracks) > TrackerHyperParams.max_object:
            all_missed_frames = [t.missed_frame for t in self.tracks]
            oldest_track_index = np.argmax(all_missed_frames)
            self.saved_tracks = self.saved_tracks + \
                [self.tracks[oldest_track_index]]
            del self.tracks[oldest_track_index]

    def one_frame_pass(self, saved_ids=[]):
        keep_track_set = list()
        saved_track_set = list()
        for i, t in enumerate(self.tracks):
            if t.track_id in saved_ids:
                saved_track_set.append(i)
                continue
            if t.missed_frame > TrackerHyperParams.max_missed_frame:
                saved_track_set.append(i)
                continue
            keep_track_set.append(i)
        self.saved_tracks = self.saved_tracks + \
            [self.tracks[i] for i in saved_track_set]
        self.tracks = [self.tracks[i] for i in keep_track_set]
