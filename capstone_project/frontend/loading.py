"""This module contains the LoadingScreen class"""


import os
from PyQt5 import QtGui, QtCore
from PyQt5.QtWidgets import (
    QWidget,
    QLabel,
)


class LoadingScreen(QWidget):
    """A class that displays a widget to represent loading"""

    def __init__(self):
        """Initialize the loading screen"""
        super(LoadingScreen, self).__init__()
        self.setFixedSize(200, 200)
        self.setWindowFlags(
            QtCore.Qt.WindowStaysOnTopHint
            | QtCore.Qt.CustomizeWindowHint
            | QtCore.Qt.FramelessWindowHint
        )

        # make background transparent
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        self.label_animation = QLabel(self)

        self.movie = QtGui.QMovie(
            os.path.join(
                os.getcwd(), "capstone_project", "frontend", "assets", "Loading.gif"
            )
        )
        self.label_animation.setMovie(self.movie)

    def start_animation(self):
        """Start the loading animation"""
        self.movie.start()
        self.show()

    def stop_animation(self):
        """Stop the loading animation"""
        self.movie.stop()
        self.close()
