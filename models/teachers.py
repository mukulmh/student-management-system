from ..extensions import db

# user model/class
class Teachers(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    initial = db.Column(db.String(100), nullable=False, unique=True)
    classes = db.relationship('Classes')

    def __repr__(self):
        return '<Class %r>' %self.id