class HTMLGenerator:
    """Generate html report from analysis data"""

    def __init__(self) -> None:
        """Initialize html report"""
        self.html = [
            "<h1>Data-Driven Software Security Assessment Report</h1>",
            "<h2>Stall Statements:</h2>",
        ]

    def add_sr_data(self, data):
        """Add sr data data to html report"""
        if len(data[1]) > 0:
            self.html.append(
                "<div>File: "
                + data[0]
                + " contains: "
                + str(len(data[1]))
                + " stall statements</div>"
            )
            self.html.append(
                "<div><div>The following statements are stall statements:</div><ol>"
            )
            for i in range(len(data[1])):
                self.html.append(
                    "<li> Line number: "
                    + str(data[1][i][0])
                    + ", statement: "
                    + data[1][i][1].strip()
                    + "</li>"
                )
            self.html.append("</ol></div>")

    def get_html(self):
        """Return html report"""
        return "".join(self.html)
