# -*- coding: UTF-8 -*-

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from ..utils import get_icon


class AnnotationTools(QWidget):
    def __init__(self):
        super().__init__()

        self.annotation_tools_stylesheet = """
        QLabel
            {
                font-family: Verdana;
                font-size: 12px;
                color: rgb(245, 245, 245);
            }
        """

        self.annotation_tools = QWidget()
        self.annotation_tools.setStyleSheet(self.annotation_tools_stylesheet)

        self.setup_ui()

    def setup_ui(self):

        load_layout = QVBoxLayout()

        load_button = QPushButton()
        load_button.setText("Load images")
        load_button.setStyleSheet("background: #454545;"
                                  "color: rgb(245, 245, 245);")
        load_button.setContentsMargins(0, 0, 0, 0)
        load_button.setFixedHeight(25)

        origin_img_label = QLabel()
        origin_img_label.setText("Load the images to be annotated.")
        origin_img_label.setContentsMargins(0, 0, 0, 0)

        load_layout.addWidget(origin_img_label)
        load_layout.addWidget(load_button)
        load_layout.setSpacing(10)

        set_layout = QVBoxLayout()

        set_button = QPushButton()
        set_button.setText("Set path")
        set_button.setStyleSheet("background: #454545;"
                                 "color: rgb(245, 245, 245);")
        set_button.setContentsMargins(0, 0, 0, 0)
        set_button.setFixedHeight(25)

        set_path_label = QLabel()
        set_path_label.setText("Set the path to save results.")
        set_path_label.setContentsMargins(0, 0, 0, 0)

        save_label = QLabel()
        save_label.setText("Not saved.")
        save_label.setContentsMargins(0, 0, 0, 0)
        save_label.setAlignment(Qt.AlignRight)

        set_layout.addWidget(set_path_label)
        set_layout.addWidget(set_button)
        set_layout.setSpacing(10)

        result_path_show_lineedit = QLineEdit()
        result_path_show_lineedit.setPlaceholderText("Result path")
        result_path_show_lineedit.setEnabled(False)
        result_path_show_lineedit.setStyleSheet("background: #454545;"
                                                "border: 0px;"
                                                "color: white;"
                                                "border-radius: 5px;"
                                                "font-family: Verdana;"
                                                "font-size: 10px;")

        save_annotation_button = QPushButton()
        save_annotation_button.setText("Save")
        save_annotation_button.setFixedSize(60, 20)
        save_annotation_button.setStyleSheet("background: #454545;"
                                             "color: white;"
                                             "border-radius: 5px;"
                                             "font-family: Verdana;")

        finish_annotation_button = QPushButton()
        finish_annotation_button.setText("Finish")
        finish_annotation_button.setFixedSize(60, 20)
        finish_annotation_button.setStyleSheet("background: #454545;"
                                               "color: white;"
                                               "border-radius: 5px;"
                                               "font-family: Verdana;")

        buttons_layout = QHBoxLayout()

        main_layout = QVBoxLayout()
        main_layout.addLayout(load_layout)
        main_layout.addLayout(set_layout)
        main_layout.addWidget(result_path_show_lineedit)
        buttons_layout.addWidget(save_annotation_button)
        buttons_layout.addWidget(finish_annotation_button)
        main_layout.addLayout(buttons_layout)
        main_layout.addWidget(save_label)
        main_layout.setAlignment(Qt.AlignTop)
        main_layout.setSpacing(15)

        self.load_button = load_button
        self.set_button = set_button
        self.result_path_show_lineedit = result_path_show_lineedit
        self.save_annotation_button = save_annotation_button
        self.finish_annotation_button = finish_annotation_button
        self.save_label = save_label

        self.annotation_tools.setLayout(main_layout)
