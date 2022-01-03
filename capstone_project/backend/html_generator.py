from htmlBuilder.tags import Head, Body, Html, Div, Title, P, Ul, Li
from htmlBuilder.attributes import Class, Style as InlineStyle


class HTMLGenerator:
    """[summary]
    """

    def __init__(self) -> None:
        self.head = Head([],
                         Title(
            [InlineStyle()], "Data-Driven Software Security Assessment Report")
        )
        self.sr_data = []
        self.stall_header = P([], "Stall Statements:")

    def add_sr_data(self, data):
        title = Div([],
                    "File: " + data[0] + " contains: " +
                    str(len(data[1])) + " stall statements")
        sr_statements = []

        if len(data[1]) > 0:
            statement = Div(
                [], "The following statements are stall statements: ")

            stall_statements = Div([],
                                   statement,
                                   Ul([],
                                      [Li([], "Line number: " +
                                          str(data[1][i][0]) + ", statement: " +
                                          data[1][i][1].strip()) for i in range(len(data[1]))]
                                      ))
            sr_statements = Div([], statement, stall_statements)

        self.sr_data.append(Div([],
                                title,
                                sr_statements))

    def save_html(self, filename):
        html = Html([],
                    self.head,
                    Body([],
                         self.stall_header,
                         self.sr_data))
        print(html.render(pretty=True, doctype=True))


gen = HTMLGenerator()
gen.save_html("")
