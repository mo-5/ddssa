from fpdf import FPDF


class PDFGenerator:
    """This class is responsible for generating the pdf report.
    """

    def __init__(self):
        self.pdf = FPDF()
        self.pdf.add_page()
        self.pdf.set_font('Arial', size=20)
        self.pdf.cell(200, 10, txt="Data-Driven Software Security "
                                   "Assessment Report", ln=1, align='C')
        self.pdf.set_font('Arial', size=12)

    def add_header(self, header):
        self.pdf.set_font('Arial', size=15)
        self.pdf.cell(200, 10, txt=header, ln=1, align='L')
        self.pdf.set_font('Arial', size=12)

    def add_sr_data(self, data):
        text = "File: " + data[0] + " contains: " + \
            str(len(data[1])) + " stall statements"
        if len(data[1]) > 0:
            text += "\nThe following statements are stall statements: "
            for i in range(len(data[1])):
                text += "\n     " + str(i + 1) + ") line number: " + \
                    str(data[1][i][0]) + ", statement: " + \
                    data[1][i][1].strip()
        self.pdf.write(5, text)
        self.pdf.write(5, "\n")

    def save_pdf(self, filename):
        self.pdf.output(filename, 'F')
