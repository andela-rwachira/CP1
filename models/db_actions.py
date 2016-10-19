from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.database import *
from models.amity import Amity

amity = Amity()


class Database(object):

	def save_state(self, db_name):
		self.engine = create_engine_db(db_name)
		engine = create_engine("sqlite:///models/"+db_name)
		Base.metadata.bind = engine
		DBSession = sessionmaker(bind=engine)
		session = DBSession()

		db_rooms_table = session.query(Rooms).all()
		db_rooms = []
		for db_room in db_rooms_table:
			db_rooms.append(db_room.room_name)	
		if len(amity.all_rooms) > 0:
			for room in amity.all_rooms:
				if room.room_name in db_rooms:
					session.query(Rooms).filter_by(room_name=room.room_name).update({Rooms.room_occupants: len(room.occupants)})
					session.commit()
				else:
					new_room = Rooms()
					new_room.room_name = room.room_name
					new_room.room_type = room.room_type
					new_room.room_capacity = room.capacity
					new_room.room_occupants = len(room.occupants)
					session.add(new_room)
					session.commit()
		else:
			print ("There are currently no rooms to save")

		db_people_table = session.query(People).all()
		db_people = []
		for db_person in db_people_table:
			db_people.append(db_person.person_name)
		if len(amity.all_people) > 0:
			for person in amity.all_people:
				if person.person in db_people: 
					session.query(People).filter_by(person_name=person.person).update({People.assigned_office: person.assigned_office})
					session.query(People).filter_by(person_name=person.person).update({People.assigned_office: person.assigned_living})
					session.commit()
				else:
					new_person = People()
					new_person.person_name = person.person
					new_person.person_role = person.role
					new_person.accomodation = person.accomodation
					new_person.assigned_office = person.assigned_office
					new_person.assigned_living = person.assigned_living
					session.add(new_person)
					session.commit()
		else:
			print ("There are currently no people to save")

	def load_state(self, db_name):
		self.engine = create_engine_db(db_name)
		engine = create_engine("sqlite:///models/"+db_name)
		Base.metadata.bind = engine
		DBSession = sessionmaker(bind=engine)
		session = DBSession()



