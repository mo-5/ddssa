class HTMLGenerator:
    """Generate html report from analysis data"""

    def __init__(self) -> None:
        """Initialize html report"""
        self.html = [
            "<h1>Data-Driven Software Security Assessment Report</h1>",
            "<h2>Stall Statements</h2>",
        ]

    def add_sr_data(self, data):
        """Add SR data to the HTML report"""
        if len(data[1]) > 0:
            self.html.append(
                "<div>File "
                + "<b>"
                + data[0]
                + "</b>"
                + " contains "
                + str(len(data[1]))
                + (
                    " stall statements:</div>"
                    if len(data[1]) > 1
                    else " stall statement:</div>"
                )
            )
            self.html.append("<div><ol>")
            for i, _ in enumerate(data[1]):
                self.html.append(
                    "<li> Line number: "
                    + str(data[1][i][0])
                    + ", statement: "
                    + data[1][i][1].strip()
                    + "</li>"
                )
            self.html.append("</ol></div>")

    def add_dependency_vulnerability_data(self, df):
        """Add depdencency vulnerability data to the html report"""
        if len(df.columns) > 0:
            self.html.append("<h2>Dependency Vulnerabilities</h2>")
            self.html.append(
                "<div><div>The following dependencies have vulnerabilities:</div><ol>"
                if df.shape[1] > 1
                else "<div><div>The following dependency has a vulnerability:</div><ol>"
            )
            for _, col_data in df.iteritems():
                self.html.append(
                    "<li> Dependency: "
                    + str(col_data.values[0])
                    + (
                        ", vulnerabilities: "
                        if len(col_data.values[1]) > 1
                        else ", vulnerability: "
                    )
                    + ", ".join(
                        "<a href="
                        + "https://nvd.nist.gov/vuln/detail/"
                        + cve
                        + ">"
                        + cve
                        + "</a>"
                        for cve in col_data.values[1]
                    )
                )
                self.html.append("</ol></li>")

    def get_html(self):
        """Return html report"""
        return "".join(self.html)
