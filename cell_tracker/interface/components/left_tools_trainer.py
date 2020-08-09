# -*- coding: UTF-8 -*-

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from ..utils import slide_stylesheet


class Trainer(QWidget):
    def __init__(self):
        super().__init__()

        self.trainer = QWidget()

        self.setup_ui()

    def setup_ui(self):
        epoch_sld = QSlider(Qt.Horizontal)
        epoch_sld.setMinimum(1)
        epoch_sld.setMaximum(20)
        epoch_sld.setValue(5)
        epoch_sld.setStyleSheet(slide_stylesheet)
        epoch_sld.valueChanged.connect(self.sld2text)

        epoch_label = QLabel()
        epoch_label.setText("epoch(20~400)")
        epoch_label.setAlignment(Qt.AlignLeft)
        epoch_label.setStyleSheet("font-family: Verdana;"
                                  "color: white;")

        epoch_textline = QLineEdit()
        epoch_textline.setAlignment(Qt.AlignCenter)
        epoch_textline.setFixedSize(50, 15)
        epoch_textline.setValidator(QIntValidator())
        epoch_textline.setText("100")
        epoch_textline.setStyleSheet("background: #454545;"
                                     "border: 0px;"
                                     "color: white;"
                                     "border-radius: 5px;"
                                     "font-family: Verdana;")
        epoch_textline.textEdited.connect(self.text2sld)

        epoch_layout = QVBoxLayout()
        epoch_layout1 = QHBoxLayout()
        epoch_layout1.addWidget(epoch_sld)
        epoch_layout1.addWidget(epoch_textline)
        epoch_layout.addWidget(epoch_label)
        epoch_layout.addLayout(epoch_layout1)

        gpu_num_label = QLabel()
        gpu_num_label.setText("GPU number:")
        gpu_num_label.setStyleSheet("font-family: Verdana;"
                                    "color: white;")

        gpu_num_select = QComboBox()
        gpu_num_select.setStyleSheet("border: 0px;"
                                     "color: white;"
                                     "font-family: Verdana;"
                                     "background: #353535;")
        gpu_num_select.addItem("0")
        gpu_num_select.addItem("1")
        gpu_num_select.addItem("2")
        gpu_num_select.addItem("4")
        gpu_num_select.setCurrentIndex(0)

        gpu_num_layout = QHBoxLayout()
        gpu_num_layout.addWidget(gpu_num_label)
        gpu_num_layout.addWidget(gpu_num_select)

        trainer_layout = QVBoxLayout()
        trainer_layout.addLayout(epoch_layout)
        trainer_layout.addLayout(gpu_num_layout)

        self.trainer.setLayout(trainer_layout)

        self.gpu_num_select = gpu_num_select
        self.epoch_textline = epoch_textline
        self.epoch_sld = epoch_sld

    def sld2text(self):
        f = self.epoch_sld.value() * 20
        self.epoch_textline.setText(str(f))

    def text2sld(self):
        t = int(self.epoch_textline.text())
        self.epoch_sld.setValue(int(t / 20))
