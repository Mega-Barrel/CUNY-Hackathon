import os
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length

from app.decorators import permission_required
from app.models import StudentDetails, StateMetaData

def get_states():
    states = []
    
    base = os.path.abspath(os.path.dirname(__file__))
        
    file_name = os.path.join(base, '../resources', 'states.csv')
    with open(file_name) as file:
        lines = file.readlines()
        for line in lines:
            state_name = line.split(',')[0]
            states.append((state_name, state_name))
    
    return states

class StudentDetailsForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    address = StringField('Address', validators=[DataRequired()])
    city = StringField('City', validators=[DataRequired()])
    state = SelectField('State', choices = get_states())
    zip = StringField('Zip', validators=[DataRequired()])
    parent_name = StringField('Parent Name', validators=[DataRequired()])
    emergency_contact = StringField('Emergency Contact', validators=[DataRequired(), Length(10, 10, '10 Digit Phone number required')])
    medical_conditions = StringField('Medical Conditions')
    comments = StringField('Comments')
    submit = SubmitField('Submit')
