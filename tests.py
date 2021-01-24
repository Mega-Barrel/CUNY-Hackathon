import unittest

from app import create_app, db
from app.models import User, Role, StateMetaData, Subject, Classroom
from config import Config


class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'


class UserModelCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        Role.insert_roles()
        StateMetaData.insert_states()
        Subject.insert_subjects()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_follow(self):
        u1 = User(username='richard', email='richard@example.com', role_id=2)
        u2 = User(username='rich', email='rich@example.com', role_id=1)
        u3 = User(username='bob', email='bob@example.com', role_id=1)

        db.session.add_all([u1, u2, u3])
        db.session.commit()

        classroom = Classroom(
            name='5th Grade Math', description='math', subject='Math',
            term='Spring 2021', year=2021, time='09:00AM', active=True,
            creator_id=u1.id
        )
        db.session.add(classroom)
        db.session.commit()

        classroom.add_student(u2)
        classroom.add_student(u3)
        db.session.commit()
        self.assertTrue(classroom.is_student(u2))
        self.assertTrue(classroom.is_student(u3))
        classroom.remove_student(u3)
        db.session.commit()
        self.assertTrue(classroom.is_student(u2))
        self.assertFalse(classroom.is_student(u3))


if __name__ == '__main__':
    unittest.main(verbosity=2)