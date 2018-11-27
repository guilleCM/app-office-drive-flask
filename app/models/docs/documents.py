import mongoengine as db
import mongoengine_goodjson as gj


class Document(gj.Document):
    emitter_name = db.StringField()
    emitter_street = db.StringField()
    emitter_cp = db.StringField()
    emitter_tel = db.StringField()
    emitter_nif = db.StringField()
    client_name = db.StringField()
    client_street = db.StringField()
    client_cp = db.StringField()
    client_nif = db.StringField()
    concepts = db.EmbeddedDocumentListField()
    c_date = db.DateTimeField()
