from flask import render_template, redirect, url_for, flash, request, current_app
from flask_login import current_user, login_required

from app import db
from app.coursework import bp
from app.coursework.forms import AddCourseWorkForm
from app.models import Classroom, Coursework


@bp.route('/coursework', methods=['GET'])
@bp.route('/coursework/<int:coursework_id>', methods=['GET'])
@login_required
def show_coursework(coursework_id = None):
    if coursework_id:
        coursework = Coursework.query.filter_by(id=coursework_id).first_or_404()
        return render_template('coursework/coursework_detail.html', title=f'Coursework - {coursework.name}', coursework=coursework)

    page = request.args.get('page', 1, type=int)
    coursework = Coursework.query.filter_by(creator_id=current_user.id).paginate(
        page, current_app.config['CARDS_PER_PAGE'], False
    )
    
    coursework_urls = []
    for course in coursework.items:
        coursework_urls.append(('/coursework/coursework/' + str(course.id)))
    
    next_url = url_for('coursework.show_coursework', page=coursework.next_num) if coursework.has_next else None
    prev_url = url_for('coursework.show_coursework', page=coursework.prev_num) if coursework.has_prev else None

    return render_template('coursework/list_coursework.html', title=f'Coursework - {current_user.username}',
                           coursework=coursework.items, coursework_urls = coursework_urls, next_url=next_url,
                           prev_url=prev_url)



@bp.route('/add', methods = ['GET', 'POST'])
@login_required
def add_coursework():
    form = AddCourseWorkForm()
    
    form.classroom.choices = [(_class.id, _class.name) for _class in Classroom.query.filter_by(creator_id = current_user.id).all()]
    
    if form.validate_on_submit():
        classroom = Classroom.query.filter_by(id = form.classroom.data).first()
        coursework = Coursework(classroom = classroom, name = form.name.data, creator_id = current_user.id)
        
        db.session.add(coursework)
        db.session.commit()

        flash('Coursework added successfully')

        return redirect(url_for('coursework.show_coursework'))


    return render_template('coursework/add_coursework.html', title='Enter Details',
                           form=form)



