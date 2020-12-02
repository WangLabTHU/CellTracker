# -*- coding: UTF-8 -*-

import collections
import os
import sys
import numpy as np
import cv2
import imageio
import threading
import time
import csv
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import QSize, Qt
from PyQt5 import QtCore, QtWidgets
from PyQt5 import QtGui
import pyqtgraph as pg
from .config import SYSTEM
from .components import CorrectionTools
from .components import ChangedInstances
from .components import CellAttributeWindow
from .components import FileTree
from .components import InstanceSettings
from .components import LeftNavigation
from .components import LeftTools
from .components import Menu
from .components import ProjectWindow
from .components import StatusBar
from .components import VisualizeWindow
from .components import QuestionMessageBox, InformationMessageBox, WarningMessageBox
from PyQt5.QtGui import QDesktopServices
from PyQt5.QtCore import QFileInfo, QUrl
from .components import AnnotationTools
from .utils import color_groups, annotation_colors
from .utils import load_images
from .utils import mkdir
from ..normalizers import get_normalizer
from ..segmenters import get_segmenter
from ..trackers import get_tracker
from ..writer import get_writer
from .utils import get_icon, slide_stylesheet, general_qss
from ..utils import logger
from cell_tracker import PACKAGEPATH
from cell_tracker.segmenters.unet import TrainParameters, TrainerWrapper


class MainWindow(QMainWindow):
    # MainWindow
    # contains:

    def __init__(self, parent=None):
        super().__init__()

        pg.setConfigOption('imageAxisOrder', 'row-major')
        default_output_folder = os.path.join(PACKAGEPATH, "../output")
        self.tutorial_path = os.path.join(
            PACKAGEPATH, "../doc/Cell-Tracker tutorial.pdf")
        mkdir(default_output_folder)
        mkdir(os.path.join(PACKAGEPATH, "../checkpoint"))
        self.open_path = os.path.join(PACKAGEPATH, "../output")
        self.project_path = os.path.join(PACKAGEPATH, "../output/untitled")
        mkdir(self.project_path)
        logger.info('The default output folder is setted to: %s' %
                    self.project_path)
        self.unet_model_path = None
        self.last_index = 0             # left navigation update
        self.frames_num = 0             # num of frames
        self.frames = collections.OrderedDict()
        self.show_flag = 1    # 1:raw raw 2.mask raw 3.color+raw raw 4.annotation: raw label_img
        self.segmenter_dict = {0: 'binary_thresholding', 1: 'otsu_thresholding',  2: 'unet',
                               3: 'water_shed', 4: 'grab_cut', 5: 'User-defined'}
        self.segmenter_name = 'binary_thresholding'
        self.segment_flag = 0    # which segmenter
        self.tracker_dict = {0: 'none', 1: 'bipartite_tracker'}
        self.tracker_name = 'bipartite_tracker'
        self.normalizer_dict = {0: 'equalize_hist', 1: 'CLAHE', 2: 'min_max',
                                3: 'retinex_MSRCP', 4: 'retinex_MSRCR', 5: 'reset'}
        self.normalizer_name = 'equalize_hist'
        self.previous_frame = 0
        self.previous_algorithm = 4
        self.brush_flag = 0  # 0:not using brush 1:using brush

        self.grabcut_pos_begin = None
        self.grabcut_pos_finish = None
        self.grabcut_roi = None
        self.grabcut_rect = None

        # annotation
        # -1 none 0 modify 1 modify and add instance 2 annotation and add instance
        self.annotation_flag = -1
        # self.frames_roi         = {}
        self.widget_list = []       # CurrentRow->label_id
        self.changed_instances = ChangedInstances()
        self.bboxroi = None
        # self.color_roi          = []
        self.drag_flag = 0    # 0 ignore 1 dragging
        self.background_color = [54, 54, 54]
        self.my_colors = color_groups

        # train
        self.source_img_root = ''
        self.label_img_root = ''
        self.log_root = ''
        self.validation_ratio = 0.2
        self.scale_img = 1
        self.scale_img_list = [4.0, 2.0, 1.0, 0.5, 0.25, 0.125]
        # 'edge_weighted'，'sample_balance' and 'None'
        self.weighted_type = 'edge_weighted'
        self.aug_list = ['Flip', 'Rotate', 'GaussianNoise', 'GaussianBlur']
        self.batch_size = 2
        self.workers = 2
        self.gpu_num = 0
        self.resume = None
        self.epochs = 4
        self.lr = 0.01
        self.weight_decay = 0.0005
        self.loss_type = 'DiceLoss'
        self.weighted_type_list = ['edge_weighted', 'sample_balance', None]
        self.loss_type_list = []

        self.result_dir_path = ""
        self.origin_dir_path = ""

        self.params_dict = {}

        self.sld_stylesheet = slide_stylesheet
        self.general_qss = general_qss
        self.setStyleSheet(self.general_qss)

        self.setup_ui()
        self.update_params()


    def setup_ui(self):

        # Initialize five parts of the main window
        main_widget = QWidget()
        main_layout = QHBoxLayout(main_widget)

        self.main_widget = main_widget

        self.init_menu()
        self.init_left_part()
        self.init_visualize_window()
        self.init_correction_tools()
        self.init_status_bar()

        main_layout.setSpacing(0)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(self.left_navigation)
        main_layout.addWidget(self.left_tools)
        main_layout.addWidget(self.visualize_window)
        main_layout.addWidget(self.correction_tools)
        main_layout.setStretch(0, 1)
        main_layout.setStretch(1, 3)
        main_layout.setStretch(2, 12)
        main_layout.setStretch(3, 4)

        self.setCentralWidget(main_widget)

        self.setGeometry(300, 300, 1500, 800)
        self.setWindowTitle("CellTracker")
        self.setWindowIcon(QIcon(get_icon("cell.png")))
        self.setStatusBar(self.status_bar)
        self.center()
        self.show()

    def init_menu(self):
        # Initialize menu bar
        self.menu = Menu()
        self.menu_bar = self.menu.menu_bar

        self.menu.new_project_act.triggered.connect(self.new_project_fnc)
        self.menu.default_project_act.triggered.connect(self.default_fnc)
        self.menu.load_act.triggered.connect(self.load_fnc)
        self.menu.source_folder_act.triggered.connect(
            self.set_source_button_fnc)
        self.menu.label_folder_act.triggered.connect(self.set_label_button_fnc)
        self.menu.log_folder_act.triggered.connect(self.set_log_button_fnc)
        self.menu.exit_act.triggered.connect(self.exit_fnc)

        self.menu.equalize_act.triggered.connect(
            lambda: self.normalize('equalize_hist'))
        self.menu.min_max_act.triggered.connect(
            lambda: self.normalize('min_max'))
        self.menu.r_p_act.triggered.connect(
            lambda: self.normalize('retinex_MSRCP'))
        self.menu.r_r_act.triggered.connect(
            lambda: self.normalize('retinex_MSRCR'))
        self.menu.remove_act.triggered.connect(lambda: self.normalize('reset'))

        self.menu.threshold_act.triggered.connect(
            lambda: self.segment('binary_thresholding',
                                 threshold=self.tools.segment.thresh_sld1.value(),
                                 minimal_size=int(self.tools.segment.thresh_min_size_editor.text())))

        self.menu.unet_act.triggered.connect(
            lambda: self.segment('unet',
                                 model_path=self.unet_model_path,
                                 scale_img=self.scale_img_list[self.tools.segment.scale_img_select.currentIndex(
                                 )],
                                 device=self.tools.segment.device_select.currentText().lower(),
                                 threshold=self.tools.segment.thresh_sld2.value()/10,
                                 minimal_size=int(self.tools.segment.thresh_min_size_editor.text())))

        self.menu.water_act.triggered.connect(
            lambda: self.segment('water_shed',
                                 noise_amplitude=self.tools.segment.noise_sld.value(),
                                 dist_thresh=self.tools.segment.dist_thresh_sld.value()/10,
                                 minimal_size=int(self.tools.segment.thresh_min_size_editor.text())))

        self.menu.grabcut_act.triggered.connect(
            lambda: self.segment('grab_cut',
                                 iteration=self.tools.segment.iteration_sld.value()))

        self.menu.track_act.triggered.connect(
            lambda: self.track(self.tracker_name))
        self.menu.output_act.triggered.connect(
            lambda: self.write(write_folder=self.project_path,
                               add_color=self.tools.output.visualization_color_checkbox.isChecked(),
                               add_box=self.tools.output.visualization_box_checkbox.isChecked(),
                               add_edge=self.tools.output.visualization_edge_checkbox.isChecked(),
                               add_trajectory=self.tools.output.visualization_trajectory_checkbox.isChecked(),
                               add_label=self.tools.output.visualization_label_checkbox.isChecked(),
                               trajectory_length=int(
                                   self.tools.output.visualization_trajectory_length.text()),
                               video_fps=int(self.tools.output.visualization_video_fps.text())))

        self.menu.brush_act.triggered.connect(self.brush_fnc)
        self.menu.eraser_act.triggered.connect(self.eraser_fnc)
        self.menu.drag_act.triggered.connect(self.drag_fnc)
        self.menu.confirm_act.triggered.connect(self.confirm_fnc)
        self.menu.save_act.triggered.connect(self.save_annotation_fnc)

        self.menu.tutorial_act.triggered.connect(self.open_tutorial)

        self.setMenuBar(self.menu_bar)

    def init_left_part(self):
        self.navigation = LeftNavigation()
        self.left_navigation = self.navigation.left_navigation
        self.tools = LeftTools()
        self.left_tools = self.tools.left_tools

        self.left_navigation.clicked.connect(self.left_navigation_fnc)
        self.last_item = self.left_navigation.item(self.last_index)
        self.last_item.setBackground(QColor("#323232"))

        # file_tree
        self.tools.file_tree_widget.create_button.clicked.connect(
            self.new_project_fnc)
        self.tools.file_tree_widget.load_button.clicked.connect(self.load_fnc)
        self.tools.file_tree_widget.default_button.clicked.connect(
            self.default_fnc)

        # seg alg1
        self.tools.segment.thresh_segment_button.clicked.connect(
            lambda: self.segment('binary_thresholding',
                                 threshold=self.tools.segment.thresh_sld1.value(),
                                 minimal_size=int(self.tools.segment.thresh_min_size_editor.text())))

        # seg alg11
        self.tools.segment.thresh_segment_button11.clicked.connect(
            lambda: self.segment('otsu_thresholding',
                                 minimal_size=int(self.tools.segment.thresh_min_size_editor11.text())))

        # seg alg2
        self.tools.segment.model_browse_button.clicked.connect(
            self.model_select_fnc)
        self.tools.segment.unet_segment_button.clicked.connect(
            lambda: self.segment('unet',
                                 model_path=self.unet_model_path,
                                 scale_img=self.scale_img_list[self.tools.segment.scale_img_select.currentIndex(
                                 )],
                                 device=self.tools.segment.device_select.currentText().lower(),
                                 threshold=self.tools.segment.thresh_sld2.value()/10,
                                 minimal_size=int(self.tools.segment.unet_min_size_editor.text())))

        # seg alg3
        self.tools.segment.watershed_segment_button.clicked.connect(
            lambda: self.segment('water_shed',
                                 noise_amplitude=self.tools.segment.noise_sld.value(),
                                 dist_thresh=self.tools.segment.dist_thresh_sld.value()/10,
                                 minimal_size=int(self.tools.segment.watershed_min_size_editor.text())))

        # seg alg4
        self.tools.segment.select_roi_button.clicked.connect(
            self.select_roi_button_fnc)
        self.tools.segment.grabcut_segment_button.clicked.connect(
            lambda: self.segment('grab_cut',
                                 iteration=self.tools.segment.iteration_sld.value()))

        self.tools.segment.thresh_segment_butto5.clicked.connect(self.revoke_operation)

        # normalization
        self.tools.normlize.equalize_hist_button.clicked.connect(
            lambda: self.normalize('equalize_hist'))
        self.tools.normlize.clahe_button.clicked.connect(
            lambda: self.normalize('CLAHE',
                                   clip_limit=self.tools.normlize.clip_limit_sld.value(),
                                   grid_width=self.tools.normlize.grid_width_sld.value(),
                                   grid_height=self.tools.normlize.grid_width_sld.value()))
        self.tools.normlize.min_max_button.clicked.connect(
            lambda: self.normalize('min_max'))
        self.tools.normlize.retinex_MSRCP_button.clicked.connect(
            lambda: self.normalize('retinex_MSRCP'))
        self.tools.normlize.retinex_MSRCR_button.clicked.connect(
            lambda: self.normalize('retinex_MSRCR'))
        self.tools.normlize.reset_raw_button.clicked.connect(
            self.reset_raw_button_fnc)

        # track
        self.tools.track.run_button.clicked.connect(
            lambda: self.track(self.tracker_name))

        # output

        self.tools.output.output_button.clicked.connect(
            lambda: self.write(write_folder=self.project_path,
                               add_color=self.tools.output.visualization_color_checkbox.isChecked(),
                               add_box=self.tools.output.visualization_box_checkbox.isChecked(),
                               add_edge=self.tools.output.visualization_edge_checkbox.isChecked(),
                               add_trajectory=self.tools.output.visualization_trajectory_checkbox.isChecked(),
                               add_label=self.tools.output.visualization_label_checkbox.isChecked(),
                               trajectory_length=int(
                                   self.tools.output.visualization_trajectory_length.text()),
                               video_fps=int(self.tools.output.visualization_video_fps.text())))

        # annotation
        self.tools.annotation.load_button.clicked.connect(self.load_fnc)
        self.tools.annotation.set_button.clicked.connect(self.result_path_fnc)
        self.tools.annotation.save_annotation_button.clicked.connect(
            self.save_annotation_fnc)
        self.tools.annotation.finish_annotation_button.clicked.connect(
            self.finish_annotation_fnc)

        # train
        self.tools.io.set_source_button.clicked.connect(
            self.set_source_button_fnc)
        self.tools.io.set_label_button.clicked.connect(
            self.set_label_button_fnc)
        self.tools.io.set_log_button.clicked.connect(self.set_log_button_fnc)
        self.tools.run_train.train_model_button.clicked.connect(
            self.train_model_button_fnc)
        self.tools.run_train.load_model_button.clicked.connect(
            self.load_model_button_fnc)

    def init_visualize_window(self):
        self.visualize = VisualizeWindow()
        self.visualize_window = self.visualize.visualize_window
        self.visualize.main_left.clicked.connect(self.main_left_fnc)
        self.visualize.main_right.clicked.connect(self.main_right_fnc)
        self.visualize.main_sld.valueChanged.connect(self.main_sld_fnc)

    def init_correction_tools(self):
        self.correction = CorrectionTools()
        self.correction_tools = self.correction.right_widget

        self.correction.add_instance_button.clicked.connect(
            self.add_instance_fnc)
        self.correction.instances_widget.clicked.connect(
            self.instances_widget_fnc)
        self.correction.instances_widget.doubleClicked.connect(
            self.instances_widget_fnc_double)
        self.correction.size_editor.textChanged.connect(self.size_editor_fnc)
        self.correction.size_left_button.clicked.connect(self.size_left_fnc)
        self.correction.size_right_button.clicked.connect(self.size_right_fnc)
        self.correction.brush_button.clicked.connect(self.brush_fnc)
        self.correction.eraser_button.clicked.connect(self.eraser_fnc)
        self.correction.drag_button.clicked.connect(self.drag_fnc)
        self.correction.confirm_button.clicked.connect(self.confirm_fnc)
        self.correction.delete_button.clicked.connect(self.instance_delete_fnc)

    def init_status_bar(self):
        # Initialize status bar
        self.status = StatusBar()
        self.status_bar = self.status.status_bar

    def revoke_operation(self):
        self.open_path              = self.params_dict["open_path"]
        self.project_path           = self.params_dict["project_path"]
        self.unet_model_path        = self.params_dict["unet_model_path"]
        self.last_index             = self.params_dict["last_index"]
        self.frames_num             = self.params_dict["frames_num"]
        self.frames                 = self.params_dict["frames"]
        self.show_flag              = self.params_dict["show_flag"]
        self.segment_flag           = self.params_dict["segment_flag"]
        self.segmenter_name         = self.params_dict["segmenter_name"]
        self.tracker_name           = self.params_dict["tracker_name"]
        self.normalizer_name        = self.params_dict["normalizer_name"]
        self.previous_frame         = self.params_dict["previous_frame"]
        self.previous_algorithm     = self.params_dict["previous_algorithm"]
        self.brush_flag             = self.params_dict["brush_flag"]
        self.grabcut_pos_begin      = self.params_dict["grabcut_pos_begin"]
        self.grabcut_pos_finish     = self.params_dict["grabcut_pos_finish"]
        self.grabcut_roi            = self.params_dict["grabcut_roi"]
        self.grabcut_rect           = self.params_dict["grabcut_rect"]
        self.annotation_flag        = self.params_dict["annotation_flag"]
        self.widget_list            = self.params_dict["widget_list"]
        self.changed_instances      = self.params_dict["changed_instances"]
        self.bboxroi                = self.params_dict["bboxroi"]
        self.drag_flag              = self.params_dict["drag_flag"]
        self.source_img_root        = self.params_dict["source_img_root"]
        self.label_img_root         = self.params_dict["label_img_root"]
        self.log_root               = self.params_dict["log_root"]
        self.validation_ratio       = self.params_dict["validation_ratio"]
        self.scale_img              = self.params_dict["scale_img"]
        self.weighted_type          = self.params_dict["weighted_type"]
        self.batch_size             = self.params_dict["batch_size"]
        self.workers                = self.params_dict["workers"]
        self.gpu_num                = self.params_dict["gpu_num"]
        self.lr                     = self.params_dict["lr"]
        self.epochs                 = self.params_dict["epochs"]
        self.weight_decay           = self.params_dict["weight_decay"]
        self.loss_type              = self.params_dict["loss_type"]
        self.loss_type_list         = self.params_dict["loss_type_list"]
        self.result_dir_path        = self.params_dict["result_dir_path"]
        self.origin_dir_path        = self.params_dict["origin_dir_path"]

        # params
        self.tools.segment.thresh_sld1.setValue(self.params_dict["segment_thresh_sld1"])
        self.tools.segment.thresh_textline1.setText(self.params_dict["segment_thresh_text1"])
        self.tools.segment.thresh_min_size_editor.setText(self.params_dict["segment_thresh_min_size"])
        self.tools.segment.thresh_sld11.setValue(self.params_dict["segment_thresh_sld11"])
        self.tools.segment.thresh_textline11.setText(self.params_dict["segment_thresh_text11"])
        self.tools.segment.thresh_min_size_editor11.setText(self.params_dict["segment_thresh_min_size11"])
        self.tools.segment.model_path_label.setText(self.params_dict["segment_model_path"])
        self.tools.segment.scale_img_select.setCurrentIndex(self.params_dict["segment_scale_img"])
        self.tools.segment.thresh_sld2.setValue(self.params_dict["segment_thresh_sld2"])
        self.tools.segment.thresh_textline2.setText(self.params_dict["segment_thresh_text2"])
        self.tools.segment.unet_min_size_editor.setText(self.params_dict["segment_unet_min_size"])
        self.tools.segment.device_select.setCurrentIndex(self.params_dict["GPU_CPU"])
        self.tools.segment.noise_sld.setValue(self.params_dict["segment_noise_sld"])
        self.tools.segment.noise_textline.setText(self.params_dict["segment_noise_text"])
        self.tools.segment.dist_thresh_sld.setValue(self.params_dict["segment_dist_sld"])
        self.tools.segment.dist_thresh_textline.setText(self.params_dict["segment_dist_text"])
        self.tools.segment.watershed_min_size_editor.setText(self.params_dict["segment_water_min_size"])
        self.tools.segment.iteration_sld.setValue(self.params_dict["segment_it_sld"])
        self.tools.segment.iteration_textline.setText(self.params_dict["segment_it_text"])
        self.tools.normlize.clip_limit_sld.setValue(self.params_dict["normlize_clip_limit_sld"])
        self.tools.normlize.clip_limit_textline.setText(self.params_dict["normlize_clip_limit_textline"])
        self.tools.normlize.grid_width_sld.setValue(self.params_dict["normlize_grid_width_sld"])
        self.tools.normlize.grid_width_textline.setText(self.params_dict["normlize_grid_width_textline"])
        self.tools.normlize.grid_height_sld.setValue(self.params_dict["normlize_grid_height_sld"])
        self.tools.normlize.grid_height_textline.setText(self.params_dict["normlize_grid_height_textline"])
        self.tools.track.tracker_select.setCurrentIndex(self.params_dict["track_index"])

        # update main_frame and list widget
        self.visualize.main_sld.setValue(0)
        self.visualize.main_sld.setMaximum(self.frames_num - 1)
        self.status.frame_info_label.setText(
            " Current frame: " + str(1))
        self.status.total_frame_label.setText(
            " Total frames: " + str(self.frames_num))
        self.main_sld_fnc()
        self.instance_widget_update_fnc()

    def update_params(self):
        self.params_dict["open_path"]           = self.open_path
        self.params_dict["project_path"]        = self.project_path
        self.params_dict["unet_model_path"]     = self.unet_model_path
        self.params_dict["last_index"]          = self.last_index
        self.params_dict["frames_num"]          = self.frames_num
        self.params_dict["frames"]              = self.frames
        self.params_dict["show_flag"]           = self.show_flag
        self.params_dict["segment_flag"]        = self.segment_flag
        self.params_dict["segmenter_name"]      = self.segmenter_name
        self.params_dict["tracker_name"]        = self.tracker_name
        self.params_dict["normalizer_name"]     = self.normalizer_name
        self.params_dict["previous_frame"]      = self.previous_frame
        self.params_dict["previous_algorithm"]  = self.previous_algorithm
        self.params_dict["brush_flag"]          = self.brush_flag
        self.params_dict["grabcut_pos_begin"]   = self.grabcut_pos_begin
        self.params_dict["grabcut_pos_finish"]  = self.grabcut_pos_finish
        self.params_dict["grabcut_roi"]         = self.grabcut_roi
        self.params_dict["grabcut_rect"]        = self.grabcut_rect
        self.params_dict["annotation_flag"]     = self.annotation_flag
        self.params_dict["widget_list"]         = self.widget_list
        self.params_dict["changed_instances"]   = self.changed_instances
        self.params_dict["bboxroi"]             = self.bboxroi
        self.params_dict["drag_flag"]           = self.drag_flag
        self.params_dict["source_img_root"]     = self.source_img_root
        self.params_dict["label_img_root"]      = self.label_img_root
        self.params_dict["log_root"]            = self.log_root
        self.params_dict["validation_ratio"]    = self.validation_ratio
        self.params_dict["scale_img"]           = self.scale_img
        self.params_dict["weighted_type"]       = self.weighted_type
        self.params_dict["batch_size"]          = self.batch_size
        self.params_dict["workers"]             = self.workers
        self.params_dict["gpu_num"]             = self.gpu_num
        self.params_dict["lr"]                  = self.lr
        self.params_dict["epochs"]              = self.epochs
        self.params_dict["weight_decay"]        = self.weight_decay
        self.params_dict["loss_type"]           = self.loss_type
        self.params_dict["loss_type_list"]      = self.loss_type_list
        self.params_dict["result_dir_path"]     = self.result_dir_path
        self.params_dict["origin_dir_path"]     = self.origin_dir_path


        # segmenter
        self.params_dict["segment_thresh_sld1"]         = self.tools.segment.thresh_sld1.value()
        self.params_dict["segment_thresh_text1"]        = self.tools.segment.thresh_textline1.text()
        self.params_dict["segment_thresh_min_size"]     = self.tools.segment.thresh_min_size_editor.text()

        self.params_dict["segment_thresh_sld11"] = self.tools.segment.thresh_sld11.value()
        self.params_dict["segment_thresh_text11"] = self.tools.segment.thresh_textline11.text()
        self.params_dict["segment_thresh_min_size11"] = self.tools.segment.thresh_min_size_editor11.text()

        self.params_dict["segment_model_path"]          = self.tools.segment.model_path_label.text()
        self.params_dict["segment_scale_img"]           = self.tools.segment.scale_img_select.currentIndex()
        self.params_dict["segment_thresh_sld2"]         = self.tools.segment.thresh_sld2.value()
        self.params_dict["segment_thresh_text2"]        = self.tools.segment.thresh_textline2.text()
        self.params_dict["segment_unet_min_size"]       = self.tools.segment.unet_min_size_editor.text()
        self.params_dict["GPU_CPU"]                     = self.tools.segment.device_select.currentIndex()

        self.params_dict["segment_noise_sld"]           = self.tools.segment.noise_sld.value()
        self.params_dict["segment_noise_text"]          = self.tools.segment.noise_textline.text()
        self.params_dict["segment_dist_sld"]            = self.tools.segment.dist_thresh_sld.value()
        self.params_dict["segment_dist_text"]           = self.tools.segment.dist_thresh_textline.text()
        self.params_dict["segment_water_min_size"]      = self.tools.segment.watershed_min_size_editor.text()

        self.params_dict["segment_it_sld"]              = self.tools.segment.iteration_sld.value()
        self.params_dict["segment_it_text"]             = self.tools.segment.iteration_textline.text()

        self.params_dict["track_index"]                 = self.tools.track.tracker_select.currentIndex()

        # normalize
        self.params_dict["normlize_clip_limit_sld"] = self.tools.normlize.clip_limit_sld.value()
        self.params_dict["normlize_clip_limit_textline"] = self.tools.normlize.clip_limit_textline.text()

        self.params_dict["normlize_grid_width_sld"] = self.tools.normlize.grid_width_sld.value()
        self.params_dict["normlize_grid_width_textline"] = self.tools.normlize.grid_width_textline.text()

        self.params_dict["normlize_grid_height_sld"] = self.tools.normlize.grid_height_sld.value()
        self.params_dict["normlize_grid_height_textline"] = self.tools.normlize.grid_height_textline.text()

    def open_tutorial(self):
        if os.path.exists(self.tutorial_path):
            url = self.tutorial_path
            QDesktopServices.openUrl(QUrl.fromLocalFile(url))

    def set_source_button_fnc(self):
        source_img_root = QFileDialog.getExistingDirectory()
        if self.has_chinese(source_img_root):
            self.chinese_path_message_box = WarningMessageBox(
                "Please select a path without chinese characters.")
            self.chinese_path_message_box.show()
        else:
            self.source_img_root = source_img_root
            self.tools.io.source_folder_show_lineedit.setText(
                self.source_img_root)

    def set_label_button_fnc(self):
        label_img_root = QFileDialog.getExistingDirectory()
        if self.has_chinese(label_img_root):
            self.chinese_path_message_box = WarningMessageBox(
                "Please select a path without chinese characters.")
            self.chinese_path_message_box.show()
        else:
            self.label_img_root = label_img_root
            self.tools.io.label_folder_show_lineedit.setText(
                self.label_img_root)

    def set_log_button_fnc(self):
        log_root = QFileDialog.getExistingDirectory()
        if self.has_chinese(log_root):
            self.chinese_path_message_box = WarningMessageBox(
                "Please select a path without chinese characters.")
            self.chinese_path_message_box.show()
        else:
            self.log_root = log_root
            self.tools.io.log_folder_show_lineedit.setText(self.log_root)

    def train_model_button_fnc(self):
        QApplication.processEvents()
        self.status.work_info_label.setText("Training the model...")
        self.validation_ratio = self.tools.data_loader.validation_radio_sld.value()/10
        self.scale_img = self.scale_img_list[self.tools.data_loader.scale_img_select.currentIndex(
        )]
        self.weighted_type = self.weighted_type_list[self.tools.weighted_loss.weighted_loss_select.currentIndex(
        )]
        self.aug_list = []
        if self.tools.data_loader.flip_checkbox.isChecked():
            self.aug_list.append("Flip")
        if self.tools.data_loader.rotate_checkbox.isChecked():
            self.aug_list.append("Rotate")
        if self.tools.data_loader.gaussian_noise_checkbox.isChecked():
            self.aug_list.append("GaussianNoise")
        if self.tools.data_loader.gaussian_blur_checkbox.isChecked():
            self.aug_list.append("GaussianBlur")
        self.batch_size = int(
            self.tools.data_loader.batch_size_select.currentText())
        self.workers = int(
            self.tools.data_loader.paraller_works_select.currentText())
        self.gpu_num = int(self.tools.trainer.gpu_num_select.currentText())
        self.resume = self.tools.run_train.model_path
        self.epochs = int(self.tools.trainer.epoch_textline.text())
        self.lr = float(self.tools.optimizer.lr_select.currentText())
        self.weight_decay = float(
            self.tools.optimizer.weight_decay_select.currentText())
        self.loss_type = self.tools.loss.loss_select.currentText()
        train_parameters = TrainParameters(source_img_root=self.source_img_root,
                                           label_img_root=self.label_img_root,
                                           log_root=self.log_root,
                                           validation_ratio=self.validation_ratio,
                                           scale_img=self.scale_img,
                                           weighted_type=self.weighted_type,
                                           aug_list=self.aug_list,
                                           batch_size=self.batch_size,
                                           workers=self.workers,
                                           gpu_num=self.gpu_num,
                                           resume=self.resume,
                                           epochs=self.epochs,
                                           lr=self.lr,
                                           weight_decay=self.weight_decay,
                                           loss_type=self.loss_type)

        train_wrapper = TrainerWrapper(train_parameters)
        start_epoch = train_wrapper.start_epoch
        self.status.progressbar.setMaximum(train_parameters.epochs-start_epoch)
        self.status.progressbar.setVisible(True)
        QApplication.processEvents()
        self.status.work_info_label.setText("Training the model...")

        t = 1
        for epoch in range(start_epoch, train_parameters.epochs):
            self.status.update_progressbar(t)
            t = t + 1
            train_wrapper.train_epoch(epoch)
        self.status.progressbar.setVisible(False)
        QApplication.processEvents()
        self.status.work_info_label.setText("")

    def load_model_button_fnc(self):
        model_path = QFileDialog.getOpenFileName(None, "Select a model file..",
                                                 filter="*.tar")[0]
        if not model_path == "":
            self.tools.run_train.model_path_show_lineedit.setText(model_path)
            self.tools.run_train.model_path = model_path

    def default_fnc(self):
        self.tools.update_file_tree(self.project_path)
        self.tools.file_tree_widget.create_button.clicked.connect(
            self.new_project_fnc)
        self.tools.file_tree_widget.load_button.clicked.connect(self.load_fnc)
        self.tools.file_tree_widget.default_button.clicked.connect(
            self.default_fnc)

    def reset_raw_button_fnc(self):
        if not len(self.frames) == 0:
            for key in self.frames.keys():
                self.frames[key].norm_img = self.frames[key].raw_img

            self.visualize.main_frame.setImage(
                self.frames[self.visualize.main_sld.value()].norm_img)

    def select_roi_button_fnc(self):
        self.visualize.main_frame.getImageItem().mouseDragEvent = self.grabcut_drag

    def grabcut_drag(self, event):
        event.accept()
        pos = event.pos()
        if event.isStart():
            self.grabcut_pos_begin = pos
            # self.grabcut_rect[0] = int(pos[0])
        elif event.isFinish():
            self.grabcut_pos_finish = pos
            event.ignore()
        else:
            if self.grabcut_roi is not None:
                self.visualize.main_frame.removeItem(self.grabcut_roi)
            self.grabcut_roi = pg.RectROI(
                self.grabcut_pos_begin, pos-self.grabcut_pos_begin)
            self.visualize.main_frame.addItem(self.grabcut_roi)

    def warp_fnc(self):
        algorithm_key = self.tools.main_algorithm.currentIndex()
        if algorithm_key == self.previous_algorithm:
            self.tools.main_algorithm.setCurrentIndex(4)
            self.previous_algorithm = 4
        else:
            self.previous_algorithm = algorithm_key

    def main_algorithm_changed_fnc(self):
        algorithm_key = self.tools.main_algorithm.currentIndex()

        for i in range(4):
            if i == algorithm_key:
                self.tools.main_algorithm.setItemIcon(
                    i, QIcon(get_icon("Arrow_down.png")))
            else:
                self.tools.main_algorithm.setItemIcon(
                    i, QIcon(get_icon("Arrow_right.png")))

    def normalizer_changed_fnc(self):
        normalizer_key = self.tools.normlize.normalize_tools.currentIndex()
        for i in range(5):
            if i == normalizer_key:
                self.tools.normlize.normalize_tools.setItemIcon(
                    i, QIcon(get_icon("Arrow_down.png")))
            else:
                self.tools.normlize.normalize_tools.setItemIcon(
                    i, QIcon(get_icon("Arrow_right.png")))
        self.normalizer_name = self.normalizer_dict[normalizer_key]

    def segmenter_changed_fnc(self):
        segmenter_key = self.tools.segment.segment_tools.currentIndex()
        for i in range(5):
            if i == segmenter_key:
                self.tools.segment.segment_tools.setItemIcon(
                    i, QIcon(get_icon("Arrow_down.png")))
            else:
                self.tools.segment.segment_tools.setItemIcon(
                    i, QIcon(get_icon("Arrow_right.png")))
        self.segmenter_name = self.segmenter_dict[segmenter_key]

    def model_select_fnc(self):
        model_path = QFileDialog.getOpenFileName(None, "Select a model file..",
                                                 filter="*.tar")[0]
        if model_path == "":
            self.tools.segment.model_path_label.setText("Select a model..")
        else:
            self.tools.segment.model_path_label.setText(model_path)
            self.unet_model_path = model_path

    def main_left_fnc(self):
        if not len(self.frames) == 0:
            v = self.visualize.main_sld.value()
            if v > 0:
                self.visualize.main_sld.setValue(v-1)
                # self.main_sld_fnc()
                ml = " Current frame: " + str(v)
                self.status.frame_info_label.setText(ml)

    def main_right_fnc(self):
        if not len(self.frames) == 0:
            v = self.visualize.main_sld.value()
            if v < self.frames_num:
                self.visualize.main_sld.setValue(v+1)
                # self.main_sld_fnc()
                ml = " Current frame: " + str(v + 2)
                self.status.frame_info_label.setText(ml)

    def main_sld_fnc(self):
        if not len(self.frames) == 0:
            main_sld_val = self.visualize.main_sld.value()
            main_sld_val_label = " Current frame: " + str(main_sld_val+1)
            self.status.frame_info_label.setText(main_sld_val_label)
            if not np.shape(len(self.frames)) == 0:

                if self.show_flag == 1:
                    self.visualize.main_frame.setImage(
                        self.frames[main_sld_val].norm_img)
                    self.correction.assist_frame.setImage(
                        self.frames[main_sld_val].raw_img)

                elif self.show_flag == 2:
                    self.visualize.main_frame.setImage(
                        self.frames[main_sld_val].binary_mask)
                    self.correction.assist_frame.setImage(
                        self.frames[main_sld_val].raw_img)

                elif self.show_flag == 3:
                    self.visualize.main_frame.removeItem(self.bboxroi)
                    self.visualize.main_frame.setImage(
                        self.frames[main_sld_val].raw_color_img)
                    self.correction.assist_frame.setImage(
                        self.frames[main_sld_val].raw_img)
                    self.instance_widget_update_fnc()
                elif self.show_flag == 4:
                    if self.bboxroi is not None:
                        self.visualize.main_frame.removeItem(self.bboxroi)
                    self.visualize.main_frame.setImage(
                        self.frames[main_sld_val].annotation_color_img)
                    self.correction.assist_frame.setImage(
                        self.frames[main_sld_val].raw_img)
                    self.instance_widget_update_fnc()
            else:
                pass

            self.previous_frame = main_sld_val

    def instance_widget_update_fnc(self):
        self.widget_list = []
        self.correction.instances_widget.clear()
        for key in self.frames[self.visualize.main_sld.value()].instances.keys():
            if self.frames[self.visualize.main_sld.value()].instances[key].name is not None:
                show_contents = "Name: " + self.frames[self.visualize.main_sld.value()].instances[key].name + "\n" + \
                                " Centroid: " + \
                    str(self.frames[self.visualize.main_sld.value()
                                    ].instances[key].centroid)
            else:
                show_contents = "Name: cell_" + str(self.correction.instances_widget.currentRow()+1) + "\n" + \
                                " Centroid: " + \
                    str(self.frames[self.visualize.main_sld.value()
                                    ].instances[key].centroid)
            item = QListWidgetItem(
                show_contents, self.correction.instances_widget)
            pix = QPixmap(30, 30)
            pix.fill(QColor(self.frames[self.visualize.main_sld.value()].instances[key].color[0],
                            self.frames[self.visualize.main_sld.value(
                            )].instances[key].color[1],
                            self.frames[self.visualize.main_sld.value()].instances[key].color[2]))
            item.setIcon(QIcon(pix))
            item.setSizeHint(QSize(35, 35))
            self.widget_list.append(
                self.frames[self.visualize.main_sld.value()].instances[key].label_id)
            item.setTextAlignment(Qt.AlignCenter)
            self.correction.instances_widget.addItem(item)

    def new_project_fnc(self):
        dir_path = QFileDialog.getExistingDirectory()
        if self.has_chinese(dir_path):
            self.chinese_path_message_box = WarningMessageBox(
                "Please select a path without chinese characters.")
            self.chinese_path_message_box.show()
        elif not dir_path:
            self.blank_path_message_box = WarningMessageBox(
                "Please select a valid path.")
            self.blank_path_message_box.show()
        else:
            self.project_path = dir_path
            self.tools.update_file_tree(self.project_path)
            self.tools.file_tree_widget.create_button.clicked.connect(
                self.new_project_fnc)
            self.tools.file_tree_widget.load_button.clicked.connect(
                self.load_fnc)
            self.tools.file_tree_widget.default_button.clicked.connect(
                self.default_fnc)

    def result_path_fnc(self):
        if len(self.frames) == 0:
            self.origin_first_message_box = InformationMessageBox(
                "Please load the origin images first!")
            self.origin_first_message_box.show()
        else:
            self.result_dir_path = QFileDialog.getExistingDirectory()
            logger.info('The annotation result save path is: %s' %
                        self.result_dir_path)
            if len(self.result_dir_path) > 0:
                if len(os.listdir(self.result_dir_path)) > 0:
                    self.continue_annotation_message_box = QuestionMessageBox(
                        "Do you want to continue the last annotation?")
                    self.continue_annotation_message_box.show()
                    self.continue_annotation_message_box.yes_button.clicked.connect(
                        self.continue_annotation_message_box_yes)
                    self.continue_annotation_message_box.cancel_button.clicked.connect(
                        self.continue_annotation_message_box_cancel)

                else:
                    self.new_annotation()

    def timer_fnc(self):
        global timer
        self.save_annotation_fnc()
        timer = threading.Timer(3, self.timer_fnc)
        self.tools.annotation.save_label.setText("Last save at " +
                                                 time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
        timer.start()

    def continue_annotation_message_box_yes(self):
        annotation_dir_list = os.listdir(self.result_dir_path)
        for annotation_x in annotation_dir_list:
            annotation_x_img = cv2.imread(os.path.join(
                self.result_dir_path, annotation_x), -1)
            for key in self.frames.keys():
                if self.ismatched(os.path.split(self.frames[key].file_name)[1], annotation_x):
                    self.frames[key].label_img = annotation_x_img

        for key in self.frames.keys():
            if self.frames[key].label_img is not None:
                if self.frames[key].label_img.max() > 0:
                    self.frames[key].auto_labeling1(color_groups, None)

        self.tools.annotation.result_path_show_lineedit.setText(
            self.result_dir_path)
        self.annotation_flag = 2
        self.show_flag = 4
        self.visualize.main_frame.setImage(
            self.frames[self.visualize.main_sld.value()].annotation_color_img)
        self.correction.assist_frame.setImage(
            self.frames[self.visualize.main_sld.value()].raw_img)
        self.instance_widget_update_fnc()
        self.timer_fnc()

        self.continue_annotation_message_box.close()

    def ismatched(self, raw_file_name, annotation_file_name):
        raw_str = raw_file_name.split('.')[0]
        raw_str = "annotation_" + raw_str
        annotation_str = annotation_file_name.split('.')[0]

        return annotation_str == raw_str

    def new_annotation(self):
        if self.has_chinese(self.result_dir_path):
            self.chinese_path_message_box = WarningMessageBox(
                "Please select a path without chinese characters.")
            self.chinese_path_message_box.show()
        else:
            self.tools.annotation.result_path_show_lineedit.setText(
                self.result_dir_path)
            for key in self.frames.keys():
                self.frames[key].label_img = np.zeros(
                    np.shape(self.frames[key].raw_img[:, :, 0]))
                self.frames[key].label_img.astype(np.uint16)
            self.annotation_flag = 2
            self.show_flag = 4
            self.timer_fnc()

    def str2list(self, s):
        s = s.replace(" ", "")
        s1 = s.split(",")
        sc0 = s1[0]
        sc1 = s1[1]
        sc2 = s1[2]
        color0 = int(sc0[1:])
        color1 = int(sc1)
        color2 = int(sc2[: -1])

        return [color0, color1, color2]

    def continue_annotation_message_box_cancel(self):
        if self.has_chinese(self.result_dir_path):
            self.chinese_path_message_box = WarningMessageBox(
                "Please select a path without chinese characters.")
            self.chinese_path_message_box.show()
        else:
            self.tools.annotation.result_path_show_lineedit.setText(
                self.result_dir_path)
            for key in self.frames.keys():
                self.frames[key].label_img = np.zeros(
                    np.shape(self.frames[key].raw_img[:, :, 0]))
                self.frames[key].label_img.astype(np.uint16)
            self.annotation_flag = 2
            self.show_flag = 4
            self.timer_fnc()
        self.continue_annotation_message_box.close()

    def load_fnc(self):
        if len(self.frames) == 0:
            self.files_loader()

        else:
            self.reload_question = QuestionMessageBox(
                "Are you sure to reload the data?")
            self.reload_question.show()
            self.reload_question.yes_button.clicked.connect(self.reload_fnc)

    def reload_fnc(self):
        self.annotation_flag = -1
        self.visualize.main_frame.clear()
        self.correction.assist_frame.clear()
        self.correction.instances_widget.clear()

        self.reload_question.close_fnc()
        self.files_loader()

    def files_loader(self):
        filenames = QFileDialog.getOpenFileNames(None, "Select image files ...",
                                                 filter="*bmp *.tif *.png *.jpg *.JPEG *avi *mp4 *mpg")[0]
        if not filenames == []:
            if self.has_chinese(filenames[0]):
                self.chinese_path_message_box = WarningMessageBox(
                    "Please select a path without chinese characters.")
                self.chinese_path_message_box.show()
            else:
                self.frames = load_images(filenames)
                self.frames_num = len(self.frames)

                self.visualize.main_frame.setImage(img=self.frames[0].raw_img)
                self.correction.assist_frame.setImage(self.frames[0].raw_img)

                self.show_flag = 1
                self.visualize.main_sld.setValue(0)
                self.visualize.main_sld.setMaximum(self.frames_num - 1)
                self.status.frame_info_label.setText(
                    " Current frame: " + str(1))
                self.status.total_frame_label.setText(
                    " Total frames: " + str(self.frames_num))

    def dir_loader(self):
        self.origin_dir_path = QFileDialog.getExistingDirectory()
        self.tools.annotation.origin_path_show_lineedit.setText(
            self.origin_dir_path)

        filenames = []
        if not self.origin_dir_path == "":
            for name in os.listdir(self.origin_dir_path):
                file_path = os.path.join(self.origin_dir_path, name)
                filenames.append(file_path)
        if not filenames == []:
            self.frames = load_images(filenames)
            self.frames_num = len(self.frames)
            self.visualize.main_frame.setImage(
                self.frames[0].annotation_color_img)
            self.correction.assist_frame.setImage(self.frames[0].raw_img)

            self.show_flag = 1
            self.visualize.main_sld.setValue(0)
            self.visualize.main_sld.setMaximum(self.frames_num - 1)
            self.status.frame_info_label.setText(" Current frame: " + str(1))
            self.status.total_frame_label.setText(
                " Total frames: " + str(self.frames_num))

    def exit_fnc(self):
        self.quit_message_box = QuestionMessageBox('You sure to exit?')
        self.quit_message_box.show()

        self.quit_message_box.yes_button.clicked.connect(self.exit_fnc_yes)

    def exit_fnc_yes(self):
        qApp.quit()

    def save_annotation_fnc(self):
        if not self.annotation_flag == 2:
            self.annotation_first_message_box = InformationMessageBox(
                "Please do annotation first!")
            self.annotation_first_message_box.show()
        elif self.annotation_flag == 2:
            for key in self.frames.keys():
                filepath, fullflname = os.path.split(
                    self.frames[key].file_name)
                file_name = fullflname.split('.')[0]

                name = "annotation_" + file_name + ".tif"
                annotation_path = os.path.join(self.result_dir_path, name)
                annotation_path = "/".join([self.result_dir_path, name])
                logger.info('Annotation image saved in : %s' % annotation_path)
                if self.frames[key].label_img.max() > 0:
                    imageio.imwrite(
                        annotation_path, self.frames[key].label_img.astype(np.uint16))
        else:
            self.annotation_save_message_box = InformationMessageBox(
                "The result has been successfully saved.")
            self.annotation_save_message_box.show()

    def finish_annotation_fnc(self):
        if not self.annotation_flag == 2:
            self.annotation_first_message_box = InformationMessageBox(
                "Please do annotation first!")
            self.annotation_first_message_box.show()
        else:
            self.annotation_finish_message_box = \
                QuestionMessageBox("Are you sure to finish the annotation?")
            self.annotation_finish_message_box.show()
            self.annotation_finish_message_box.yes_button.clicked.connect(
                self.annotation_finish_message_box_yes_fnc)
            timer.cancel()

    def annotation_finish_message_box_yes_fnc(self):
        self.annotation_flag = -1
        for key in self.frames.keys():
            name = "annotation_" + str(key) + ".tif"
            annotation_path = os.path.join(self.result_dir_path, name)
            imageio.imwrite(annotation_path,
                            self.frames[key].label_img.astype(np.uint16))

        self.annotation_finish_message_box.close_fnc()

    def brush_fnc(self):
        if len(self.frames) == 0:
            self.brush_message_box = InformationMessageBox(
                "Please load images first!")
            self.brush_message_box.show()
        elif not len(self.frames) == 0 and self.frames[0].label_img is None and self.annotation_flag == 0:
            self.brush_message_box = InformationMessageBox(
                "Please do segmentation first!")
            self.brush_message_box.show()
        elif self.annotation_flag == 1 or self.annotation_flag == 2:
            if self.bboxroi is not None:
                self.visualize.main_frame.removeItem(self.bboxroi)
                self.bboxroi = None
            self.brush_flag = 1
            ssv = int(self.correction.size_editor.text())
            pix = QPixmap(get_icon("circle.png"))
            pix = pix.scaled(QSize(ssv * 2, ssv * 2))
            cursor = QCursor(pix)
            self.visualize_window.setCursor(cursor)

            current_frame = self.frames[self.visualize.main_sld.value()]
            current_id = self.correction.instances_widget.currentRow()
            if current_id >= 0 and self.annotation_flag == 2:
                self.visualize.main_frame.imageItem.updateImage(
                    current_frame.annotation_color_img)
                self.visualize.main_frame.getImageItem().mouseDragEvent = self.brush_drag1
            elif current_id >= 0 and self.annotation_flag == 1:
                self.visualize.main_frame.imageItem.updateImage(
                    current_frame.raw_color_img)
                self.visualize.main_frame.getImageItem().mouseDragEvent = self.brush_drag1
            else:
                self.brush_message_box = InformationMessageBox(
                    "Please select a cell first!")
                self.brush_message_box.show()
        elif self.annotation_flag == 0:
            if self.bboxroi is not None:
                self.visualize.main_frame.removeItem(self.bboxroi)
                self.bboxroi = None
            self.brush_flag = 1
            ssv = int(self.correction.size_editor.text())
            pix = QPixmap(get_icon("circle.png"))
            pix = pix.scaled(QSize(ssv * 2, ssv * 2))
            cursor = QCursor(pix)
            self.visualize_window.setCursor(cursor)
            self.show_flag = 4

            colormap = pg.ColorMap([0, 1], color=[[0, 0, 0], [255, 255, 255]])
            self.visualize.main_frame.setColorMap(colormap)
            # self.visualize.main_frame.imageItem.updateImage(self.frames[self.visualize.main_sld.value()].raw_color_img)
            self.visualize.main_frame.getImageItem().mouseDragEvent = self.brush_drag1
        else:
            self.brush_message_box = InformationMessageBox(
                "Please select a cell first!")
            self.brush_message_box.show()

    def eraser_fnc(self):
        if len(self.frames) == 0:
            self.eraser_message_box = InformationMessageBox(
                "Please load images first!")
            self.eraser_message_box.show()
        elif not len(self.frames) == 0 and self.frames[0].label_img is None and self.annotation_flag == 0:
            self.eraser_message_box = InformationMessageBox(
                "Please do segmentation first!")
            self.eraser_message_box.show()
        elif self.annotation_flag == 1 or self.annotation_flag == 2:
            self.brush_flag = 0
            pix = QPixmap(get_icon("eraser1.png"))
            cursor = QCursor(pix)
            self.visualize_window.setCursor(cursor)
            current_frame = self.frames[self.visualize.main_sld.value()]
            current_id = self.correction.instances_widget.currentRow()
            if current_id >= 0 and self.annotation_flag == 2:
                self.visualize.main_frame.imageItem.updateImage(
                    current_frame.annotation_color_img)
                self.visualize.main_frame.getImageItem().mouseDragEvent = self.eraser_drag1
            elif current_id >= 0 and self.annotation_flag == 1:
                self.visualize.main_frame.imageItem.updateImage(
                    current_frame.raw_color_img)
                self.visualize.main_frame.getImageItem().mouseDragEvent = self.eraser_drag1
            else:
                self.eraser_message_box = InformationMessageBox(
                    "Please select a cell first!")
                self.eraser_message_box.show()
        elif self.annotation_flag == 0:
            self.brush_flag = 0
            self.brush_flag = 0
            pix = QPixmap(get_icon("eraser1.png"))
            cursor = QCursor(pix)
            self.visualize_window.setCursor(cursor)
            self.show_flag = 4
            self.visualize.main_frame.getImageItem().mouseDragEvent = self.eraser_drag1
        else:
            self.eraser_message_box = InformationMessageBox(
                "Please select a cell first!")
            self.eraser_message_box.show()

    def brush_drag1(self, event):

        ssv = int(self.correction.size_editor.text())
        pix = QPixmap(get_icon("circle.png"))
        pix = pix.scaled(QSize(ssv * 2, ssv * 2))
        cursor = QCursor(pix)
        self.visualize_window.setCursor(cursor)
        event.accept()
        pos = event.pos()
        current_frame = self.frames[self.visualize.main_sld.value()]
        current_id = self.correction.instances_widget.currentRow()
        current_label = current_frame.instances[self.widget_list[current_id]].label_id
        current_name = current_frame.instances[self.widget_list[current_id]].name
        current_color = current_frame.instances[self.widget_list[current_id]].color
        self.changed_instances.add_update_ins(
            current_id, current_label, current_name, current_color)

        x0 = max(int(pos[1]) - ssv + 1, 0)
        x1 = max(int(pos[1]) + ssv, 0)
        y0 = max(int(pos[0]) - ssv + 1, 0)
        y1 = max(int(pos[0]) + ssv, 0)
        if self.annotation_flag == 2:

            self.frames[self.visualize.main_sld.value(
            )].label_img[x0: x1, y0: y1] = current_label
            self.frames[self.visualize.main_sld.value(
            )].annotation_color_img[x0: x1, y0: y1, :] = current_color
            self.visualize.main_frame.imageItem.updateImage(
                self.frames[self.visualize.main_sld.value()].annotation_color_img)
        else:
            self.frames[self.visualize.main_sld.value(
            )].label_img[x0: x1, y0: y1] = current_label
            temp = np.zeros_like(
                self.frames[self.visualize.main_sld.value()].raw_color_img)
            temp[x0: x1, y0: y1, :] = current_color
            self.frames[self.visualize.main_sld.value()].raw_color_img[x0: x1, y0: y1, :] = \
                0.5*self.frames[self.visualize.main_sld.value()].raw_color_img[x0: x1, y0: y1, :] + \
                0.5*temp[x0: x1, y0: y1, :]
            self.visualize.main_frame.imageItem.updateImage(
                self.frames[self.visualize.main_sld.value()].raw_color_img)

    def eraser_drag1(self, event):
        event.accept()
        pos = event.pos()
        ssv = int(self.correction.size_editor.text())

        current_frame = self.frames[self.visualize.main_sld.value()]
        current_id = self.correction.instances_widget.currentRow()
        current_label = current_frame.instances[self.widget_list[current_id]].label_id
        current_name = current_frame.instances[self.widget_list[current_id]].name
        current_color = current_frame.instances[self.widget_list[current_id]].color

        self.changed_instances.add_update_ins(
            current_id, current_label, current_name, current_color)
        x0 = int(pos[1]) - ssv + 1
        x1 = int(pos[1]) + ssv
        y0 = int(pos[0]) - ssv + 1
        y1 = int(pos[0]) + ssv
        if self.annotation_flag == 2:
            self.frames[self.visualize.main_sld.value()
                        ].label_img[x0:x1, y0:y1] = 0
            self.frames[self.visualize.main_sld.value()].annotation_color_img[x0: x1, y0: y1, :] =\
                self.frames[self.visualize.main_sld.value()
                            ].raw_img[x0: x1, y0: y1, :]
            self.visualize.main_frame.imageItem.updateImage(
                self.frames[self.visualize.main_sld.value()].annotation_color_img)
        else:
            self.frames[self.visualize.main_sld.value()
                        ].label_img[x0:x1, y0:y1] = 0
            self.frames[self.visualize.main_sld.value()].raw_color_img[x0:x1, y0:y1, :] = \
                self.frames[self.visualize.main_sld.value()
                            ].raw_img[x0:x1, y0:y1, :]
            self.visualize.main_frame.imageItem.updateImage(
                self.frames[self.visualize.main_sld.value()].raw_color_img)

        if self.show_flag == 3:
            pass
        else:
            pass

    def confirm_fnc(self):
        if len(self.frames) == 0:
            self.confirm_message_box = InformationMessageBox(
                "Please load images first!")
            self.confirm_message_box.show()
        elif not len(self.frames) == 0 and self.frames[0].label_img is None and self.annotation_flag == 0:
            self.confirm_message_box = InformationMessageBox(
                "Please do segmentation first!")
            self.confirm_message_box.show()
        elif self.annotation_flag == 0 or self.annotation_flag == 1:
            self.brush_flag = 0
            current_frame = self.frames[self.visualize.main_sld.value()]
            self.show_flag = 3
            self.visualize.main_frame.clear()

            self.visualize_window.setCursor(Qt.ArrowCursor)
            self.visualize.main_frame.setImage(current_frame.raw_color_img)
            self.frames[self.visualize.main_sld.value()].update_labling(self.changed_instances.update_ins_id,
                                                                        self.changed_instances.update_ins_label,
                                                                        self.changed_instances.update_ins_name,
                                                                        self.changed_instances.update_ins_color)
            self.annotation_flag = 0
            self.instance_widget_update_fnc()
            # self.instances_widget_fnc()
        elif self.annotation_flag == 2:
            self.brush_flag = 0
            self.frames[self.visualize.main_sld.value()].add_labeling(self.changed_instances.update_ins_id,
                                                                      self.changed_instances.update_ins_label,
                                                                      self.changed_instances.update_ins_name,
                                                                      self.changed_instances.update_ins_color)
            self.instance_widget_update_fnc()
            # self.instances_widget_fnc()

    def drag_fnc(self):
        if len(self.frames) == 0:
            self.drag_message_box = InformationMessageBox(
                "Please load images first!")
            self.drag_message_box.show()
        elif not len(self.frames) == 0 and self.frames[0].label_img is None and self.annotation_flag == 0:
            self.drag_message_box = InformationMessageBox(
                "Please do segmentation first!")
            self.drag_message_box.show()
        elif self.annotation_flag == 1 or self.annotation_flag == 2 or self.annotation_flag == 0:
            self.brush_flag = 0
            pix = QPixmap(get_icon("hand1.png"))
            cursor = QCursor(pix)
            self.visualize_window.setCursor(cursor)
            self.visualize.main_frame.getImageItem().mouseDragEvent = self.drag_begin

    def drag_begin(self, event):
        event.ignore()

    def size_editor_fnc(self):
        if not len(self.correction.size_editor.text()) == 0:
            if int(self.correction.size_editor.text()) > 10:
                self.correction.size_editor.setText(str(10))
            elif int(self.correction.size_editor.text()) < 1:
                self.correction.size_editor.setText(str(1))

    def size_left_fnc(self):
        v = int(self.correction.size_editor.text())
        if v > 1:
            self.correction.size_editor.setText(str(v - 1))
            if self.brush_flag == 1:
                ssv = int(self.correction.size_editor.text())
                pix = QPixmap(get_icon("circle.png"))
                pix = pix.scaled(QSize(ssv * 2, ssv * 2))
                cursor = QCursor(pix)
                self.visualize_window.setCursor(cursor)

    def size_right_fnc(self):
        v = int(self.correction.size_editor.text())
        if v < 11:
            self.correction.size_editor.setText(str(v + 1))
            if self.brush_flag == 1:
                ssv = int(self.correction.size_editor.text())
                pix = QPixmap(get_icon("circle.png"))
                pix = pix.scaled(QSize(ssv * 2, ssv * 2))
                cursor = QCursor(pix)
                self.visualize_window.setCursor(cursor)

    def add_instance_fnc(self):
        if self.annotation_flag == 2:
            self.timer_fnc()
        if self.annotation_flag == 0:
            self.instances_setting = InstanceSettings(self.my_colors, self.frames[self.visualize.main_sld.value()].raw_img,
                                                      self.frames[self.visualize.main_sld.value(
                                                      )].label_max+1,
                                                      self.frames[self.visualize.main_sld.value()].frame_id)
            self.instances_setting.confirm_button.clicked.connect(
                self.add_instance_main)
            self.instances_setting.show()
            self.annotation_flag = 1
        elif self.annotation_flag == 2:
            self.instances_setting = InstanceSettings(self.my_colors,
                                                      self.frames[self.visualize.main_sld.value(
                                                      )].raw_img,
                                                      int(self.frames[self.visualize.main_sld.value(
                                                      )].label_max + 1),
                                                      self.frames[self.visualize.main_sld.value()].frame_id)
            self.instances_setting.confirm_button.clicked.connect(
                self.add_instance_main)
            self.instances_setting.show()
        else:
            self.add_instance_message_box = InformationMessageBox("Please do segmentation or "
                                                                  "select an output path first!")
            self.add_instance_message_box.show()

    def add_instance_main(self):
        pix = QPixmap(30, 30)
        pix.fill(QColor(self.instances_setting.color[0],
                        self.instances_setting.color[1],
                        self.instances_setting.color[2]))
        contents_show = "Name: " + self.instances_setting.name + "\n" + \
                        " Centroid: NAF"
        item = QListWidgetItem(contents_show, self.correction.instances_widget)
        item.setIcon(QIcon(pix))
        item.setSizeHint(QSize(35, 35))
        item.setTextAlignment(Qt.AlignCenter)

        self.correction.instances_widget.addItem(item)
        self.widget_list.append(self.instances_setting.ins.label_id)
        self.frames[self.visualize.main_sld.value()].add_instance(self.instances_setting.ins.label_id,
                                                                  self.instances_setting.ins)
        self.correction.instances_widget.setCurrentRow(
            len(self.widget_list) - 1)

        if self.segmenter_name == "grab_cut":
            self.frames[self.visualize.main_sld.value()].update_labling([self.correction.instances_widget.currentRow()],
                                                                        [self.instances_setting.ins.label_id],
                                                                        [self.instances_setting.ins.name],
                                                                        [self.instances_setting.ins.color])

            self.instance_widget_update_fnc()
            self.instances_widget_fnc()
            self.visualize.main_frame.removeItem(self.grabcut_roi)
            if self.bboxroi is not None:
                self.visualize.main_frame.removeItem(self.bboxroi)

        current_frame = self.frames[self.visualize.main_sld.value()]
        if self.annotation_flag == 2:
            self.visualize.main_frame.imageItem.updateImage(
                current_frame.annotation_color_img)
        else:
            self.visualize.main_frame.imageItem.updateImage(
                current_frame.raw_color_img)

    def instances_widget_fnc(self):
        self.visualize_window.setCursor(Qt.ArrowCursor)
        self.visualize.main_frame.getImageItem().mouseDragEvent = self.drag_begin
        if self.bboxroi is not None:
            self.visualize.main_frame.removeItem(self.bboxroi)

        bbox = self.frames[self.visualize.main_sld.value()].instances[
            self.widget_list[self.correction.instances_widget.currentRow()]].bbox
        if bbox is not None:
            self.bboxroi = pg.RectROI(
                [bbox[0], bbox[1]], [bbox[2]-bbox[0], bbox[3]-bbox[1]])
            self.visualize.main_frame.addItem(self.bboxroi)

    def instances_widget_fnc_double(self):
        ins = self.frames[self.visualize.main_sld.value()].instances[
            self.widget_list[self.correction.instances_widget.currentRow()]]
        if ins.coords is None:
            self.coords_instance_message_box = InformationMessageBox(
                "There is no cell area yet!")
            self.coords_instance_message_box.show()
        else:
            self.cell_window = CellAttributeWindow(ins)
            self.cell_window.show()

    def instance_delete_fnc(self):
        current_row = self.correction.instances_widget.currentRow()

        if self.annotation_flag == 2 and current_row >= 0:
            current_frame = self.frames[self.visualize.main_sld.value()]
            current_color = current_frame.instances[self.widget_list[current_row]].color
            ins_id = self.widget_list[current_row]
            self.widget_list.remove(ins_id)

            delete_ins_label = []
            delete_ins_id = []
            delete_ins_id.append(current_row)
            delete_ins_label.append(ins_id)
            self.frames[self.visualize.main_sld.value()].update_labling([], [], [], [], delete_ins_id=delete_ins_id,
                                                                        delete_ins_label=delete_ins_label,
                                                                        annotation_flag=2)
            self.visualize.main_frame.imageItem.updateImage(
                self.frames[self.visualize.main_sld.value()].annotation_color_img)
            self.correction.instances_widget.takeItem(current_row)
            self.correction.assist_frame.setImage(
                self.frames[self.visualize.main_sld.value()].raw_img)

        elif self.annotation_flag == 0 and current_row >= 0:
            current_frame = self.frames[self.visualize.main_sld.value()]
            current_color = current_frame.instances[self.widget_list[current_row]].color
            ins_id = self.widget_list[current_row]
            self.widget_list.remove(ins_id)

            delete_ins_label = []
            delete_ins_id = []
            delete_ins_id.append(current_row)
            delete_ins_label.append(ins_id)
            self.frames[self.visualize.main_sld.value()].update_labling([], [], [], [], delete_ins_id=delete_ins_id,
                                                                        delete_ins_label=delete_ins_label)
            self.correction.instances_widget.takeItem(current_row)

            current_frame = self.frames[self.visualize.main_sld.value()]
            if self.annotation_flag == 2:
                self.visualize.main_frame.imageItem.updateImage(
                    current_frame.annotation_color_img)
            else:
                self.visualize.main_frame.imageItem.updateImage(
                    current_frame.raw_color_img)
        else:
            self.delete_instance_message_box = InformationMessageBox(
                "Please select a cell first!")
            self.delete_instance_message_box.show()

    def center(self):
        qr = self.frameGeometry()
        self.desktop = QApplication.desktop()
        self.screenRect = self.desktop.screenGeometry()
        qr.moveCenter(self.screenRect.center())
        self.move(qr.topLeft())

    def change_show(self):
        if not self.left_tools.isVisible():
            self.left_tools.setVisible(True)

    # TODO
    def left_navigation_fnc(self):
        if self.last_index == self.left_navigation.currentRow() and self.left_tools.isVisible():
            self.left_tools.setVisible(False)
            self.last_item = self.left_navigation.item(self.last_index)
            self.last_item.setBackground(QColor("#414141"))
        elif self.last_index == self.left_navigation.currentRow() and (not self.left_tools.isVisible()):
            self.left_tools.setVisible(True)
            self.current_item = self.left_navigation.currentItem()
            self.current_item.setBackground(QColor("#323232"))
        elif (not self.last_index == self.left_navigation.currentRow()) and self.left_tools.isVisible():
            self.left_tools.setCurrentIndex(self.left_navigation.currentRow())
            self.last_item = self.left_navigation.item(self.last_index)
            self.last_item.setBackground(QColor("#414141"))
            self.current_item = self.left_navigation.currentItem()
            self.current_item.setBackground(QColor("#323232"))

            self.last_index = self.left_navigation.currentRow()
        else:
            self.left_tools.setCurrentIndex(self.left_navigation.currentRow())
            self.left_tools.setVisible(True)
            self.last_item = self.left_navigation.item(self.last_index)
            self.last_item.setBackground(QColor("#414141"))
            self.current_item = self.left_navigation.currentItem()
            self.current_item.setBackground(QColor("#323232"))

            self.last_index = self.left_navigation.currentRow()

    # algorithm API
    def normalize(self, name, **kwargs):
        self.normalizer_name = name

        if not len(self.frames) == 0:
            self.status.progressbar.setMaximum(self.frames_num)
            QApplication.processEvents()
            self.status.work_info_label.setText("Normalizing...")
            QApplication.processEvents()
            self.status.progressbar.setVisible(True)
            QApplication.processEvents()
            normalizer = get_normalizer(name=name, **kwargs)
            t = 1
            for key in self.frames.keys():
                self.frames[key].norm_img = normalizer(
                    self.frames[key].raw_img)
                QApplication.processEvents()
                self.status.update_progressbar(t)
                t = t + 1
            self.visualize.main_frame.setImage(
                self.frames[self.visualize.main_sld.value()].norm_img)
            QApplication.processEvents()
            self.status.work_info_label.setText("")
            QApplication.processEvents()
            self.status.progressbar.setVisible(False)
            QApplication.processEvents()
        else:
            self.normalize_message_box = InformationMessageBox(
                "Please load images first!")
            self.normalize_message_box.show()

    def segment(self, name, **kwargs):

        self.segmenter_name = name
        if (not len(self.frames) == 0 and self.segment_flag == 0) or \
                self.segmenter_name == 'grab_cut':
            self.segment_message_box1_fnc(name, **kwargs)
        elif not len(self.frames) == 0 and self.segment_flag == 1:
            self.segment_message_box1 = QuestionMessageBox(
                "Are you sure to re-segment the images?")
            self.segment_message_box1.yes_button.clicked.connect(
                lambda: self.segment_message_box1_fnc(name, close_flag=1, **kwargs))
            self.segment_message_box1.cancel_button.clicked.connect(
                self.segment_message_box1.close_fnc)
            self.segment_message_box1.show()
        else:
            self.segment_message_box2 = InformationMessageBox(
                "Please load images first!")
            self.segment_message_box2.show()
        self.update_params()

    def segment_message_box1_fnc(self, name, close_flag=0, **kwargs):

        self.segment_flag = 1
        if close_flag == 1:
            self.segment_message_box1.close()
        if not name == 'grab_cut':
            self.status.progressbar.setMaximum(self.frames_num)

            if name == 'unet':
                QApplication.processEvents()
                self.status.work_info_label.setText(
                    "Loading selected model...")
                QApplication.processEvents()
            if self.unet_model_path is None and name == 'unet':
                self.segment_message_box2 = InformationMessageBox(
                    "Please select a model first!")
                self.segment_message_box2.show()
            else:
                t = 1
                segmenter = get_segmenter(name=name, **kwargs)
                QApplication.processEvents()
                self.status.work_info_label.setText("Segmenting...")
                QApplication.processEvents()
                self.status.progressbar.setVisible(True)
                QApplication.processEvents()
                instance_zeros = []
                instance_bigger = []
                for key in self.frames.keys():
                    label_img = segmenter(self.frames[key].norm_img)
                    self.frames[key].label_img = label_img
                    instance_num = len(np.unique(label_img)) - 1
                    if instance_num == 0:
                        instance_zeros.append(key)
                    if instance_num > 100:
                        instance_bigger.append(key)
                    QApplication.processEvents()
                    self.status.work_info_label.setText("Segmenting...")
                    self.status.update_progressbar(t)
                    QApplication.processEvents()
                    t = t + 1
                QApplication.processEvents()
                self.status.progressbar.setVisible(False)
                QApplication.processEvents()
                self.status.work_info_label.setText("")
                QApplication.processEvents()

                if self.annotation_flag == 2:
                    pass
                else:
                    self.annotation_flag = 0

                if len(instance_zeros) > 0:
                    zeros_str = ",".join([str(x) for x in instance_zeros])
                    self.segment_message_box4 = WarningMessageBox("The instance number of " + zeros_str
                                                                  + " frame(s) is 0, please do re-segmentation.")
                    self.segment_message_box4.show()
                elif len(instance_bigger) > 0:
                    bigger_str = ",".join([str(x) for x in instance_bigger])
                    self.segment_message_box3 = QuestionMessageBox("The instance number of "
                                                                   + bigger_str +
                                                                   " frame(s) is bigger than 100, continue?")
                    self.segment_message_box3.show()
                    self.segment_message_box3.yes_button.clicked.connect(
                        self.get_label_and_close)

                else:
                    sv = self.visualize.main_sld.value()

                    self.visualize.main_frame.setImage(
                        np.sign(self.frames[sv].binary_mask[:, :, 0]))
                    self.show_flag = 2
                    self.get_label_fnc()

        else:
            segmenter = get_segmenter(name=name, **kwargs)
            QApplication.processEvents()
            self.status.work_info_label.setText("Segmenting...")
            QApplication.processEvents()
            if self.frames[self.visualize.main_sld.value()].label_img is None:
                label_img = segmenter(img=self.frames[self.visualize.main_sld.value()].norm_img,
                                      rect=[int(self.grabcut_roi.state['pos'][0]),
                                            int(self.grabcut_roi.state['pos'][1]),
                                            int(self.grabcut_roi.state['pos'][0] +
                                                self.grabcut_roi.state['size'][0]),
                                            int(self.grabcut_roi.state['pos'][1]+self.grabcut_roi.state['size'][1])],
                                      obj_idx=1)
            else:
                label_img = segmenter(img=self.frames[self.visualize.main_sld.value()].raw_img,
                                      rect=[int(self.grabcut_roi.state['pos'][0]),
                                            int(self.grabcut_roi.state['pos'][1]),
                                            int(self.grabcut_roi.state['pos'][0] +
                                                self.grabcut_roi.state['size'][0]),
                                            int(self.grabcut_roi.state['pos'][1] + self.grabcut_roi.state['size'][1])],
                                      obj_idx=np.max(self.frames[self.visualize.main_sld.value()].label_img) + 1)

            if label_img.max() == 0:
                self.segment_message_box3 = InformationMessageBox(
                    "Segmentation failed!")
                self.segment_message_box3.show()
            else:
                if self.frames[self.visualize.main_sld.value()].label_img is None:
                    self.frames[self.visualize.main_sld.value()
                                ].label_img = label_img
                else:
                    self.frames[self.visualize.main_sld.value()
                                ].label_img += label_img

                self.instances_setting = InstanceSettings(self.my_colors,
                                                          self.frames[self.visualize.main_sld.value(
                                                          )].raw_img,
                                                          self.frames[self.visualize.main_sld.value(
                                                          )].label_max,
                                                          self.frames[self.visualize.main_sld.value()].frame_id)
                self.instances_setting.confirm_button.clicked.connect(
                    self.add_instance_main)
                self.instances_setting.show()

    def get_label_and_close(self):
        self.segment_message_box3.close()
        self.get_label_fnc()

    def track(self, name, **kwargs):
        if not len(self.frames) == 0 and self.frames[0].label_img is None:
            self.track_message_box1 = InformationMessageBox(
                "Please do segment first!")
            self.track_message_box1.show()
        elif not len(self.frames) == 0 and self.frames[0].label_img is not None and \
                self.tools.track.tracker_select.currentIndex() == 0:
            self.status.progressbar.setMaximum(self.frames_num)
            QApplication.processEvents()
            self.status.work_info_label.setText("Tracking...")
            QApplication.processEvents()
            tracker = get_tracker(name=name, **kwargs)
            QApplication.processEvents()
            self.status.work_info_label.setText("Tracking...")
            QApplication.processEvents()
            self.frames = tracker(self.frames)
            self.get_label_fnc1()
            QApplication.processEvents()
            self.status.work_info_label.setText("")
            QApplication.processEvents()
        elif not len(self.frames) == 0 and self.frames[0].label_img is not None and \
                self.tools.track.tracker_select.currentIndex() == 1:
            pass
        else:
            self.track_message_box2 = InformationMessageBox(
                "Please load images first!")
            self.track_message_box2.show()

    def status_fnc(self):
        QApplication.processEvents()
        self.status.work_info_label.setText("Tracking...")

    def write(self, **kwargs):
        if not len(self.frames) == 0 and self.frames[0].label_img is None:
            self.write_message_box1 = InformationMessageBox(
                "Please do segment first!")
            self.write_message_box1.show()
        elif not len(self.frames) == 0 and self.frames[0].label_img is not None:
            QApplication.processEvents()
            self.status.work_info_label.setText("Exporting result...")
            QApplication.processEvents()
            writer = get_writer(**kwargs)
            QApplication.processEvents()
            self.status.work_info_label.setText("Exporting result...")
            QApplication.processEvents()
            writer(self.frames,
                   output_csv=self.tools.output.csv_checkbox.isChecked(),
                   output_html=self.tools.output.html_checkbox.isChecked(),
                   output_img=self.tools.output.visualization_checkbox.isChecked())
            # self.status.progressbar.setVisible(True)
            QApplication.processEvents()
            self.status.work_info_label.setText("")
            QApplication.processEvents()
            self.status.progressbar.setVisible(False)
            self.tools.update_file_tree(self.project_path)
        else:
            self.write_message_box2 = InformationMessageBox(
                "Please load images first!")
            self.write_message_box2.show()

    def get_label_fnc(self):
        """get instances"""
        self.status.progressbar.setMaximum(self.frames_num)
        self.status.progressbar.setVisible(True)
        self.status.work_info_label.setText("Labeling...")

        t = 1
        for key in self.frames.keys():
            self.status.update_progressbar(t)
            self.frames[key].auto_labling(self.my_colors)
            t = t+1
        self.status.progressbar.setVisible(False)
        self.status.work_info_label.setText("")

        current_frame = self.frames[self.visualize.main_sld.value()]

        self.visualize.main_frame.setImage(current_frame.raw_color_img)
        self.widget_list = []
        self.correction.instances_widget.clear()
        for key in self.frames[self.visualize.main_sld.value()].instances.keys():
            pix = QPixmap(30, 30)
            pix.fill(QColor(current_frame.instances[key].color[0],
                            current_frame.instances[key].color[1],
                            current_frame.instances[key].color[2]))
            contents_show = "Name: " + self.frames[self.visualize.main_sld.value()].instances[key].name + "\n" +\
                            " Centroid: " + \
                str(self.frames[self.visualize.main_sld.value()
                                ].instances[key].centroid)
            item = QListWidgetItem(
                contents_show, self.correction.instances_widget)
            item.setIcon(QIcon(pix))
            item.setSizeHint(QSize(35, 35))
            # item.setSizeHint(Qsize(100, 100))
            self.widget_list.append(
                self.frames[self.visualize.main_sld.value()].instances[key].label_id)
            item.setTextAlignment(Qt.AlignCenter)
            self.correction.instances_widget.addItem(item)
        self.show_flag = 3

    def get_label_fnc1(self):
        """get instances"""
        self.status.progressbar.setMaximum(self.frames_num)
        self.status.progressbar.setVisible(True)
        self.status.work_info_label.setText("Labeling...    ")

        t = 1
        color_map_dict = None
        for key in self.frames.keys():
            self.status.update_progressbar(t)
            self.frames[key].auto_labeling1(self.my_colors, color_map_dict)
            t = t+1
            color_map_dict = self.frames[key].color_map_dict
        self.status.progressbar.setVisible(False)
        self.status.work_info_label.setText("")

        current_frame = self.frames[self.visualize.main_sld.value()]
        self.visualize.main_frame.setImage(current_frame.raw_color_img)
        self.widget_list = []
        self.correction.instances_widget.clear()
        for key in self.frames[self.visualize.main_sld.value()].instances.keys():
            pix = QPixmap(30, 30)
            pix.fill(QColor(current_frame.instances[key].color[0],
                            current_frame.instances[key].color[1],
                            current_frame.instances[key].color[2]))
            contents_show = "Name: " + self.frames[self.visualize.main_sld.value()].instances[key].name + "\n" + \
                            " Centroid: " + \
                str(self.frames[self.visualize.main_sld.value()
                                ].instances[key].centroid)
            item = QListWidgetItem(
                contents_show, self.correction.instances_widget)
            item.setIcon(QIcon(pix))
            item.setSizeHint(QSize(35, 35))
            self.widget_list.append(
                self.frames[self.visualize.main_sld.value()].instances[key].label_id)
            item.setTextAlignment(Qt.AlignCenter)
            self.correction.instances_widget.addItem(item)
        self.show_flag = 3

    def has_chinese(self, path):
        for ch in path:
            if '\u4e00' <= ch <= '\u9fff':
                return True
        return False


def run():
    app = QApplication(sys.argv)
    ex = MainWindow()
    sys.exit(app.exec_())
