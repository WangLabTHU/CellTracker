# -*- coding: UTF-8 -*-

import os.path as osp
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from ..utils import get_icon


class OutputTools(QWidget):

    def __init__(self):
        super().__init__()
        self.output_tools = QWidget()
        self.output_tools.setStyleSheet("background: #323232;")

        self.setup_ui()

    def setup_ui(self):

        output_layout = QVBoxLayout()
        output_visualization_layout = QVBoxLayout()
        output_visualization_layout1 = QVBoxLayout()
        output_visualization_layout11 = QHBoxLayout()
        output_visualization_layout12 = QHBoxLayout()
        output_csv_layout = QVBoxLayout()
        output_html_layout = QVBoxLayout()
        output_button_layout = QHBoxLayout()

        visualization_checkbox = QCheckBox()
        visualization_checkbox.setText("Visualization")
        visualization_checkbox.setStyleSheet("font-family: Verdana;"
                                             "font-size: 15px;"
                                             "color: white;")

        visualization_color_checkbox = QCheckBox()
        visualization_color_checkbox.setText("Color")
        visualization_color_checkbox.setStyleSheet("font-family: Verdana;"
                                                   "font-size: 12px;"
                                                   "color: white;")

        visualization_box_checkbox = QCheckBox()
        visualization_box_checkbox.setText("Bounding box")
        visualization_box_checkbox.setStyleSheet("font-family: Verdana;"
                                                 "font-size: 12px;"
                                                 "color: white;")

        visualization_edge_checkbox = QCheckBox()
        visualization_edge_checkbox.setText("Edge")
        visualization_edge_checkbox.setStyleSheet("font-family: Verdana;"
                                                  "font-size: 12px;"
                                                  "color: white;")

        visualization_trajectory_checkbox = QCheckBox()
        visualization_trajectory_checkbox.setText("Trajectory")
        visualization_trajectory_checkbox.setStyleSheet("font-family: Verdana;"
                                                        "font-size: 12px;"
                                                        "color: white;")

        visualization_label_checkbox = QCheckBox()
        visualization_label_checkbox.setText("Label")
        visualization_label_checkbox.setStyleSheet("font-family: Verdana;"
                                                   "font-size: 12px;"
                                                   "color: white;")

        visualization_trajectory_length_label = QLabel()
        visualization_trajectory_length_label.setText("Trajectory length")

        visualization_trajectory_length_left = QPushButton()
        visualization_trajectory_length_left.setIcon(
            QIcon((get_icon("left.png"))))
        visualization_trajectory_length_left.setIconSize(QSize(15, 15))
        visualization_trajectory_length_left.setFixedSize(QSize(15, 15))
        visualization_trajectory_length_left.setFlat(True)
        visualization_trajectory_length_left.setStyleSheet("border: 0px")
        visualization_trajectory_length_left.clicked.connect(self.length_left)

        visualization_trajectory_length = QLineEdit()
        visualization_trajectory_length.setFixedSize(QSize(20, 20))
        visualization_trajectory_length.setAlignment(Qt.AlignCenter)
        visualization_trajectory_length.setText(str(3))
        visualization_trajectory_length.setValidator(QIntValidator())
        visualization_trajectory_length.setStyleSheet("background: #545454;"
                                                      "border: 0px;"
                                                      "border-radius: 3px;"
                                                      "color: white;")

        visualization_trajectory_length_right = QPushButton()
        visualization_trajectory_length_right.setIcon(
            QIcon((get_icon("right.png"))))
        visualization_trajectory_length_right.setIconSize(QSize(15, 15))
        visualization_trajectory_length_right.setFixedSize(QSize(15, 15))
        visualization_trajectory_length_right.setFlat(True)
        visualization_trajectory_length_right.setStyleSheet("border: 0px")
        visualization_trajectory_length_right.clicked.connect(
            self.length_right)

        visualization_video_fps_left_label = QLabel()
        visualization_video_fps_left_label.setText("Video FPS")

        visualization_video_fps_left = QPushButton()
        visualization_video_fps_left.setIcon(QIcon((get_icon("left.png"))))
        visualization_video_fps_left.setIconSize(QSize(15, 15))
        visualization_video_fps_left.setFixedSize(QSize(15, 15))
        visualization_video_fps_left.setFlat(True)
        visualization_video_fps_left.setStyleSheet("border: 0px")
        visualization_video_fps_left.clicked.connect(self.fps_left)

        visualization_video_fps = QLineEdit()
        visualization_video_fps.setFixedSize(QSize(20, 20))
        visualization_video_fps.setAlignment(Qt.AlignCenter)
        visualization_video_fps.setText(str(3))
        visualization_video_fps.setValidator(QIntValidator())
        visualization_video_fps.setStyleSheet("background: #545454;"
                                              "border: 0px;"
                                              "border-radius: 3px;"
                                              "color: white;")

        visualization_video_fps_right = QPushButton()
        visualization_video_fps_right.setIcon(QIcon((get_icon("right.png"))))
        visualization_video_fps_right.setIconSize(QSize(15, 15))
        visualization_video_fps_right.setFixedSize(QSize(15, 15))
        visualization_video_fps_right.setFlat(True)
        visualization_video_fps_right.setStyleSheet("border: 0px")
        visualization_video_fps_right.clicked.connect(self.fps_right)

        csv_checkbox = QCheckBox()
        csv_checkbox.setText("CSV")
        csv_checkbox.setStyleSheet("font-family: Verdana;"
                                   "font-size: 15px;"
                                   "color: white;")

        html_checkbox = QCheckBox()
        html_checkbox.setText("HTML")
        html_checkbox.setStyleSheet("font-family: Verdana;"
                                    "font-size: 15px;"
                                    "color: white;")

        output_button = QPushButton()
        output_button.setText("Output")
        output_button.setFixedSize(60, 20)
        output_button.setStyleSheet("background: #454545;"
                                    "color: white;"
                                    "border-radius: 5px;"
                                    "font-family: Verdana;")

        output_visualization_layout1.addWidget(visualization_color_checkbox)
        output_visualization_layout1.addWidget(visualization_box_checkbox)
        output_visualization_layout1.addWidget(visualization_edge_checkbox)
        output_visualization_layout1.addWidget(
            visualization_trajectory_checkbox)
        output_visualization_layout1.addWidget(visualization_label_checkbox)
        output_visualization_layout11.addWidget(
            visualization_trajectory_length_label)
        output_visualization_layout11.addWidget(
            visualization_trajectory_length_left)
        output_visualization_layout11.addWidget(
            visualization_trajectory_length)
        output_visualization_layout11.addWidget(
            visualization_trajectory_length_right)
        output_visualization_layout1.addLayout(output_visualization_layout11)
        output_visualization_layout12.addWidget(
            visualization_video_fps_left_label)
        output_visualization_layout12.addWidget(visualization_video_fps_left)
        output_visualization_layout12.addWidget(visualization_video_fps)
        output_visualization_layout12.addWidget(visualization_video_fps_right)
        output_visualization_layout1.addLayout(output_visualization_layout12)
        output_visualization_layout1.setContentsMargins(20, 0, 0, 0)

        output_visualization_layout.addWidget(visualization_checkbox)
        output_visualization_layout.addLayout(output_visualization_layout1)
        output_visualization_layout.setAlignment(Qt.AlignLeft)
        output_visualization_layout.setSpacing(3)

        output_csv_layout.addWidget(csv_checkbox)
        output_csv_layout.setAlignment(Qt.AlignLeft)
        output_html_layout.addWidget(html_checkbox)
        output_html_layout.setAlignment(Qt.AlignLeft)

        output_button_layout.addWidget(output_button)
        output_button_layout.setAlignment(Qt.AlignRight)

        output_layout.addLayout(output_visualization_layout)
        output_layout.addLayout(output_csv_layout)
        output_layout.addLayout(output_html_layout)
        output_layout.addLayout(output_button_layout)

        self.output_tools.setLayout(output_layout)

        self.output_button = output_button
        self.visualization_checkbox = visualization_checkbox
        self.visualization_color_checkbox = visualization_color_checkbox
        self.visualization_box_checkbox = visualization_box_checkbox
        self.visualization_edge_checkbox = visualization_edge_checkbox
        self.visualization_trajectory_checkbox = visualization_trajectory_checkbox
        self.visualization_label_checkbox = visualization_label_checkbox
        self.visualization_trajectory_length_left = visualization_trajectory_length_left
        self.visualization_trajectory_length = visualization_trajectory_length
        self.visualization_trajectory_length_right = visualization_trajectory_length_right
        self.visualization_video_fps_left = visualization_video_fps_left
        self.visualization_video_fps = visualization_video_fps
        self.visualization_video_fps_right = visualization_video_fps_right
        self.csv_checkbox = csv_checkbox
        self.html_checkbox = html_checkbox

    def length_left(self):
        current_length = int(self.visualization_trajectory_length.text())
        self.visualization_trajectory_length.setText(str(current_length - 1))

    def length_right(self):
        current_length = int(self.visualization_trajectory_length.text())
        self.visualization_trajectory_length.setText(str(current_length + 1))

    def fps_left(self):
        current_fps = int(self.visualization_video_fps.text())
        self.visualization_video_fps.setText(str(current_fps - 1))

    def fps_right(self):
        current_fps = int(self.visualization_video_fps.text())
        self.visualization_video_fps.setText(str(current_fps + 1))
