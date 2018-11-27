from flask import request, jsonify
from flask_restful import Resource


class Document(Resource):
    def get(self):
        return jsonify({'status': 'ok', 'message': 'Get Doc!!!'})
    def put(self):
        incoming_data = request.json
