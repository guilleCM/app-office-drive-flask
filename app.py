from flask import Flask, make_response
from datetime import datetime
import re
from fpdf import FPDF, HTMLMixin

app = Flask(__name__)

@app.route("/")
def home():
    return "Hello, Flask!"

@app.route("/hello/<name>")
def hello_there(name):
    now = datetime.now()
    formatted_now = now.strftime("%A, %d %B, %Y at %X")

    # Filter the name argument to letters only using regular expressions. URL arguments
    # can contain arbitrary text, so we restrict to safe characters only.
    match_object = re.match("[a-zA-Z]+", name)

    if match_object:
        clean_name = match_object.group(0)
    else:
        clean_name = "Friend"

    content = "Hello there, " + clean_name + "! It's " + formatted_now
    return content



class CustomPDF(FPDF, HTMLMixin):
    # def header(self):
    #     # Set up a logo
    #     # self.image('snakehead.jpg', 10, 8, 33)
    #     self.set_font('Arial', 'B', 15)
 
    #     # Add an address
    #     self.cell(100)
    #     self.cell(0, 5, 'Mike Driscoll', ln=1)
    #     self.cell(100)
    #     self.cell(0, 5, '123 American Way', ln=1)
    #     self.cell(100)
    #     self.cell(0, 5, 'Any Town, USA', ln=1)
 
    #     # Line break
    #     self.ln(20)
 
    def footer(self):
        self.set_y(-10)

        self.set_font('Arial', 'I', 8)
 
        # Add a page number
        page = 'Página ' + str(self.page_no()) + '/{nb}'
        self.cell(0, 10, page, 0, 0, 'C')
        

@app.route("/pdf")
def pdf():
    # pdf = CustomPDF()
    # pdf.add_page()
    # pdf.set_font("Arial", size=12)
    # pdf.cell(200, 10, txt="Welcome to Python!", ln=1, align="C")
    # pdf.output("simple_demo.pdf")
    pdf = CustomPDF()
    # Create the special value {nb}
    pdf.alias_nb_pages()
    pdf.add_page()
    pdf.set_font('Arial', '', 12)
    # line_no = 1
    # for i in range(50):
    #     pdf.cell(0, 10, txt="Line #{}".format(line_no), ln=1)
    #     line_no += 1
    emitter_street = "C/ Manobre n 28, Local 2"
    emitter_cp = "07008 PALMA DE MALLORCA"
    emitter_tel = "656716108"
    emitter_nif = "B57743734"

    client_name = "AGRO EXPERT"
    client_street = "Psaje de Santa Catalina n1 fewfew we fewf wefe we fwefwef wef we we"
    client_cp = "07002 Palma de Mallorca"
    client_nif = "A-07152626"

    date = "11-12-2017"


    header = "Obra: arreglo suelo sótano (local americano)"
    budget_num = "100-2017"

    # pdf.cell(200, 10, txt=emitter_street, ln=1)
    # pdf.cell(200, 10, txt="CLIENTE", ln=1, align="R")
    table = """
    <table border="0" align="center" width="100%">
        <thead>
            <tr>
                <th width="60%"> </th>
                <th width="40%" align="left">CLIENTE:</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td>
                      <table width="100%">
                        <thead><tr><th width="100%"></th></tr></thead>
                        <tr>
                            <td>"""+emitter_street+"""</td>
                        </tr>
                        <tr>
                            <td>"""+emitter_cp+"""</td>
                        </tr>
                        <tr>
                            <td>"""+emitter_tel+"""</td>
                        </tr>
                        <tr>
                            <td>"""+emitter_nif+"""</td>
                        </tr>
                    </table>
                </td>
            </tr>
        </tbody>
    </table>
    """
    pdf.write_html(table)

    pdf.output("simple_demo.pdf")

    response = make_response(pdf.output(dest='S').encode('latin-1'))
    response.headers.set('Content-Disposition', 'attachment', filename="simple_demo" + '.pdf')
    response.headers.set('Content-Type', 'application/pdf')
    return response