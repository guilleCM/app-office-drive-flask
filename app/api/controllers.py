from flask import Blueprint
from flask_restful import Api

from app.api.docs.controller import Documents, CountByYearDocuments, FilterByYearDocuments, GetPdfDocuments

api_module = Blueprint("api", __name__)
api_wrap = Api(api_module)

api_wrap.add_resource(Documents, "/docs/")
api_wrap.add_resource(CountByYearDocuments, "/docs/CountByYear")
api_wrap.add_resource(FilterByYearDocuments, "/docs/FilterByYear")
api_wrap.add_resource(GetPdfDocuments, "/docs/GetPdf")
