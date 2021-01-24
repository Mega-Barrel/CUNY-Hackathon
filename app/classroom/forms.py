from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, BooleanField, SelectField, IntegerField, DateField
from wtforms.validators import ValidationError, DataRequired, Length, NumberRange


class AddClassroomForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=4, max=100)])
    description = TextAreaField('Classroom Description', validators=[Length(min=0, max=140)])
    subject = SelectField('Subject', validators=[DataRequired()])
    term = StringField('Term', validators=[DataRequired(), Length(min=4, max=50)])
    year = IntegerField('Year', [DataRequired(), NumberRange(min=1900, max=2100)])
    time = StringField('Time', validators=[DataRequired(), Length(min=4, max=10)])
    active = BooleanField('Active')

    submit = SubmitField('Submit')


class AddStudentForm(FlaskForm):
    student = SelectField('Student Name', validators=[DataRequired()])
    submit = SubmitField('Add')


class AddStudentGradeForm(FlaskForm):
    grade = IntegerField('Grade', [DataRequired(), NumberRange(min=0, max=100)])
    date_occurred = DateField('Date Taken', format='%m/%d/%y')
    graded = BooleanField('Graded Item')
    comments = TextAreaField('Comments', validators=[Length(min=0, max=140)])
    coursework_item = SelectField('Coursework Item', validators=[DataRequired()])

    submit = SubmitField('Add Grade')
