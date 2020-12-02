# -*- coding: UTF-8 -*-

import os.path as osp
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from ..utils import get_icon, normalize_tools_stylesheet, slide_stylesheet


class NormalizeTools(QWidget):
    def __init__(self):
        super().__init__()

        self.normalize_tools_stylesheet = normalize_tools_stylesheet
        self.sld_stylesheet = slide_stylesheet
        self.normalize_tools = QWidget()
        self.normalize_tools.setStyleSheet("background: #323232")
        self.normalize_tools.setContentsMargins(20, 0, 0, 0)

        self.setup_ui()

    def setup_ui(self):
        self.init_equalize_hist()
        self.init_clahe()
        self.init_min_max()
        self.init_retinex_MSRCP()
        self.init_retinex_MSRCR()
        self.init_reset_raw()

        self.normalize_tools_layout = QVBoxLayout()
        self.normalize_tools_layout.setAlignment(Qt.AlignTop)
        self.normalize_tools_layout.setContentsMargins(0, 0, 0, 0)
        self.normalize_tools_layout.setSpacing(1)

        self.equalize_hist_tool_button = QPushButton()
        self.equalize_hist_tool_button.setStyleSheet("background: #454545;"
                                                     "font-family: Verdana;"
                                                     "border: 0px;"
                                                     "text-align:left;")
        self.equalize_hist_tool_button.setFixedHeight(20)
        self.equalize_hist_tool_button.setText("Equalize Histogram")
        self.equalize_hist_tool_button.clicked.connect(
            self.equalize_hist_tool_button_fnc)
        self.equalize_hist_tool_button.setIcon(
            QIcon(get_icon("Arrow_right.png")))

        self.clahe_tool_button = QPushButton()
        self.clahe_tool_button.setStyleSheet("background: #454545;"
                                                     "font-family: Verdana;"
                                                     "border: 0px;"
                                                     "text-align:left;")
        self.clahe_tool_button.setFixedHeight(20)
        self.clahe_tool_button.setText("CLAHE")
        self.clahe_tool_button.clicked.connect(
            self.clahe_tool_button_fnc)
        self.clahe_tool_button.setIcon(
            QIcon(get_icon("Arrow_right.png")))

        self.min_max_tool_button = QPushButton()
        self.min_max_tool_button.setStyleSheet("background: #454545;"
                                               "font-family: Verdana;"
                                               "border: 0px;"
                                               "text-align:left;")
        self.min_max_tool_button.setFixedHeight(20)
        self.min_max_tool_button.setText("Min-Max")
        self.min_max_tool_button.clicked.connect(self.min_max_tool_button_fnc)
        self.min_max_tool_button.setIcon(QIcon(get_icon("Arrow_right.png")))

        self.retinex_MSRCP_tool_button = QPushButton()
        self.retinex_MSRCP_tool_button.setStyleSheet("background: #454545;"
                                                     "font-family: Verdana;"
                                                     "border: 0px;"
                                                     "text-align:left;")
        self.retinex_MSRCP_tool_button.setFixedHeight(20)
        self.retinex_MSRCP_tool_button.setText("Retinex-MSRCP")
        self.retinex_MSRCP_tool_button.clicked.connect(
            self.retinex_MSRCP_tool_button_fnc)
        self.retinex_MSRCP_tool_button.setIcon(
            QIcon(get_icon("Arrow_right.png")))

        self.retinex_MSRCR_tool_button = QPushButton()
        self.retinex_MSRCR_tool_button.setStyleSheet("background: #454545;"
                                                     "font-family: Verdana;"
                                                     "border: 0px;"
                                                     "text-align:left;")
        self.retinex_MSRCR_tool_button.setFixedHeight(20)
        self.retinex_MSRCR_tool_button.setText("Retinex-MSRCR")
        self.retinex_MSRCR_tool_button.clicked.connect(
            self.retinex_MSRCR_tool_button_fnc)
        self.retinex_MSRCR_tool_button.setIcon(
            QIcon(get_icon("Arrow_right.png")))

        self.reset_raw_tool_button = QPushButton()
        self.reset_raw_tool_button.setStyleSheet("background: #454545;"
                                                 "font-family: Verdana;"
                                                 "border: 0px;"
                                                 "text-align:left;")
        self.reset_raw_tool_button.setFixedHeight(20)
        self.reset_raw_tool_button.setText("Remove Norm")
        self.reset_raw_tool_button.clicked.connect(
            self.reset_raw_tool_button_fnc)
        self.reset_raw_tool_button.setIcon(QIcon(get_icon("Arrow_right.png")))

        self.normalize_tools_layout.addWidget(self.equalize_hist_tool_button)
        self.normalize_tools_layout.addWidget(self.equalize_hist)
        self.equalize_hist.setVisible(False)
        self.normalize_tools_layout.addWidget(self.clahe_tool_button)
        self.normalize_tools_layout.addWidget(self.clahe)
        self.clahe.setVisible(False)
        self.normalize_tools_layout.addWidget(self.min_max_tool_button)
        self.normalize_tools_layout.addWidget(self.min_max)
        self.min_max.setVisible(False)
        self.normalize_tools_layout.addWidget(self.retinex_MSRCP_tool_button)
        self.normalize_tools_layout.addWidget(self.retinex_MSRCP)
        self.retinex_MSRCP.setVisible(False)
        self.normalize_tools_layout.addWidget(self.retinex_MSRCR_tool_button)
        self.normalize_tools_layout.addWidget(self.retinex_MSRCR)
        self.retinex_MSRCR.setVisible(False)
        self.normalize_tools_layout.addWidget(self.reset_raw_tool_button)
        self.normalize_tools_layout.addWidget(self.reset_raw)
        self.reset_raw.setVisible(False)

        self.normalize_tools.setLayout(self.normalize_tools_layout)

    def init_equalize_hist(self):
        equalize_hist = QWidget()
        equalize_hist.setStyleSheet("border: 0px;"
                                    "background: #323232;")
        equalize_hist_layout = QHBoxLayout()
        equalize_hist_layout_main = QVBoxLayout()

        equalize_hist_label = QLabel()
        equalize_hist_label.setText("Equalize histogram: ")
        equalize_hist_label.setAlignment(Qt.AlignLeft)
        equalize_hist_label.setStyleSheet("font-family: Verdana;"
                                          "color: white;")

        equalize_hist_button = QPushButton()
        equalize_hist_button.setFixedSize(60, 20)
        equalize_hist_button.setText("Run")
        equalize_hist_button.setStyleSheet("background: #454545;"
                                           "color: white;"
                                           "border-radius: 5px;"
                                           "font-family: Verdana;")

        equalize_hist_layout.addWidget(equalize_hist_label)
        equalize_hist_layout.addWidget(equalize_hist_button)
        equalize_hist_layout_main.addLayout(equalize_hist_layout)
        equalize_hist_layout_main.setAlignment(Qt.AlignTop)
        equalize_hist.setLayout(equalize_hist_layout_main)

        self.equalize_hist = equalize_hist
        self.equalize_hist_label = equalize_hist_label
        self.equalize_hist_button = equalize_hist_button

    def init_clahe(self):
        clahe = QWidget()
        clahe.setStyleSheet("border: 0px;"
                                          "background: #323232;")

        clahe_layout_main = QVBoxLayout(clahe)
        clahe_layout1 = QHBoxLayout()
        clahe_layout11 = QHBoxLayout()
        clahe_layout2 = QHBoxLayout()
        clahe_layout22 = QHBoxLayout()
        clahe_layout3 = QHBoxLayout()
        clahe_layout33 = QHBoxLayout()
        clahe_layout4 = QHBoxLayout()

        clip_limit_sld = QSlider(Qt.Horizontal)
        clip_limit_sld.setMinimum(0)
        clip_limit_sld.setMaximum(100)
        clip_limit_sld.setValue(2)
        clip_limit_sld.setStyleSheet(self.sld_stylesheet)
        clip_limit_sld.valueChanged.connect(self.sld2text1)

        clip_limit_label = QLabel()
        clip_limit_label.setText("Clip limit")
        clip_limit_label.setAlignment(Qt.AlignCenter)
        clip_limit_label.setStyleSheet("font-family: Verdana;"
                                     "color: white;")

        clip_limit_textline = QLineEdit()
        clip_limit_textline.setAlignment(Qt.AlignCenter)
        clip_limit_textline.setFixedSize(50, 15)
        clip_limit_textline.setValidator(QIntValidator())
        clip_limit_textline.setText("2")
        clip_limit_textline.setStyleSheet("background: #454545;"
                                        "border: 0px;"
                                        "color: white;"
                                        "border-radius: 5px;"
                                        "font-family: Verdana;")
        clip_limit_textline.textEdited.connect(self.text2sld1)

        grid_width_sld = QSlider(Qt.Horizontal)
        grid_width_sld.setMinimum(1)
        grid_width_sld.setMaximum(50)
        grid_width_sld.setValue(8)
        grid_width_sld.setStyleSheet(self.sld_stylesheet)
        grid_width_sld.valueChanged.connect(self.sld2text2)

        grid_width_label = QLabel()
        grid_width_label.setText("Grid width")
        grid_width_label.setAlignment(Qt.AlignCenter)
        grid_width_label.setStyleSheet("font-family: Verdana;"
                                       "color: white;")

        grid_width_textline = QLineEdit()
        grid_width_textline.setAlignment(Qt.AlignCenter)
        grid_width_textline.setFixedSize(50, 15)
        grid_width_textline.setValidator(QIntValidator())
        grid_width_textline.setText("8")
        grid_width_textline.setStyleSheet("background: #454545;"
                                          "border: 0px;"
                                          "color: white;"
                                          "border-radius: 5px;"
                                          "font-family: Verdana;")
        grid_width_textline.textEdited.connect(self.text2sld2)

        grid_height_sld = QSlider(Qt.Horizontal)
        grid_height_sld.setMinimum(1)
        grid_height_sld.setMaximum(50)
        grid_height_sld.setValue(8)
        grid_height_sld.setStyleSheet(self.sld_stylesheet)
        grid_height_sld.valueChanged.connect(self.sld2text3)

        grid_height_label = QLabel()
        grid_height_label.setText("Grid height")
        grid_height_label.setAlignment(Qt.AlignCenter)
        grid_height_label.setStyleSheet("font-family: Verdana;"
                                       "color: white;")

        grid_height_textline = QLineEdit()
        grid_height_textline.setAlignment(Qt.AlignCenter)
        grid_height_textline.setFixedSize(50, 15)
        grid_height_textline.setValidator(QIntValidator())
        grid_height_textline.setText("8")
        grid_height_textline.setStyleSheet("background: #454545;"
                                          "border: 0px;"
                                          "color: white;"
                                          "border-radius: 5px;"
                                          "font-family: Verdana;")
        grid_height_textline.textEdited.connect(self.text2sld3)

        clahe_button = QPushButton()
        clahe_button.setFixedSize(60, 20)
        clahe_button.setText("Run")
        clahe_button.setStyleSheet("background: #454545;"
                                              "color: white;"
                                              "border-radius: 5px;"
                                              "font-family: Verdana;")

        clahe_layout1.addWidget(clip_limit_label)
        clahe_layout1.setAlignment(Qt.AlignLeft)
        clahe_layout11.addWidget(clip_limit_sld)
        clahe_layout11.addWidget(clip_limit_textline)

        clahe_layout2.addWidget(grid_width_label)
        clahe_layout2.setAlignment(Qt.AlignLeft)
        clahe_layout22.addWidget(grid_width_sld)
        clahe_layout22.addWidget(grid_width_textline)

        clahe_layout3.addWidget(grid_height_label)
        clahe_layout3.setAlignment(Qt.AlignLeft)
        clahe_layout33.addWidget(grid_height_sld)
        clahe_layout33.addWidget(grid_height_textline)
        clahe_layout4.addWidget(clahe_button)
        clahe_layout4.setAlignment(Qt.AlignRight)

        clahe_layout_main.addLayout(clahe_layout1)
        clahe_layout_main.addLayout(clahe_layout11)
        clahe_layout_main.addLayout(clahe_layout2)
        clahe_layout_main.addLayout(clahe_layout22)
        clahe_layout_main.addLayout(clahe_layout3)
        clahe_layout_main.addLayout(clahe_layout33)
        clahe_layout_main.addLayout(clahe_layout4)
        clahe_layout_main.setAlignment(Qt.AlignTop)

        self.clahe = clahe
        self.clip_limit_sld = clip_limit_sld
        self.clip_limit_label = clip_limit_label
        self.clip_limit_textline = clip_limit_textline
        self.grid_width_sld = grid_width_sld
        self.grid_width_label = grid_width_label
        self.grid_width_textline = grid_width_textline
        self.grid_height_sld = grid_height_sld
        self.grid_height_label = grid_height_label
        self.grid_height_textline = grid_height_textline

        self.clahe_button = clahe_button

    def init_min_max(self):
        min_max = QWidget()
        min_max.setStyleSheet("border: 0px;"
                              "background: #323232;")
        min_max_layout_main = QVBoxLayout()
        min_max_layout = QHBoxLayout()

        min_max_label = QLabel()
        min_max_label.setText("Min-Max: ")
        min_max_label.setAlignment(Qt.AlignLeft)
        min_max_label.setStyleSheet("font-family: Verdana;"
                                    "color: white;")

        min_max_button = QPushButton()
        min_max_button.setFixedSize(50, 20)
        min_max_button.setText("Run")
        min_max_button.setStyleSheet("background: #454545;"
                                     "color: white;"
                                     "border-radius: 5px;"
                                     "font-family: Verdana;")

        min_max_layout.addWidget(min_max_label)
        min_max_layout.addWidget(min_max_button)
        min_max_layout_main.addLayout(min_max_layout)
        min_max_layout_main.setAlignment(Qt.AlignTop)
        min_max.setLayout(min_max_layout_main)

        self.min_max = min_max
        self.min_max_label = min_max_label
        self.min_max_button = min_max_button

    def init_retinex_MSRCP(self):
        retinex_MSRCP = QWidget()
        retinex_MSRCP.setStyleSheet("border: 0px;"
                                    "background: #323232;")
        retinex_MSRCP_layout_main = QVBoxLayout()
        retinex_MSRCP_layout = QHBoxLayout()

        retinex_MSRCP_label = QLabel()
        retinex_MSRCP_label.setText("Retinex-MSRCP: ")
        retinex_MSRCP_label.setAlignment(Qt.AlignLeft)
        retinex_MSRCP_label.setStyleSheet("font-family: Verdana;"
                                          "color: white;")

        retinex_MSRCP_button = QPushButton()
        retinex_MSRCP_button.setFixedSize(50, 20)
        retinex_MSRCP_button.setText("Run")
        retinex_MSRCP_button.setStyleSheet("background: #454545;"
                                           "color: white;"
                                           "border-radius: 5px;"
                                           "font-family: Verdana;")

        retinex_MSRCP_layout.addWidget(retinex_MSRCP_label)
        retinex_MSRCP_layout.addWidget(retinex_MSRCP_button)
        retinex_MSRCP_layout_main.addLayout(retinex_MSRCP_layout)
        retinex_MSRCP_layout_main.setAlignment(Qt.AlignTop)
        retinex_MSRCP.setLayout(retinex_MSRCP_layout_main)

        self.retinex_MSRCP = retinex_MSRCP
        self.retinex_MSRCP_label = retinex_MSRCP_label
        self.retinex_MSRCP_button = retinex_MSRCP_button

    def init_retinex_MSRCR(self):
        retinex_MSRCR = QWidget()
        retinex_MSRCR.setStyleSheet("border: 0px;"
                                    "background: #323232;")
        retinex_MSRCR_layout_main = QVBoxLayout()
        retinex_MSRCR_layout = QHBoxLayout()

        retinex_MSRCR_label = QLabel()
        retinex_MSRCR_label.setText("Retinex-MSRCR: ")
        retinex_MSRCR_label.setAlignment(Qt.AlignLeft)
        retinex_MSRCR_label.setStyleSheet("font-family: Verdana;"
                                          "color: white;")

        retinex_MSRCR_button = QPushButton()
        retinex_MSRCR_button.setFixedSize(60, 20)
        retinex_MSRCR_button.setText("Run")
        retinex_MSRCR_button.setStyleSheet("background: #454545;"
                                           "color: white;"
                                           "border-radius: 5px;"
                                           "font-family: Verdana;")

        retinex_MSRCR_layout.addWidget(retinex_MSRCR_label)
        retinex_MSRCR_layout.addWidget(retinex_MSRCR_button)
        retinex_MSRCR_layout_main.addLayout(retinex_MSRCR_layout)
        retinex_MSRCR_layout_main.setAlignment(Qt.AlignTop)
        retinex_MSRCR.setLayout(retinex_MSRCR_layout_main)

        self.retinex_MSRCR = retinex_MSRCR
        self.retinex_MSRCR_label = retinex_MSRCR_label
        self.retinex_MSRCR_button = retinex_MSRCR_button

    def init_reset_raw(self):
        reset_raw = QWidget()
        reset_raw.setStyleSheet("border: 0px;"
                                "background: #323232;")
        reset_raw_layout_main = QVBoxLayout()
        reset_raw_layout = QHBoxLayout()

        reset_raw_label = QLabel()
        reset_raw_label.setText("Remove normalization: ")
        reset_raw_label.setAlignment(Qt.AlignLeft)
        reset_raw_label.setStyleSheet("font-family: Verdana;"
                                      "color: white;")

        reset_raw_button = QPushButton()
        reset_raw_button.setFixedSize(50, 20)
        reset_raw_button.setText("Run")
        reset_raw_button.setStyleSheet("background: #454545;"
                                       "color: white;"
                                       "border-radius: 5px;"
                                       "font-family: Verdana;")

        reset_raw_layout.addWidget(reset_raw_label)
        reset_raw_layout.addWidget(reset_raw_button)
        reset_raw_layout_main.addLayout(reset_raw_layout)
        reset_raw_layout_main.setAlignment(Qt.AlignTop)
        reset_raw.setLayout(reset_raw_layout_main)

        self.reset_raw = reset_raw
        self.reset_raw_label = reset_raw_label
        self.reset_raw_button = reset_raw_button

    def equalize_hist_tool_button_fnc(self):
        if self.equalize_hist.isVisible():
            self.equalize_hist.setVisible(False)
            self.equalize_hist_tool_button.setIcon(
                QIcon(get_icon("Arrow_right.png")))
            self.equalize_hist_tool_button.setStyleSheet("background: #454545;"
                                                         "font-family: Verdana;"
                                                         "border: 0px;"
                                                         "text-align:left;"
                                                         "color: #000000")
        else:
            self.equalize_hist.setVisible(True)
            self.equalize_hist_tool_button.setIcon(
                QIcon(get_icon("Arrow_down.png")))
            self.equalize_hist_tool_button.setStyleSheet("background: #454545;"
                                                         "font-family: Verdana;"
                                                         "border: 0px;"
                                                         "text-align:left;"
                                                         "color: #FFFFFF")

    def clahe_tool_button_fnc(self):
        if self.clahe.isVisible():
            self.clahe.setVisible(False)
            self.clahe_tool_button.setIcon(
                QIcon(get_icon("Arrow_right.png")))
            self.clahe_tool_button.setStyleSheet("background: #454545;"
                                                         "font-family: Verdana;"
                                                         "border: 0px;"
                                                         "text-align:left;"
                                                         "color: #000000")
        else:
            self.clahe.setVisible(True)
            self.clahe_tool_button.setIcon(
                QIcon(get_icon("Arrow_down.png")))
            self.clahe_tool_button.setStyleSheet("background: #454545;"
                                                         "font-family: Verdana;"
                                                         "border: 0px;"
                                                         "text-align:left;"
                                                         "color: #FFFFFF")

    def min_max_tool_button_fnc(self):
        if self.min_max.isVisible():
            self.min_max.setVisible(False)
            self.min_max_tool_button.setIcon(
                QIcon(get_icon("Arrow_right.png")))
            self.min_max_tool_button.setStyleSheet("background: #454545;"
                                                   "font-family: Verdana;"
                                                   "border: 0px;"
                                                   "text-align:left;"
                                                   "color: #000000")
        else:
            self.min_max.setVisible(True)
            self.min_max_tool_button.setIcon(QIcon(get_icon("Arrow_down.png")))
            self.min_max_tool_button.setStyleSheet("background: #454545;"
                                                   "font-family: Verdana;"
                                                   "border: 0px;"
                                                   "text-align:left;"
                                                   "color: #FFFFFF")

    def retinex_MSRCP_tool_button_fnc(self):
        if self.retinex_MSRCP.isVisible():
            self.retinex_MSRCP.setVisible(False)
            self.retinex_MSRCP_tool_button.setIcon(
                QIcon(get_icon("Arrow_right.png")))
            self.retinex_MSRCP_tool_button.setStyleSheet("background: #454545;"
                                                         "font-family: Verdana;"
                                                         "border: 0px;"
                                                         "text-align:left;"
                                                         "color: #000000")
        else:
            self.retinex_MSRCP.setVisible(True)
            self.retinex_MSRCP_tool_button.setIcon(
                QIcon(get_icon("Arrow_down.png")))
            self.retinex_MSRCP_tool_button.setStyleSheet("background: #454545;"
                                                         "font-family: Verdana;"
                                                         "border: 0px;"
                                                         "text-align:left;"
                                                         "color: #FFFFFF")

    def retinex_MSRCR_tool_button_fnc(self):
        if self.retinex_MSRCR.isVisible():
            self.retinex_MSRCR.setVisible(False)
            self.retinex_MSRCR_tool_button.setIcon(
                QIcon(get_icon("Arrow_right.png")))
            self.retinex_MSRCR_tool_button.setStyleSheet("background: #454545;"
                                                         "font-family: Verdana;"
                                                         "border: 0px;"
                                                         "text-align:left;"
                                                         "color: #000000")
        else:
            self.retinex_MSRCR.setVisible(True)
            self.retinex_MSRCR_tool_button.setIcon(
                QIcon(get_icon("Arrow_down.png")))
            self.retinex_MSRCR_tool_button.setStyleSheet("background: #454545;"
                                                         "font-family: Verdana;"
                                                         "border: 0px;"
                                                         "text-align:left;"
                                                         "color: #FFFFFF")

    def reset_raw_tool_button_fnc(self):
        if self.reset_raw.isVisible():
            self.reset_raw.setVisible(False)
            self.reset_raw_tool_button.setIcon(
                QIcon(get_icon("Arrow_right.png")))
            self.reset_raw_tool_button.setStyleSheet("background: #454545;"
                                                     "font-family: Verdana;"
                                                     "border: 0px;"
                                                     "text-align:left;"
                                                     "color: #000000")
        else:
            self.reset_raw.setVisible(True)
            self.reset_raw_tool_button.setIcon(
                QIcon(get_icon("Arrow_down.png")))
            self.reset_raw_tool_button.setStyleSheet("background: #454545;"
                                                     "font-family: Verdana;"
                                                     "border: 0px;"
                                                     "text-align:left;"
                                                     "color: #FFFFFF")

    def sld2text1(self):
        f = self.clip_limit_sld.value()
        self.clip_limit_textline.setText(str(f))

    def text2sld1(self):
        t = self.clip_limit_textline.text()
        self.clip_limit_sld.setValue(int(t))

    def sld2text2(self):
        f = self.grid_width_sld.value()
        self.grid_width_textline.setText(str(f))

    def text2sld2(self):
        t = self.grid_width_textline.text()
        self.grid_width_sld.setValue(int(t))

    def sld2text3(self):
        f = self.grid_height_sld.value()
        self.grid_height_textline.setText(str(f))

    def text2sld3(self):
        t = self.grid_height_textline.text()
        self.grid_height_sld.setValue(int(t))
