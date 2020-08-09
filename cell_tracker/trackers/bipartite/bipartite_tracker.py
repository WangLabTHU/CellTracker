# -*- coding: UTF-8 -*-

from __future__ import absolute_import
import torch
import numpy as np
from scipy.optimize import linear_sum_assignment
from .tracks import Track
from .tracks import Tracks
from .tracks import Region
from ..components import Recorder
from ..components.kalman_filter import KalmanFilter
from ..utils import BboxTransfer
from ..utils import non_max_suppression
from ..utils import TrackerHyperParams


class BiTracker:
    def __init__(self):

        self.minimal_tracklet_len = TrackerHyperParams.minimal_tracklet_len
        self.roi_verify_max_iteration = TrackerHyperParams.roi_verify_max_iteration
        self.roi_verify_punish_rate = TrackerHyperParams.roi_verify_punish_rate
        self.using_kfgating = TrackerHyperParams.using_kfgating
        self.mitosis_th = TrackerHyperParams.mitosis_th
        self.dis_th = TrackerHyperParams.dis_th
        self.area_th = TrackerHyperParams.area_th
        self.edge_pixel = TrackerHyperParams.edge_pixel
        
        self.kalman_filter = KalmanFilter()
        self.tracks = Tracks()
        self.recorder = Recorder()

        self.frame_index = 0
        self.predict_detections = []

        self.img_sz = None

    def get_all_tracks(self):
        return self.tracks.get_all_tracks(minimal_len=self.minimal_tracklet_len)

    def _assinment_mitosis(self, seg_ious, assigned_pairs_id, unassigned_tracks_id, 
                            unassigned_detections_id, ids, detections_id=None, mitosis_th=0.15):
        track_num = seg_ious.shape[0]
        if track_num > 0:
            box_num = seg_ious.shape[1]
        else:
            box_num = 0
        if detections_id is None:
            detections_id = list(range(box_num))
        
        continue_pairs_id, mitosis_pair_id, children_det_id = [], [], []
        assigned_pairs_id_continue = []
        for (track_id, det_id) in assigned_pairs_id:
            t_index = ids.index(track_id)
            iou = seg_ious[t_index, :]
            topk_index = (-iou).argsort()[:2]
            candidate_id = [detections_id[topk_index[0]], detections_id[topk_index[1]]]
            if iou[topk_index[1]] >= mitosis_th:
                if candidate_id[0] not in children_det_id and \
                    candidate_id[1] not in children_det_id:
                    children_det_id.extend(candidate_id)
                    mitosis_pair_id.append((track_id, candidate_id[0], candidate_id[1]))
                else:
                    assigned_pairs_id_continue.append((track_id, det_id))
            else:
                assigned_pairs_id_continue.append((track_id, det_id))
            
        for (track_id, det_id) in assigned_pairs_id_continue:
            if det_id not in children_det_id:
                continue_pairs_id.append((track_id, det_id))
        
        assigned_det_id = [pairs[1] for pairs in continue_pairs_id] + \
            [pairs[1] for pairs in mitosis_pair_id] + \
                [pairs[2] for pairs in mitosis_pair_id]
        unassigned_detections_id = sorted(list(set(detections_id) - set(assigned_det_id)))

        assigned_trk_id = [pairs[0] for pairs in continue_pairs_id] + \
            [pairs[0] for pairs in mitosis_pair_id]
        unassigned_tracks_id = sorted(list(set(ids) - set(assigned_trk_id)))

        return continue_pairs_id, mitosis_pair_id, unassigned_tracks_id, unassigned_detections_id
 

    def _assinment_heuristic(self, tracks, distance, ids, detections_id=None):
        # find the corresponding by the similar matrix
        track_num = distance.shape[0]
        if track_num > 0:
            box_num = distance.shape[1]
        else:
            box_num = 0
        if detections_id is None:
            detections_id = list(range(box_num))

        row_index, col_index = linear_sum_assignment(distance)

        # verification by iou
        verify_iteration = 0
        while verify_iteration < self.roi_verify_max_iteration:
            is_change = False
            for idx, track_idx in enumerate(row_index):
                track_id = ids[track_idx]
                det_idx = col_index[idx]
                det_id = detections_id[det_idx]
                t = tracks.get_track_by_id(track_id)
                # TODO verify in MHT
                if not t.verify(self.frame_index, self.recorder, det_id):
                    distance[track_idx, det_idx] /= self.roi_verify_punish_rate
                    is_change = True
            if is_change:
                row_index, col_index = linear_sum_assignment(distance)
            else:
                break
            verify_iteration += 1

        assigned_pairs_id = []
        for idx, track_idx in enumerate(row_index):
            track_id = ids[track_idx]
            det_idx = col_index[idx]
            det_id = detections_id[det_idx]
            if distance[track_idx, det_idx] < 0:
                assigned_pairs_id.append((track_id, det_id))

        unassigned_tracks_id = sorted(list(set(ids) - set([pairs[0] for pairs in assigned_pairs_id])))
        unassigned_detections_id = sorted(list(set(detections_id) - set([pairs[1] for pairs in assigned_pairs_id])))
        return assigned_pairs_id, unassigned_tracks_id, unassigned_detections_id

    def update_detections(self, detections, mask, area_th=20, edge_pixel=10):
        def bbox_area(bbox):
            return (bbox[2] - bbox[0]) * (bbox[3] - bbox[1])
        def edge_filter(bbox, height, width, edge_pixel):
            if width - bbox[0] <= edge_pixel or bbox[2] <= edge_pixel or height - bbox[1] <= edge_pixel or bbox[3] <= edge_pixel:
                return False
            else:
                return True
        regions = []
        detections_filter = []
        height, width = mask[0].shape
        for idx in range(detections.shape[0]):
            bbox = detections[idx, 0:4]
            if bbox_area(bbox) > pow(area_th, 2) and edge_filter(bbox, height, width, edge_pixel):
                regions.append(Region(detections[idx, :], mask[idx]))
                detections_filter.append(detections[idx, :])
        return regions, np.array(detections_filter)


    def update_track(self, frame_index, img_size, detections, mask):
        """
        :param frame_index: frame number of video
        :param img_size: image size of original image for this frame
        :param detections: all detections results for one frame
        :return:
        """
        self.frame_index = frame_index
        self.img_sz = img_size  # [height, width]


        regions, detections = self.update_detections(detections, mask, area_th=self.area_th, edge_pixel=self.edge_pixel)
        if len(detections) == 0:
            return True

        self.recorder.update(self.frame_index, regions, detections)

        # Create new branch from the every detection results
        if self.frame_index == 0 or len(self.tracks.tracks) == 0:
            for index in range(detections.shape[0]):
                _ = self.tracks.add_new_track(frame_index=self.frame_index,
                                            det_id=index,
                                            regions=regions[index],
                                            kalman_filter=self.kalman_filter)
            self.tracks.one_frame_pass()
            return True
        else:
            distance = []
            seg_ious = []
            ids = []
            for track in self.tracks.tracks:
                ids.append(track.track_id)
                regions = self.recorder.get_region(self.frame_index, None)
                dis, ious = track.get_distance(self.frame_index, detections, regions,
                                                kf=self.kalman_filter, dis_th=self.dis_th,
                                                using_kfgating=self.using_kfgating)
                distance.append(dis)
                seg_ious.append(ious)
            distance = np.array(distance).squeeze().reshape(-1, len(detections))
            seg_ious = np.array(seg_ious).squeeze().reshape(-1, len(detections))

            if len(distance) > 0:
                assigned_pairs_id, unassigned_tracks_id, unassigned_detections_id = \
                  self._assinment_heuristic(self.tracks, -seg_ious, ids)

                continue_pairs_id, mitosis_pair_id, unassigned_tracks_id, unassigned_detections_id = \
                    self._assinment_mitosis(seg_ious, assigned_pairs_id, unassigned_tracks_id, 
                            unassigned_detections_id, ids, detections_id=None, mitosis_th=self.mitosis_th)

                # update the tracks for no mitosis
                for track_id, det_id in continue_pairs_id:
                    track = self.tracks.get_track_by_id(track_id)
                    track.update_track(frame_index=self.frame_index,
                                       det_id=det_id,
                                       region=self.recorder.get_region(self.frame_index, det_id),
                                       kalman_filter=self.kalman_filter,
                                       visual_mode=False)

                parent_track = []
                for track_id, det_id_1, det_id_2 in mitosis_pair_id:
                    track = self.tracks.get_track_by_id(track_id)
                    parent_track.append(track_id)
                    child_track = []
                    for det_id in [det_id_1, det_id_2]:
                        t_id = self.tracks.add_new_track(frame_index=self.frame_index,
                                                    det_id=det_id,
                                                    regions=self.recorder.get_region(self.frame_index, det_id),
                                                    kalman_filter=self.kalman_filter,
                                                    parent=track_id)
                        child_track.append(t_id)

                for track_id in unassigned_tracks_id:
                    track = self.tracks.get_track_by_id(track_id)
                    track.update_track(frame_index=self.frame_index,
                                       det_id=None, 
                                       region=None,
                                       kalman_filter=self.kalman_filter,
                                       visual_mode=False)

                # add new track
                for det_id in unassigned_detections_id:
                    _ = self.tracks.add_new_track(frame_index=self.frame_index,
                                                  det_id=det_id,
                                                  regions=self.recorder.get_region(self.frame_index, det_id),
                                                  kalman_filter=self.kalman_filter)

            # remove the old track
            self.tracks.one_frame_pass(saved_ids=parent_track)

        return True

