
# -*- coding: UTF-8 -*-

from __future__ import absolute_import


class TrackerHyperParams:
    max_record_frame = 5000
    iou_base = 0.1
    max_track_node = 3000
    max_object = 8000
    using_kfgating = False
    mitosis_th = 0.15
    dis_th = 1000.0
    area_th = 1
    edge_pixel = 0
    min_merge_threshold = 0.6
    minimal_tracklet_len = 2
    roi_verify_max_iteration = 2
    roi_verify_punish_rate = 0.6
    max_frame_gap = 5  # association
    max_missed_frame = 5  # inter and filter
