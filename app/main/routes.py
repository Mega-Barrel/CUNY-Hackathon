from flask import render_template
from flask_login import login_required
from app.main import bp


@bp.route('/', methods=['GET', 'POST'])
@bp.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    return render_template('main/index.html', title='Home')


@bp.route('/home', methods=['GET', 'POST'])
@login_required
def home():
    return render_template('main/home.html', title='Home')


