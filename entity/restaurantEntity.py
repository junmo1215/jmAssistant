# coding = UTF8

import os
from pony import orm
import globalVariable
db = orm.Database()
DB_PATH = os.path.join(globalVariable.root_path, 'db', 'restaurant.db')

class Restaurant(db.Entity):
    name = orm.Required(str, unique=True)
    # orm.PrimaryKey(name)

db.bind(provider='sqlite', filename=DB_PATH, create_db=True)
db.generate_mapping(create_tables=True)
