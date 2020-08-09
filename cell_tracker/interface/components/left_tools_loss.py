# -*- coding: UTF-8 -*-

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *


class Loss(QWidget):
    def __init__(self):
        super().__init__()

        self.loss = QWidget()

        self.setup_ui()

    def setup_ui(self):
        loss_label = QLabel()
        loss_label.setText("Loss:")
        loss_label.setStyleSheet("font-family: Verdana;"
                                 "color: white;")

        loss_select = QComboBox()
        loss_select.setMinimumWidth(160)
        loss_select.setStyleSheet("border: 0px;"
                                  "color: white;"
                                  "font-family: Verdana;"
                                  "background: #353535;")
        loss_select.addItem("DiceLoss")
        loss_select.addItem("WeightedSoftDice")
        loss_select.addItem("BCELoss")
        loss_select.addItem("WBCELoss")
        loss_select.addItem("MSELoss")
        loss_select.addItem("MAELoss")
        loss_select.setCurrentIndex(0)

        loss_layout = QHBoxLayout()
        loss_layout.addWidget(loss_label)
        loss_layout.addWidget(loss_select)

        self.loss.setLayout(loss_layout)

        self.loss_select = loss_select
