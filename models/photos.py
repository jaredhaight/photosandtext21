import ast
from photosandtext21 import db
from flask import abort


class CropSettings(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    width = db.Column(db.Integer)
    height = db.Column(db.Integer)


class Gallery(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String, unique=True)
    name = db.Column(db.String)
    date = db.Column(db.DateTime)
    desc = db.Column(db.String)
    photos = db.relationship('Photo', backref='gallery', order_by="Photo.date_taken", lazy='dynamic')

    def save(self):
        if not self.date:
            self.date = self.photos.order_by(Photo.date_taken).first().date_taken
        db.session.add(self)
        db.session.commit()


class Photo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String, unique=True)
    gallery_id = db.Column(db.Integer, db.ForeignKey('gallery.id'))
    filename = db.Column(db.String)
    exif = db.Column(db.String)
    crops = db.Column(db.String)
    orientation = db.Column(db.String)
    date_taken = db.Column(db.DateTime)

    def save(self):
        db.session.add(self)
        db.session.commit()

    def get_exif(self, key):
        exif = ast.literal_eval(self.exif)
        try:
            return exif[key]
        except:
            return "No Value"

    def get_crop(self, crop_name):
        crops = ast.literal_eval(self.crops)
        try:
            response = crops[crop_name]
        except:
            response = "null"
        return response

    def add_crops(self, crop_name, filename):
        existing_crops = ast.literal_eval(self.crops)
        existing_crops[crop_name] = filename
        self.crops = str(existing_crops)
        self.save()
