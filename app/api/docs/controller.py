from flask import request, jsonify, make_response
from flask_restful import Resource
from reportlab.platypus import SimpleDocTemplate, Paragraph, PageBreak, Image, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import mm, inch, cm
from reportlab.lib.enums import TA_LEFT
from reportlab.lib import colors
from io import BytesIO
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
