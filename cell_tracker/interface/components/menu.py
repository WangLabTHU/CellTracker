# -*- coding: UTF-8 -*-

from PyQt5.QtWidgets import *
from PyQt5.QtGui import QDesktopServices
from PyQt5.QtCore import QFileInfo, QUrl


class Menu(QWidget):

    def __init__(self, parent=None):
        super().__init__()

        self.menu_bar_style_sheet = """
            background-color:#525252;
        """
        self.menu_bar = QMenuBar()
        self.menu_bar.setStyleSheet(self.menu_bar_style_sheet)

        self.setup_ui()

    def setup_ui(self):
        # Initialize menu bar
        self.init_file()
        self.init_edit()
        self.init_run()
        self.init_help()

    def init_file(self):
        # File
        file_menu = self.menu_bar.addMenu("&File")

        new_project_act = QAction("Open project...", self)
        new_project_act.setShortcut('Ctrl+O')
        file_menu.addAction(new_project_act)

        default_project_act = QAction("Default project...", self)
        file_menu.addAction(default_project_act)

        load_act = QAction("&Load images...", self)
        load_act.setShortcut('Ctrl+L')
        file_menu.addAction(load_act)

        source_folder_act = QAction("Source folder...", self)
        file_menu.addAction(source_folder_act)

        label_folder_act = QAction("Label folder...", self)
        file_menu.addAction(label_folder_act)

        log_folder_act = QAction("Log folder...", self)
        file_menu.addAction(log_folder_act)

        exit_act = QAction("&Exit", self)
        exit_act.setShortcut('Ctrl+Q')
        file_menu.addAction(exit_act)

        self.file_menu = file_menu
        self.new_project_act = new_project_act
        self.default_project_act = default_project_act
        self.load_act = load_act
        self.source_folder_act = source_folder_act
        self.label_folder_act = label_folder_act
        self.log_folder_act = log_folder_act
        self.exit_act = exit_act

    def init_edit(self):
        edit_menu = self.menu_bar.addMenu("&Edit")

        brush_act = QAction("Brush", self)
        edit_menu.addAction(brush_act)

        eraser_act = QAction("Eraser", self)
        edit_menu.addAction(eraser_act)

        drag_act = QAction("Drag", self)
        edit_menu.addAction(drag_act)

        confirm_act = QAction("Confirm", self)
        edit_menu.addAction(confirm_act)

        save_act = QAction("Save annotation", self)
        save_act.setShortcut('Ctrl+S')
        edit_menu.addAction(save_act)

        self.edit_menu = edit_menu
        self.brush_act = brush_act
        self.eraser_act = eraser_act
        self.drag_act = drag_act
        self.confirm_act = confirm_act
        self.save_act = save_act

    def init_run(self):
        run_menu = self.menu_bar.addMenu("&Run")

        normalize_menu = run_menu.addMenu("&Normalization")
        equalize_act = QAction("Equalize Histogram", self)
        min_max_act = QAction("Min-Max", self)
        r_p_act = QAction("Retinex-MSRCP", self)
        r_r_act = QAction("Retinex-MSRCR", self)
        remove_act = QAction("Remove norm", self)
        normalize_menu.addAction(equalize_act)
        normalize_menu.addAction(min_max_act)
        normalize_menu.addAction(r_p_act)
        normalize_menu.addAction(r_r_act)
        normalize_menu.addAction(remove_act)

        segment_menu = run_menu.addMenu("&Segmentation")
        threshold_act = QAction("Threshold", self)
        unet_act = QAction("U-net", self)
        water_act = QAction("WaterShed", self)
        grabcut_act = QAction("GrabCut", self)
        segment_menu.addAction(threshold_act)
        segment_menu.addAction(unet_act)
        segment_menu.addAction(water_act)
        segment_menu.addAction(grabcut_act)

        track_act = QAction("Track", self)
        output_act = QAction("Export result", self)
        run_menu.addAction(track_act)
        run_menu.addAction(output_act)

        self.run_menu = run_menu
        self.equalize_act = equalize_act
        self.min_max_act = min_max_act
        self.r_p_act = r_p_act
        self.r_r_act = r_r_act
        self.remove_act = remove_act
        self.threshold_act = threshold_act
        self.unet_act = unet_act
        self.water_act = water_act
        self.grabcut_act = grabcut_act
        self.track_act = track_act
        self.output_act = output_act

    def init_help(self):
        help_menu = self.menu_bar.addMenu("&Help")

        gitlab_act = QAction("Gitlab", self)
        gitlab_act.triggered.connect(self.open_gitlab)
        tutorial_act = QAction("Tutorial", self)
        # tutorial_act.triggered.connect(self.open_tutorial)
        help_menu.addAction(gitlab_act)
        help_menu.addAction(tutorial_act)

        self.help_menu = help_menu
        self.gitlab_act = gitlab_act
        self.tutorial_act = tutorial_act

    def open_gitlab(self):
        QDesktopServices.openUrl(
            QUrl("https://gitlab.com/ecart18/cell-tracker.git"))

