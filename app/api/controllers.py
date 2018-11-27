from flask import Blueprint, make_response
from flask_restful import Api

from app.api.docs.controller import Document

api_module = Blueprint("api", __name__)
api_wrap = Api(api_module)

api_wrap.add_resource(Document, "/doc/")
