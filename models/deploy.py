from photosandtext21 import db


class DeployedFiles(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    path = db.Column(db.String, unique=True)
    hash = db.Column(db.String)

    def save(self):
        db.session.add(self)
        db.session.commit()
