from flask_login import login_required, current_user
import sqlalchemy
from flask import render_template, redirect, url_for, flash, request

from app.models import StudentDetails
from app.decorators import permission_required, role_required
from app.student import bp
from app.student.forms import StudentDetailsForm
from app import db


@bp.route('/main')
@login_required
def student_main_page():
    return render_template('student/main.html')

@bp.route('/details', methods = ['GET', 'POST'])
@login_required
@role_required('Student')
def get_student_details():
    form = StudentDetailsForm()
    
    student_details = StudentDetails.query.filter_by(user_id = current_user.id).first()

    if form.validate_on_submit():
        student_details = StudentDetails.query.filter_by(first_name = form.first_name.data, last_name = form.last_name.data).first()
        if student_details is None: 
            student_details = StudentDetails(first_name = form.first_name.data, last_name = form.last_name.data, 
                                            address = form.address.data, city = form.city.data, state = form.state.data,
                                            zip = form.zip.data, parent_name = form.parent_name.data, emergency_contact = form.emergency_contact.data,
                                            medical_conditions = form.medical_conditions.data, comments = form.comments.data, user_id=current_user.id)
        else:
            student_details.address = form.address.data
            student_details.city = form.city.data
            student_details.state = form.state.data
            student_details.zip = form.zip.data
            student_details.parent_name = form.parent_name.data
            student_details.emergency_contact = form.emergency_contact.data
            student_details.medical_conditions = form.medical_conditions.data
            student_details.comments = form.comments.data
            student_details.user_id = current_user.id

        db.session.add(student_details)
        db.session.commit()

        flash('Student Details entered successfully')

        return redirect(url_for('student.student_main_page'))
    if student_details is not None:
        form.first_name.data = student_details.first_name
        form.last_name.data = student_details.last_name
        form.address.data = student_details.address
        form.city.data = student_details.city
        form.state.data = student_details.state
        form.zip.data = student_details.zip
        form.parent_name.data = student_details.parent_name
        form.emergency_contact.data = student_details.emergency_contact
        form.medical_conditions.data = student_details.medical_conditions
        form.comments.data = student_details.comments
        

    return render_template('student/details.html', title='Enter Details',
                           form=form)



