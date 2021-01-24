from flask import Blueprint

bp = Blueprint('classroom', __name__)

from app.classroom import routes