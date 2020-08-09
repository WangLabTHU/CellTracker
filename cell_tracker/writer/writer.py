# -*- coding: UTF-8 -*-

from __future__ import absolute_import

from collections import OrderedDict
import os
import os.path as osp
from pathlib import Path
import numpy as np
import pandas as pd
import cv2
from jinja2 import Environment, FileSystemLoader

from ..utils import format_out
from .utils import mkdir
from .visualize import Visualization, plot_double_line
from cell_tracker import PACKAGEPATH


class Writer(Visualization):
    def __init__(self, write_folder, add_color=True, add_box=True, add_edge=True,
                 add_trajectory=True, add_label=True, trajectory_length=None, video_fps=1):
        super(Writer, self).__init__(write_folder, add_color, add_box, add_edge, add_trajectory,
                                     add_label, trajectory_length, video_fps)
        self._write_folder = write_folder
        mkdir(osp.join(self._write_folder, 'statis'))

    def __call__(self, frames, output_csv=True, output_html=True, output_img=True):
        instance_info_label_id = self._generate_instance_info(frames)
        instance_info_label_id = self._generate_statis(
            instance_info_label_id, output_csv, output_html)
        if output_html:
            self._generate_html(instance_info_label_id)
        if output_img:
            self._visual(instance_info_label_id, frames)

    def _set_statis_img_path(self, label_id):
        return osp.join(self._write_folder, 'statis', "instance_{:0>4d}.png".format(label_id))

    def _set_csv_path(self):
        return osp.join(self._write_folder, "instance_information.csv")

    def _get_statis_img_path(self, label_id):
        return osp.join('./statis', "instance_{:0>4d}.png".format(label_id))

    def _set_proj_infos(self, frames):
        self.frame_num = len(frames)
        self.img_size = frames[0].raw_img.shape

    def _generate_instance_info(self, frames):
        self._set_proj_infos(frames)
        instance_info_label_id = OrderedDict()
        for frame_index, frame in frames.items():
            instances = frame.instances

            for label_id, ins in instances.items():
                assert label_id == ins.label_id
                if label_id in instance_info_label_id.keys():
                    instance_info_label_id[label_id]['end_frame'] = frame_index
                    instance_info_label_id[label_id]['instances'][frame_index] = ins
                else:
                    ins_info = {'instance_id': label_id,
                                'start_frame': frame_index,
                                'end_frame': frame_index,
                                'statis_img_path': self._get_statis_img_path(label_id),
                                'instances': {frame_index: ins}
                                }
                    instance_info_label_id[label_id] = ins_info

        return instance_info_label_id

    def _generate_statis(self, instance_info_label_id, output_csv, output_html):
        col_names = ['frame_%s' % f_idx for f_idx in range(self.frame_num)]
        row_names = []
        results = []
        for label_id in list(instance_info_label_id.keys()):
            ins_info = instance_info_label_id[label_id]
            row_names.extend(['instance_%s_area' %
                              label_id, 'instance_%s_intensity' % label_id])
            instances_map = ins_info['instances']
            instensities = []
            areas = []
            filter_areas = []
            filter_intensities = []
            filter_frame_index = []
            for frame_index in range(self.frame_num):
                try:
                    ins = instances_map[frame_index]
                    instensities.append(ins.intensity)
                    areas.append(ins.area)
                    filter_frame_index.append(frame_index)
                    filter_intensities.append(ins.intensity)
                    filter_areas.append(ins.area)
                except KeyError:
                    instensities.append(None)
                    areas.append(None)
            # output result with null value
            results.append(instensities)
            results.append(areas)

            # output plot with filte none value
            mean_intensity = [area * instensity for area,
                              instensity in zip(filter_areas, filter_intensities)]
            mean_intensity = float(np.sum(mean_intensity)) / \
                float(np.sum(filter_areas))
            mean_area = np.mean(filter_areas)
            instance_info_label_id[label_id]['mean_area'] = mean_area
            instance_info_label_id[label_id]['mean_intensity'] = mean_intensity

            # plot
            if output_html:
                save_name = self._set_statis_img_path(label_id)
                plot_double_line(filter_frame_index, filter_areas,
                                 filter_intensities, label_id, save_name)
            # save as cvs file
            if output_csv:
                results_pd = pd.DataFrame(
                    results, index=row_names, columns=col_names, dtype=np.float)
                results_pd.to_csv(self._set_csv_path(), float_format='%.4f')

        return instance_info_label_id

    def _generate_html(self, instance_info_label_id):
        env = Environment(loader=FileSystemLoader('./'))
        # template_file_path = str(Path(osp.join(PACKAGEPATH, 'writer/templates/results.html')).relative_to(os.getcwd()))
        template_file_path = './cell_tracker/writer/templates/results.html'
        template = env.get_template(template_file_path)
        img_size = '%s * %s ' % (self.img_size[0], self.img_size[1])
        infos = [info for info in instance_info_label_id.values()]
        with open(osp.join(self._write_folder, "results.html"), 'w+') as html_file:
            html_content = template.render(
                frame_num=self.frame_num, img_size=img_size, infos=infos)
            html_file.write(html_content)
