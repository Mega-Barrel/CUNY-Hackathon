from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, BooleanField, SelectField, IntegerField
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
