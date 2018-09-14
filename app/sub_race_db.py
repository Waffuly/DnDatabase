from app import db
from app.models import Sub_Race

def new_sub_race(race, name):
	x = Sub_Race(race=race, name=name)
	db.session.add(x)
	db.session.commit()
	return "Committed {}, sub-race of {} to DB!".format(name, race)