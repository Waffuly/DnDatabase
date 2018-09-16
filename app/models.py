from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from hashlib import md5
from flask_table import Table, Col

class User(UserMixin, db.Model):
		
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(64), index=True, unique=True)
	first_name = db.Column(db.String(64))
	password_hash = db.Column(db.String(128))
	profile_photo = db.Column(db.String(128))
	characters = db.relationship('Character', backref='player', lazy='dynamic')

	def set_password(self, password):
		self.password_hash = generate_password_hash(password)

	def check_password(self, password):
		return check_password_hash(self.password_hash, password)


	def __repr__(self):
	    return '<{}>'.format(self.username)

	def get_photo(self):
		photo_exists = self.profile_photo
		if photo_exists:
			return photo_exists.filename
		else:
			return ''

	def avatar(self, size):
		digest = md5(self.first_name.lower().encode('utf-8')).hexdigest()
		return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(
	    digest, size)

	def get_characters(self):
		char_list = Character.query.filter_by(user_id=self.id).all()   
		return char_list

class Character(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(64), index=True)
	level = db.Column(db.Integer)
	race = db.Column(db.String(64))
	sub_race = db.Column(db.String(64))
	char_class = db.Column(db.String(64))
	sub_class = db.Column(db.String(64))
	hp = db.Column(db.Integer)
	party = db.Column(db.String(64), nullable=True)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

	def __repr__(self):
		return "<{}>".format(self.name)

class Sub_Race(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	race = db.Column(db.String(64))
	name = db.Column(db.String(64))

class Sub_Class(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	char_class = db.Column(db.String(64))
	name = db.Column(db.String(64))

class Results(Table):
	id = Col('Id', show=False)
	name = Col('Name')
	char_class = Col('Class')
	race = Col('Race')
	level = Col('Level')
	party = Col('Party')


@login.user_loader
def load_user(id):
	return User.query.get(int(id))