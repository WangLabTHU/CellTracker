# -*- coding: UTF-8 -*-

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *


class WeightedLoss(QWidget):
    def __init__(self):
        super().__init__()

        self.weighted_loss = QWidget()

        self.setup_ui()

    def setup_ui(self):
        weighted_loss_label = QLabel()
        weighted_loss_label.setText("Weight:")
        weighted_loss_label.setStyleSheet("font-family: Verdana;"
                                          "color: white;")

        weighted_loss_select = QComboBox()
        weighted_loss_select.setMinimumWidth(160)
        weighted_loss_select.setStyleSheet("border: 0px;"
                                           "color: white;"
                                           "font-family: Verdana;"
                                           "background: #353535;")
        weighted_loss_select.addItem("Edge Enhance")
        weighted_loss_select.addItem("Sample balance")
        weighted_loss_select.addItem("No")
        weighted_loss_select.setCurrentIndex(2)

        weighted_loss_layout = QHBoxLayout()
        weighted_loss_layout.addWidget(weighted_loss_label)
        weighted_loss_layout.addWidget(weighted_loss_select)

        self.weighted_loss.setLayout(weighted_loss_layout)

        self.weighted_loss_select = weighted_loss_select
