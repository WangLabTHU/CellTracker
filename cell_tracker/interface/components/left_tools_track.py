# -*- coding: UTF-8 -*-

import os.path as osp
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *


class TrackTools(QWidget):

    def __init__(self):
        super().__init__()

        self.track_tools = QWidget()
        self.track_tools.setStyleSheet("background: #323232;"
                                       "border-radius: 10px;")
        self.setup_ui()

    def setup_ui(self):

        tracker_select_label = QLabel()
        tracker_select_label.setText("Select a tracker:")
        tracker_select_label.setStyleSheet("font-family: Verdana;"
                                           "color: white;")

        tracker_select = QComboBox()
        tracker_select.setFixedSize(100, 20)
        tracker_select.setStyleSheet("border: 0px;"
                                     "color: white;"
                                     "font-family: Verdana;"
                                     "background: #353535;")
        tracker_select.addItem("Bi-Graph")
        tracker_select.addItem("None")

        none_tracker_button = QPushButton()
        none_tracker_button.setText("None")
        none_tracker_button.setFixedSize(70, 15)
        none_tracker_button.setStyleSheet("background: #454545;"
                                          "color: white;"
                                          "border-radius: 5px;"
                                          "font-family: Verdana;")

        bipartite_tracker_button = QPushButton()
        bipartite_tracker_button.setText("Bi-Graph")
        bipartite_tracker_button.setFixedSize(70, 15)
        bipartite_tracker_button.setStyleSheet("background: #454545;"
                                               "color: white;"
                                               "border-radius: 5px;"
                                               "font-family: Verdana;")

        run_button = QPushButton()
        run_button.setText("Run")
        run_button.setFixedSize(60, 20)
        run_button.setStyleSheet("background: #454545;"
                                 "color: white;"
                                 "border-radius: 5px;"
                                 "font-family: Verdana;")

        track_layout = QVBoxLayout()
        track_layout1 = QHBoxLayout()
        track_layout2 = QHBoxLayout()
        track_layout3 = QHBoxLayout()

        track_layout1.addWidget(tracker_select_label)
        track_layout1.addWidget(tracker_select)
        track_layout3.addWidget(run_button)
        track_layout3.setAlignment(Qt.AlignRight)

        track_layout.addLayout(track_layout1)
        track_layout.addLayout(track_layout3)
        track_layout.setAlignment(Qt.AlignTop)
        track_layout.setSpacing(5)
        self.track_tools.setLayout(track_layout)

        self.none_tracker_button = none_tracker_button
        self.bipartite_tracker_button = bipartite_tracker_button
        self.tracker_select = tracker_select
        self.run_button = run_button
