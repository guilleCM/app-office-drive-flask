from flask import Flask, make_response
from datetime import datetime
import re
# from fpdf import FPDF, HTMLMixin
from reportlab.platypus import SimpleDocTemplate, Paragraph, PageBreak, Image, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import mm, inch, cm
from reportlab.lib.enums import TA_LEFT
from reportlab.lib import colors
from io import BytesIO

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
        clean_name = "Friends"

    content = "Hello there, " + clean_name + "! It's " + formatted_now
    return content


# class CustomPDF(FPDF, HTMLMixin):
#     # def header(self):
#     #     # Set up a logo
#     #     # self.image('snakehead.jpg', 10, 8, 33)
#     #     self.set_font('Arial', 'B', 15)

#     #     # Add an address
#     #     self.cell(100)
#     #     self.cell(0, 5, 'Mike Driscoll', ln=1)
#     #     self.cell(100)
#     #     self.cell(0, 5, '123 American Way', ln=1)
#     #     self.cell(100)
#     #     self.cell(0, 5, 'Any Town, USA', ln=1)

#     #     # Line break
#     #     self.ln(20)

#     def footer(self):
#         self.set_y(-10)

#         self.set_font('Arial', 'I', 8)

#         # Add a page number
#         page = 'Página ' + str(self.page_no()) + '/{nb}'
#         self.cell(0, 10, page, 0, 0, 'C')


@app.route("/pdf")
def pdf():
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

    pdf_buffer = BytesIO()
    # pagesize = (140 * mm, 216 * mm)
    my_doc = SimpleDocTemplate(
        pdf_buffer,
        topMargin=0.5 * inch,
        leftMargin=0.5 * inch,
        rightMargin=0.5 * inch,
        bottomMargin=0.5 * inch,
        title="Recibo",
        author="DITANA Servicios SL"
    )
    flowables = []

    sample_style_sheet = getSampleStyleSheet()

    brand_logo = Image("350x150.jpg")
    brand_logo.hAlign = 'LEFT'

    paragraph_1 = Paragraph("A title", sample_style_sheet['Heading1'])
    paragraph_2 = Paragraph(
        "Some normal body text",
        sample_style_sheet['BodyText']
    )

    body_text_style = sample_style_sheet["BodyText"]
    body_text_style.alignment = TA_LEFT

    concepto_largo = "conceptosuperlargconceptosuperlargoconceptosuperlargoconceptosuperlargoconceptosuperlargoconceptosuperlargoconceptosuperlargooconconceptosuperlargoconceptosuperlargoceptosuperlargo"
    concepto_corto = "fifiewfiewofihweoifhweoifhwoif"

    concepto_largo = Paragraph(concepto_largo, body_text_style)
    concepto_corto = Paragraph(concepto_corto, body_text_style)

    data = [
        ["Concepto", "Importe"]
    ]

    for i in range(0, 100):
        if i % 2 == 0:
            c = [concepto_corto, "342 €"]
            data.append(c)
        else:
            c = [concepto_largo, "13 €"]
            data.append(c)

    table = Table(data, colWidths=[13.5 * cm, 5 * cm])
    table.setStyle(TableStyle([
        ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
    ]))

    flowables.append(brand_logo)
    flowables.append(paragraph_1)
    flowables.append(paragraph_2)
    flowables.append(table)
    flowables.append(PageBreak())

    def add_page_number(canvas, doc):
        canvas.saveState()
        canvas.setFont('Times-Roman', 10)
        page_number_text = "Página %d" % doc.page
        canvas.drawCentredString(
            10.5 * cm,
            0.75 * cm,
            page_number_text
        )
        canvas.restoreState()

    my_doc.build(
        flowables,
        onFirstPage=add_page_number,
        onLaterPages=add_page_number,
    )

    pdf_out = pdf_buffer.getvalue()
    pdf_buffer.close()

    # response = make_response(pdf.output(dest='S').encode('latin-1'))
    response = make_response(pdf_out)
    response.headers.set('Content-Disposition', 'attachment', filename="simple_demo" + '.pdf')
    response.headers.set('Content-Type', 'application/pdf')
    return response


# app.run(host='0.0.0.0', port=5000)
app.run()