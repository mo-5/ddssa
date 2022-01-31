class FileExport:

    @staticmethod
    def export_html(filename, content):
        """Export html report to a file"""
        with open(filename, "w") as f:
            f.write(content)
    
    @staticmethod
    def export_pdf(filename):
        """Export pdf report to a file"""
        pass
