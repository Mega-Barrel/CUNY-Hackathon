from flask import render_template, redirect, url_for, flash, request, current_app, jsonify
from flask_login import current_user, login_required

from app import db
from app.classroom import bp
from app.classroom.forms import AddClassroomForm, AddStudentForm
from app.decorators import role_required
from app.models import Classroom, User, Subject, Role


@bp.route('/', methods=['GET'])
@bp.route('/<int:classroom_id>', methods=['GET'])
@login_required
def show_classroom(classroom_id=None):
    # Classroom for students
    _role = Role.query.filter_by(id=current_user.role_id).first()
    
    if _role.name == 'Student':
        if classroom_id:
            classroom = Classroom.query.filter_by(id=classroom_id).first()
            return render_template('classroom/classroom_detail.html', title=f'Classroom - {classroom.name}', classroom=classroom)
        page = request.args.get('page', 1, type=int)
        classrooms = Classroom.query.filter_by(creator_id=current_user.id).paginate(
            page, current_app.config['CARDS_PER_PAGE'], False
        )
        next_url = url_for('classroom.show_classroom', page=classrooms.next_num) if classrooms.has_next else None
        prev_url = url_for('classroom.show_classroom', page=classrooms.prev_num) if classrooms.has_prev else None

        return render_template('classroom/list_classrooms.html', title=f'Classrooms - {current_user.username}',
                               classrooms=classrooms.items, next_url=next_url,
                               prev_url=prev_url)
    # Classroom for Admins
    # Classroom for teachers
    if classroom_id:
        classroom = Classroom.query.filter_by(id=classroom_id).first()
        return render_template('classroom/classroom_detail.html', title=f'Classroom - {classroom.name}', classroom=classroom)

    page = request.args.get('page', 1, type=int)
    classrooms = Classroom.query.filter_by(creator_id=current_user.id).paginate(
        page, current_app.config['CARDS_PER_PAGE'], False
    )
    next_url = url_for('classroom.show_classroom', page=classrooms.next_num) if classrooms.has_next else None
    prev_url = url_for('classroom.show_classroom', page=classrooms.prev_num) if classrooms.has_prev else None

    return render_template('classroom/list_classrooms.html', title=f'Classrooms - {current_user.username}',
                           classrooms=classrooms.items, next_url=next_url,
                           prev_url=prev_url)



@bp.route('/add', methods=['GET', 'POST'])
@login_required
@role_required('Teacher')
def add_classroom():
    # TODO: Permission for Teachers
    form = AddClassroomForm()
    form.subject.choices = [(_subject.id, _subject.name) for _subject in Subject.query.order_by('name')]
    if form.validate_on_submit():
        classroom = Classroom(
            name = form.name.data,
            description = form.description.data,
            subject = form.subject.data,
            term = form.term.data,
            year = form.year.data,
            time = form.time.data,
            active = form.active.data,
            creator_id = current_user.id
        )
        db.session.add(classroom)
        db.session.commit()
        flash('Your new classroom has been saved.')
        return redirect(url_for('classroom.show_classroom', classroom_id=classroom.id))
    return render_template('classroom/add_classroom.html', title='Add Classroom', form=form)


@bp.route('/edit/<int:classroom_id>', methods=['GET', 'POST'])
@login_required
@role_required('Teacher')
def edit_classroom(classroom_id):
    classroom = Classroom.query.filter_by(id=classroom_id).first_or_404()
    form = AddClassroomForm()
    form.subject.choices = [(_subject.id, _subject.name) for _subject in Subject.query.order_by('name')]
    if form.validate_on_submit():
        classroom.name = form.name.data
        classroom.description = form.description.data
        classroom.subject = form.subject.data
        classroom.term = form.term.data
        classroom.year = form.year.data
        classroom.time = form.time.data
        classroom.active = form.active.data

        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('classroom.show_classroom', id=classroom.id))
    elif request.method == 'GET':
        form.name.data = classroom.name
        form.description.data = classroom.description
        form.subject.data = classroom.subject
        form.term.data = classroom.term
        form.year.data = classroom.year
        form.time.data = classroom.time
        form.active.data = classroom.active
    return render_template('classroom/edit_classroom.html', title='Edit Classroom',
                           form=form)


@bp.route('/add_classroom/<int:classroom_id>', methods=['GET', 'POST'])
@login_required
@role_required('Teacher')
def add_student_to_classroom(classroom_id):
    form = AddStudentForm()
    classroom = Classroom.query.filter_by(id=classroom_id).first_or_404()
    in_class_students = [student.id for student in classroom.students.all()]
    results = db.session.query(User).filter(User.role_id==1).filter(User.id.notin_(in_class_students)).all()
    form.student.choices = [(student.id, student.username) for student in results]
    # form.student.choices = [(student.id, student.username) for student in User.query.filter_by(role_id=1).filter(id.notin_(in_class_students)).order_by('name')]
    if request.method == 'POST':
        student_name = form.student.data
        student = User.query.filter_by(id=int(student_name)).first_or_404()
        classroom.add_student(student)
        
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('classroom.show_classroom', classroom_id=classroom.id))
    return render_template('classroom/add_student_to_classroom.html', title='Add Student to Classroom',
                           form=form)


@bp.route('/remove_student_classroom/<int:classroom_id>/<int:student_id>', methods=['DELETE'])
@login_required
@role_required('Teacher')
def remove_student_from_classroom(classroom_id, student_id):
    classroom = Classroom.query.filter_by(id=classroom_id).first_or_404()
    user = User.query.filter_by(id=student_id).first_or_404()
    # Delete logic
    classroom.remove_student(user)
    db.session.commit()
    return jsonify({
        'status': 'success'
    }), 200

@bp.route('/add_grade/', methods=['GET', 'POST'])
@login_required
@role_required('Teacher')
def add_grade():
    pass


# @bp.route('/add_student/<int:classroom_id>/<int:student_id>/<int:coursework_id>', methods=['POST'])
# @bp.route('/add_student/<int:classroom_id>/<int:student_id>/<int:coursework_id>', methods=['DELETE'])
# @login_required
# @role_required('Teacher')
# def add_student_to_classroom(classroom_id, student_id, coursework_id):
#     classroom = Classroom.query.filter_by(id=classroom_id).first_or_404()
#     user = User.query.filter_by(id=student_id).first_or_404()

#     if request.method == 'POST':
#         classroom.add_student(user)
#         db.session.commit()
#     # Delete logic
#     classroom.remove_student(user)
#     db.session.commit()
#     return jsonify({
#         'status': 'success'
#     }), 200
