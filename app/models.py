from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import os

from app import db, login


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
        

