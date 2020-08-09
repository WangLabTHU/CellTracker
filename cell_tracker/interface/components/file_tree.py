# -*- coding: UTF-8 -*-

import os
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QDesktopServices, QIcon
from PyQt5.QtCore import QFileInfo, QUrl
from PyQt5 import QtGui
from PyQt5 import QtCore
from ..utils import get_icon, left_tools_stylesheet, instance_widget_stylesheet


class FileTree(QWidget):
    def __init__(self, dir_path=None, view_flag=0):
        super(FileTree, self).__init__()
        self.dir_path = dir_path
        self.view_flag = view_flag

        self.setup_ui()

    def setup_ui(self):
        if self.dir_path is None:
            create_button = QPushButton()
            create_button.setText("Open folder")
            create_button.setStyleSheet("background: #454545;"
                                        "color: rgb(245, 245, 245);"
                                        "font-size: 12px;"
                                        "font-family: Verdana;")
            create_button.setContentsMargins(0, 0, 0, 0)
            create_button.setFixedHeight(25)

            label = QLabel()
            label.setText("You have not yet set project folder.")
            label.setStyleSheet("color: rgb(245, 245, 245);"
                                "font-size: 12px;"
                                "font-family: Verdana;")
            label.setContentsMargins(0, 0, 0, 0)

            label1 = QLabel()
            label1.setText("Otherwise the default folder is:")
            label1.setStyleSheet("color: rgb(245, 245, 245);"
                                 "font-size: 12px;"
                                 "font-family: Verdana;")
            label1.setContentsMargins(0, 0, 0, 0)

            default_button = QPushButton()
            default_button.setText("Use .output/untitled")
            default_button.setStyleSheet("background: #454545;"
                                         "color: rgb(245, 245, 245);"
                                         "font-size: 12px;"
                                         "font-family: Verdana;")
            default_button.setContentsMargins(0, 0, 0, 0)
            default_button.setFixedHeight(25)

            load_button = QPushButton()
            load_button.setText("Load images")
            load_button.setStyleSheet("background: #454545;"
                                      "color: rgb(245, 245, 245);"
                                      "font-size: 12px;"
                                      "font-family: Verdana;")
            load_button.setContentsMargins(0, 0, 0, 0)
            load_button.setFixedHeight(25)

            label2 = QLabel()
            label2.setText("Load images or set image files folder.")
            label2.setStyleSheet("color: rgb(245, 245, 245);"
                                 "font-size: 12px;"
                                 "font-family: Verdana;")
            label2.setContentsMargins(0, 0, 0, 0)

            layout1 = QVBoxLayout()
            layout1.addWidget(label2)
            layout1.addWidget(load_button)
            layout1.addWidget(label)
            layout1.addWidget(create_button)
            layout1.addWidget(label1)
            layout1.addWidget(default_button)
            layout1.setSpacing(10)

            layout2 = QVBoxLayout()
            layout2.addLayout(layout1)
            layout2.setAlignment(QtCore.Qt.AlignTop)

            self.setLayout(layout2)
            self.create_button = create_button
            self.default_button = default_button
            self.load_button = load_button

        elif self.view_flag == 1 and self.dir_path is not None:
            self.tool_box = QToolBox()

            self.basic_settings_button = QPushButton()
            self.basic_settings_button.setStyleSheet("background: #454545;"
                                                     "font-family: Verdana;"
                                                     "font-size: 14px;"
                                                     "border: 0px;"
                                                     "text-align:left;")
            self.basic_settings_button.setFixedHeight(25)
            self.basic_settings_button.setText("Basic settings")
            self.basic_settings_button.clicked.connect(
                self.basic_settings_button_fnc)
            self.basic_settings_button.setIcon(
                QIcon(get_icon("Arrow_right.png")))

            widget1 = QWidget()

            create_button = QPushButton()
            create_button.setText("Open folder")
            create_button.setStyleSheet("background: #454545;"
                                        "color: rgb(245, 245, 245);"
                                        "font-size: 12px;"
                                        "font-family: Verdana;"
                                        "border: 0px;")
            create_button.setContentsMargins(0, 0, 0, 0)
            create_button.setFixedHeight(25)

            label = QLabel()
            label.setText("You have not yet set project folder.")
            label.setStyleSheet("color: rgb(245, 245, 245);"
                                "font-size: 12px;"
                                "font-family: Verdana;")
            label.setContentsMargins(0, 0, 0, 0)

            label1 = QLabel()
            label1.setText("Otherwise the default folder is:")
            label1.setStyleSheet("color: rgb(245, 245, 245);"
                                 "font-size: 12px;"
                                 "font-family: Verdana;")
            label1.setContentsMargins(0, 0, 0, 0)

            default_button = QPushButton()
            default_button.setText("Use .output/untitled")
            default_button.setStyleSheet("background: #454545;"
                                         "color: rgb(245, 245, 245);"
                                         "font-size: 12px;"
                                         "font-family: Verdana;"
                                         "border: 0px;")
            default_button.setContentsMargins(0, 0, 0, 0)
            default_button.setFixedHeight(25)

            load_button = QPushButton()
            load_button.setText("Load images")
            load_button.setStyleSheet("background: #454545;"
                                      "color: rgb(245, 245, 245);"
                                      "font-size: 12px;"
                                      "font-family: Verdana;"
                                      "border: 0px;")
            load_button.setContentsMargins(0, 0, 0, 0)
            load_button.setFixedHeight(25)

            label2 = QLabel()
            label2.setText("Load images or set image files folder.")
            label2.setStyleSheet("color: rgb(245, 245, 245);"
                                 "font-size: 12px;"
                                 "font-family: Verdana;")
            label2.setContentsMargins(0, 0, 0, 0)

            layout1 = QVBoxLayout()
            layout1.addWidget(label2)
            layout1.addWidget(load_button)
            layout1.addWidget(label)
            layout1.addWidget(create_button)
            layout1.addWidget(label1)
            layout1.addWidget(default_button)
            layout1.setSpacing(10)
            layout1.setAlignment(QtCore.Qt.AlignTop)

            widget1.setLayout(layout1)
            widget1.setStyleSheet("background: #323232;"
                                  "padding: 0px;")

            self.file_system_button = QPushButton()
            self.file_system_button.setStyleSheet("background: #454545;"
                                                  "font-family: Verdana;"
                                                  "font-size: 14px;"
                                                  "border: 0px;"
                                                  "text-align:left;")
            self.file_system_button.setFixedHeight(25)
            self.file_system_button.setText("File system")
            self.file_system_button.clicked.connect(
                self.file_system_button_fnc)
            self.file_system_button.setIcon(QIcon(get_icon("Arrow_right.png")))

            self.create_button = create_button
            self.default_button = default_button
            self.load_button = load_button

            widget2 = QWidget()
            widget2.setStyleSheet("background: #323232;")
            tree_stylesheet = """
                        QTreeWidget 
                        {
                            font-family: Verdana;
                            color: rgb(245, 245, 245);
                            border: 0px;
                        }
                        """
            tree = QTreeWidget()
            tree.doubleClicked.connect(self.open_file)
            tree.setStyleSheet(tree_stylesheet)
            tree.setColumnCount(1)
            tree.setColumnWidth(0, 50)
            tree.setHeaderHidden(True)
            tree.setHeaderLabel("EXPLORE")
            tree.setSelectionMode(QAbstractItemView.ExtendedSelection)
            tree.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)

            dirs = os.listdir(self.dir_path)

            file_info = QFileInfo(self.dir_path)
            file_icon = QFileIconProvider()
            icon = QtGui.QIcon(file_icon.icon(file_info))
            tree_root = QTreeWidgetItem(tree)
            tree_root.setText(0, self.dir_path.split('/')[-1])
            tree_root.setIcon(0, QtGui.QIcon(icon))
            self.create_tree(dirs, tree_root, self.dir_path)
            layout3 = QVBoxLayout()
            layout3.addWidget(tree)
            widget2.setLayout(layout3)

            self.tree = tree

            # self.tool_box.addItem(self.widget2, "File system")
            # self.tool_box.addItem(self.widget1, "Basic settings")
            # self.tool_box.setStyleSheet(left_tools_stylesheet)

            self.main_layout = QVBoxLayout()
            self.main_layout.setContentsMargins(0, 0, 0, 0)
            self.main_layout.setAlignment(QtCore.Qt.AlignTop)
            self.main_layout.setSpacing(1)
            self.main_layout.addWidget(self.basic_settings_button)
            self.main_layout.addWidget(widget1)
            widget1.setVisible(False)
            self.main_layout.addWidget(self.file_system_button)
            self.main_layout.addWidget(widget2)
            widget2.setVisible(False)

            # main_layout.addWidget(self.tool_box)
            self.setLayout(self.main_layout)
            self.widget1 = widget1
            self.widget2 = widget2

        else:
            tree_stylesheet = """
            QTreeWidget 
            {
                font-family: Verdana;
                color: rgb(245, 245, 245);
            }
            """
            tree = QTreeWidget()
            tree.doubleClicked.connect(self.open_file)
            tree.setStyleSheet(tree_stylesheet)
            tree.setColumnCount(1)
            tree.setColumnWidth(0, 50)
            tree.setHeaderHidden(True)
            tree.setHeaderLabel("EXPLORE")
            tree.setSelectionMode(QAbstractItemView.ExtendedSelection)
            tree.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)

            dirs = os.listdir(self.dir_path)

            file_info = QFileInfo(self.dir_path)
            file_icon = QFileIconProvider()
            icon = QtGui.QIcon(file_icon.icon(file_info))
            tree_root = QTreeWidgetItem(tree)
            tree_root.setText(0, self.dir_path.split('/')[-1])
            tree_root.setIcon(0, QtGui.QIcon(icon))
            self.create_tree(dirs, tree_root, self.dir_path)
            layout2 = QHBoxLayout()
            layout2.addWidget(tree)
            self.setLayout(layout2)

            self.tree = tree

    def create_tree(self, dirs, root, path):
        for dir in dirs:
            new_path = os.path.join(path, dir)
            file_info = QFileInfo(new_path)
            file_icon = QFileIconProvider()
            icon = QtGui.QIcon(file_icon.icon(file_info))
            child_node = QTreeWidgetItem(root)
            child_node.setText(0, dir)
            child_node.setIcon(0, QtGui.QIcon(icon))
            if os.path.isdir(new_path):
                new_dirs = os.listdir(new_path)
                self.create_tree(new_dirs, child_node, new_path)

    def open_file(self):
        url_list = [self.tree.currentItem().text(0)]
        parent_item = self.tree.currentItem().parent()
        while parent_item is not None:
            url_list.append(parent_item.text(0))
            parent_item = parent_item.parent()
        url_list = url_list[:-1]
        url = "/".join(url_list[::-1])
        url = "/".join([self.dir_path, url])
        url_info = QFileInfo(url)
        if not url_info.isDir():
            QDesktopServices.openUrl(QUrl.fromLocalFile(url))

    def file_system_button_fnc(self):
        if self.widget2.isVisible():
            self.widget2.setVisible(False)
            self.file_system_button.setIcon(QIcon(get_icon("Arrow_right.png")))
            self.file_system_button.setStyleSheet("background: #454545;"
                                                  "font-family: Verdana;"
                                                  "font-size: 14px;"
                                                  "border: 0px;"
                                                  "text-align:left;"
                                                  "color: #000000")
        else:
            self.widget2.setVisible(True)
            self.file_system_button.setIcon(QIcon(get_icon("Arrow_down.png")))
            self.file_system_button.setStyleSheet("background: #454545;"
                                                  "font-family: Verdana;"
                                                  "font-size: 14px;"
                                                  "border: 0px;"
                                                  "text-align:left;"
                                                  "color: #FFFFFF")

    def basic_settings_button_fnc(self):
        if self.widget1.isVisible():
            self.widget1.setVisible(False)
            self.basic_settings_button.setIcon(
                QIcon(get_icon("Arrow_right.png")))
            self.basic_settings_button.setStyleSheet("background: #454545;"
                                                     "font-family: Verdana;"
                                                     "font-size: 14px;"
                                                     "border: 0px;"
                                                     "text-align:left;"
                                                     "color: #000000")
        else:
            self.widget1.setVisible(True)
            self.basic_settings_button.setIcon(
                QIcon(get_icon("Arrow_down.png")))
            self.basic_settings_button.setStyleSheet("background: #454545;"
                                                     "font-family: Verdana;"
                                                     "font-size: 14px;"
                                                     "border: 0px;"
                                                     "text-align:left;"
                                                     "color: #FFFFFF")
