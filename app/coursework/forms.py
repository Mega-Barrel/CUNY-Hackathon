from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, BooleanField, SelectField, IntegerField
from wtforms.validators import ValidationError, DataRequired, Length, NumberRange


class AddCourseWorkForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=4, max=100)])
    classroom = SelectField('Class', validators = [DataRequired()], coerce = int)
    
    submit = SubmitField('Submit')
