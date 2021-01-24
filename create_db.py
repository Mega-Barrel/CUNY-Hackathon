from app import create_app, db
from config import Config
from app.models import Role, StateMetaData, Subject, Classroom, User, CourseworkInstance, Coursework

def create_metadata_tables():
    Role.insert_roles()
    StateMetaData.insert_states()
    Subject.insert_subjects()
    

_app = create_app(Config)
app_context = _app.app_context()
app_context.push()
db.drop_all()
db.create_all()
create_metadata_tables()

teacher_role = Role.query.filter_by(name = 'Teacher').first()
teacher = User(username='teacher', email='teacher@gmail.com', role=teacher_role)
teacher.password = '1234'

student_role = Role.query.filter_by(name = 'Student').first()
student = User(username='student', email='student@gmail.com', role=student_role)
student.password = '1234'
db.session.add(teacher)
db.session.add(student)

classroom = Classroom(name='Math 5th Grade', subject='Maths', creator_id=1)
db.session.add(classroom)
coursework1 = Coursework(name='Quiz 1', classroom=classroom, creator_id=1)
db.session.add(coursework1)
db.session.commit()

coursework2 = Coursework(name='Quiz 2', classroom=classroom, creator_id=1)
db.session.add(coursework2)
db.session.commit()


coursework_instance = CourseworkInstance(value=90.0, classroom_id=1, student_id=2, creator_id=1, coursework=coursework1)
db.session.add(coursework_instance)
db.session.commit()
coursework_instance = CourseworkInstance(value=90.0, classroom_id=1, student_id=2, creator_id=1, coursework=coursework2)
db.session.add(coursework_instance)

db.session.commit()
