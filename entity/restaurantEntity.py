# coding = UTF8

import os
from pony import orm
import globalVariable
db = orm.Database()
DB_PATH = os.path.join(globalVariable.root_path, 'db', 'restaurant.db')

class Restaurant(db.Entity):
    user_name = orm.Required(str)
    name = orm.Required(str)
    score = orm.Required(int)
    orm.PrimaryKey(user_name, name)

db.bind(provider='sqlite', filename=DB_PATH, create_db=True)
db.generate_mapping(create_tables=True)
