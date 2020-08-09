# -*- coding: UTF-8 -*-

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from ..utils import get_icon


class QuestionMessageBox(QWidget):
    """question warning infomation"""

    def __init__(self, message):
        super().__init__()
        self.message = message
        self.setup_ui()

    def setup_ui(self):
        icon_label = QLabel()
        pix = QPixmap(get_icon("question.png"))
        icon_label.setFixedSize(60, 60)
        icon_label.setPixmap(pix)

        message_label = QLabel()
        message_label.setText(self.message)
        message_label.setStyleSheet("font-family: Verdana;"
                                    "color: rgb(245, 245, 245);")
        message_label.setWordWrap(True)

        yes_button = QPushButton()
        yes_button.setText("Yes")
        yes_button.setFixedSize(80, 25)
        yes_button.setStyleSheet("font-family: Verdana;"
                                 "border-radius: 4px;"
                                 "background: #454545;"
                                 "color: rgb(245, 245, 245);")

        cancel_button = QPushButton()
        cancel_button.setText("Cancel")
        cancel_button.setFixedSize(80, 25)
        cancel_button.clicked.connect(self.close_fnc)
        cancel_button.setStyleSheet("font-family: Verdana;"
                                    "border-radius: 4px;"
                                    "background: #454545;"
                                    "color: rgb(245, 245, 245);")

        layout1 = QHBoxLayout()
        layout1.addWidget(icon_label)
        layout1.addWidget(message_label)
        layout2 = QHBoxLayout()
        layout2.addWidget(yes_button)
        layout2.addWidget(cancel_button)
        layout3 = QVBoxLayout()
        layout3.addLayout(layout1)
        layout3.addLayout(layout2)

        self.icon_label = icon_label
        self.message_label = message_label
        self.yes_button = yes_button
        self.cancel_button = cancel_button

        self.setLayout(layout3)
        self.setWindowIcon(QIcon(get_icon("cell.png")))
        self.setWindowTitle("Question")
        self.setFixedSize(400, 150)
        self.setStyleSheet("background: #323232;")

    def close_fnc(self):
        self.close()


class InformationMessageBox(QWidget):
    """question warning information"""

    def __init__(self, message):
        super().__init__()
        self.message = message
        self.setup_ui()

    def setup_ui(self):
        icon_label = QLabel()
        pix = QPixmap(get_icon("info.png"))
        icon_label.setFixedSize(60, 60)
        icon_label.setPixmap(pix)

        message_label = QLabel()
        message_label.setText(self.message)
        message_label.setStyleSheet("font-family: Verdana;"
                                    "color: rgb(245, 245, 245);")
        message_label.setWordWrap(True)

        ok_button = QPushButton()
        ok_button.setText("Ok")
        ok_button.setFixedSize(80, 25)
        ok_button.clicked.connect(self.close_fnc)
        ok_button.setStyleSheet("font-family: Verdana;"
                                "border-radius: 4px;"
                                "background: #454545;"
                                "color: rgb(245, 245, 245);")

        cancel_button = QPushButton()
        cancel_button.setText("Cancel")
        cancel_button.setFixedSize(80, 25)
        cancel_button.clicked.connect(self.close_fnc)
        cancel_button.setStyleSheet("font-family: Verdana;"
                                    "border-radius: 4px;"
                                    "background: #454545;"
                                    "color: rgb(245, 245, 245);")

        layout1 = QHBoxLayout()
        layout1.addWidget(icon_label)
        layout1.addWidget(message_label)
        layout2 = QHBoxLayout()
        layout2.addWidget(ok_button)
        layout3 = QVBoxLayout()
        layout3.addLayout(layout1)
        layout3.addLayout(layout2)

        self.icon_label = icon_label
        self.message_label = message_label
        self.ok_button = ok_button
        self.cancel_button = cancel_button

        self.setLayout(layout3)
        self.setWindowIcon(QIcon(get_icon("cell.png")))
        self.setWindowTitle("Information")
        self.setFixedSize(400, 150)
        self.setStyleSheet("background: #323232;")

    def close_fnc(self):
        self.close()


class WarningMessageBox(QWidget):
    """question warning information"""

    def __init__(self, message):
        super().__init__()
        self.message = message
        self.setup_ui()

    def setup_ui(self):
        icon_label = QLabel()
        pix = QPixmap(get_icon("warning.png"))
        icon_label.setFixedSize(60, 60)
        icon_label.setPixmap(pix)

        message_label = QLabel()
        message_label.setText(self.message)
        message_label.setStyleSheet("font-family: Verdana;"
                                    "color: rgb(245, 245, 245);")
        message_label.setWordWrap(True)

        ok_button = QPushButton()
        ok_button.setText("Ok")
        ok_button.setFixedSize(80, 25)
        ok_button.setStyleSheet("font-family: Verdana;"
                                "border-radius: 4px;"
                                "background: #454545;"
                                "color: rgb(245, 245, 245);")
        ok_button.clicked.connect(self.close_fnc)
        layout1 = QHBoxLayout()
        layout1.addWidget(icon_label)
        layout1.addWidget(message_label)
        layout2 = QHBoxLayout()
        layout2.addWidget(ok_button)
        layout3 = QVBoxLayout()
        layout3.addLayout(layout1)
        layout3.addLayout(layout2)

        self.icon_label = icon_label
        self.message_label = message_label

        self.setLayout(layout3)
        self.setWindowIcon(QIcon(get_icon("cell.png")))
        self.setWindowTitle("Warning")
        self.setFixedSize(400, 150)
        self.setStyleSheet("background: #323232;")

    def close_fnc(self):
        self.close()
