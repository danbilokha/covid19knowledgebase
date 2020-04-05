import os

from flask import Flask, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy

from project.constants import DB_URL

app = Flask(__name__)
Bootstrap(app)
SECRET_KEY = os.urandom(32)

app.config['SECRET_KEY'] = os.urandom(32)
app.config['TESTING'] = True
app.config['TEMPLATES_AUTO_RELOAD'] = True

app.config['SQLALCHEMY_DATABASE_URI'] = DB_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.config['BOOTSTRAP_USE_MINIFIED'] = False

db = SQLAlchemy(app)

from project.dbmanager.views import dbmanager_blueprint
from project.api.views import api_v1_blueprint

app.register_blueprint(dbmanager_blueprint, url_prefix='/manager')
app.register_blueprint(api_v1_blueprint, url_prefix='/api/v1')


@app.before_first_request
def setup():
    # if not database_exists(db.engine.url):

    from project.tables import Base
    Base.metadata.create_all(db.engine)  # will not re-write existing tables, just will create new one

    # db.create_all()
    # db.session.commit()
    # create_database(db.engine.url)
    # Base.metadata.drop_all(bind=db.engine)
    # Base.metadata.create_all(bind=db.engine)


@app.route('/', methods=['GET'])
def index():
    return redirect(url_for('dbmanager.index'))
