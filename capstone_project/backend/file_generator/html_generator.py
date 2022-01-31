class HTMLGenerator:
    """Generate html report from analysis data"""

    def __init__(self) -> None:
        """Initialize html report"""
        self.html = [
            "<h1>Data-Driven Software Security Assessment Report</h1>"]

    def add_sr_data(self, sr_data):
        """Add SR data to the HTML report"""
        if len(sr_data) > 0:
            self.html.append("<h2>Stall Statements</h2>")
            for sr_detection in sr_data:
                self.html.append(
                    f'<div>File <b>{sr_detection[0]}</b> contains {str(len(sr_detection[1]))}{" stall statements:</div>" if len(sr_detection[1]) > 1 else " stall statement:</div>"}'
                )
                self.html.append("<div><ol>")
                for i, _ in enumerate(sr_detection[1]):
                    self.html.append(
                        f"<li> Line number: {str(sr_detection[1][i][0])}, statement: {sr_detection[1][i][1].strip()}</li>"
                    )
                self.html.append("</ol></div>")

    def add_dependency_vulnerability_data(self, df):
        """Add depdencency vulnerability data to the html report"""
        if len(df.columns) > 0:
            self.html.append("<h2>Dependency Vulnerabilities</h2>")
            self.html.append(
                f'{"<div><div>The following dependencies have vulnerabilities:</div><ol>" if df.shape[1] > 1 else "<div><div>The following dependency has vulnerabilities:</div><ol>"}'
            )
            for _, col_data in df.iteritems():
                self.html.append(
                    "<li>"
                    + str(col_data.values[0])
                    + self._parse_version_list(col_data.values[1])
                    + "<ul>"
                )
                for cve in col_data.values[2]:
                    self.html.append(
                        f'<li><a href="https://nvd.nist.gov/vuln/detail/{cve}">{cve}</a></li>'
                    )
                self.html.append("</ul></li>")
            self.html.append("</ol>")

    def _parse_version_list(self, version):
        """Parse the version tuple and return a neatly-formatted string"""
        if len(version) == 1:
            return f" {version[0][0]} {version[0][1]}"
        return f" {version[0][0]} {version[0][1]}, {version[1][0]} {version[1][1]}"

    def get_html(self):
        """Return html report"""
        return "".join(self.html)
