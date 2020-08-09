# -*- coding: UTF-8 -*-

import os.path as osp
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from ..utils import get_icon, slide_stylesheet, segment_tools_stylesheet


class SegmentTools(QWidget):

    def __init__(self):
        super().__init__()

        self.segment_tools_stylesheet = segment_tools_stylesheet
        self.sld_stylesheet = slide_stylesheet
        self.segment_tools = QWidget()
        self.segment_tools.setContentsMargins(20, 0, 0, 0)
        self.segment_tools.setStyleSheet("background: #323232")

        self.qtooltips_stylesheet = """
        QPushButton {border:0px;}
        QToolTip
            {
                font-family: Verdana;
                color: black;
                background-color: rgb(255, 255, 255);
            }
        """

        self.setup_ui()

    def setup_ui(self):
        self.init_seg1()
        self.init_seg2()
        self.init_seg3()
        self.init_seg4()
        self.init_user_defined()

        self.segment_tools_layout = QVBoxLayout()
        self.segment_tools_layout.setAlignment(Qt.AlignTop)
        self.segment_tools_layout.setContentsMargins(0, 0, 0, 0)
        self.segment_tools_layout.setSpacing(1)

        self.segment_algorithm1_tool_button = QPushButton()
        self.segment_algorithm1_tool_button.setStyleSheet("background: #454545;"
                                                          "font-family: Verdana;"
                                                          "border: 0px;"
                                                          "text-align:left;")
        self.segment_algorithm1_tool_button.setFixedHeight(20)
        self.segment_algorithm1_tool_button.setText("Threshold")
        self.segment_algorithm1_tool_button.clicked.connect(
            self.segment_algorithm1_tool_button_fnc)
        self.segment_algorithm1_tool_button.setIcon(
            QIcon(get_icon("Arrow_right.png")))

        self.segment_algorithm2_tool_button = QPushButton()
        self.segment_algorithm2_tool_button.setStyleSheet("background: #454545;"
                                                          "font-family: Verdana;"
                                                          "border: 0px;"
                                                          "text-align:left;")
        self.segment_algorithm2_tool_button.setFixedHeight(20)
        self.segment_algorithm2_tool_button.setText("U-net")
        self.segment_algorithm2_tool_button.clicked.connect(
            self.segment_algorithm2_tool_button_fnc)
        self.segment_algorithm2_tool_button.setIcon(
            QIcon(get_icon("Arrow_right.png")))

        self.segment_algorithm3_tool_button = QPushButton()
        self.segment_algorithm3_tool_button.setStyleSheet("background: #454545;"
                                                          "font-family: Verdana;"
                                                          "border: 0px;"
                                                          "text-align:left;")
        self.segment_algorithm3_tool_button.setFixedHeight(20)
        self.segment_algorithm3_tool_button.setText("WaterShed")
        self.segment_algorithm3_tool_button.clicked.connect(
            self.segment_algorithm3_tool_button_fnc)
        self.segment_algorithm3_tool_button.setIcon(
            QIcon(get_icon("Arrow_right.png")))

        self.segment_algorithm4_tool_button = QPushButton()
        self.segment_algorithm4_tool_button.setStyleSheet("background: #454545;"
                                                          "font-family: Verdana;"
                                                          "border: 0px;"
                                                          "text-align:left;")
        self.segment_algorithm4_tool_button.setFixedHeight(20)
        self.segment_algorithm4_tool_button.setText("CrabCut")
        self.segment_algorithm4_tool_button.clicked.connect(
            self.segment_algorithm4_tool_button_fnc)
        self.segment_algorithm4_tool_button.setIcon(
            QIcon(get_icon("Arrow_right.png")))

        self.segment_algorithm5_tool_button = QPushButton()
        self.segment_algorithm5_tool_button.setStyleSheet("background: #454545;"
                                                          "font-family: Verdana;"
                                                          "border: 0px;"
                                                          "text-align:left;")
        self.segment_algorithm5_tool_button.setFixedHeight(20)
        self.segment_algorithm5_tool_button.setText("User-defined")
        self.segment_algorithm5_tool_button.clicked.connect(
            self.segment_algorithm5_tool_button_fnc)
        self.segment_algorithm5_tool_button.setIcon(
            QIcon(get_icon("Arrow_right.png")))

        self.segment_tools_layout.addWidget(
            self.segment_algorithm1_tool_button)
        self.segment_tools_layout.addWidget(self.segment_algorithm1)
        self.segment_algorithm1.setVisible(False)
        self.segment_tools_layout.addWidget(
            self.segment_algorithm2_tool_button)
        self.segment_tools_layout.addWidget(self.segment_algorithm2)
        self.segment_algorithm2.setVisible(False)
        self.segment_tools_layout.addWidget(
            self.segment_algorithm3_tool_button)
        self.segment_tools_layout.addWidget(self.segment_algorithm3)
        self.segment_algorithm3.setVisible(False)
        self.segment_tools_layout.addWidget(
            self.segment_algorithm4_tool_button)
        self.segment_tools_layout.addWidget(self.segment_algorithm4)
        self.segment_algorithm4.setVisible(False)
        self.segment_tools_layout.addWidget(
            self.segment_algorithm5_tool_button)
        self.segment_tools_layout.addWidget(self.segment_algorithm5)
        self.segment_algorithm5.setVisible(False)

        self.segment_tools.setLayout(self.segment_tools_layout)

    def init_seg1(self):
        segment_algorithm1 = QWidget()
        segment_algorithm1.setStyleSheet("border: 0px;"
                                         "background: #323232;")

        segment_algorithm1_layout = QVBoxLayout(segment_algorithm1)
        segment_algorithm1_layout1 = QHBoxLayout()
        segment_algorithm1_layout2 = QHBoxLayout()
        segment_algorithm1_layout3 = QHBoxLayout()

        thresh_sld1 = QSlider(Qt.Horizontal)
        thresh_sld1.setMinimum(0)
        thresh_sld1.setMaximum(255)
        thresh_sld1.setValue(129)
        thresh_sld1.setStyleSheet(self.sld_stylesheet)
        thresh_sld1.valueChanged.connect(self.sld2text1)

        thresh_label1 = QLabel()
        thresh_label1.setText("Threshold(0~255)")
        thresh_label1.setAlignment(Qt.AlignCenter)
        thresh_label1.setStyleSheet("font-family: Verdana;"
                                    "color: white;")

        thresh_textline1 = QLineEdit()
        thresh_textline1.setAlignment(Qt.AlignCenter)
        thresh_textline1.setFixedSize(50, 15)
        thresh_textline1.setValidator(QIntValidator())
        thresh_textline1.setText("129")
        thresh_textline1.setStyleSheet("background: #454545;"
                                       "border: 0px;"
                                       "color: white;"
                                       "border-radius: 5px;"
                                       "font-family: Verdana;")
        thresh_textline1.textEdited.connect(self.text2sld1)

        thresh_min_size_label = QLabel()
        thresh_min_size_label.setText("Minimal size:")
        thresh_min_size_label.setAlignment(Qt.AlignLeft)
        thresh_min_size_label.setStyleSheet("font-family: Verdana;"
                                            "color: white;")

        thresh_min_size_editor = QLineEdit()
        thresh_min_size_editor.setFixedSize(QSize(50, 20))
        thresh_min_size_editor.setAlignment(Qt.AlignCenter)
        thresh_min_size_editor.setText(str(0))
        thresh_min_size_editor.setValidator(QIntValidator())
        thresh_min_size_editor.setStyleSheet("background: #545454;"
                                             "border: 0px;"
                                             "border-radius: 3px;"
                                             "color: white;")

        thresh_min_size_left_button = QPushButton()
        thresh_min_size_left_button.setIcon(QIcon((get_icon("left.png"))))
        thresh_min_size_left_button.setIconSize(QSize(15, 15))
        thresh_min_size_left_button.setFixedSize(QSize(15, 15))
        thresh_min_size_left_button.setFlat(True)
        thresh_min_size_left_button.setStyleSheet(self.qtooltips_stylesheet)
        thresh_min_size_left_button.clicked.connect(self.min_size_left_fnc1)

        thresh_min_size_right_button = QPushButton()
        thresh_min_size_right_button.setIcon(QIcon((get_icon("right.png"))))
        thresh_min_size_right_button.setIconSize(QSize(15, 15))
        thresh_min_size_right_button.setFixedSize(QSize(15, 15))
        thresh_min_size_right_button.setFlat(True)
        thresh_min_size_right_button.setStyleSheet(self.qtooltips_stylesheet)
        thresh_min_size_right_button.clicked.connect(self.min_size_right_fnc1)

        thresh_min_size_layout = QHBoxLayout()
        thresh_min_size_layout.addWidget(thresh_min_size_label)
        thresh_min_size_layout.addWidget(thresh_min_size_left_button)
        thresh_min_size_layout.addWidget(thresh_min_size_editor)
        thresh_min_size_layout.addWidget(thresh_min_size_right_button)

        thresh_segment_button = QPushButton()
        thresh_segment_button.setFixedSize(180, 20)
        thresh_segment_button.setText("Threshold")
        thresh_segment_button.setStyleSheet("background: #454545;"
                                            "color: white;"
                                            "border-radius: 5px;"
                                            "font-family: Verdana;")

        segment_algorithm1_layout1.addWidget(thresh_label1)
        segment_algorithm1_layout1.setAlignment(Qt.AlignLeft)
        segment_algorithm1_layout2.addWidget(thresh_sld1)
        segment_algorithm1_layout2.addWidget(thresh_textline1)
        segment_algorithm1_layout2.setAlignment(Qt.AlignCenter)
        segment_algorithm1_layout3.addWidget(thresh_segment_button)
        segment_algorithm1_layout3.setAlignment(Qt.AlignRight)

        segment_algorithm1_layout.addLayout(segment_algorithm1_layout1)
        segment_algorithm1_layout.addLayout(segment_algorithm1_layout2)
        segment_algorithm1_layout.addLayout(thresh_min_size_layout)
        segment_algorithm1_layout.addLayout(segment_algorithm1_layout3)
        segment_algorithm1_layout.setAlignment(Qt.AlignTop)

        self.segment_algorithm1 = segment_algorithm1
        self.thresh_sld1 = thresh_sld1
        self.thresh_label1 = thresh_label1
        self.thresh_textline1 = thresh_textline1
        self.thresh_segment_button = thresh_segment_button
        self.thresh_min_size_editor = thresh_min_size_editor
        self.thresh_min_size_left_button = thresh_min_size_left_button
        self.thresh_min_size_right_button = thresh_min_size_right_button

    def init_seg2(self):
        segment_algorithm2 = QWidget()
        segment_algorithm2.setStyleSheet("border: 0px;"
                                         "background: #323232;")

        segment_algorithm2_layout = QVBoxLayout(segment_algorithm2)
        segment_algorithm2_layout1 = QHBoxLayout()
        segment_algorithm2_layout2 = QHBoxLayout()
        segment_algorithm2_layout3 = QHBoxLayout()
        segment_algorithm2_layout4 = QHBoxLayout()

        model_select_label = QLabel()
        model_select_label.setText("Model: ")
        model_select_label.setFixedSize(50, 20)
        model_select_label.setStyleSheet("font-family: Verdana;"
                                         "color: white;")

        model_path_label = QLineEdit()
        model_path_label.setText("Select a model")
        model_path_label.setStyleSheet("background: #454545;"
                                       "border: 0px;"
                                       "color: white;"
                                       "border-radius: 5px;"
                                       "font-family: Verdana;")

        model_browse_button = QPushButton()
        model_browse_button.setIcon(QIcon((get_icon("browse.png"))))
        model_browse_button.setIconSize(QSize(15, 15))
        model_browse_button.setFlat(True)
        model_browse_button.setStyleSheet("border: 0px")
        model_browse_button.setFixedSize(20, 20)
        model_browse_button.setStyleSheet("background: #454545;"
                                          "color: white;"
                                          "border-radius: 5px;"
                                          "font-family: Verdana;")

        device_label = QLabel()
        device_label.setText("GPU number:")
        device_label.setStyleSheet("font-family: Verdana;"
                                   "color: white;")

        device_select = QComboBox()
        device_select.setStyleSheet("border: 0px;"
                                    "color: white;"
                                    "font-family: Verdana;"
                                    "background: #353535;")
        device_select.addItem("CPU")
        device_select.addItem("GPU")
        device_select.setCurrentIndex(0)

        device_layout = QHBoxLayout()
        device_layout.addWidget(device_label)
        device_layout.addWidget(device_select)

        scale_img_label = QLabel()
        scale_img_label.setText("Scale image:")
        scale_img_label.setStyleSheet("font-family: Verdana;"
                                      "color: white;")

        scale_img_select = QComboBox()
        scale_img_select.setFixedSize(80, 20)
        scale_img_select.setStyleSheet("border: 0px;"
                                       "color: white;"
                                       "font-family: Verdana;"
                                       "background: #353535;")
        scale_img_select.addItem("4")
        scale_img_select.addItem("2")
        scale_img_select.addItem("1")
        scale_img_select.addItem("0.5")
        scale_img_select.addItem("0.25")
        scale_img_select.addItem("0.125")
        scale_img_select.setCurrentIndex(2)

        scale_img_layout = QHBoxLayout()
        scale_img_layout.addWidget(scale_img_label)
        scale_img_layout.addWidget(scale_img_select)

        thresh_sld2 = QSlider(Qt.Horizontal)
        thresh_sld2.setMinimum(0)
        thresh_sld2.setMaximum(10)
        thresh_sld2.setValue(5)
        thresh_sld2.setStyleSheet(self.sld_stylesheet)
        thresh_sld2.valueChanged.connect(self.sld2text2)

        thresh_label2 = QLabel()
        thresh_label2.setText("Threshold(0~1)")
        thresh_label2.setAlignment(Qt.AlignCenter)
        thresh_label2.setStyleSheet("font-family: Verdana;"
                                    "color: white;")

        thresh_textline2 = QLineEdit()
        thresh_textline2.setAlignment(Qt.AlignCenter)
        thresh_textline2.setFixedSize(50, 15)
        thresh_textline2.setText("0.5")
        thresh_textline2.setStyleSheet("background: #454545;"
                                       "border: 0px;"
                                       "color: white;"
                                       "border-radius: 5px;"
                                       "font-family: Verdana;")
        thresh_textline2.textEdited.connect(self.text2sld2)

        unet_min_size_label = QLabel()
        unet_min_size_label.setText("Minimal size:")
        unet_min_size_label.setAlignment(Qt.AlignLeft)
        unet_min_size_label.setStyleSheet("font-family: Verdana;"
                                          "color: white;")

        unet_min_size_editor = QLineEdit()
        unet_min_size_editor.setFixedSize(QSize(50, 20))
        unet_min_size_editor.setAlignment(Qt.AlignCenter)
        unet_min_size_editor.setText(str(0))
        unet_min_size_editor.setValidator(QIntValidator())
        unet_min_size_editor.setStyleSheet("background: #545454;"
                                           "border: 0px;"
                                           "border-radius: 3px;"
                                           "color: white;")

        unet_min_size_left_button = QPushButton()
        unet_min_size_left_button.setIcon(QIcon((get_icon("left.png"))))
        unet_min_size_left_button.setIconSize(QSize(15, 15))
        unet_min_size_left_button.setFixedSize(QSize(15, 15))
        unet_min_size_left_button.setFlat(True)
        unet_min_size_left_button.setStyleSheet(self.qtooltips_stylesheet)
        unet_min_size_left_button.clicked.connect(self.min_size_left_fnc2)

        unet_min_size_right_button = QPushButton()
        unet_min_size_right_button.setIcon(QIcon((get_icon("right.png"))))
        unet_min_size_right_button.setIconSize(QSize(15, 15))
        unet_min_size_right_button.setFixedSize(QSize(15, 15))
        unet_min_size_right_button.setFlat(True)
        unet_min_size_right_button.setStyleSheet(self.qtooltips_stylesheet)
        unet_min_size_right_button.clicked.connect(self.min_size_right_fnc2)

        unet_min_size_layout = QHBoxLayout()
        unet_min_size_layout.addWidget(unet_min_size_label)
        unet_min_size_layout.addWidget(unet_min_size_left_button)
        unet_min_size_layout.addWidget(unet_min_size_editor)
        unet_min_size_layout.addWidget(unet_min_size_right_button)

        unet_segment_button = QPushButton()
        unet_segment_button.setFixedSize(180, 20)
        unet_segment_button.setText("U-net segment")
        unet_segment_button.setStyleSheet("background: #454545;"
                                          "color: white;"
                                          "border-radius: 5px;"
                                          "font-family: Verdana;")

        segment_algorithm2_layout1.addWidget(model_select_label)
        segment_algorithm2_layout1.addWidget(model_path_label)
        segment_algorithm2_layout1.addWidget(model_browse_button)
        segment_algorithm2_layout1.setSpacing(1)
        segment_algorithm2_layout2.addWidget(thresh_label2)
        segment_algorithm2_layout2.setAlignment(Qt.AlignLeft)
        segment_algorithm2_layout3.addWidget(thresh_sld2)
        segment_algorithm2_layout3.addWidget(thresh_textline2)
        segment_algorithm2_layout3.setAlignment(Qt.AlignCenter)
        segment_algorithm2_layout4.addWidget(unet_segment_button)
        segment_algorithm2_layout4.setAlignment(Qt.AlignRight)

        segment_algorithm2_layout.addLayout(segment_algorithm2_layout1)
        segment_algorithm2_layout.addLayout(device_layout)
        segment_algorithm2_layout.addLayout(scale_img_layout)
        segment_algorithm2_layout.addLayout(segment_algorithm2_layout2)
        segment_algorithm2_layout.addLayout(segment_algorithm2_layout3)
        segment_algorithm2_layout.addLayout(unet_min_size_layout)
        segment_algorithm2_layout.addLayout(segment_algorithm2_layout4)
        segment_algorithm2_layout.setAlignment(Qt.AlignTop)
        segment_algorithm2_layout.setSpacing(5)
        segment_algorithm2_layout.setContentsMargins(5, 5, 5, 5)

        self.segment_algorithm2 = segment_algorithm2
        self.device_select = device_select
        self.model_select_label = model_select_label
        self.model_path_label = model_path_label
        self.model_browse_button = model_browse_button
        self.thresh_label2 = thresh_label2
        self.thresh_sld2 = thresh_sld2
        self.thresh_textline2 = thresh_textline2
        self.unet_segment_button = unet_segment_button
        self.scale_img_select = scale_img_select
        self.unet_min_size_editor = unet_min_size_editor
        self.unet_min_size_left_button = unet_min_size_left_button
        self.unet_min_size_right_button = unet_min_size_right_button

    def init_seg3(self):
        segment_algorithm3 = QWidget()
        segment_algorithm3.setStyleSheet("border: 0px;"
                                         "background: #323232;")

        segment_algorithm3_layout = QVBoxLayout(segment_algorithm3)
        segment_algorithm3_layout1 = QHBoxLayout()
        segment_algorithm3_layout2 = QHBoxLayout()
        segment_algorithm3_layout3 = QHBoxLayout()
        segment_algorithm3_layout4 = QHBoxLayout()
        segment_algorithm3_layout5 = QHBoxLayout()

        noise_sld = QSlider(Qt.Horizontal)
        noise_sld.setMinimum(0)
        noise_sld.setMaximum(20)
        noise_sld.setValue(5)
        noise_sld.setStyleSheet(self.sld_stylesheet)
        noise_sld.valueChanged.connect(self.sld2text31)

        noise_label = QLabel()
        noise_label.setText("Noise Amplitude(0~20)")
        noise_label.setAlignment(Qt.AlignCenter)
        noise_label.setStyleSheet("font-family: Verdana;"
                                  "color: white;")

        noise_textline = QLineEdit()
        noise_textline.setAlignment(Qt.AlignCenter)
        noise_textline.setFixedSize(50, 15)
        noise_textline.setValidator(QIntValidator())
        noise_textline.setText("5")
        noise_textline.setStyleSheet("background: #454545;"
                                     "border: 0px;"
                                     "color: white;"
                                     "border-radius: 5px;"
                                     "font-family: Verdana;")
        noise_textline.textEdited.connect(self.text2sld31)

        dist_thresh_sld = QSlider(Qt.Horizontal)
        dist_thresh_sld.setMinimum(0)
        dist_thresh_sld.setMaximum(20)
        dist_thresh_sld.setValue(5)
        dist_thresh_sld.setStyleSheet(self.sld_stylesheet)
        dist_thresh_sld.valueChanged.connect(self.sld2text32)

        dist_thresh_label = QLabel()
        dist_thresh_label.setText("Dist thresh(0~1)")
        dist_thresh_label.setAlignment(Qt.AlignCenter)
        dist_thresh_label.setStyleSheet("font-family: Verdana;"
                                        "color: white;")

        dist_thresh_textline = QLineEdit()
        dist_thresh_textline.setAlignment(Qt.AlignCenter)
        dist_thresh_textline.setFixedSize(50, 15)
        dist_thresh_textline.setText("0.5")
        dist_thresh_textline.setStyleSheet("background: #454545;"
                                           "border: 0px;"
                                           "color: white;"
                                           "border-radius: 5px;"
                                           "font-family: Verdana;")
        dist_thresh_textline.textEdited.connect(self.text2sld32)

        watershed_min_size_label = QLabel()
        watershed_min_size_label.setText("Minimal size:")
        watershed_min_size_label.setAlignment(Qt.AlignLeft)
        watershed_min_size_label.setStyleSheet("font-family: Verdana;"
                                               "color: white;")

        watershed_min_size_editor = QLineEdit()
        watershed_min_size_editor.setFixedSize(QSize(50, 20))
        watershed_min_size_editor.setAlignment(Qt.AlignCenter)
        watershed_min_size_editor.setText(str(0))
        watershed_min_size_editor.setValidator(QIntValidator())
        watershed_min_size_editor.setStyleSheet("background: #545454;"
                                                "border: 0px;"
                                                "border-radius: 3px;"
                                                "color: white;")

        watershed_min_size_left_button = QPushButton()
        watershed_min_size_left_button.setIcon(QIcon((get_icon("left.png"))))
        watershed_min_size_left_button.setIconSize(QSize(15, 15))
        watershed_min_size_left_button.setFixedSize(QSize(15, 15))
        watershed_min_size_left_button.setFlat(True)
        watershed_min_size_left_button.setStyleSheet(self.qtooltips_stylesheet)
        watershed_min_size_left_button.clicked.connect(self.min_size_left_fnc3)

        watershed_min_size_right_button = QPushButton()
        watershed_min_size_right_button.setIcon(QIcon((get_icon("right.png"))))
        watershed_min_size_right_button.setIconSize(QSize(15, 15))
        watershed_min_size_right_button.setFixedSize(QSize(15, 15))
        watershed_min_size_right_button.setFlat(True)
        watershed_min_size_right_button.setStyleSheet(
            self.qtooltips_stylesheet)
        watershed_min_size_right_button.clicked.connect(
            self.min_size_right_fnc3)

        watershed_min_size_layout = QHBoxLayout()
        watershed_min_size_layout.addWidget(watershed_min_size_label)
        watershed_min_size_layout.addWidget(watershed_min_size_left_button)
        watershed_min_size_layout.addWidget(watershed_min_size_editor)
        watershed_min_size_layout.addWidget(watershed_min_size_right_button)

        watershed_segment_button = QPushButton()
        watershed_segment_button.setFixedSize(180, 20)
        watershed_segment_button.setText("WaterShed")
        watershed_segment_button.setStyleSheet("background: #454545;"
                                               "color: white;"
                                               "border-radius: 5px;"
                                               "font-family: Verdana;")

        segment_algorithm3_layout1.addWidget(noise_label)
        segment_algorithm3_layout1.setAlignment(Qt.AlignLeft)
        segment_algorithm3_layout2.addWidget(noise_sld)
        segment_algorithm3_layout2.addWidget(noise_textline)
        segment_algorithm3_layout2.setAlignment(Qt.AlignCenter)
        segment_algorithm3_layout3.addWidget(dist_thresh_label)
        segment_algorithm3_layout3.setAlignment(Qt.AlignLeft)
        segment_algorithm3_layout4.addWidget(dist_thresh_sld)
        segment_algorithm3_layout4.addWidget(dist_thresh_textline)
        segment_algorithm3_layout4.setAlignment(Qt.AlignCenter)
        segment_algorithm3_layout5.addWidget(watershed_segment_button)
        segment_algorithm3_layout5.setAlignment(Qt.AlignRight)

        segment_algorithm3_layout.addLayout(segment_algorithm3_layout1)
        segment_algorithm3_layout.addLayout(segment_algorithm3_layout2)
        segment_algorithm3_layout.addLayout(segment_algorithm3_layout3)
        segment_algorithm3_layout.addLayout(segment_algorithm3_layout4)
        segment_algorithm3_layout.addLayout(watershed_min_size_layout)
        segment_algorithm3_layout.addLayout(segment_algorithm3_layout5)
        segment_algorithm3_layout.setAlignment(Qt.AlignTop)
        segment_algorithm3_layout.setSpacing(5)
        segment_algorithm3_layout.setContentsMargins(5, 5, 5, 5)

        self.segment_algorithm3 = segment_algorithm3
        self.noise_sld = noise_sld
        self.noise_label = noise_label
        self.noise_textline = noise_textline
        self.dist_thresh_sld = dist_thresh_sld
        self.dist_thresh_label = dist_thresh_label
        self.dist_thresh_textline = dist_thresh_textline
        self.watershed_segment_button = watershed_segment_button
        self.watershed_min_size_editor = watershed_min_size_editor
        self.watershed_min_size_left_button = watershed_min_size_left_button
        self.watershed_min_size_right_button = watershed_min_size_right_button

    def init_seg4(self):
        segment_algorithm4 = QWidget()
        segment_algorithm4.setStyleSheet("border: 0px;"
                                         "background: #323232;")

        segment_algorithm4_layout = QVBoxLayout(segment_algorithm4)
        segment_algorithm4_layout1 = QHBoxLayout()
        segment_algorithm4_layout2 = QHBoxLayout()
        segment_algorithm4_layout3 = QHBoxLayout()

        select_roi_label = QLabel()
        select_roi_label.setText("Select a Rectangle: ")
        select_roi_label.setAlignment(Qt.AlignLeft)
        select_roi_label.setStyleSheet("font-family: Verdana;"
                                       "color: white;")

        select_roi_button = QPushButton()
        select_roi_button.setFixedSize(60, 20)
        select_roi_button.setText("Select")
        select_roi_button.setStyleSheet("background: #454545;"
                                        "color: white;"
                                        "border-radius: 5px;"
                                        "font-family: Verdana;")

        iteration_sld = QSlider(Qt.Horizontal)
        iteration_sld.setMinimum(1)
        iteration_sld.setMaximum(20)
        iteration_sld.setValue(3)
        iteration_sld.setStyleSheet(self.sld_stylesheet)
        iteration_sld.valueChanged.connect(self.sld2text4)

        iteration_label = QLabel()
        iteration_label.setText("Iteration")
        iteration_label.setAlignment(Qt.AlignCenter)
        iteration_label.setStyleSheet("font-family: Verdana;"
                                      "color: white;")

        iteration_textline = QLineEdit()
        iteration_textline.setAlignment(Qt.AlignCenter)
        iteration_textline.setFixedSize(50, 15)
        iteration_textline.setEnabled(False)
        iteration_textline.setValidator(QIntValidator())
        iteration_textline.setText("3")
        iteration_textline.setStyleSheet("background: #454545;"
                                         "border: 0px;"
                                         "color: white;"
                                         "border-radius: 5px;"
                                         "font-family: Verdana;")
        iteration_textline.textEdited.connect(self.text2sld4)

        grabcut_segment_label = QLabel()
        grabcut_segment_label.setText("Do grabcut: ")
        grabcut_segment_label.setAlignment(Qt.AlignLeft)
        grabcut_segment_label.setStyleSheet("font-family: Verdana;"
                                            "color: white;")

        grabcut_segment_button = QPushButton()
        grabcut_segment_button.setFixedSize(60, 20)
        grabcut_segment_button.setText("Run")
        grabcut_segment_button.setStyleSheet("background: #454545;"
                                             "color: white;"
                                             "border-radius: 5px;"
                                             "font-family: Verdana;")

        segment_algorithm4_layout1.addWidget(select_roi_label)
        segment_algorithm4_layout1.addWidget(select_roi_button)

        segment_algorithm4_layout2.addWidget(iteration_label)
        segment_algorithm4_layout2.setAlignment(Qt.AlignLeft)
        segment_algorithm4_layout2.addWidget(iteration_sld)
        segment_algorithm4_layout2.addWidget(iteration_textline)
        segment_algorithm4_layout3.addWidget(grabcut_segment_label)
        segment_algorithm4_layout3.addWidget(grabcut_segment_button)

        segment_algorithm4_layout.addLayout(segment_algorithm4_layout1)
        segment_algorithm4_layout.addLayout(segment_algorithm4_layout2)
        segment_algorithm4_layout.addLayout(segment_algorithm4_layout3)
        segment_algorithm4_layout.setAlignment(Qt.AlignTop)
        segment_algorithm4_layout.setSpacing(5)
        segment_algorithm4_layout.setContentsMargins(5, 5, 5, 5)

        self.segment_algorithm4 = segment_algorithm4
        self.select_roi_label = select_roi_label
        self.select_roi_button = select_roi_button
        self.grabcut_segment_label = grabcut_segment_label
        self.grabcut_segment_button = grabcut_segment_button
        self.iteration_sld = iteration_sld
        self.iteration_textline = iteration_textline

    def init_user_defined(self):
        segment_algorithm5 = QWidget()
        segment_algorithm5.setStyleSheet("border: 0px;"
                                         "background: #323232;")

        segment_algorithm5_layout = QVBoxLayout(segment_algorithm5)
        segment_algorithm5_layout1 = QHBoxLayout()

        thresh_sld5 = QSlider(Qt.Horizontal)
        thresh_sld5.setMinimum(0)
        thresh_sld5.setMaximum(255)
        thresh_sld5.setValue(129)
        thresh_sld5.setStyleSheet(self.sld_stylesheet)
        thresh_sld5.valueChanged.connect(self.sld2text5)

        thresh_label5 = QLabel()
        thresh_label5.setText("Run the algorithm: ")
        thresh_label5.setAlignment(Qt.AlignLeft)
        thresh_label5.setStyleSheet("font-family: Verdana;"
                                    "color: white;")

        thresh_textline5 = QLineEdit()
        thresh_textline5.setAlignment(Qt.AlignCenter)
        thresh_textline5.setFixedSize(50, 15)
        thresh_textline5.setValidator(QIntValidator())
        thresh_textline5.setText("129")
        thresh_textline5.setStyleSheet("background: #454545;"
                                       "border: 0px;"
                                       "color: white;"
                                       "border-radius: 5px;"
                                       "font-family: Verdana;")
        thresh_textline5.textEdited.connect(self.text2sld5)

        thresh_segment_button5 = QPushButton()
        thresh_segment_button5.setFixedSize(50, 20)
        thresh_segment_button5.setText("Run")
        thresh_segment_button5.setStyleSheet("background: #454545;"
                                             "color: white;"
                                             "border-radius: 5px;"
                                             "font-family: Verdana;")

        segment_algorithm5_layout1.addWidget(thresh_label5)
        segment_algorithm5_layout1.addWidget(thresh_segment_button5)
        segment_algorithm5_layout.addLayout(segment_algorithm5_layout1)
        segment_algorithm5_layout.setAlignment(Qt.AlignTop)
        segment_algorithm5_layout.setSpacing(5)
        segment_algorithm5_layout.setContentsMargins(5, 5, 5, 5)

        self.segment_algorithm5 = segment_algorithm5
        self.thresh_sld5 = thresh_sld5
        self.thresh_label5 = thresh_label5
        self.thresh_textline5 = thresh_textline5
        self.thresh_segment_butto5 = thresh_segment_button5

    def sld2text1(self):
        f = self.thresh_sld1.value()
        self.thresh_textline1.setText(str(f))

    def text2sld1(self):
        t = self.thresh_textline1.text()
        self.thresh_sld1.setValue(int(t))

    def sld2text2(self):
        f = self.thresh_sld2.value()/10
        self.thresh_textline2.setText(str(f))

    def text2sld2(self):
        t = self.thresh_textline2.text()
        self.thresh_sld2.setValue(int(t)*10)

    def sld2text31(self):
        f = self.noise_sld.value()
        self.noise_textline.setText(str(f))

    def text2sld31(self):
        t = self.noise_textline.text()
        self.noise_sld.setValue(int(t))

    def sld2text32(self):
        f = self.dist_thresh_sld.value()/10
        self.dist_thresh_textline.setText(str(f))

    def text2sld32(self):
        t = self.dist_thresh_textline.text()
        self.dist_thresh_sld.setValue(int(t)*10)

    def sld2text4(self):
        f = self.iteration_sld.value()
        self.iteration_textline.setText(str(f))

    def text2sld4(self):
        t = self.iteration_textline.text()
        self.iteration_sld.setValue(int(t))

    def sld2text5(self):
        f = self.thresh_sld5.value()
        self.thresh_textline5.setText(str(f))

    def text2sld5(self):
        t = self.thresh_textline5.text()
        self.thresh_sld5.setValue(int(t))

    def segment_algorithm1_tool_button_fnc(self):
        if self.segment_algorithm1.isVisible():
            self.segment_algorithm1.setVisible(False)
            self.segment_algorithm1_tool_button.setIcon(
                QIcon(get_icon("Arrow_right.png")))
            self.segment_algorithm1_tool_button.setStyleSheet("background: #454545;"
                                                              "font-family: Verdana;"
                                                              "border: 0px;"
                                                              "text-align:left;"
                                                              "color: #000000")
        else:
            self.segment_algorithm1.setVisible(True)
            self.segment_algorithm1_tool_button.setIcon(
                QIcon(get_icon("Arrow_down.png")))
            self.segment_algorithm1_tool_button.setStyleSheet("background: #454545;"
                                                              "font-family: Verdana;"
                                                              "border: 0px;"
                                                              "text-align:left;"
                                                              "color: #FFFFFF")

    def min_size_left_fnc1(self):
        v = int(self.thresh_min_size_editor.text())
        if v > 1:
            self.thresh_min_size_editor.setText(str(v - 1))

    def min_size_right_fnc1(self):
        v = int(self.thresh_min_size_editor.text())
        self.thresh_min_size_editor.setText(str(v + 1))

    def min_size_left_fnc2(self):
        v = int(self.unet_min_size_editor.text())
        if v > 1:
            self.unet_min_size_editor.setText(str(v - 1))

    def min_size_right_fnc2(self):
        v = int(self.unet_min_size_editor.text())
        self.unet_min_size_editor.setText(str(v + 1))

    def min_size_left_fnc3(self):
        v = int(self.watershed_min_size_editor.text())
        if v > 1:
            self.watershed_min_size_editor.setText(str(v - 1))

    def min_size_right_fnc3(self):
        v = int(self.watershed_min_size_editor.text())
        self.watershed_min_size_editor.setText(str(v + 1))

    def segment_algorithm2_tool_button_fnc(self):
        if self.segment_algorithm2.isVisible():
            self.segment_algorithm2.setVisible(False)
            self.segment_algorithm2_tool_button.setIcon(
                QIcon(get_icon("Arrow_right.png")))
            self.segment_algorithm2_tool_button.setStyleSheet("background: #454545;"
                                                              "font-family: Verdana;"
                                                              "border: 0px;"
                                                              "text-align:left;"
                                                              "color: #000000")
        else:
            self.segment_algorithm2.setVisible(True)
            self.segment_algorithm2_tool_button.setIcon(
                QIcon(get_icon("Arrow_down.png")))
            self.segment_algorithm2_tool_button.setStyleSheet("background: #454545;"
                                                              "font-family: Verdana;"
                                                              "border: 0px;"
                                                              "text-align:left;"
                                                              "color: #FFFFFF")

    def segment_algorithm3_tool_button_fnc(self):
        if self.segment_algorithm3.isVisible():
            self.segment_algorithm3.setVisible(False)
            self.segment_algorithm3_tool_button.setIcon(
                QIcon(get_icon("Arrow_right.png")))
            self.segment_algorithm3_tool_button.setStyleSheet("background: #454545;"
                                                              "font-family: Verdana;"
                                                              "border: 0px;"
                                                              "text-align:left;"
                                                              "color: #000000")
        else:
            self.segment_algorithm3.setVisible(True)
            self.segment_algorithm3_tool_button.setIcon(
                QIcon(get_icon("Arrow_down.png")))
            self.segment_algorithm3_tool_button.setStyleSheet("background: #454545;"
                                                              "font-family: Verdana;"
                                                              "border: 0px;"
                                                              "text-align:left;"
                                                              "color: #FFFFFF")

    def segment_algorithm4_tool_button_fnc(self):
        if self.segment_algorithm4.isVisible():
            self.segment_algorithm4.setVisible(False)
            self.segment_algorithm4_tool_button.setIcon(
                QIcon(get_icon("Arrow_right.png")))
            self.segment_algorithm4_tool_button.setStyleSheet("background: #454545;"
                                                              "font-family: Verdana;"
                                                              "border: 0px;"
                                                              "text-align:left;"
                                                              "color: #000000")
        else:
            self.segment_algorithm4.setVisible(True)
            self.segment_algorithm4_tool_button.setIcon(
                QIcon(get_icon("Arrow_down.png")))
            self.segment_algorithm4_tool_button.setStyleSheet("background: #454545;"
                                                              "font-family: Verdana;"
                                                              "border: 0px;"
                                                              "text-align:left;"
                                                              "color: #FFFFFF")

    def segment_algorithm5_tool_button_fnc(self):
        if self.segment_algorithm5.isVisible():
            self.segment_algorithm5.setVisible(False)
            self.segment_algorithm5_tool_button.setIcon(
                QIcon(get_icon("Arrow_right.png")))
            self.segment_algorithm5_tool_button.setStyleSheet("background: #454545;"
                                                              "font-family: Verdana;"
                                                              "border: 0px;"
                                                              "text-align:left;"
                                                              "color: #000000")
        else:
            self.segment_algorithm5.setVisible(True)
            self.segment_algorithm5_tool_button.setIcon(
                QIcon(get_icon("Arrow_down.png")))
            self.segment_algorithm5_tool_button.setStyleSheet("background: #454545;"
                                                              "font-family: Verdana;"
                                                              "border: 0px;"
                                                              "text-align:left;"
                                                              "color: #FFFFFF")
