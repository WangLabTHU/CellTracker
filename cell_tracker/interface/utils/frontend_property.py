# -*- coding: UTF-8 -*-

from __future__ import absolute_import

instance_widget_stylesheet = """
            QListWidget
            {
                background: #323232;
                border: 0px;
                color: rgb(245, 245, 245);
            }
            QScrollBar:vertical
                {
                    width:8px;
                    background:rgba(0,0,0,0%);
                    margin:0px,0px,0px,0px;
                    padding-top:0px;   /*上预留位置*/
                    padding-bottom:0px;    /*下预留位置*/
                }

                /*滚动条中滑块的样式*/
                QScrollBar::handle:vertical
                {
                    width:8px;
                    background:rgba(0,0,0,25%);
                    border-radius:4px;
                    min-height:20px;
                }

                /*鼠标触及滑块样式*/
                QScrollBar::handle:vertical:hover
                {
                    width:9px;
                    background:rgba(0,0,0,50%);
                    border-radius:4px;
                    min-height:20;
                }

                /*设置下箭头*/
                QScrollBar::add-line:vertical
                {
                    height:12px;
                    width:10px;
                    border-image:url(:/selectfile/scroll/3.png);
                    subcontrol-position:bottom;
                }

                /*设置上箭头*/
                QScrollBar::sub-line:vertical
                {
                    height:12px;
                    width:10px;
                    border-image:url(:/selectfile/scroll/1.png);
                    subcontrol-position:top;
                }

                /*设置下箭头:悬浮状态*/
                QScrollBar::add-line:vertical:hover
                {
                    height:12px;
                    width:10px;
                    border-image:url(:/selectfile/scroll/4.png);
                    subcontrol-position:bottom;
                }

                /*设置上箭头：悬浮状态*/
                QScrollBar::sub-line:vertical:hover
                {
                    height:12px;
                    width:10px;
                    border-image:url(:/selectfile/scroll/2.png);
                    subcontrol-position:top;
                }

                /*当滚动条滚动的时候，上面的部分和下面的部分*/
                QScrollBar::add-page:vertical,QScrollBar::sub-page:vertical
                {
                    background:rgba(0,0,0,10%);
                    border-radius:4px;
                }
        """

slide_stylesheet = """QSlider:horizontal 
            {
                min-height: 20px;
            }
            QSlider::groove:horizontal {
                height: 1px;
                background: white; 
            }
            QSlider::handle:horizontal {
                width: 12px;
                margin-top: -6px;
                margin-bottom: -6px;
                border-radius: 6px;
                background: qradialgradient(spread:reflect, cx:0.5, cy:0.5, radius:0.5, fx:0.5, fy:0.5, stop:0.7 rgba(210, 210, 210, 255), stop:0.7 rgba(210, 210, 210, 255));
            }
            QSlider::handle:horizontal:hover {
                background: qradialgradient(spread:reflect, cx:0.5, cy:0.5, radius:0.5, fx:0.5, fy:0.5, stop:0.7 rgba(255, 255, 255, 255), stop:0.7 rgba(255, 255, 255, 255));
            }"""

segment_tools_stylesheet = """
            QToolBox 
            {
                background: #323232;
                padding-bottom: 0px;
            }
            QToolBox::tab 
            {
                font-family: Verdana;
                font-size: 12px;
                background: #353535;
                
            }
            QToolBoxButton 
            {
                min-height: 20px;
            }
            QToolBox::tab:selected 
            { 
                color: white;
            }
        """

left_tools_stylesheet = """
                    QToolBox 
                    {
                        background: #323232;
                        
                    }
                    QToolBox::tab 
                    {
                        font-family: Verdana;
                        font-size: 15px;
                        border-style: solid;
                        background: #454545;
                    }
                    QToolBoxButton 
                    {
                        min-height: 25px;
                    }
                    QToolBox::tab:selected 
                    { 
                        color: white;
                        background: #454545;
                    }
                """

normalize_tools_stylesheet = """
            QToolBox 
            {
                background: #323232;
                padding-bottom: 0px;
            }
            QToolBox::tab 
            {
                font-family: Verdana;
                font-size: 12px;
                background: #353535;
                
            }
            QToolBoxButton 
            {
                min-height: 20px;
            }
            QToolBox::tab:selected 
            { 
                color: white;
            }
        """

general_qss = """
            QSlider
            {
                background: #212121;
            }
            QSlider:horizontal 
            {
                min-height: 20px;
            }
            QSlider::groove:horizontal 
            {
                height: 1px;
                background: white; 
            }
            QSlider::handle:horizontal 
            {
                width: 12px;
                margin-top: -6px;
                margin-bottom: -6px;
                border-radius: 6px;
                background: qradialgradient(spread:reflect, cx:0.5, cy:0.5, radius:0.5, fx:0.5, fy:0.5, stop:0.7 rgba(210, 210, 210, 255), stop:0.7 rgba(210, 210, 210, 255));
            }
            QSlider::handle:horizontal:hover 
            {
                background: qradialgradient(spread:reflect, cx:0.5, cy:0.5, radius:0.5, fx:0.5, fy:0.5, stop:0.7 rgba(255, 255, 255, 255), stop:0.7 rgba(255, 255, 255, 255));
            }
            QToolTip
            {
                font-family: Verdana;
                color: rgb(245, 245, 245);
                background: #323232;
            }
            QLabel
            {
                font-family: Verdana;
                font-size: 12px;
                color: rgb(245, 245, 245);
            }
            QLineEdit
            {
                font-family: Verdana;
                font-size: 12px;
            }
            QPushButton
            {
                font-family: Verdana;
                font-size: 12px;
            }
        """

button_stylesheet = """"""

lineedit_stylesheet = """"""

