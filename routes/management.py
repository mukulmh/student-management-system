from flask import Blueprint,request,redirect,render_template,url_for,flash
from sqlalchemy import desc
from sqlalchemy.sql import func

from ..models.teachers import Teachers
from ..models.classes import Classes
from .auth import login_required
from ..models.students import Student
from ..extensions import db

mgt = Blueprint('management',__name__)


# home page
@mgt.route('/index')
@login_required
def index():
    classes = Classes.query.all()
    students = db.session.query(Student,Classes,Teachers).join(Classes, Student.s_class == Classes.class_name).join(Teachers, Classes.class_teacher == Teachers.initial).order_by(Student.id).all()
    return render_template('management/index.html',students=students,classes=classes)


# create student
@mgt.route('/create/student',methods=['POST','GET'])
@login_required
def create():
    classes = Classes.query.all()
    if request.method == 'POST':
        name = request.form['name']
        id = request.form['id']
        s_class = request.form.get('class')
        cgpa = request.form['cgpa']
        address = request.form['address']
        message = None
        if float(cgpa) > 4.0:
            message = 'CGPA can not be greater than 4.0'
        else:
            student = Student.query.filter_by(student_id=id).first()
            new_student = Student(name=name,student_id=id,s_class=s_class,cgpa=cgpa,address=address)
            if not student:
                db.session.add(new_student)
                db.session.commit()
                message ='Student added'
                flash(message)
                return redirect(url_for('management.index'))
            else:
                message = f'Student with id {id} has already registered!'
        
        flash(message)
    return render_template('management/create.html',classes=classes)


# update student
@mgt.route('/update/student/<int:id>',methods=['POST','GET'])
@login_required
def update(id):
    classes = Classes.query.all()
    student = Student.query.get(id)
    if request.method == 'POST':
        student.student_id = request.form['id']
        student.name = request.form['name']
        student.s_class = request.form.get('class')
        student.cgpa = request.form['cgpa']
        student.address = request.form['address']
        message = None
        if float(student.cgpa) > 4.0:
            message = 'CGPA can not be greater than 4.0'
            flash(message)
            return redirect(url_for('management.index'))

        db.session.commit()
        message = 'Student Updated'
        flash(message)
        return redirect(url_for('management.index'))

    return render_template('management/update.html',student=student,classes=classes)


# delete student
@mgt.route('/delete/student/<int:id>')
@login_required
def delete(id):
    student = Student.query.get(id)
    
    db.session.delete(student)
    db.session.commit()
    message = 'Student Deleted!'
    flash(message)
    return redirect(url_for('management.index'))


# filter student by class
@mgt.route('/filter/<int:id>')
@login_required
def filter(id):
    classes = Classes.query.all()
    students = db.session.query(Student,Classes,Teachers).join(Classes, Student.s_class == Classes.class_name).filter_by(id=id).join(Teachers, Classes.class_teacher == Teachers.initial).order_by(Student.id).all()
    return render_template('management/index.html',students=students,classes=classes)


# search student by id
@mgt.route('/search/<int:id>')
@login_required
def search(id):
    classes = Classes.query.all()
    students = db.session.query(Student,Classes,Teachers).join(Classes, Student.s_class == Classes.class_name).filter_by(student_id=id).join(Teachers, Classes.class_teacher == Teachers.initial).order_by(Student.id).all()
    return render_template('management/index.html',students=students,classes=classes)


# student ranking
@mgt.route('/ranking/student')
@login_required
def ranking_student():
    classes = Classes.query.all()
    students = Student.query.order_by(desc(Student.cgpa))
    print(students)
    return render_template('management/student-ranking.html', students=students, classes=classes)


# teacher ranking
@mgt.route('/ranking/teacher')
@login_required
def ranking_teacher():
    classes = Classes.query.all()
    teachers = db.session.query(Teachers.name,func.avg(Student.cgpa),Classes.class_name).join(Classes, Student.s_class == Classes.class_name).join(Teachers, Classes.class_teacher == Teachers.initial).group_by(Teachers.initial).order_by(desc(func.avg(Student.cgpa))).all()
    cgpas = teachers[1]
    for cgpa in cgpas:
        print(cgpa)
    
    return render_template('management/teacher-ranking.html', teachers=teachers, classes=classes)