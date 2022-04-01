# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './ddssa/frontend/main.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_main_window(object):
    def setupUi(self, main_window):
        main_window.setObjectName("main_window")
        main_window.resize(1000, 750)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            main_window.sizePolicy().hasHeightForWidth())
        main_window.setSizePolicy(sizePolicy)
        self.centralwidget = QtWidgets.QWidget(main_window)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.dir_select_btn = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.dir_select_btn.sizePolicy().hasHeightForWidth())
        self.dir_select_btn.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.dir_select_btn.setFont(font)
        self.dir_select_btn.setObjectName("dir_select_btn")
        self.verticalLayout.addWidget(self.dir_select_btn)
        self.file_select_btn = QtWidgets.QPushButton(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.file_select_btn.setFont(font)
        self.file_select_btn.setObjectName("file_select_btn")
        self.verticalLayout.addWidget(self.file_select_btn)
        self.text_browser = QtWidgets.QTextBrowser(self.centralwidget)
        self.text_browser.setStyleSheet("font: 12pt \"MS Shell Dlg 2\";")
        self.text_browser.setObjectName("text_browser")
        self.verticalLayout.addWidget(self.text_browser)
        main_window.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(main_window)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1000, 27))
        self.menubar.setObjectName("menubar")
        self.menuOptions = QtWidgets.QMenu(self.menubar)
        self.menuOptions.setObjectName("menuOptions")
        self.menuExport = QtWidgets.QMenu(self.menubar)
        self.menuExport.setObjectName("menuExport")
        main_window.setMenuBar(self.menubar)
        self.menu_action_help = QtWidgets.QAction(main_window)
        self.menu_action_help.setObjectName("menu_action_help")
        self.menu_action_quit = QtWidgets.QAction(main_window)
        self.menu_action_quit.setObjectName("menu_action_quit")
        self.menu_action_export_HTML = QtWidgets.QAction(main_window)
        self.menu_action_export_HTML.setObjectName("menu_action_export_HTML")
        self.menu_action_export_PDF = QtWidgets.QAction(main_window)
        self.menu_action_export_PDF.setObjectName("menu_action_export_PDF")
        self.menu_action_add_api_key = QtWidgets.QAction(main_window)
        self.menu_action_add_api_key.setCheckable(False)
        self.menu_action_add_api_key.setObjectName("menu_action_add_api_key")
        self.menuOptions.addAction(self.menu_action_help)
        self.menuOptions.addAction(self.menu_action_add_api_key)
        self.menuOptions.addAction(self.menu_action_quit)
        self.menuExport.addAction(self.menu_action_export_HTML)
        self.menuExport.addAction(self.menu_action_export_PDF)
        self.menubar.addAction(self.menuOptions.menuAction())
        self.menubar.addAction(self.menuExport.menuAction())

        self.retranslateUi(main_window)
        QtCore.QMetaObject.connectSlotsByName(main_window)

    def retranslateUi(self, main_window):
        _translate = QtCore.QCoreApplication.translate
        main_window.setWindowTitle(_translate(
            "main_window", "Data-Driven Software Security Assessment"))
        self.dir_select_btn.setText(_translate(
            "main_window", "Choose a Python Project Directory"))
        self.file_select_btn.setText(_translate(
            "main_window", "Choose a Python File"))
        self.text_browser.setHtml(_translate("main_window", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
                                             "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
                                             "p, li { white-space: pre-wrap; }\n"
                                             "</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:12pt; font-weight:400; font-style:normal;\">\n"
                                             "<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:\'Times New Roman\';\"><br /></p></body></html>"))
        self.menuOptions.setTitle(_translate("main_window", "Options"))
        self.menuExport.setTitle(_translate("main_window", "Export"))
        self.menu_action_help.setText(_translate("main_window", "Help"))
        self.menu_action_quit.setText(_translate("main_window", "Quit"))
        self.menu_action_quit.setToolTip(
            _translate("main_window", "Quit the program"))
        self.menu_action_export_HTML.setText(_translate("main_window", "HTML"))
        self.menu_action_export_PDF.setText(_translate("main_window", "PDF"))
        self.menu_action_add_api_key.setText(
            _translate("main_window", "Add API Key"))
        self.menu_action_add_api_key.setToolTip(
            _translate("main_window", "Add your NIST NVD API Key"))
