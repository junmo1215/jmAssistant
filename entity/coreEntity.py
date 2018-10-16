from pony import orm

db = orm.Database()

class Services(db.Entity):
    service_name = orm.Required(str)
    function_name = orm.Required(str)
    params = orm.Required(str)
    orm.PrimaryKey(service_name, function_name)

db.bind(provider='sqlite', filename='../db/core.db', create_db=True)
db.generate_mapping(create_tables=True)
