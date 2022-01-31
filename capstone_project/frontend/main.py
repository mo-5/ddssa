# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\capstone_project\frontend\main.ui'
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
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(main_window.sizePolicy().hasHeightForWidth())
        main_window.setSizePolicy(sizePolicy)
        self.centralwidget = QtWidgets.QWidget(main_window)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.file_select_btn = QtWidgets.QPushButton(self.centralwidget)
        self.file_select_btn.setObjectName("file_select_btn")
        self.verticalLayout.addWidget(self.file_select_btn)
        self.text_browser = QtWidgets.QTextBrowser(self.centralwidget)
        self.text_browser.setObjectName("text_browser")
        self.verticalLayout.addWidget(self.text_browser)
        main_window.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(main_window)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1000, 21))
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
        self.menuOptions.addAction(self.menu_action_help)
        self.menuOptions.addAction(self.menu_action_quit)
        self.menuExport.addAction(self.menu_action_export_HTML)
        self.menuExport.addAction(self.menu_action_export_PDF)
        self.menubar.addAction(self.menuOptions.menuAction())
        self.menubar.addAction(self.menuExport.menuAction())

        self.retranslateUi(main_window)
        QtCore.QMetaObject.connectSlotsByName(main_window)

    def retranslateUi(self, main_window):
        _translate = QtCore.QCoreApplication.translate
        main_window.setWindowTitle(_translate("main_window", "Data-Driven Software Security Assessment"))
        self.file_select_btn.setText(_translate("main_window", "Choose a File or Directory"))
        self.menuOptions.setTitle(_translate("main_window", "Options"))
        self.menuExport.setTitle(_translate("main_window", "Export"))
        self.menu_action_help.setText(_translate("main_window", "Help"))
        self.menu_action_quit.setText(_translate("main_window", "Quit"))
        self.menu_action_export_HTML.setText(_translate("main_window", "HTML"))
        self.menu_action_export_PDF.setText(_translate("main_window", "PDF"))
