from . import db

class Loan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    amount = db.Column(db.Float)