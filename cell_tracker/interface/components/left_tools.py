# -*- coding: UTF-8 -*-

import os.path as osp
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from .file_tree import FileTree
from .left_tools_segment import SegmentTools
from .left_tools_output import OutputTools
from .left_tools_track import TrackTools
from .left_tools_annotation import AnnotationTools
from .left_tools_io import InputOutput
from .left_tools_data_loader import DataLoader
from .left_tools_loss import Loss
from .left_tools_optimizer import Optimizer
from .left_tools_run_train import RunTrain
from .left_tools_normalization import NormalizeTools
from .left_tools_weighted_loss import WeightedLoss
from .left_tools_trainer import Trainer
from ..utils import get_icon, left_tools_stylesheet, instance_widget_stylesheet


class LeftTools(QWidget):
    def __init__(self, parent=None, open_path=None):
        super().__init__()
        self.left_tools = QStackedWidget()
        self.left_tools.setStyleSheet("background: #323232;"
                                      "border: 0px;")
        self.left_tools.setMinimumWidth(260)

        self.project_path = "./output/untitled"
        self.open_path = open_path

        self.setup_ui()

    def setup_ui(self):

        self.init_file_tree()
        self.init_algorithms()
        self.init_annotation()
        self.init_network_training()

    def init_file_tree(self):
        self.file_system = QWidget()
        self.file_system_layout = QVBoxLayout(self.file_system)
        self.file_system_layout.setContentsMargins(0, 0, 0, 0)
        self.file_tree_widget = FileTree()
        self.file_system_layout.addWidget(self.file_tree_widget)
        self.left_tools.addWidget(self.file_system)

    def init_algorithms(self):
        self.normlize = NormalizeTools()
        self.segment = SegmentTools()
        self.track = TrackTools()
        self.output = OutputTools()

        self.left_tools_stylesheet = left_tools_stylesheet

        self.out_widget = QWidget()
        self.out_widget.setContentsMargins(0, 0, 0, 0)
        self.out_layout = QVBoxLayout(self.out_widget)
        self.out_layout.setContentsMargins(0, 0, 0, 0)

        self.main_algorithm = QWidget()
        self.main_algorithm.setMinimumSize(240, 1500)
        self.scroll = QScrollArea()
        self.scroll.setStyleSheet(instance_widget_stylesheet)

        self.scroll.setWidget(self.main_algorithm)
        self.scroll.setVerticalScrollBarPolicy(0)
        self.scroll.setHorizontalScrollBarPolicy(0)
        self.main_algorithm.setStyleSheet("background: #323232")

        self.main_algorithm_layout = QVBoxLayout()
        self.main_algorithm_layout.setAlignment(Qt.AlignTop)
        self.main_algorithm_layout.setContentsMargins(0, 0, 0, 0)
        self.main_algorithm_layout.setSpacing(1)

        self.normlize_button = QPushButton()
        self.normlize_button.setStyleSheet("background: #454545;"
                                           "font-family: Verdana;"
                                           "font-size: 14px;"
                                           "border: 0px;"
                                           "text-align:left;")
        self.normlize_button.setFixedHeight(25)
        self.normlize_button.setText("Normalization")
        self.normlize_button.clicked.connect(self.normlize_button_fnc)
        self.normlize_button.setIcon(QIcon(get_icon("Arrow_right.png")))

        self.segment_button = QPushButton()
        self.segment_button.setStyleSheet("background: #454545;"
                                          "font-family: Verdana;"
                                          "font-size: 14px;"
                                          "border: 0px;"
                                          "text-align:left;")
        self.segment_button.setFixedHeight(25)
        self.segment_button.setText("Segmentation")
        self.segment_button.clicked.connect(self.segment_button_fnc)
        self.segment_button.setIcon(QIcon(get_icon("Arrow_right.png")))

        self.track_button = QPushButton()
        self.track_button.setStyleSheet("background: #454545;"
                                        "font-family: Verdana;"
                                        "font-size: 14px;"
                                        "border: 0px;"
                                        "text-align:left;")
        self.track_button.setFixedHeight(25)
        self.track_button.setText("Track")
        self.track_button.clicked.connect(self.track_button_fnc)
        self.track_button.setIcon(QIcon(get_icon("Arrow_right.png")))

        self.output_button = QPushButton()
        self.output_button.setStyleSheet("background: #454545;"
                                         "font-family: Verdana;"
                                         "font-size: 14px;"
                                         "border: 0px;"
                                         "text-align:left;")
        self.output_button.setFixedHeight(25)
        self.output_button.setText("Output")
        self.output_button.clicked.connect(self.output_button_fnc)
        self.output_button.setIcon(QIcon(get_icon("Arrow_right.png")))

        self.main_algorithm_layout.addWidget(self.normlize_button)
        self.main_algorithm_layout.addWidget(self.normlize.normalize_tools)
        self.normlize.normalize_tools.setVisible(False)
        self.main_algorithm_layout.addWidget(self.segment_button)
        self.main_algorithm_layout.addWidget(self.segment.segment_tools)
        self.segment.segment_tools.setVisible(False)
        self.main_algorithm_layout.addWidget(self.track_button)
        self.main_algorithm_layout.addWidget(self.track.track_tools)
        self.track.track_tools.setVisible(False)
        self.main_algorithm_layout.addWidget(self.output_button)
        self.main_algorithm_layout.addWidget(self.output.output_tools)
        self.output.output_tools.setVisible(False)

        self.main_algorithm.setLayout(self.main_algorithm_layout)
        self.out_layout.addWidget(self.scroll)
        self.left_tools.addWidget(self.out_widget)

    def init_annotation(self):
        self.annotation = AnnotationTools()
        self.left_annotation = self.annotation.annotation_tools

        self.left_tools.addWidget(self.left_annotation)

    def init_network_training(self):
        self.io = InputOutput()
        self.data_loader = DataLoader()
        self.loss = Loss()
        self.weighted_loss = WeightedLoss()
        self.optimizer = Optimizer()
        self.run_train = RunTrain()
        self.trainer = Trainer()

        self.out_widget1 = QWidget()
        self.out_widget1.setContentsMargins(0, 0, 0, 0)
        self.out_layout1 = QVBoxLayout(self.out_widget1)
        self.out_layout1.setContentsMargins(0, 0, 0, 0)

        self.main_training = QWidget()
        self.main_training.setMinimumSize(240, 1500)
        self.scroll1 = QScrollArea()
        self.scroll1.setStyleSheet(instance_widget_stylesheet)

        self.scroll1.setWidget(self.main_training)
        self.scroll1.setVerticalScrollBarPolicy(0)
        self.scroll1.setHorizontalScrollBarPolicy(0)
        self.main_training.setStyleSheet("background: #323232")

        self.main_training_layout = QVBoxLayout()
        self.main_training_layout.setAlignment(Qt.AlignTop)
        self.main_training_layout.setContentsMargins(0, 0, 0, 0)
        self.main_training_layout.setSpacing(1)

        self.input_output_button = QPushButton()
        self.input_output_button.setStyleSheet("background: #454545;"
                                               "font-family: Verdana;"
                                               "font-size: 14px;"
                                               "border: 0px;"
                                               "text-align:left;")
        self.input_output_button.setFixedHeight(25)
        self.input_output_button.setText("IO")
        self.input_output_button.clicked.connect(self.input_output_button_fnc)
        self.input_output_button.setIcon(QIcon(get_icon("Arrow_right.png")))

        self.data_loader_button = QPushButton()
        self.data_loader_button.setStyleSheet("background: #454545;"
                                              "font-family: Verdana;"
                                              "font-size: 14px;"
                                              "border: 0px;"
                                              "text-align:left;")
        self.data_loader_button.setFixedHeight(25)
        self.data_loader_button.setText("DataLoader")
        self.data_loader_button.clicked.connect(self.data_loader_button_fnc)
        self.data_loader_button.setIcon(QIcon(get_icon("Arrow_right.png")))

        self.loss_button = QPushButton()
        self.loss_button.setStyleSheet("background: #454545;"
                                       "font-family: Verdana;"
                                       "font-size: 14px;"
                                       "border: 0px;"
                                       "text-align:left;")
        self.loss_button.setFixedHeight(25)
        self.loss_button.setText("Loss")
        self.loss_button.clicked.connect(self.loss_button_fnc)
        self.loss_button.setIcon(QIcon(get_icon("Arrow_right.png")))

        self.weighted_loss_button = QPushButton()
        self.weighted_loss_button.setStyleSheet("background: #454545;"
                                                "font-family: Verdana;"
                                                "font-size: 14px;"
                                                "border: 0px;"
                                                "text-align:left;")
        self.weighted_loss_button.setFixedHeight(25)
        self.weighted_loss_button.setText("Loss Weighted")
        self.weighted_loss_button.clicked.connect(
            self.weighted_loss_button_fnc)
        self.weighted_loss_button.setIcon(QIcon(get_icon("Arrow_right.png")))

        self.optimizer_button = QPushButton()
        self.optimizer_button.setStyleSheet("background: #454545;"
                                            "font-family: Verdana;"
                                            "font-size: 14px;"
                                            "border: 0px;"
                                            "text-align:left;")
        self.optimizer_button.setFixedHeight(25)
        self.optimizer_button.setText("Optimizer")
        self.optimizer_button.clicked.connect(self.optimizer_button_fnc)
        self.optimizer_button.setIcon(QIcon(get_icon("Arrow_right.png")))

        self.trainer_button = QPushButton()
        self.trainer_button.setStyleSheet("background: #454545;"
                                          "font-family: Verdana;"
                                          "font-size: 14px;"
                                          "border: 0px;"
                                          "text-align:left;")
        self.trainer_button.setFixedHeight(25)
        self.trainer_button.setText("Trainer")
        self.trainer_button.clicked.connect(self.trainer_button_fnc)
        self.trainer_button.setIcon(QIcon(get_icon("Arrow_right.png")))

        self.run_train_button = QPushButton()
        self.run_train_button.setStyleSheet("background: #454545;"
                                            "font-family: Verdana;"
                                            "font-size: 14px;"
                                            "border: 0px;"
                                            "text-align:left;")
        self.run_train_button.setFixedHeight(25)
        self.run_train_button.setText("Run")
        self.run_train_button.clicked.connect(self.run_train_button_fnc)
        self.run_train_button.setIcon(QIcon(get_icon("Arrow_right.png")))

        self.main_training_layout.addWidget(self.input_output_button)
        self.main_training_layout.addWidget(self.io.input_output)
        self.io.input_output.setVisible(False)
        self.main_training_layout.addWidget(self.data_loader_button)
        self.main_training_layout.addWidget(self.data_loader.data_loader)
        self.data_loader.data_loader.setVisible(False)
        self.main_training_layout.addWidget(self.loss_button)
        self.main_training_layout.addWidget(self.loss.loss)
        self.loss.loss.setVisible(False)
        self.main_training_layout.addWidget(self.weighted_loss_button)
        self.main_training_layout.addWidget(self.weighted_loss.weighted_loss)
        self.weighted_loss.weighted_loss.setVisible(False)
        self.main_training_layout.addWidget(self.optimizer_button)
        self.main_training_layout.addWidget(self.optimizer.optimizer)
        self.optimizer.optimizer.setVisible(False)
        self.main_training_layout.addWidget(self.trainer_button)
        self.main_training_layout.addWidget(self.trainer.trainer)
        self.trainer.trainer.setVisible(False)
        self.main_training_layout.addWidget(self.run_train_button)
        self.main_training_layout.addWidget(self.run_train.run_train)
        self.run_train.run_train.setVisible(False)

        self.main_training.setLayout(self.main_training_layout)
        self.out_layout1.addWidget(self.scroll1)
        self.left_tools.addWidget(self.out_widget1)

    def update_file_tree(self, project_path):
        self.project_path = project_path
        self.file_tree_widget.close()
        self.file_system_layout.removeWidget(self.file_tree_widget)
        self.file_tree_widget = FileTree(self.project_path, view_flag=1)

        self.file_system_layout.addWidget(self.file_tree_widget)
        self.file_system.setLayout(self.file_system_layout)
        QApplication.processEvents()

    def normlize_button_fnc(self):
        if self.normlize.normalize_tools.isVisible():
            self.normlize.normalize_tools.setVisible(False)
            self.normlize_button.setIcon(QIcon(get_icon("Arrow_right.png")))
            self.normlize_button.setStyleSheet("background: #454545;"
                                               "font-family: Verdana;"
                                               "font-size: 14px;"
                                               "border: 0px;"
                                               "text-align:left;"
                                               "color: #000000")
        else:
            self.normlize.normalize_tools.setVisible(True)
            self.normlize_button.setIcon(QIcon(get_icon("Arrow_down.png")))
            self.normlize_button.setStyleSheet("background: #454545;"
                                               "font-family: Verdana;"
                                               "font-size: 14px;"
                                               "border: 0px;"
                                               "text-align:left;"
                                               "color: #FFFFFF")

    def segment_button_fnc(self):
        if self.segment.segment_tools.isVisible():
            self.segment.segment_tools.setVisible(False)
            self.segment_button.setIcon(QIcon(get_icon("Arrow_right.png")))
            self.segment_button.setStyleSheet("background: #454545;"
                                              "font-family: Verdana;"
                                              "font-size: 14px;"
                                              "border: 0px;"
                                              "text-align:left;"
                                              "color: #000000")
        else:
            self.segment.segment_tools.setVisible(True)
            self.segment_button.setIcon(QIcon(get_icon("Arrow_down.png")))
            self.segment_button.setStyleSheet("background: #454545;"
                                              "font-family: Verdana;"
                                              "font-size: 14px;"
                                              "border: 0px;"
                                              "text-align:left;"
                                              "color: #FFFFFF")

    def track_button_fnc(self):
        if self.track.track_tools.isVisible():
            self.track.track_tools.setVisible(False)
            self.track_button.setIcon(QIcon(get_icon("Arrow_right.png")))
            self.track_button.setStyleSheet("background: #454545;"
                                            "font-size: 14px;"
                                            "font-family: Verdana;"
                                            "border: 0px;"
                                            "text-align:left;"
                                            "color: #000000")
        else:
            self.track.track_tools.setVisible(True)
            self.track_button.setIcon(QIcon(get_icon("Arrow_down.png")))
            self.track_button.setStyleSheet("background: #454545;"
                                            "font-size: 14px;"
                                            "font-family: Verdana;"
                                            "border: 0px;"
                                            "text-align:left;"
                                            "color: #FFFFFF")

    def output_button_fnc(self):
        if self.output.output_tools.isVisible():
            self.output.output_tools.setVisible(False)
            self.output_button.setIcon(QIcon(get_icon("Arrow_right.png")))
            self.output_button.setStyleSheet("background: #454545;"
                                             "font-size: 14px;"
                                             "font-family: Verdana;"
                                             "border: 0px;"
                                             "text-align:left;"
                                             "color: #000000")
        else:
            self.output.output_tools.setVisible(True)
            self.output_button.setIcon(QIcon(get_icon("Arrow_down.png")))
            self.output_button.setStyleSheet("background: #454545;"
                                             "font-family: Verdana;"
                                             "font-size: 14px;"
                                             "border: 0px;"
                                             "text-align:left;"
                                             "color: #FFFFFF")

    def input_output_button_fnc(self):
        if self.io.input_output.isVisible():
            self.io.input_output.setVisible(False)
            self.input_output_button.setIcon(
                QIcon(get_icon("Arrow_right.png")))
            self.input_output_button.setStyleSheet("background: #454545;"
                                                   "font-family: Verdana;"
                                                   "font-size: 14px;"
                                                   "border: 0px;"
                                                   "text-align:left;"
                                                   "color: #000000")
        else:
            self.io.input_output.setVisible(True)
            self.input_output_button.setIcon(QIcon(get_icon("Arrow_down.png")))
            self.input_output_button.setStyleSheet("background: #454545;"
                                                   "font-family: Verdana;"
                                                   "font-size: 14px;"
                                                   "border: 0px;"
                                                   "text-align:left;"
                                                   "color: #FFFFFF")

    def data_loader_button_fnc(self):
        if self.data_loader.data_loader.isVisible():
            self.data_loader.data_loader.setVisible(False)
            self.data_loader_button.setIcon(QIcon(get_icon("Arrow_right.png")))
            self.data_loader_button.setStyleSheet("background: #454545;"
                                                  "font-family: Verdana;"
                                                  "font-size: 14px;"
                                                  "border: 0px;"
                                                  "text-align:left;"
                                                  "color: #000000")
        else:
            self.data_loader.data_loader.setVisible(True)
            self.data_loader_button.setIcon(QIcon(get_icon("Arrow_down.png")))
            self.data_loader_button.setStyleSheet("background: #454545;"
                                                  "font-family: Verdana;"
                                                  "font-size: 14px;"
                                                  "border: 0px;"
                                                  "text-align:left;"
                                                  "color: #FFFFFF")

    def loss_button_fnc(self):
        if self.loss.loss.isVisible():
            self.loss.loss.setVisible(False)
            self.loss_button.setIcon(QIcon(get_icon("Arrow_right.png")))
            self.loss_button.setStyleSheet("background: #454545;"
                                           "font-family: Verdana;"
                                           "font-size: 14px;"
                                           "border: 0px;"
                                           "text-align:left;"
                                           "color: #000000")
        else:
            self.loss.loss.setVisible(True)
            self.loss_button.setIcon(QIcon(get_icon("Arrow_down.png")))
            self.loss_button.setStyleSheet("background: #454545;"
                                           "font-family: Verdana;"
                                           "font-size: 14px;"
                                           "border: 0px;"
                                           "text-align:left;"
                                           "color: #FFFFFF")

    def weighted_loss_button_fnc(self):
        if self.weighted_loss.weighted_loss.isVisible():
            self.weighted_loss.weighted_loss.setVisible(False)
            self.weighted_loss_button.setIcon(
                QIcon(get_icon("Arrow_right.png")))
            self.weighted_loss_button.setStyleSheet("background: #454545;"
                                                    "font-family: Verdana;"
                                                    "font-size: 14px;"
                                                    "border: 0px;"
                                                    "text-align:left;"
                                                    "color: #000000")
        else:
            self.weighted_loss.weighted_loss.setVisible(True)
            self.weighted_loss_button.setIcon(
                QIcon(get_icon("Arrow_down.png")))
            self.weighted_loss_button.setStyleSheet("background: #454545;"
                                                    "font-family: Verdana;"
                                                    "font-size: 14px;"
                                                    "border: 0px;"
                                                    "text-align:left;"
                                                    "color: #FFFFFF")

    def optimizer_button_fnc(self):
        if self.optimizer.optimizer.isVisible():
            self.optimizer.optimizer.setVisible(False)
            self.optimizer_button.setIcon(QIcon(get_icon("Arrow_right.png")))
            self.optimizer_button.setStyleSheet("background: #454545;"
                                                "font-family: Verdana;"
                                                "font-size: 14px;"
                                                "border: 0px;"
                                                "text-align:left;"
                                                "color: #000000")
        else:
            self.optimizer.optimizer.setVisible(True)
            self.optimizer_button.setIcon(QIcon(get_icon("Arrow_down.png")))
            self.optimizer_button.setStyleSheet("background: #454545;"
                                                "font-family: Verdana;"
                                                "font-size: 14px;"
                                                "border: 0px;"
                                                "text-align:left;"
                                                "color: #FFFFFF")

    def run_train_button_fnc(self):
        if self.run_train.run_train.isVisible():
            self.run_train.run_train.setVisible(False)
            self.run_train_button.setIcon(QIcon(get_icon("Arrow_right.png")))
            self.run_train_button.setStyleSheet("background: #454545;"
                                                "font-family: Verdana;"
                                                "font-size: 14px;"
                                                "border: 0px;"
                                                "text-align:left;"
                                                "color: #000000")
        else:
            self.run_train.run_train.setVisible(True)
            self.run_train_button.setIcon(QIcon(get_icon("Arrow_down.png")))
            self.run_train_button.setStyleSheet("background: #454545;"
                                                "font-family: Verdana;"
                                                "font-size: 14px;"
                                                "border: 0px;"
                                                "text-align:left;"
                                                "color: #FFFFFF")

    def trainer_button_fnc(self):
        if self.trainer.trainer.isVisible():
            self.trainer.trainer.setVisible(False)
            self.trainer_button.setIcon(QIcon(get_icon("Arrow_right.png")))
            self.trainer_button.setStyleSheet("background: #454545;"
                                              "font-family: Verdana;"
                                              "font-size: 14px;"
                                              "border: 0px;"
                                              "text-align:left;"
                                              "color: #000000")
        else:
            self.trainer.trainer.setVisible(True)
            self.trainer_button.setIcon(QIcon(get_icon("Arrow_down.png")))
            self.trainer_button.setStyleSheet("background: #454545;"
                                              "font-family: Verdana;"
                                              "font-size: 14px;"
                                              "border: 0px;"
                                              "text-align:left;"
                                              "color: #FFFFFF")

