from ..extensions import db

# user model/class
class Classes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    class_name = db.Column(db.String(100), nullable=False, unique=True)
    student = db.relationship('Student')
    class_teacher = db.Column(db.String(100), db.ForeignKey('teachers.initial'), nullable=False)

    def __repr__(self):
        return '<Class %r>' %self.id