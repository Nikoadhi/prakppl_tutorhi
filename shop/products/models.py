from shop import db

from datetime import datetime


class Addcourse(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    price = db.Column(db.DECIMAL(asdecimal=False), nullable=False)
    description = db.Column(db.Text, nullable=False)

    image_1 = db.Column(db.String(150), nullable=False, default='image.jpg')
    image_2 = db.Column(db.String(150), nullable=False, default='image.jpg')

    def __repr__(self):
        return '<Addcourse %r>' % self.name

class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False, unique=True)

    def __repr__(self):
        return '<Course %r>' % self.name


db.create_all()