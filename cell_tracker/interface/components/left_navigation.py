# -*- coding: UTF-8 -*-

import os.path as osp
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from ..utils import get_icon


class LeftNavigation(QWidget):

    def __init__(self, parent=None):
        super().__init__()

        self.left_navigation_stylesheet = """
            QListWidget
            {
                background-color:#414141;
            }
            QListWidget::item
            {
                font-size: 100px;
            }
            QToolTip
            {
                font-family: Verdana;
                color: black;
                background-color: rgb(255, 255, 255);
            }
        """
        self.left_navigation = QListWidget()
        self.left_navigation.setStyleSheet(self.left_navigation_stylesheet)

        self.setup_ui()

    def setup_ui(self):
        self.left_navigation.setContentsMargins(0, 0, 0, 0)
        self.left_navigation.setSpacing(0)
        self.left_navigation.setStyleSheet(self.left_navigation_stylesheet)
        self.left_navigation.setObjectName('left_widget')
        self.left_navigation.setIconSize(QSize(30, 30))
        self.left_navigation.setViewMode(QListView.IconMode)
        self.left_navigation.setFixedWidth(50)
        self.left_navigation.setItemAlignment(Qt.AlignCenter)
        self.left_navigation.setHorizontalScrollBarPolicy(
            Qt.ScrollBarAlwaysOff)
        self.left_navigation.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.left_navigation.setFrameShape(QListWidget.NoFrame)
        self.left_navigation.setAcceptDrops(False)

        icon_list = [get_icon(icon) for icon in ["project_management.png", "algorithm.png", "annotation.png",
                                                 "network_train.png"]]
        tool_tips = ["Explorer",
                     "Algorithm tools",
                     "Annotation tools",
                     "Training"]

        for i in range(4):
            item = QListWidgetItem(self.left_navigation)
            item.setSizeHint(QSize(50, 50))
            item.setToolTip(tool_tips[i])

            navigation_icon_widget = QWidget()
            navigation_icon_layout = QHBoxLayout()
            navigation_icon_layout.setContentsMargins(0, 0, 0, 0)
            navigation_icon_layout.setAlignment(Qt.AlignCenter)
            navigation_icon_label = QLabel()
            navigation_icon_label.setAlignment(Qt.AlignCenter)

            navigation_icon_label.setFixedSize(50, 50)
            navigation_icon_pix = QPixmap(icon_list[i])
            navigation_icon_pix = navigation_icon_pix.scaled(
                QSize(30, 30), Qt.KeepAspectRatio, Qt.SmoothTransformation)
            navigation_icon_label.setPixmap(navigation_icon_pix)
            navigation_icon_layout.addWidget(navigation_icon_label)
            navigation_icon_widget.setLayout(navigation_icon_layout)
            self.left_navigation.setItemWidget(item, navigation_icon_widget)
