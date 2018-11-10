# coding = UTF8

import os
from pony import orm
import globalVariable

db = orm.Database()
DB_PATH = os.path.join(globalVariable.root_path, 'db', 'core.db')

class Service(db.Entity):
    service_name = orm.Required(str)
    function_name = orm.Required(str)
    params = orm.Required(str)
    users = orm.Set("User")
    key_words = orm.Set("KeyWord")
    orm.PrimaryKey(service_name, function_name)

class User(db.Entity):
    # 系统中的名字
    name = orm.PrimaryKey(str)
    wechat_id = orm.Optional(str)
    wechat_open_id = orm.Optional(str)
    services = orm.Set(Service)

class KeyWord(db.Entity):
    """
    调用相关服务输入的关键字
    """
    key_word = orm.PrimaryKey(str)
    service = orm.Required(Service)

db.bind(provider='sqlite', filename=DB_PATH, create_db=True)
db.generate_mapping(create_tables=True)
