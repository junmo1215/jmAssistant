from pony import orm

db = orm.Database()

class Restaurant(db.Entity):
    name = orm.Required(str, unique=True)
    # orm.PrimaryKey(name)

db.bind(provider='sqlite', filename='../db/restaurant.db', create_db=True)
db.generate_mapping(create_tables=True)
