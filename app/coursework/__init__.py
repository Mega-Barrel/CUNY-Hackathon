from flask import Blueprint

bp = Blueprint('coursework', __name__)

from app.coursework import routes