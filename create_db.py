from app import create_app, db
from config import Config
from app.models import Role, StateMetaData

def create_metadata_tables():
    Role.insert_roles()
    StateMetaData.insert_states()

_app = create_app(Config)
app_context = _app.app_context()
app_context.push()
db.create_all()
create_metadata_tables()