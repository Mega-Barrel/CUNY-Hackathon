import os

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from app import db, login


class_students = db.Table('class_students',
    db.Column('student_id', db.Integer(), db.ForeignKey('user.id')),
    db.Column('classroom_id', db.Integer(), db.ForeignKey('classroom.id'))
)

student_parents = db.Table('student_parents',
    db.Column('student_id', db.Integer(), db.ForeignKey('user.id')),
    db.Column('parent_id', db.Integer(), db.ForeignKey('user.id'))
)


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))


    def __repr__(self):
        return '<User {}>'.format(self.username)

    @property
    def password(self):
        raise AttributeError('Password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(
            digest, size)
        
    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        if self.role is None:
            self.role = Role.query.filter_by(default = True).first()
        
        
class Permissions:
    ## Modify to add permissions as powers of 2
    WRITE_GRADES = 1
    READ_GRADES = 2
    WRITE_COMMENTS = 4
    LIST_DB_DATA = 8

class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(64), unique = True)
    default = db.Column(db.Boolean, default = False, index = True)
    permissions = db.Column(db.Integer)
    users = db.relationship('User', backref = 'role')
    
    def __init__(self, **kwargs):
        super(Role, self).__init__(**kwargs)
        if self.permissions is None:
            self.permissions = 0
            
    def has_permission(self, permission):
        return self.permissions & permission == permission
    
    def reset_permissions(self):
        self.permissions = 0
    
    def add_permission(self, permission):
        if not self.has_permission(permission):
            self.permissions += permission
            
    @staticmethod
    def insert_roles():
        ## Modify to define roles and associated permissions
        roles = {
            'Student': [Permissions.WRITE_COMMENTS, Permissions.READ_GRADES],
            'Teacher': [Permissions.WRITE_COMMENTS, Permissions.WRITE_GRADES, Permissions.READ_GRADES],
            'Administrator': [Permissions.WRITE_COMMENTS, Permissions.WRITE_GRADES, Permissions.READ_GRADES, Permissions.LIST_DB_DATA]
        }
        default_role = 'Student'
        for r, permissions in roles.items():
            role = Role.query.filter_by(name = r).first()
            if role is None:
                role = Role(name = r)
            role.reset_permissions()
            for permission in permissions:
                role.add_permission(permission)
            role.default = (r == default_role)
            db.session.add(role)
        db.session.commit()
        
    def __repr__(self):
        return '<Role {}>'.format(self.name)


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class Classroom(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100)) 
    description = db.Column(db.String(140)) 
    subject = db.Column(db.String(50)) 
    term = db.Column(db.String(50))
    year = db.Column(db.Integer())
    time = db.Column(db.String(10))
    active = db.Column(db.Boolean())
    creator_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    students = db.relationship('User', secondary=class_students,
                               backref=db.backref('classroom', lazy='dynamic'))

    def __init__(self, name, description, subject, term, year, time, active, creator_id):
        self.name = name
        self.description = description
        self.subject = subject
        self.term = term
        self.year = year
        self.time = time
        self.active = active
        self.creator_id = creator_id



class CourseworkInstance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.Float)
    date_occurred = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime)
    graded = db.Column(db.Boolean)
    comments = db.Column(db.String(120))
    classroom_id = db.Column(db.Integer, db.ForeignKey('classroom.id'), nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    creator_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    coursework_id = db.Column(db.Integer, db.ForeignKey('coursework.id'), nullable=False)

    def __init__(self, value, date_occurred, updated_at, created_at, graded, comments, classroom_id, student_id, creator_id, coursework_id):
        self.value = value
        self.date_occurred = date_occurred
        self.updated_at = updated_at
        self.created_at = created_at
        self.graded = graded
        self.comments = comments
        self.classroom_id = classroom_id
        self.student_id = student_id
        self.creator_id = creator_id
        self.coursework_id = coursework_id

class Coursework(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    score_type = db.Column(db.String(120))
    max_value = db.Column(db.Float)
    min_value = db.Column(db.Float)
    graded_item_type = db.Column(db.String(120))
    classroom_id = db.Column(db.Integer, db.ForeignKey('classroom.id'), nullable=False)
    creator_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __init__(self, id, score_type, max_value, min_value, graded_item_type, class_id, creator_id):
        self.score_type = score_type
        self.max_value = max_value
        self.min_value = min_value
        self.graded_item_type = graded_item_type
        self.classroom_id = classroom_id
        self.creator_id = creator_id


class CourseworkType(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    category = db.Column(db.String(120))
    item_type = db.Column(db.String(120))
    updated_at = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime)
    classroom_id = db.Column(db.Integer, db.ForeignKey('classroom.id'), nullable=False)
    creator_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    def __init__(self, name, category, item_type, updated_at, created_at, classroom_id, creator_id):
        self.name = name
        self.category = category
        self.item_type = item_type
        self.updated_at = updated_at
        self.created_at = created_at
        self.classroom_id = classroom_id
        self.creator_id = creator_id


class Subject(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    
    def __init__(self, name):
        self.name = name

    @staticmethod
    def insert_subjects():
        # Some testing subjects
        for _subject in ['Math', 'Science', 'History', 'English', 'Spanish']:
            db.session.add(Subject(name=_subject))
        db.session.commit()


class StudentDetails(db.Model):
    __tablename__ = 'student_details'
    id = db.Column(db.Integer, primary_key = True)
    first_name = db.Column(db.String(64))
    last_name = db.Column(db.String(64))
    address = db.Column(db.String(128))
    city = db.Column(db.String(64))
    state = db.Column(db.String(64))
    zip = db.Column(db.String(64))
    parent_name = db.Column(db.String(64))
    emergency_contact = db.Column(db.String(64))
    medical_conditions = db.Column(db.String(256))
    comments = db.Column(db.String(256))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    
class StateMetaData(db.Model):
    __tablename__ = 'state_metadata'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(64), index = True)
    
    @staticmethod
    def insert_states():
        base = os.path.abspath(os.path.dirname(__file__))
        
        file_name = os.path.join(base, 'resources', 'states.csv')
        with open(file_name) as file:
            line = file.readline()
            state_name = line.split(',')[0]
            state = StateMetaData.query.filter_by(name = state_name).first()
            if state is None:
                state = StateMetaData(name = state_name)
            db.session.add(state)
        db.session.commit()
