# -*- coding: UTF-8 -*-

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *


class Optimizer(QWidget):
    def __init__(self):
        super().__init__()

        self.optimizer = QWidget()

        self.setup_ui()

    def setup_ui(self):
        weight_decay_label = QLabel()
        weight_decay_label.setText("Weight decay:")
        weight_decay_label.setStyleSheet("font-family: Verdana;"
                                         "color: white;")

        weight_decay_select = QComboBox()
        weight_decay_select.setStyleSheet("border: 0px;"
                                          "color: white;"
                                          "font-family: Verdana;"
                                          "background: #353535;")
        weight_decay_select.addItem("0.0001")
        weight_decay_select.addItem("0.0005")
        weight_decay_select.addItem("0.001")
        weight_decay_select.addItem("0.005")
        weight_decay_select.addItem("0.01")
        weight_decay_select.setCurrentIndex(1)

        weight_decay_layout = QHBoxLayout()
        weight_decay_layout.addWidget(weight_decay_label)
        weight_decay_layout.addWidget(weight_decay_select)

        lr_label = QLabel()
        lr_label.setText("Learning rate:")
        lr_label.setStyleSheet("font-family: Verdana;"
                               "color: white;")

        lr_select = QComboBox()
        lr_select.setStyleSheet("border: 0px;"
                                "color: white;"
                                "font-family: Verdana;"
                                "background: #353535;")

        lr_select.addItem("0.001")
        lr_select.addItem("0.01")
        lr_select.addItem("0.1")
        lr_select.setCurrentIndex(0)

        lr_layout = QHBoxLayout()
        lr_layout.addWidget(lr_label)
        lr_layout.addWidget(lr_select)

        optimizer_layout = QVBoxLayout()
        optimizer_layout.addLayout(weight_decay_layout)
        optimizer_layout.addLayout(lr_layout)

        self.optimizer.setLayout(optimizer_layout)

        self.weight_decay_select = weight_decay_select
        self.lr_select = lr_select
