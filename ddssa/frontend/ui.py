import os
import sys
from functools import partial
from os.path import expanduser
from PyQt5 import QtGui, QtCore, QtPrintSupport
from PyQt5.QtWidgets import (
    QMainWindow,
    QDesktopWidget,
    QApplication,
    QFileDialog,
    QMessageBox,
    QInputDialog,
)

# Add the ddssa module to the system path if this is the entry point
if __name__ == "__main__":
    import sys

    sys.path.insert(
        0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
    )

from ddssa.frontend import main
from ddssa.frontend.ddssa import DDSSA
from ddssa.backend.file_generator.file_export import FileExport
from ddssa.frontend.loading import LoadingScreen


class AnalysisWorker(QtCore.QObject):
    finished = QtCore.pyqtSignal(str)

    def run(self, target, api_key=None):
        """Perform analysis"""
        tool = DDSSA([target], api_key)
        # Display our report after analysis
        html = tool.analyze()
        self.finished.emit(html)


class UI(QMainWindow):
    """UI Represents the main graphical user interface
    that serves as the entry-point for the application.

    This class relies on the main.py file that is generated
    by running the following command from the frontend directory:
      pyuic5 -o ./ddssa/frontend/main.py ./ddssa/frontend/main.ui

    Run the application from the root project directory using
    the following command (note os.sep might need to change)
      python ./ddssa/frontend/ui.py
    """

    def __init__(self):
        super(UI, self).__init__()

        # Setup user settings
        self.settings = QtCore.QSettings("DDSSA", "DDSSA")

        self.ui = main.Ui_main_window()
        self.ui.setupUi(self)
        self.thread = QtCore.QThread()
        self.thread.setTerminationEnabled(True)
        self.worker = AnalysisWorker()
        self.worker.moveToThread(self.thread)
        self.worker.finished.connect(self._display_report)
        self.icon = QtGui.QIcon(
            os.path.join(os.getcwd(), "ddssa", "frontend", "assets", "icon.png")
        )

        # Set the icon
        self.setWindowIcon(self.icon)

        # Prepare connections for menu actions and UI buttons
        self.ui.menu_action_help.triggered.connect(self._display_help)
        self.ui.menu_action_add_api_key.triggered.connect(self._add_api_key)
        self.ui.menu_action_quit.triggered.connect(self._try_quit)
        self.ui.menu_action_export_HTML.triggered.connect(self._export_html)
        self.ui.menu_action_export_PDF.triggered.connect(self._export_pdf)
        self.ui.dir_select_btn.clicked.connect(partial(self._analyze, True))
        self.ui.file_select_btn.clicked.connect(partial(self._analyze, False))

        # Prepare a message box
        self.msg = QMessageBox()

        # Open external links in the text browser
        self.ui.text_browser.setOpenExternalLinks(True)

        # Center the application on launch.
        frame = self.frameGeometry()
        center = QDesktopWidget().availableGeometry().center()
        frame.moveCenter(center)
        self.move(frame.topLeft())
        # set loading screen
        self.loading_screen = LoadingScreen()

    def _analyze(self, mode):
        # Get our target directory or Python file

        target = self._get_file_path(mode)
        if target is None:
            return

        self._loading_on()

        # Use the correct file separators for Windows based operating systems
        if os.name == "nt":
            target = target.replace("/", "\\")

        self.thread.started.connect(
            partial(self.worker.run, target, self.settings.value("api_key"))
        )
        self.thread.start()

    def _get_file_path(self, mode):
        """Attempt to get the file path the user specifies"""
        if mode:
            user_input = QFileDialog.getExistingDirectory(
                None, "Select a directory", expanduser(".")
            )
            if user_input == "" or not os.path.isdir(user_input):
                self.msg.setWindowTitle("Invalid Selection")
                self.msg.setWindowIcon(self.icon)
                self.msg.setIcon(QMessageBox.Information)
                self.msg.setText("Please select a directory")
                self.msg.setStandardButtons(QMessageBox.Ok)
                self.msg.exec_()
                return None
            return user_input
        else:
            user_input = QFileDialog.getOpenFileName(
                None, "Select a file", expanduser("."), "Python (*.py)"
            )
            if user_input[0] == "" or not os.path.isfile(user_input[0]):
                self.msg.setWindowTitle("Invalid Selection")
                self.msg.setWindowIcon(self.icon)
                self.msg.setIcon(QMessageBox.Information)
                self.msg.setText("Please select a file")
                self.msg.setStandardButtons(QMessageBox.Ok)
                self.msg.exec_()
                return None
            return user_input[0]

    def _display_report(self, report_html):
        """Display the HTML report generated by the analysis."""
        self.thread.disconnect()
        self.thread.terminate()
        self.ui.text_browser.setText(report_html)
        with open(
            os.path.join(os.getcwd(), "ddssa", "frontend", "assets", "report.css"),
            "r",
        ) as f:
            self.ui.text_browser.setStyleSheet(f.read())
        self._loading_off()

    def _display_help(self):
        """Display helpful information that includes how to use
        the application, alongside an explanation of what the
        application will be doing.
        """
        self.ui.text_browser.setHtml(
            "<h1>Data-Driven Security Assessment Tool</h1>"
            "</br><h2>Usage</h2>"
            "</br>Press the 'Choose a File or Directory' button to specify "
            "which Python file or project you would like to analyze. Once "
            "selected, analysis will immediately take place and the path "
            "to the generated report will be displayed."
            "</br>"
            "</br><h2>Stall Ratio and Stall Statements</h2>"
            "</br>Stall ratio is a measure of how much a program’s progress "
            "is impeded by frivolous activities within loops. "
            "It is calculated by taking the lines of non-progressive "
            "statements in a loop divided by the total lines in a loop. "
            "</br> Stall statements are the detected non-progressive "
            "statements identified in a loop. The recommendation is to move "
            "any detected stall statements outside of the loop to improve "
            "program efficiency to decrease impacts to accessibility when "
            "user's use your program."
            "<h2>Software Vulnerabilities</h2>"
            "</br>"
            "The <a href='https://csrc.nist.gov/glossary/term/software_vulnerability'>National Institute of Standards and Technology</a> defines a "
            "software vulnerability as being a, "
            '<blockquote>"A security flaw, glitch, or '
            'weakness found in software code that could be exploited by an attacker (threat source)."'
            "</blockquote>"
            "<h3>Dependency Vulnerabilities</h3>"
            "The reality about software projects is that they often depend on other "
            "libraries and packages in order to gain functionality from them. "
            "</br>"
            "When it comes to these dependencies, they can have vulnerabilities. "
            "<a href=https://docs.github.com/en/code-security/supply-chain-security/managing-vulnerabilities-in-your-projects-dependencies/about-alerts-for-vulnerable-dependencies>"
            "One source</a> sums it up by saying, "
            "<blockquote>"
            '"When your code depends on a package that has a security vulnerability, this vulnerable dependency can cause a range '
            'of problems for your project or the people who use it."'
            "</blockquote>"
            "This tool, the Data-Driven Security Assessment Tool, works by searching software projects to find all the packages "
            "that the project depends on. The tool then queries the <a href='https://nvd.nist.gov/developers/products'>CPE database</a> "
            "with the package names and version information "
            "to see if any of the packages have known vulnerabilities. "
            "The final report which the tool generates will then inform the user about package vulnerabilities in order for them to "
            "consider these vulnerabilities. As an example, the user may decide to update their package version to the latest version "
            "to avoid vulnerabilities in an older version."
        )

    def _add_api_key(self):
        dialog = QInputDialog(self)
        dialog.resize(450, 150)
        dialog.setWindowTitle("NIST NVD API Key Input")
        dialog.setLabelText("Enter your NIST NVD API key: ")
        confirm = dialog.exec_()
        if confirm:
            self.settings.setValue("api_key", dialog.textValue().strip())

    def _try_quit(self):
        """Attempt to safely exit the application.
        Triggered via a menu action.
        """
        self.close()

    def _export_prompt(self, type):
        """Attempt to get the file path the user specifies"""
        input_dir = QFileDialog.getSaveFileName(
            None, "Select where to store the file", expanduser("."), type
        )

        return input_dir[0]

    def _export_html(self):
        """Export the HTML report to a file."""
        input_dir = self._export_prompt("HTML (*.html)")
        if os.name == "nt":
            input_dir = input_dir.replace("/", "\\")
        if input_dir != "":
            FileExport.export_html(input_dir, self.ui.text_browser.toHtml())
        else:
            self.msg.setWindowTitle("Invalid Selection")
            self.msg.setWindowIcon(self.icon)
            self.msg.setIcon(QMessageBox.Information)
            self.msg.setText("Please add a file name and select a location")
            self.msg.setStandardButtons(QMessageBox.Ok)
            self.msg.exec_()

    def _export_pdf(self):
        """Export the HTML report to a file."""
        input_dir = self._export_prompt("PDF (*.pdf)")
        if os.name == "nt":
            input_dir = input_dir.replace("/", "\\")
        if input_dir != "":
            FileExport.export_html(input_dir, self.ui.text_browser.toHtml())
        else:
            self.msg.setWindowTitle("Invalid Selection")
            self.msg.setWindowIcon(self.icon)
            self.msg.setIcon(QMessageBox.Information)
            self.msg.setText("Please add a file name and select a location")
            self.msg.setStandardButtons(QMessageBox.Ok)
            self.msg.exec_()
            return
        export = QtPrintSupport.QPrinter(QtPrintSupport.QPrinter.HighResolution)
        export.setOutputFormat(QtPrintSupport.QPrinter.PdfFormat)
        export.setOutputFileName(input_dir)
        self.ui.text_browser.print(export)

    def _loading_on(self):
        self.loading_screen.start_animation()
        self.hide()

    def _loading_off(self):
        self.loading_screen.stop_animation()
        self.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = UI()
    window.show()

    sys.exit(app.exec_())
