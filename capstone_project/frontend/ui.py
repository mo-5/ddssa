import os
import sys
from functools import partial
from os.path import expanduser
from PyQt5 import QtGui, QtCore
from PyQt5.QtWidgets import (
    QMainWindow,
    QDesktopWidget,
    QApplication,
    QFileDialog,
    QMessageBox,
)

from capstone_project.frontend import main
from capstone_project.frontend.ddssa import DDSSA
from capstone_project.backend.file_generator.file_export import FileExport
from capstone_project.frontend.loading import LoadingScreen


class AnalysisWorker(QtCore.QObject):
    finished = QtCore.pyqtSignal(str)

    def run(self, target):
        """Perform analysis"""
        tool = DDSSA([target])
        # Display our report after analysis
        html = tool.analyze()
        self.finished.emit(html)


class UI(QMainWindow):
    """UI Represents the main graphical user interface
    that serves as the entry-point for the application.

    This class relies on the main.py file that is generated
    by running the following command from the frontend directory:
      pyuic5 -o main.py main.ui

    Run the application from the root project directory using
    the following command (note os.sep might need to change)
      python ./capstone_project/frontend/ui.py
    """

    def __init__(self):
        super(UI, self).__init__()

        self.ui = main.Ui_main_window()
        self.ui.setupUi(self)

        self.thread = QtCore.QThread()
        self.worker = AnalysisWorker()
        self.worker.moveToThread(self.thread)
        self.worker.finished.connect(self._display_report)

        # Set the icon
        self.setWindowIcon(
            QtGui.QIcon(
                os.path.join(
                    os.getcwd(), "capstone_project", "frontend", "assets", "icon.png"
                )
            )
        )

        # Prepare connections
        self.ui.menu_action_quit.triggered.connect(self._try_quit)
        self.ui.file_select_btn.clicked.connect(self._analyze)
        self.ui.menu_action_help.triggered.connect(self._display_help)

        # export files
        self.ui.menu_action_export_HTML.triggered.connect(self._export_html)
        self.ui.menu_action_export_PDF.triggered.connect(self._export_pdf)

        # until it has been implemented
        self.ui.menu_action_export_PDF.setEnabled(False)

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

    def _analyze(self):
        # Get our target directory or Python file
        target = self._get_file_path()
        if target is None:
            return

        self._loading_on()

        # Deal with PyQt bug that uses the wrong file separators for
        # Windows based operating systems.
        target = target.replace("/", "\\")
        self.thread.started.connect(partial(self.worker.run, target))
        self.thread.start()

    def _get_file_path(self):
        """Attempt to get the file path the user specifies"""
        input_dir = QFileDialog.getExistingDirectory(
            None, "Select a directory or .py file", expanduser(".")
        )
        if input_dir == "" or not os.path.isdir(input_dir):
            self.msg.setWindowTitle("Invalid Selection")
            self.msg.setIcon(QMessageBox.Information)
            self.msg.setText("Please select a directory or .py file.")
            self.msg.setStandardButtons(QMessageBox.Ok)
            self.msg.exec_()
            return None
        return input_dir

    def _display_report(self, report_html):
        """Display the HTML report generated by the analysis."""
        self.ui.text_browser.setText(report_html)
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
            "in order to see if any of the packages have known vulnerabilites. "
            "The final report which the tool generates will then inform the user about package vulnerabilities in order for them to "
            "consider these vulnerabilities. As an example, the user may decide to update their package version to the latest version "
            "in order to avoid vulnerabilities in an older version."
        )

    def _try_quit(self):
        """Attempt to safely exit the application.
        Triggered via a menu action.
        """
        self.close()

    def _export_html(self):
        """Export the HTML report to a file."""
        FileExport.export_html("report.html", self.ui.text_browser.toHtml())

    def _export_pdf(self):
        """Export the HTML report to a file."""
        FileExport.export_pdf("report.pdf", self.ui.text_browser.toHtml())

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
