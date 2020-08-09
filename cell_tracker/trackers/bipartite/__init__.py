
# -*- coding: UTF-8 -*-

from __future__ import absolute_import

from .bipartite_tracker import BiTracker
import numpy as np


class Bipartite:

    def __init__(self):
        self.tracker = BiTracker()

    def _frame2instance(self, frame):
        instances = frame.instances
        label_img = frame.label_img
        img_size = label_img.shape[0:2]
        masks = []
        detections = []
        for _, ins in instances.items():
            mask = np.squeeze(np.zeros_like(label_img))
            mask[ins.coords[0], ins.coords[1]] = 1
            masks.append(mask)
            detections.append(ins.bbox)
        detections = np.array(detections)
        return detections, masks, img_size

    def _get_track_label(self, frames):
        img_sz = self.tracker.img_sz
        all_tracks = self.tracker.get_all_tracks()
        for frame_index, frame in frames.items():
            label_img = np.zeros(img_sz)
            for t in all_tracks:
                nodes = t.nodes
                track_id = t.track_id
                for n in nodes:
                    if n.frame_index == frame_index:
                        mask = n.region.mask
                        label_img[mask > 0] = track_id
            frame.label_img = np.expand_dims(label_img, 2)
        return frames

    def __call__(self, frames):
        """
        label_imgs: list: N * label_image
        """
        for frame_index, frame in frames.items():
            detections, masks, img_size = self._frame2instance(frame)
            _ = self.tracker.update_track(
                frame_index, img_size, detections, masks)
        return self._get_track_label(frames)
