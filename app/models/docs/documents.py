from app import db
import mongoengine_goodjson as gj
from datetime import datetime


class Concepts(gj.EmbeddedDocument):
    description = db.StringField()
    cost = db.DecimalField()


class Documents(gj.Document):
    # EMITTER DATA
    emitter_name = db.StringField()
    emitter_address = db.StringField()
    emitter_city = db.StringField()
    emitter_zip_code = db.StringField()
    emitter_tel = db.StringField()
    emitter_nif = db.StringField()
    # CLIENT DATA
    client_name = db.StringField()
    client_address = db.StringField()
    client_zip_code = db.StringField()
    client_city = db.StringField()
    client_cif = db.StringField()
    doc_type = db.StringField()
    doc_type_description = db.StringField()
    concepts = db.EmbeddedDocumentListField(Concepts, default=[])
    # COSTS DATA
    concepts_cost = db.DecimalField()
    IVA_percent = db.DecimalField()
    IVA_cost = db.DecimalField()
    total_cost = db.DecimalField()
    # DB DATA
    c_date = db.DateTimeField(default=datetime.now())
    _active = db.BooleanField(default=True)
