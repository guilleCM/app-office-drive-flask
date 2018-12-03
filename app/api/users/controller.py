from flask import request, jsonify
from flask_restful import Resource

from app.bo.users.users import UsersBO


class UsersLogin(Resource):
    def post(self):
        incoming_data = request.json
        try:
            user_BO = UsersBO()
            user_BO.filter_by_username(incoming_data['username'])
            response = {
                'status': 'ok',
            }
            return jsonify(response)
        except Exception as e:
            response = {
                'status': 'ko',
                'message': str(e)
            }
            return jsonify(response)

# class Users(Resource):
#     def get(self):
#         return jsonify({'status': 'ok', 'message': 'Get Doc!!!'})
#
#     def put(self):
#         incoming_data = request.json
#         try:
#             document_BO = DocumentsBO()
#             document_BO.emitter_name = incoming_data['emitter_name']
#             document_BO.emitter_address = incoming_data['emitter_address']
#             document_BO.emitter_zip_code = incoming_data['emitter_zip_code']
#             document_BO.emitter_city = incoming_data['emitter_city']
#             document_BO.emitter_tel = incoming_data['emitter_tel']
#             document_BO.emitter_nif = incoming_data['emitter_nif']
#             document_BO.client_name = incoming_data['client_name']
#             document_BO.client_address = incoming_data['client_address']
#             document_BO.client_zip_code = incoming_data['client_zip_code']
#             document_BO.client_city = incoming_data['client_city']
#             document_BO.client_cif = incoming_data['client_cif']
#             document_BO.doc_type = incoming_data['doc_type']
#             document_BO.doc_type_description = incoming_data['doc_type_description']
#             document_BO.concepts = incoming_data['concepts']
#             document_BO.concepts_cost = incoming_data['concepts_cost']
#             document_BO.IVA_percent = incoming_data['iva_percent']
#             document_BO.IVA_cost = incoming_data['iva_cost']
#             document_BO.total_cost = incoming_data['total_cost']
#             document_BO.insert()
#             response = {
#                 'status': 'ok',
#                 'id': str(document_BO.get_id())
#             }
#             return jsonify(response)
#         except Exception as e:
#             response = {
#                 'status': 'ko',
#                 'message': str(e)
#             }
#             return jsonify(response)
