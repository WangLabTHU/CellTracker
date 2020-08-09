# -*- coding: UTF-8 -*-

from __future__ import absolute_import
from .utils import mkdir
import matplotlib.pyplot as plt

import os.path as osp
import cv2
import numpy as np
import matplotlib
matplotlib.use("Agg")


class PlotFormat():
    fonttype = 'Times New Roman'
    markersize = 8
    linewidth = 3
    label_size = 10


def plot_double_line(frame_index, areas, intensity, instance_id, save_name):
    fig = plt.figure()
    ax1 = fig.add_subplot(111)
    line_intensity = ax1.plot(frame_index, intensity, 'b--o',
                              lw=PlotFormat.linewidth,
                              markersize=PlotFormat.markersize,
                              label='Intensity')
    ax1.set_xlabel('Frame Index', fontdict={
                   'family': PlotFormat.fonttype, 'size': PlotFormat.label_size})
    ax1.set_ylabel('Mean Intensity (A.U)', fontdict={
                   'family': PlotFormat.fonttype, 'size': PlotFormat.label_size})
    ax1.set_title("Instance ID {:0>4d}".format(instance_id))

    ax2 = ax1.twinx()
    line_area = ax2.plot(frame_index, areas, 'r--o',
                         lw=PlotFormat.linewidth,
                         markersize=PlotFormat.markersize,
                         label='Area')
    ax2.set_xlim([0, max(frame_index)])
    step = max(max(frame_index) // 10, 1)
    x_tick = list(range(0, max(frame_index)+step, step))
    ax2.set_xticks(x_tick)
    ax2.set_xticklabels(x_tick, fontdict={
                        'family': PlotFormat.fonttype, 'size': PlotFormat.label_size})
    ax2.set_ylabel('Area (Pixel)', fontdict={
                   'family': PlotFormat.fonttype, 'size': PlotFormat.label_size})

    lines = line_intensity + line_area
    labels = [l.get_label() for l in lines]
    ax1.legend(lines, labels, loc=0, fontsize=PlotFormat.label_size)
    fig.tight_layout()
    plt.savefig(save_name)
    plt.close()


class Visualization(object):
    def __init__(self, write_folder, add_color, add_box, add_edge, add_trajectory, add_label, trajectory_length, video_fps):
        self._write_folder = write_folder
        self.add_color = add_color
        self.add_box = add_box
        self.add_edge = add_edge
        self.add_trajectory = add_trajectory
        self.add_label = add_label
        self.video_fps = video_fps
        self.trajectory_length = trajectory_length

        self._visual_transformer = []
        if self.add_color:
            self._visual_transformer.append(self._add_color)
        if self.add_box:
            self._visual_transformer.append(self._add_bbox)
        if self.add_edge:
            self._visual_transformer.append(self._add_edge)
        if self.add_label:
            self._visual_transformer.append(self._add_label)
        if self.add_trajectory:
            self._visual_transformer.append(self._add_trajectory)

        self.video_hander = None

    def _add_frame_index(self, visual_img, frame_index, **kwargs):
        height, width = visual_img.shape[0:2]
        txt = 'Frame: {}'.format(frame_index)
        txt_coor_x, txt_coor_y = min(width, 30), min(height, 30)
        visual_img = cv2.putText(visual_img, txt, (txt_coor_x, txt_coor_y),
                                 cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        return visual_img

    def _add_label(self, visual_img, bbox, label_id, **kwargs):
        txt = '{}'.format(int(label_id))
        visual_img = cv2.putText(visual_img, txt,
                                 (int(0.5*(bbox[0] + bbox[2])),
                                  int(0.5*(bbox[1] + bbox[3]))),
                                 cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
        return visual_img

    def _add_bbox(self, visual_img, bbox, color, **kwargs):
        visual_img = cv2.rectangle(visual_img, (int(bbox[0]), int(
            (bbox[1]))), (int(bbox[2]), int(bbox[3])), tuple(color), 2)
        return visual_img

    def _add_edge(self, visual_img, edge, **kwargs):
        visual_img[edge[:, 1], edge[:, 0], :] = np.array([255, 255, 0])
        return visual_img

    def _add_color(self, visual_img, coords, color, **kwargs):
        visual_img = visual_img.astype(np.float32)
        visual_img[coords[0], coords[1], :] = 0.5 * \
            visual_img[coords[0], coords[1], :] + 0.5 * np.array(color)
        visual_img = visual_img.astype(np.uint8)
        return visual_img

    def _add_trajectory(self, visual_img, label_id, instance_info_label_id, frame_id, **kwargs):
        ins_tracklet = instance_info_label_id[label_id]['instances']
        instances = [ins_tracklet[f_idx]
                     for f_idx in range(frame_id) if f_idx in ins_tracklet.keys()]
        if len(instances) > 0:
            start = 0
            if self.trajectory_length:
                if len(instances) > self.trajectory_length:
                    start = len(instances) - self.trajectory_length
            for ins1, ins2 in zip(instances[start:], instances[start + 1:]):
                color = tuple(list(ins1.color))
                c1 = tuple(ins1.centroid)
                c2 = tuple(ins2.centroid)
                visual_img = cv2.line(visual_img, c1, c2, color, 2)
        return visual_img

    def _add_attr_per_ins(self, ins, instance_info_label_id, visual_img):
        coords = ins.coords
        color = ins.color
        bbox = ins.bbox
        label_id = ins.label_id
        edge = ins.edge
        frame_id = ins.frame_id
        for func in self._visual_transformer:
            params = {'coords': coords,
                      'color': color,
                      'bbox': bbox,
                      'label_id': label_id,
                      'edge': edge,
                      'frame_id': frame_id,
                      'instance_info_label_id': instance_info_label_id
                      }
            visual_img = func(visual_img=visual_img, **params)
        return visual_img

    def _add_attr_per_frame(self, instance_info_label_id, frame, frame_index):
        raw_img = frame.raw_img
        visual_img = np.copy(raw_img)
        visual_img = self._add_frame_index(visual_img, frame_index)
        for _, ins in frame.instances.items():
            visual_img = self._add_attr_per_ins(
                ins, instance_info_label_id, visual_img)
        return visual_img

    def _to_mp4(self, visual_img, visual_folder):
        if not self.video_hander:
            video_file_name = osp.join(
                visual_folder, 'visualization_video.avi')
            height, width = visual_img.shape[0:2]
            self.video_hander = cv2.VideoWriter(video_file_name,
                                                cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'), self.video_fps, (width, height))
            self.video_hander.write(visual_img)
        else:
            self.video_hander.write(visual_img)

    def _visual(self, instance_info_label_id, frames):
        visual_folder = osp.join(self._write_folder, 'visual')
        mkdir(visual_folder)
        for frame_index, frame in frames.items():
            visual_img = self._add_attr_per_frame(
                instance_info_label_id, frame, frame_index)
            visual_img = cv2.cvtColor(visual_img, cv2.COLOR_RGB2BGR)
            visual_save_name = osp.join(
                visual_folder, osp.basename(frame.file_name))
            cv2.imwrite(visual_save_name, visual_img)
            self._to_mp4(visual_img, visual_folder)

