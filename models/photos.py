from photosandtext21 import db
from mongoengine import IntField, StringField, DictField, DateTimeField, ListField, ReferenceField


class CropSettings(db.Document):
    name = StringField()
    width = IntField()
    height = IntField()


class Photo(db.Document):
    filename = StringField()
    exif = DictField()
    crops = DictField()
    orientation = StringField()


class Gallery(db.Document):
    name = StringField()
    date = DateTimeField()
    desc = StringField()
    photos = ListField(ReferenceField(Photo))
