"""This module contains the FileExport class"""


class FileExport:
    """Class for exporting files."""

    @staticmethod
    def export_html(filename, content):
        """Export an html report to a file."""
        with open(filename, "w", encoding="UTF-8") as f:
            f.write(content)
