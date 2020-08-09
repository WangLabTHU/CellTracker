# -*- coding: UTF-8 -*-

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import pyqtgraph as pg


class StatusBar(QWidget):

    def __init__(self):
        super().__init__()

        self.status_bar_stylesheet = """
            QStatusBar
                {
                background: #525252
                }
            QStatusBar::item
                {
                    border: 0px
                }
        """
        self.status_bar = QStatusBar()
        self.status_bar.setSizeGripEnabled(False)
        self.status_bar.setStyleSheet(self.status_bar_stylesheet)
        self.setup_ui()

    def setup_ui(self):

        work_info_label = QLabel()
        work_info_label.setText("")

        progressbar = QProgressBar()
        progressbar.setFixedSize(220, 4)
        progressbar.setMinimum(1)
        progressbar.setMaximum(10)
        progressbar.setTextVisible(False)
        progressbar.setVisible(False)
        progressbar.setStyleSheet("border: 0px solid #FFFFFF;"
                                  "border-radius: 2px;"
                                  "background: #CDC5BF;"
                                  "color:rgb(0, 0, 0);")

        frame_info_label = QLabel()
        frame_info_label.setText(" Current frame: INF")
        frame_info_label.setStyleSheet("border: 0px solid #FFFFFF;"
                                       "color: white;"
                                       "background: transparent;")

        frame_editor = QLineEdit()
        frame_editor.setFixedSize(QSize(20, 20))
        frame_editor.setText("")
        frame_editor.setValidator(QIntValidator())

        total_frame_label = QLabel()
        total_frame_label.setText(" Total frames: INF")

        self.status_bar.addPermanentWidget(work_info_label)
        self.status_bar.addPermanentWidget(progressbar)
        self.status_bar.addPermanentWidget(frame_info_label)
        self.status_bar.addPermanentWidget(total_frame_label)

        self.work_info_label = work_info_label
        self.progressbar = progressbar
        self.frame_info_label = frame_info_label
        self.frame_editor = frame_editor
        self.total_frame_label = total_frame_label

    def update_progressbar(self, val):
        self.progressbar.setValue(val)
        qApp.processEvents()
