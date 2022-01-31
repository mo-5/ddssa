

class FileExport:
    """ Class for exporting files """
    @staticmethod
    def export_html(filename, content):
        """Static method to export html report to a file"""
        with open(filename, "w") as f:
            f.write(content)

    @staticmethod
    def export_pdf(filename, content):
        """Static method to export pdf report to a file"""
        pass
