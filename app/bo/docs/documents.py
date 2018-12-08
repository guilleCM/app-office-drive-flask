from app.models.docs.documents import Documents, Concepts
from datetime import datetime
import json

class DocumentsBO:
    def __init__(self):
        # ORM
        self._ORM = None
        # EMITTER DATA
        self.emitter_name = ""
        self.emitter_address = ""
        self.emitter_zip_code = ""
        self.emitter_city = ""
        self.emitter_tel = ""
        self.emitter_nif = ""
        # CLIENT DATA
        self.client_name = ""
        self.client_address = ""
        self.client_zip_code = ""
        self.client_city = ""
        self.client_cif = ""
        self.doc_type = ""
        self.doc_type_description = ""
        self.concepts = None
        # COSTS DATA
        self.concepts_cost = 0
        self.IVA_percent = 0
        self.IVA_cost = 0
        self.total_cost = 0
        self.c_date = None

    def insert(self):
        concepts_collection = []
        for concept in self.concepts:
            embedded_concept = Concepts(
                description=concept['description'],
                cost=concept['cost']
            )
            concepts_collection.append(embedded_concept)
        document = Documents(
            emitter_name=self.emitter_name,
            emitter_address=self.emitter_address,
            emitter_zip_code=self.emitter_zip_code,
            emitter_city=self.emitter_city,
            emitter_tel=self.emitter_tel,
            emitter_nif=self.emitter_nif,
            client_name=self.client_name,
            client_address=self.client_address,
            client_zip_code=self.client_zip_code,
            client_city=self.client_city,
            client_cif=self.client_cif,
            doc_type=self.doc_type,
            doc_type_description=self.doc_type_description,
            concepts=concepts_collection,
            concepts_cost=self.concepts_cost,
            IVA_percent=self.IVA_percent,
            IVA_cost=self.IVA_cost,
            total_cost=self.total_cost
        )
        document.save()
        self.c_date = document.c_date
        self._ORM = document

    def get_id(self):
        return self._ORM.id

    def filter_by_id(self, id):
        document = Documents.objects(id=id).first()
        self._ORM = document
        self._set_data_from_ORM()

    def _set_data_from_ORM(self):
        # EMITTER DATA
        self.emitter_name = self._ORM.emitter_name
        self.emitter_address = self._ORM.emitter_address
        self.emitter_zip_code = self._ORM.emitter_zip_code
        self.emitter_city = self._ORM.emitter_city
        self.emitter_tel = self._ORM.emitter_tel
        self.emitter_nif = self._ORM.emitter_nif
        # CLIENT DATA
        self.client_name = self._ORM.client_name
        self.client_address = self._ORM.client_address
        self.client_zip_code = self._ORM.client_zip_code
        self.client_city = self._ORM.client_city
        self.client_cif = self._ORM.client_cif
        self.doc_type = self._ORM.doc_type
        self.doc_type_description = self._ORM.doc_type_description
        self.concepts = self._ORM.concepts
        # COSTS DATA
        self.concepts_cost = self._ORM.concepts_cost
        self.IVA_percent = self._ORM.IVA_percent
        self.IVA_cost = self._ORM.IVA_cost
        self.total_cost = self._ORM.total_cost
        self.c_date = self._ORM.c_date


class DocumentsCollectionBO(list):
    def count_by_year(self, year=datetime.now().year):
        datetime_format = '%Y-%m-%dT%H:%M:%SZ'
        start_year = datetime.strptime(str(year)+'-01-01T00:00:00Z', datetime_format)
        end_year = datetime.strptime(str(int(year)+1)+'-01-01T00:00:00Z', datetime_format)
        documents = Documents.objects(
            c_date__gte=start_year,
            c_date__lt=end_year
        ).count()
        return documents

    def filter_by_year(self, year=datetime.now().year):
        datetime_format = '%Y-%m-%dT%H:%M:%SZ'
        start_year = datetime.strptime(str(year)+'-01-01T00:00:00Z', datetime_format)
        end_year = datetime.strptime(str(int(year)+1)+'-01-01T00:00:00Z', datetime_format)
        documents = Documents.objects(
            c_date__gte=start_year,
            c_date__lt=end_year
        ).order_by('-c_date')
        [self.append(doc) for doc in documents]

    def get_distinct_set_of_years(self):
        documents = Documents.objects.aggregate(*[
            {"$project": {
                "year": {"$year": "$c_date"},
            }},
            {"$group": {
                "_id": None,
                "distinctDate": {"$addToSet": {"year": "$year"}}
            }}
        ])
        set_of_years = []
        for doc in documents:
            for year in doc['distinctDate']:
                set_of_years.append(str(year['year']))
        return {"years": set_of_years}

    def to_json(self):
        return [json.loads(doc.to_json()) for doc in self]

