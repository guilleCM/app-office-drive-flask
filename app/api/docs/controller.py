from flask import request, jsonify, make_response
from flask_restful import Resource
from reportlab.platypus import SimpleDocTemplate, Paragraph, PageBreak, Image, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm, inch, cm
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT
# from reportlab.lib import utils
from reportlab.lib import colors
from io import BytesIO
import math

from app.bo.docs.documents import DocumentsBO, DocumentsCollectionBO


class Documents(Resource):
    def get(self):
        return jsonify({'status': 'ok', 'message': 'Get Doc!!!'})

    def put(self):
        incoming_data = request.json
        try:
            document_BO = DocumentsBO()
            document_BO.emitter_name = incoming_data['emitter_name']
            document_BO.emitter_address = incoming_data['emitter_address']
            document_BO.emitter_zip_code = incoming_data['emitter_zip_code']
            document_BO.emitter_city = incoming_data['emitter_city']
            document_BO.emitter_tel = incoming_data['emitter_tel']
            document_BO.emitter_nif = incoming_data['emitter_nif']
            document_BO.client_name = incoming_data['client_name']
            document_BO.client_address = incoming_data['client_address']
            document_BO.client_zip_code = incoming_data['client_zip_code']
            document_BO.client_city = incoming_data['client_city']
            document_BO.client_cif = incoming_data['client_cif']
            document_BO.doc_type = incoming_data['doc_type']
            document_BO.doc_type_description = incoming_data['doc_type_description']
            document_BO.concepts = incoming_data['concepts']
            document_BO.concepts_cost = incoming_data['concepts_cost']
            document_BO.IVA_percent = incoming_data['iva_percent']
            document_BO.IVA_cost = incoming_data['iva_cost']
            document_BO.total_cost = incoming_data['total_cost']
            document_BO.insert()
            response = {
                'status': 'ok',
                'id': str(document_BO.get_id())
            }
            return jsonify(response)
        except Exception as e:
            response = {
                'status': 'ko',
                'message': str(e)
            }
            return jsonify(response)


class CountByYearDocuments(Resource):
    def get(self):
        try:
            documents_BO = DocumentsCollectionBO()
            count = documents_BO.count_by_year()
            response = {
                'status': 'ok',
                'count': count
            }
            return jsonify(response)
        except Exception as e:
            response = {
                'status': 'ko',
                'message': str(e)
            }
            return jsonify(response)


class FilterByYearDocuments(Resource):
    def get(self):
        try:
            documents_BO = DocumentsCollectionBO()
            documents_BO.filter_by_year()
            return documents_BO.to_json()
        except Exception as e:
            response = {
                'status': 'ko',
                'message': str(e)
            }
            return jsonify(response)


class GetPdfDocuments(Resource):
    def get(self):
        id = request.args['id']
        documents_BO = DocumentsBO()
        documents_BO.filter_by_id(id)

        pdf_buffer = BytesIO()
        # pagesize = (140 * mm, 216 * mm)
        my_doc = SimpleDocTemplate(
            pdf_buffer,
            topMargin=0.5 * inch,
            leftMargin=0.5 * inch,
            rightMargin=0.5 * inch,
            bottomMargin=0.5 * inch,
            title="Recibo",
            author=documents_BO.emitter_name
        )
        flowables = []

        sample_style_sheet = getSampleStyleSheet()

        # img = utils.ImageReader("company_logo.jpg")
        # iw, ih = img.getSize()
        brand_logo = Image("company_logo.jpg", width=10.054166667*cm, height=3.175*cm)
        brand_logo.hAlign = 'LEFT'

        # body_text_style_1 = getSampleStyleSheet()['BodyText']
        # body_text_style_1.alignment = TA_LEFT
        body_text_style_1 = ParagraphStyle('doc_type_paragraph', alignment=TA_LEFT)
        data = [
            [Paragraph(documents_BO.emitter_address.capitalize(), body_text_style_1), Paragraph("<b>CLIENTE:</b>", ParagraphStyle('client', alignment=TA_LEFT, backColor=colors.orange))],
            [Paragraph(documents_BO.emitter_zip_code + " " + documents_BO.emitter_city.upper(), body_text_style_1), Paragraph(documents_BO.client_name.upper(), body_text_style_1)],
            [Paragraph("Tel. " + documents_BO.emitter_tel, body_text_style_1), Paragraph(documents_BO.client_address.capitalize(), body_text_style_1)],
            [Paragraph("Nif: " + documents_BO.emitter_nif.upper(), body_text_style_1), documents_BO.client_zip_code + " " + documents_BO.client_city.capitalize()],
            ["", "Cif: " + documents_BO.client_cif.upper()],
            ["", "Fecha: " + documents_BO.c_date.strftime("%d-%m-%Y")]
        ]
        table_info = Table(data, colWidths=[9.5 * cm, 9.5 * cm])
        # table.setStyle(TableStyle([
        #     ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
        #     ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
        # ]))

        doc_type_style = ParagraphStyle('doc_type_paragraph', alignment=TA_LEFT, spaceAfter=5, spaceBefore=15)
        doc_type = "Obra: " if documents_BO.doc_type == "work" else "Servicio: "
        doc_type_paragraph = Paragraph(
            "<b>" + doc_type + documents_BO.doc_type_description + "</b>",
            doc_type_style
        )

        header_text_style = sample_style_sheet['BodyText']
        header_text_style.alignment = TA_CENTER

        concept_header = Paragraph("<b>Concepto</b>", header_text_style)
        cost_header = Paragraph("<b>Importe</b>", header_text_style)

        data = [
            [concept_header, cost_header]
        ]

        header_style_sheet = getSampleStyleSheet()
        body_text_style = header_style_sheet["BodyText"]
        body_text_style.alignment = TA_LEFT

        for concept in documents_BO.concepts:
            concept_description = Paragraph(concept.description.capitalize(), body_text_style)
            concept_cost = Paragraph(str(concept.cost)+" €", ParagraphStyle('c.cost', alignment=TA_RIGHT))
            row = [concept_description, concept_cost]
            data.append(row)

        table = Table(data, colWidths=[13.5 * cm, 5 * cm])
        table.setStyle(TableStyle([
            ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
            ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
        ]))

        flowables.append(brand_logo)
        flowables.append(table_info)
        flowables.append(doc_type_paragraph)
        flowables.append(table)
        concepts_cost = Paragraph("Importe Trabajo: " + str(documents_BO.concepts_cost) + " €",
                                  ParagraphStyle('c.costs', alignment=TA_RIGHT, spaceBefore=15, spaceAfter=5))
        IVA_cost = Paragraph(str(math.trunc(documents_BO.IVA_percent * 100))+"% de IVA: " + str(documents_BO.IVA_cost) + " €",
                                  ParagraphStyle('iva.cost', alignment=TA_RIGHT, spaceAfter=5))
        total_cost = Paragraph("TOTAL: " + str(documents_BO.total_cost) + " €",
                                  ParagraphStyle('total.costs', alignment=TA_RIGHT))
        flowables.append(concepts_cost)
        flowables.append(IVA_cost)
        flowables.append(total_cost)
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

        response = make_response(pdf_out)
        response.headers.set('Content-Disposition', 'attachment', filename="simple_demo" + '.pdf')
        response.headers.set('Content-Type', 'application/pdf')
        return response
