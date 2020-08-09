# -*- coding: UTF-8 -*-

import os.path as osp
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import pyqtgraph as pg
from ..utils import get_icon
from ..utils import instance_widget_stylesheet


class CorrectionTools(QWidget):

    def __init__(self):
        super().__init__()

        self.instance_widget_stylesheet = instance_widget_stylesheet

        self.setup_ui()

    def setup_ui(self):
        qtooltips_style_sheet = """
        QPushButton {border:0px;}
        QToolTip
            {
                font-family: Verdana;
                color: black;
                background-color: rgb(255, 255, 255);
            }
        """
        ins_label = QLabel()
        ins_label.setText("Cells")
        ins_label.setAlignment(Qt.AlignVCenter)
        ins_label.setStyleSheet("color: white;"
                                "background: transparent;")

        add_instance_button = QPushButton()
        add_instance_button.setToolTip("Add a new cell")
        add_instance_button.setIcon(QIcon((get_icon("square-plus.png"))))
        add_instance_button.setIconSize(QSize(18, 18))
        add_instance_button.setFixedSize(QSize(20, 20))
        add_instance_button.setFlat(True)
        add_instance_button.setStyleSheet(qtooltips_style_sheet)

        instances_widget = QListWidget()
        instances_widget.setStyleSheet(self.instance_widget_stylesheet)
        instances_widget.setIconSize(QSize(30, 30))
        instances_widget.setFont(QFont("Verdana", 10))

        size_editor = QLineEdit()
        size_editor.setFixedSize(QSize(20, 20))
        size_editor.setAlignment(Qt.AlignCenter)
        size_editor.setText(str(3))
        size_editor.setValidator(QIntValidator())
        size_editor.setStyleSheet("background: #545454;"
                                  "border: 0px;"
                                  "border-radius: 3px;"
                                  "color: white;")

        size_left_button = QPushButton()
        size_left_button.setIcon(QIcon((get_icon("left.png"))))
        size_left_button.setIconSize(QSize(15, 15))
        size_left_button.setFixedSize(QSize(15, 15))
        size_left_button.setFlat(True)
        size_left_button.setStyleSheet(qtooltips_style_sheet)

        size_right_button = QPushButton()
        size_right_button.setIcon(QIcon((get_icon("right.png"))))
        size_right_button.setIconSize(QSize(15, 15))
        size_right_button.setFixedSize(QSize(15, 15))
        size_right_button.setFlat(True)
        size_right_button.setStyleSheet(qtooltips_style_sheet)

        brush_button = QPushButton()
        brush_button.setToolTip("Brush")
        brush_button.setIcon(QIcon((get_icon("pen.png"))))
        brush_button.setIconSize(QSize(18, 18))
        brush_button.setFixedSize(QSize(25, 25))
        brush_button.setFlat(True)
        brush_button.setStyleSheet(qtooltips_style_sheet)

        eraser_button = QPushButton()
        eraser_button.setToolTip("Eraser")
        eraser_button.setIcon(QIcon((get_icon("eraser.png"))))
        eraser_button.setIconSize(QSize(20, 20))
        eraser_button.setFixedSize(QSize(25, 25))
        eraser_button.setFlat(True)
        eraser_button.setStyleSheet(qtooltips_style_sheet)

        drag_button = QPushButton()
        drag_button.setToolTip("Drag")
        drag_button.setIcon(QIcon((get_icon("hand.png"))))
        drag_button.setIconSize(QSize(25, 25))
        drag_button.setFixedSize(QSize(25, 25))
        drag_button.setFlat(True)
        drag_button.setStyleSheet(qtooltips_style_sheet)

        confirm_button = QPushButton()
        confirm_button.setToolTip("Update all changes")
        confirm_button.setIcon(QIcon((get_icon("check.png"))))
        confirm_button.setIconSize(QSize(23, 23))
        confirm_button.setFixedSize(QSize(25, 25))
        confirm_button.setFlat(True)
        confirm_button.setStyleSheet(qtooltips_style_sheet)

        delete_button = QPushButton()
        delete_button.setToolTip("Delete chose cell")
        delete_button.setIcon(QIcon((get_icon("trash.png"))))
        delete_button.setIconSize(QSize(20, 20))
        delete_button.setFixedSize(QSize(25, 25))
        delete_button.setFlat(True)
        delete_button.setStyleSheet(qtooltips_style_sheet)

        assist_frame = pg.ImageView(self)
        assist_frame.ui.roiBtn.hide()
        assist_frame.ui.menuBtn.hide()
        assist_frame.ui.histogram.hide()
        colormap = pg.ColorMap([0, 1], color=[[0, 0, 0], [255, 255, 255]])
        assist_frame.setColorMap(colormap)
        assist_frame.view.mouseClickEvent = self.my_mouse_click_event

        sub_layout_top = QHBoxLayout()
        sub_layout_top.addWidget(ins_label)
        sub_layout_top.addWidget(add_instance_button)
        sub_layout_top.addWidget(delete_button)

        size_layout = QHBoxLayout()
        size_layout.setSpacing(0)
        size_layout.addWidget(size_left_button)
        size_layout.addWidget(size_editor)
        size_layout.addWidget(size_right_button)

        sub_layout_bottom = QHBoxLayout()
        sub_layout_bottom.addWidget(brush_button)
        sub_layout_bottom.addWidget(eraser_button)
        sub_layout_bottom.addLayout(size_layout)
        sub_layout_bottom.addWidget(drag_button)
        sub_layout_bottom.addWidget(confirm_button)

        annotation_layout = QVBoxLayout()
        annotation_layout.addLayout(sub_layout_top)
        annotation_layout.addWidget(instances_widget)
        annotation_layout.addLayout(sub_layout_bottom)
        annotation_layout.setSpacing(3)
        annotation_layout.setContentsMargins(5, 5, 5, 0)

        assist_layout = QVBoxLayout()
        assist_layout.addWidget(assist_frame)

        self.right_layout = QVBoxLayout()
        self.right_layout.setContentsMargins(1, 0, 0, 0)
        self.right_layout.addLayout(annotation_layout)
        self.right_layout.addLayout(assist_layout)
        self.right_layout.setStretch(0, 4)
        self.right_layout.setStretch(1, 2)

        right_widget = QWidget()  # 创建右侧部件
        right_widget.setStyleSheet("background-color:#414141;")
        right_widget.setFixedWidth(250)
        right_widget.setLayout(self.right_layout)

        self.assist_frame = assist_frame
        self.brush_button = brush_button
        self.confirm_button = confirm_button
        self.eraser_button = eraser_button
        self.add_instance_button = add_instance_button
        self.instances_widget = instances_widget
        self.delete_button = delete_button
        self.ins_label = ins_label
        self.right_widget = right_widget
        self.size_editor = size_editor
        self.size_left_button = size_left_button
        self.size_right_button = size_right_button
        self.drag_button = drag_button

    def my_mouse_click_event(self, ev):
        if ev.button() == Qt.RightButton:
            ev.ignore()
