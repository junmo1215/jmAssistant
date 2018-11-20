# coding = UTF8

import uuid
from nose.tools import with_setup
from service.register import regiester, delete
from entity.coreEntity import User
from pony.orm import db_session

def user_num():
    with db_session:
        return len(list(User.select()))

def test_base():
    init_length = user_num()
    name1 = str(uuid.uuid1())
    name2 = str(uuid.uuid1())

    delete(name1)
    delete(name2)

    assert regiester(name1) == "user {} add success".format(name1)
    assert user_num() == init_length + 1, user_num()
    assert regiester(name1) == "user {} already exists".format(name1)
    assert user_num() == init_length + 1, user_num()
    assert regiester(name2) == "user {} add success".format(name2)
    assert user_num() == init_length + 2, user_num()
    delete(name1)
    delete(name2)
    assert user_num() == init_length, user_num()
