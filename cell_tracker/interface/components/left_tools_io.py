# -*- coding: UTF-8 -*-

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *


class InputOutput(QWidget):
    def __init__(self):
        super().__init__()

        self.input_output = QWidget()

        self.setup_ui()

    def setup_ui(self):
        set_source_folder_layout = QVBoxLayout()

        set_source_button = QPushButton()
        set_source_button.setText("Set source folder")
        set_source_button.setStyleSheet("background: #454545;"
                                        "color: rgb(245, 245, 245);")
        set_source_button.setContentsMargins(0, 0, 0, 0)
        set_source_button.setFixedHeight(25)

        source_img_label = QLabel()
        source_img_label.setText("Set source image folder.")
        source_img_label.setContentsMargins(0, 0, 0, 0)

        source_folder_show_lineedit = QLineEdit()
        source_folder_show_lineedit.setPlaceholderText("Source folder")
        source_folder_show_lineedit.setEnabled(False)
        source_folder_show_lineedit.setStyleSheet("background: #454545;"
                                                  "border: 0px;"
                                                  "color: white;"
                                                  "border-radius: 5px;"
                                                  "font-family: Verdana;"
                                                  "font-size: 10px;")

        set_source_folder_layout.addWidget(source_img_label)
        set_source_folder_layout.addWidget(set_source_button)
        set_source_folder_layout.addWidget(source_folder_show_lineedit)
        set_source_folder_layout.setSpacing(10)

        set_source_folder_layout = QVBoxLayout()

        set_source_button = QPushButton()
        set_source_button.setText("Set source folder")
        set_source_button.setStyleSheet("background: #454545;"
                                        "color: rgb(245, 245, 245);")
        set_source_button.setContentsMargins(0, 0, 0, 0)
        set_source_button.setFixedHeight(25)

        source_img_label = QLabel()
        source_img_label.setText("Set source image folder.")
        source_img_label.setContentsMargins(0, 0, 0, 0)

        source_folder_show_lineedit = QLineEdit()
        source_folder_show_lineedit.setPlaceholderText("Source folder")
        source_folder_show_lineedit.setEnabled(False)
        source_folder_show_lineedit.setStyleSheet("background: #454545;"
                                                  "border: 0px;"
                                                  "color: white;"
                                                  "border-radius: 5px;"
                                                  "font-family: Verdana;"
                                                  "font-size: 10px;")

        set_source_folder_layout.addWidget(source_img_label)
        set_source_folder_layout.addWidget(set_source_button)
        set_source_folder_layout.addWidget(source_folder_show_lineedit)
        set_source_folder_layout.setSpacing(10)

        set_label_folder_layout = QVBoxLayout()

        set_label_button = QPushButton()
        set_label_button.setText("Set label folder")
        set_label_button.setStyleSheet("background: #454545;"
                                       "color: rgb(245, 245, 245);")
        set_label_button.setContentsMargins(0, 0, 0, 0)
        set_label_button.setFixedHeight(25)

        label_img_label = QLabel()
        label_img_label.setText("Set label image folder.")
        label_img_label.setContentsMargins(0, 0, 0, 0)

        label_folder_show_lineedit = QLineEdit()
        label_folder_show_lineedit.setPlaceholderText("Label folder")
        label_folder_show_lineedit.setEnabled(False)
        label_folder_show_lineedit.setStyleSheet("background: #454545;"
                                                 "border: 0px;"
                                                 "color: white;"
                                                 "border-radius: 5px;"
                                                 "font-family: Verdana;"
                                                 "font-size: 10px;")

        set_label_folder_layout.addWidget(label_img_label)
        set_label_folder_layout.addWidget(set_label_button)
        set_label_folder_layout.addWidget(label_folder_show_lineedit)
        set_label_folder_layout.setSpacing(10)

        set_log_folder_layout = QVBoxLayout()

        set_log_button = QPushButton()
        set_log_button.setText("Set log folder")
        set_log_button.setStyleSheet("background: #454545;"
                                     "color: rgb(245, 245, 245);")
        set_log_button.setContentsMargins(0, 0, 0, 0)
        set_log_button.setFixedHeight(25)

        set_log_label = QLabel()
        set_log_label.setText("Set log folder to store log files.")
        set_log_label.setContentsMargins(0, 0, 0, 0)

        log_folder_show_lineedit = QLineEdit()
        log_folder_show_lineedit.setPlaceholderText("Label folder")
        log_folder_show_lineedit.setEnabled(False)
        log_folder_show_lineedit.setStyleSheet("background: #454545;"
                                               "border: 0px;"
                                               "color: white;"
                                               "border-radius: 5px;"
                                               "font-family: Verdana;"
                                               "font-size: 10px;")

        set_log_folder_layout.addWidget(set_log_label)
        set_log_folder_layout.addWidget(set_log_button)
        set_log_folder_layout.addWidget(log_folder_show_lineedit)
        set_log_folder_layout.setSpacing(10)

        main_layout = QVBoxLayout()
        main_layout.addLayout(set_source_folder_layout)
        main_layout.addLayout(set_label_folder_layout)
        main_layout.addLayout(set_log_folder_layout)
        main_layout.setAlignment(Qt.AlignTop)
        main_layout.setSpacing(15)

        self.input_output.setLayout(main_layout)

        self.set_source_button = set_source_button
        self.source_folder_show_lineedit = source_folder_show_lineedit
        self.set_label_button = set_label_button
        self.label_folder_show_lineedit = label_folder_show_lineedit
        self.set_log_button = set_log_button
        self.log_folder_show_lineedit = log_folder_show_lineedit
