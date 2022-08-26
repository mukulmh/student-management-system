from ..extensions import db

# student model/class
class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, unique=True)
    name = db.Column(db.String(100), nullable=False)
    s_class = db.Column(db.String(100), db.ForeignKey('classes.class_name'), nullable=False)
    cgpa = db.Column(db.Float, nullable=False)
    address = db.Column(db.String(100), nullable=False)
    
    def __repr__(self):
        return '<Student %r>' %self.id
