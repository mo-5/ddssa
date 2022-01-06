import os
import sys
from os.path import expanduser

from PyQt5.QtWidgets import (
    QMainWindow,
    QDesktopWidget,
    QApplication,
    QFileDialog,
    QMessageBox,
)

from capstone_project.frontend import qt_ui
from capstone_project.frontend.ddssa import DDSSA


class UI(QMainWindow):
    """UI Represents the main graphical user interface
    that serves as the entry-point for the application.

    This class relies on the qt_ui.py file that is generated
    by running the following command from the frontend directory:
      pyuic5 -o qt_ui.py main.ui

    Run the application from the root project directory using
    the following command (note os.sep might need to change)
      python ./capstone_project/frontend/ui.py
    """

    def __init__(self):
        super().__init__()
        self.ui = qt_ui.Ui_main_window()
        self.ui.setupUi(self)

        # Prepare connections
        self.ui.menu_action_quit.triggered.connect(self._try_quit)
        self.ui.file_select_btn.clicked.connect(self._analyze)
        self.ui.menu_action_help.triggered.connect(self._display_help)

        # Prepare a message box
        self.msg = QMessageBox()

        # Center the application on launch.
        frame = self.frameGeometry()
        center = QDesktopWidget().availableGeometry().center()
        frame.moveCenter(center)
        self.move(frame.topLeft())

    def _analyze(self):
        # Get our target directory or Python file
        while True:
            target = self._get_file_path()
            if target is not None:
                break

        # Deal with PyQt bug that uses the wrong file separators for
        # Windows based operating systems.
        target = target.replace("/", "\\")

        self.ui.text_browser.setText("Analyzing...")

        tool = DDSSA([target])
        tool.analyze()

        # Display our report after analysis
        self._display_report()

    def _get_file_path(self):
        """Attempt to get the"""
        input_dir = QFileDialog.getExistingDirectory(
            None, "Select a directory or .py file", expanduser("~")
        )
        if input_dir == "" or not os.path.isdir(input_dir):
            self.msg.setWindowTitle("Invalid Selection")
            self.msg.setIcon(QMessageBox.Information)
            self.msg.setText("Please select a directory or .py file.")
            self.msg.setStandardButtons(QMessageBox.Ok)
            self.msg.exec_()
            return None
        return input_dir

    def _display_report(self):
        """Display the path to the generated report upon
        completion of analysis.
        Not triggered directly.
        """
        self.ui.text_browser.setText(
            f'Report generated at {os.path.join(os.getcwd(), "report.pdf")}'
        )

    def _display_help(self):
        """Display helpful information that includes how to use
        the application, alongside an explanation of what the
        application will be doing.
        """
        self.ui.text_browser.setHtml(
            "<h1>Data-Driven Security Assessment Tool</h1>"
            "</br><h2>Usage</h2>"
            "</br>Press the Choose a File or Directory button to specify "
            "which Python file or project you would like to analyze. Once "
            "selected, analysis will immediately take place and the path "
            "to the generated report will be displayed."
            "</br>"
            "</br><h2>Stall Ratio and Stall Statements</h2>"
            "</br>Stall ratio is a measure of how much a program’s progress "
            "is impeded by frivolous activities within loops. "
            "It is calculated by taking the lines of non-progressive "
            "statements in a loop divided by the total lines in a loop. "
            "</br> Stall Statements are the detected non-progressive "
            "statements identified in a loop. The recommendation is to move "
            "any detected Stall Statements outside of the loop to improve "
            "program efficiency to decrease impacts to accessibility when "
            "user's use your program."
        )

    def _try_quit(self):
        """Attempt to safely exit the application.
        Triggered via a menu action.
        """
        self.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = UI()
    window.show()

    sys.exit(app.exec_())
