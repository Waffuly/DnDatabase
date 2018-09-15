from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField, Form, SelectField
from wtforms.validators import DataRequired, ValidationError, EqualTo
from app.models import User, Character

class LoginForm(FlaskForm):
	username = StringField('Username', validators=[DataRequired()])
	password = PasswordField('Password', validators=[DataRequired()])
	remember_me = BooleanField('Remember Me')
	submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    first_name = StringField('First Name', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

class NewCharacterForm(FlaskForm):
	class_choices = [
					('Barbarian', 'Barbarian'),
					('Bard', 'Bard'),
					('Cleric', 'Cleric'),
					('Druid', 'Druid'),
					('Fighter', 'Fighter'),
					('Monk', 'Monk'),
					('Paladin', 'Paladin'),
					('Ranger', 'Ranger'),
					('Rogue', 'Rogue'),
					('Sorcerer', 'Sorcerer'),
					('Warlock', 'Warlock'),
					('Wizard', 'Wizard')
					]
	race_choices = [
					('Aarakocra', 'Aarakocra'),
					('Aasimar', 'Aasimar'),
					('Bugbear', 'Bugbear'),
					('Centaur', 'Centaur'),
					('Changeling', 'Changeling'),
					('Dragonborn', 'Dragonborn'),
					('Dwarf', 'Dwarf'),
					('Elf', 'Elf'),
					('Feral Tiefling', 'Feral Tiefling'),
					('Firbolg', 'Firbolg'),
					('Genasi', 'Genasi'),
					('Gith', 'Gith'),
					('Gnome', 'Gnome'),
					('Goblin', 'Goblin'),
					('Goliath', 'Goliath'),
					('Half-Elf', 'Half-Elf'),
					('Halfling', 'Halfing'),
					('Half-Orc', 'Half-Orc'),
					('Hobgoblin', 'Hobgoblin'),
					('Human', 'Human'),
					('Kalashtar', 'Kalashtar'),
					('Kenku', 'Kenku'),
					('Kobold', 'Kobold'),
					('Lizardfolk', 'Lizardfolk'),
					('Loxodon', 'Loxodon'),
					('Minotaur', 'Minotaur'),
					('Orc', 'Orc'),
					('Shifter', 'Shifter'),
					('Simic Hybrid', 'Simic Hybrid'),
					('Tabaxi', 'Tabaxi'),
					('Tiefling', 'Tiefling'),
					('Tortle', 'Tortle'),
					('Triton', 'Triton'),
					('Vedalken', 'Vedalken'),
					('Viashino', 'Viashino'),
					('Warforged', 'Warforged'),
					('Yuan-ti Pureblood', 'Yuan-ti Pureblood')]
	name = StringField('Character Name', validators=[DataRequired()])
	race = SelectField('Character Race', choices=race_choices, validators=[DataRequired()])
	sub_race = SelectField('Character Sub-Race', choices=[], coerce=str, validators=[DataRequired()])
	char_class = SelectField('Character Class', choices=class_choices, validators=[DataRequired()])
	sub_class = SelectField('Character Sub-Class', choices=[], coerce=str, validators=[DataRequired()])
	level = IntegerField('Character Level', validators=[DataRequired()])
	hp = IntegerField('Max HP')
	party = StringField('Party')
	submit = SubmitField('Create Character')
	# add list of existent parties

class CharacterSearchForm(FlaskForm):
	choices = [('name', 'Name'),
				('char_class', 'Class'),
				('race', 'Race'),
				('level', 'Level'),
				('party', 'Party')]
	select = SelectField('Search for characters:', choices=choices)
	search = StringField('')

class DiceRoll(FlaskForm):
	choices = [
				(4, 'd4'),
				(6, 'd6'),
				(8, 'd8'),
				(10, 'd10'),
				(12, 'd12'),
				(20, 'd20')
				]
	dice_select = SelectField('Choose your die:', choices=choices)