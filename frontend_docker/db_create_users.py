from project import db
from project.models import User

# insert data
db.session.add(User('test','test'))
db.session.add(User('admin','admin'))

# commit the changes
db.session.commit()
