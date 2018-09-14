from app import db
from app.models import Sub_Class

def new_sub_class(char_class, name):
	x = Sub_Class(char_class=char_class, name=name)
	db.session.add(x)
	db.session.commit()
	return "Committed {}, sub-class of {} to DB!".format(name, char_class)