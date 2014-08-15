from photosandtext21 import db
from mongoengine import IntField, StringField, DictField, EmbeddedDocument, EmbeddedDocumentField, DateTimeField, ListField, ObjectIdField, ReferenceField
from bson import ObjectId

class CropSettings(db.Document):
    name = StringField()
    width = IntField()
    height = IntField()

class Photo(db.Document):
    filename = StringField()
    exif = DictField()
    crops = DictField()

class Gallery(db.Document):
    name = StringField()
    date = DateTimeField()
    desc = StringField()
    photos = ListField(ReferenceField(Photo))
