from app.models.docs.documents import Document, Concept


class DocumentBO:
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
        self.IVA = 0
        self.total_cost = 0
        self.c_date = None

    def insert(self):
        concepts_collection = []
        for concept in self.concepts:
            embedded_concept = Concept(
                description=concept['description'],
                cost=concept['cost']
            )
            concepts_collection.append(embedded_concept)
        document = Document(
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
            IVA=self.IVA,
            total_cost=self.total_cost
        )
        document.save()
        self._ORM = document
        self.c_date = document.c_date

    def get_id(self):
        return self._ORM.id

