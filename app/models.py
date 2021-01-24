from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db, login


roles_users = db.Table('roles_users',
    db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
    db.Column('role_id', db.Integer(), db.ForeignKey('role.id'))
)

class_students = db.Table('class_students',
    db.Column('student_id', db.Integer(), db.ForeignKey('user.id')),
    db.Column('classroom_id', db.Integer(), db.ForeignKey('classroom.id'))
)

student_parents = db.Table('student_parents',
    db.Column('student_id', db.Integer(), db.ForeignKey('user.id')),
    db.Column('parent_id', db.Integer(), db.ForeignKey('user.id'))
)


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    roles = db.relationship('Role', secondary=roles_users,
                            backref=db.backref('users', lazy='dynamic'))

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(
            digest, size)


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class Role(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    permissions = db.Column(db.String(255))


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
