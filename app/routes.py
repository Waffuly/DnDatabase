from flask import render_template, flash, redirect, url_for, request, jsonify
from flask_login import current_user, login_user, logout_user, login_required
from app import app, db, photos
from app.forms import LoginForm, RegistrationForm, NewCharacterForm, CharacterSearchForm, DiceRoll
from app.models import User, Character, Sub_Race, Sub_Class, Results
from werkzeug.urls import url_parse
from werkzeug.utils import secure_filename
from pathlib import Path, PureWindowsPath, PurePath
import os

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
@login_required
def index():
	characters = Character.query.all()
	return render_template('index.html', title='Home Page', characters=characters)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
	logout_user()
	return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, first_name=form.first_name.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    characters = current_user.get_characters()
    return render_template('user.html', user=user, characters=characters, title='Profile')

@app.route('/user/<username>/create_new_char', methods=['GET', 'POST'])
@login_required
def create_new_char(username):
	user = User.query.filter_by(username=username).first_or_404()
	form = NewCharacterForm()
	form.sub_class.choices = [(sub_class.name, sub_class.name) for sub_class in Sub_Class.query.filter_by(char_class='Barbarian').all()]
	form.sub_race.choices = [(sub_race.name, sub_race.name) for sub_race in Sub_Race.query.filter_by(race='Aarakocra').all()]
	if request.method == 'POST':
		character = Character(name=form.name.data, race=form.race.data,\
		 char_class=form.char_class.data, sub_class=form.sub_class.data, sub_race=form.sub_race.data, level=form.level.data, hp=form.hp.data, party=form.party.data, user_id=user.id)
		db.session.add(character)
		db.session.commit()
		flash('Your character has been created!')
		return redirect(url_for('user', username=current_user.username))
	return render_template('create_new_char.html', user=user, form=form, title='Create New Character')

@app.route('/user/<username>/edit_character/<character>', methods=['GET', 'POST'])
@login_required
def edit_character(username, character):
	user = User.query.filter_by(username=username).first_or_404()
	char_id = user.id
	char = Character.query.filter_by(user_id=char_id, name=character).first_or_404()
	form = NewCharacterForm(obj=char)
	current_char_race = char.race
	current_char_class = char.char_class
	form.sub_race.choices = [(sub_race.name, sub_race.name) for sub_race in Sub_Race.query.filter_by(race=current_char_race).all()]
	form.sub_class.choices = [(sub_class.name, sub_class.name) for sub_class in Sub_Class.query.filter_by(char_class=current_char_class).all()]
	if request.method == 'POST':
		form.populate_obj(char)
		db.session.add(char)
		db.session.commit()
		flash('Your character has been saved!')
		return redirect(url_for('user', username=current_user.username))
	return render_template('edit_character.html', user=user, form=form, title='Edit Character')

@app.route('/user/<username>/<character>', methods=['GET', 'POST'])
@login_required
def display_character(username, character):
	if character == None:
		return redirect(url_for('index'))
	user = User.query.filter_by(username=username).first_or_404()
	char_id = user.id
	char = Character.query.filter_by(user_id=char_id, name=character).first_or_404()
	return render_template('display_char.html', username=user, character=char, title=str(character))

@app.route('/search', methods=['GET', 'POST'])
@login_required
def search():
	search = CharacterSearchForm(request.form)
	if request.method == 'POST':
		return search_results(search)
	return render_template('search.html', form=search, title="Search")

@app.route('/results', methods=['GET', 'POST'])
@login_required
def search_results(search):
	results = []
	first_string = search.data['search']
	second_string = first_string.lower()
	search_string = second_string.capitalize()
	if search_string:
		if search.data['select'] == 'name':
			qry = Character.query.filter(Character.name.contains(search_string))
			results = qry.all()
		elif search.data['select'] == 'char_class':
			qry = Character.query.filter(Character.char_class.contains(search_string))
			results = qry.all()
		elif search.data['select'] == 'race':
			qry = Character.query.filter(Character.race.contains(search_string))
			results = qry.all()
		elif search.data['select'] == 'level':
			qry = Character.query.filter(Character.level.contains(search_string))
			results = qry.all()
		elif search.data['select'] == 'party':
			qry = Character.query.filter(Character.party.contains(search_string))
			results = qry.all()
		else:
			qry = db.session.query(Character)
			results = qry.all()
	else:			
		qry = db.session.query(Character)
		results = qry.all()

	if not results:
		flash('No results found!')
		return redirect(url_for('search'))

	else:
		table = Results(results)
		table.border = True
		return render_template('results.html', results=results, table=table, title="Search Results")

@app.route('/dice_roller', methods=['GET', 'POST'])
@login_required
def dice_roller():
	form = DiceRoll(request.form)
	num = 0
	return render_template('dice_roller.html', form=form, num=num)

@app.route('/dice_update', methods=['POST'])
def dice_update():
	num = request.form['result']
	return jsonify({'result': num})

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/upload/<username>', methods=['GET', 'POST'])
@login_required
def upload(username):
	user = User.query.filter_by(username=username).first_or_404()

	if request.method == 'POST':

		if 'photo' not in request.files:
			flash('No file part')
			return redirect(url_for('user', username=username))

		file = request.files['photo']

		if file.filename == '':
			flash("No selected file")
			return redirect(url_for('user', username=username))

		if file and allowed_file(file.filename):
			
			# TODO
			# language to delete old photos using OS neutral path
			# if user.profile_photo:
			# 	delete_old = os.path.normpath(user.profile_photo)
			# 	flash(str(delete_old))
			# 	os.remove(user.profile_photo)

			# save requested img to server
			filename = Path(secure_filename(file.filename)).as_posix()
			flash(filename)
			filename_2 = photos.save(request.files['photo'])

			# establish OS neutral file path to save to DB
			pure_path = Path(PureWindowsPath('\\static\\img\\'))
			user.profile_photo = os.path.join(pure_path.as_posix(), filename)

			#commit filepath string to db
			db.session.commit()

			flash("New Avatar Uploaded Sucessfully!")
			return redirect(url_for('user', username=username))
	return render_template('upload.html', username=username)


# dynamic SelectField for sub_races
@app.route('/sub_race/<race>')
def sub_race(race):
	sub_races = Sub_Race.query.filter_by(race=race).all()
	sub_race_array = []
	for sub_race in sub_races:
		sub_race_obj = {}
		sub_race_obj['name'] = sub_race.name
		sub_race_array.append(sub_race_obj)
	return jsonify({'sub_races' : sub_race_array})

# dynamic SelectField for sub_classes
@app.route('/sub_class/<char_class>')
def sub_class(char_class):
	sub_classes = Sub_Class.query.filter_by(char_class=char_class).all()
	sub_class_array = []
	for sub_class in sub_classes:
		sub_class_obj = {}
		sub_class_obj['name'] = sub_class.name
		sub_class_array.append(sub_class_obj)
	return jsonify({'sub_classes' : sub_class_array})

@app.route('/delete_confirm/<character>', methods=['GET', 'POST'])
@login_required
def delete_confirm(character):
	char = Character.query.filter_by(name=character).first_or_404()
	char_name = char.name

	if request.method == 'POST':
		db.session.delete(char)
		db.session.commit()
		flash("Character Successfully Deleted!")
		return redirect(url_for('user', username=current_user.username))
	
	return render_template('delete_character.html', title="Delete Character", character=char_name)
