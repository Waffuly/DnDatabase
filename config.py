import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
	SECRET_KEY = os.environ.get('SECRET_KEY') or 'REPLACE ME'
	SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'postgres://postgres:cello11@localhost:5432/dnd_db'
	SQLALCHEMY_TRACK_MODIFICATIONS = False
	WHOOSH_BASE = os.path.join(basedir, 'search.db')
