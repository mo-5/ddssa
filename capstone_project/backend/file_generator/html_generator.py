class HTMLGenerator:
    """Generate html report from analysis data"""

    def __init__(self) -> None:
        self.html = []
        self.html.append("<h1>Data-Driven Software Security Assessment Report</h1>")
        self.html.append("<h2>Stall Statements:</h2>")

    def add_sr_data(self, data):
        self.html.append(
            "<div>File: "
            + data[0]
            + " contains: "
            + str(len(data[1]))
            + " stall statements</div>"
        )
        if len(data[1]) > 0:
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
            print(data)
            print(self.html)

    def get_html(self):
        return "".join(self.html)
