import os
import sys
from os.path import expanduser

from PyQt5.QtWidgets import QMainWindow, QDesktopWidget, QApplication, \
    QFileDialog, QMessageBox

from capstone_project.frontend import qt_ui
from capstone_project.frontend.ddssa import DDSSA


class UI(QMainWindow):
    """ UI Represents the main graphical user interface
    that serves as the entry-point for the application.

    This class relies on the qt_ui.py file that is generated
    by running the following command from the frontend directory:
      pyuic5 -o qt_ui.py main.ui

    Run the application from the root project directory using
    the following command (note os.sep might need to change)
    """

    def __init__(self):
        super().__init__()
        self.ui = qt_ui.Ui_main_window()
        self.ui.setupUi(self)

        self.ui.file_select_btn.clicked.connect(self._analyze)

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
        input_dir = QFileDialog.getExistingDirectory(
            None, 'Select a directory or .py file', expanduser("~"))
        if input_dir == "" or not os.path.isdir(input_dir):
            self.msg.setWindowTitle("Invalid Selection")
            self.msg.setIcon(QMessageBox.Information)
            self.msg.setText("Please select a directory or .py file.")
            self.msg.setStandardButtons(QMessageBox.Ok)
            self.msg.exec_()
            return None
        return input_dir

    def _display_report(self):
        self.ui.text_browser.setText(
            f'Report generated at {os.path.join(os.getcwd(), "report.pdf")}')


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = UI()
    window.show()

    sys.exit(app.exec_())
