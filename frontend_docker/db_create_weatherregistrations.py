from project import db
from project.models import WeatherRegistration

# create the database and the db table
db.create_all()

# insert data
db.session.add(WeatherRegistration('Toronto', 123456, 'Canada', 1))

# commit the changes
db.session.commit()
