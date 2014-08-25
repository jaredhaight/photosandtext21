from photosandtext21 import db
from mongoengine import IntField, StringField, DictField, DateTimeField, ListField, ReferenceField, ComplexDateTimeField


class CropSettings(db.Document):
    name = StringField()
    width = IntField()
    height = IntField()


class Photo(db.Document):
    key = StringField(unique=True)
    filename = StringField()
    exif = DictField()
    crops = DictField()
    orientation = StringField()
    date_taken = ComplexDateTimeField()


class Gallery(db.Document):
    key = StringField(unique=True)
    name = StringField()
    date = DateTimeField()
    desc = StringField()
    photos = ListField(ReferenceField(Photo))
