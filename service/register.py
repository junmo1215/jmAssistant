# coding = UTF8

from core.common import interface_function
from pony.orm import db_session
from entity.coreEntity import User

@interface_function
def install(with_data=None):
    pass

@interface_function
def uninstall():
    pass

@interface_function(key_words=["注册用户"])
def regiester(user_name):
    assert user_name is not None, "user_name can't be empty"
    user_name = user_name.strip()
    assert user_name != "", "user_name can't be empty"

    with db_session:
        if User.get(name=user_name) is not None:
            return "user {} already exists".format(user_name)
        
        user = User(name=user_name)

    return "user {} add success".format(user_name)

@interface_function(key_words=["删除用户"])
def delete(user_name):
    assert user_name is not None, "user_name can't be empty"
    user_name = user_name.strip()
    assert user_name != "", "user_name can't be empty"

    with db_session:
        user = User.get(name=user_name)
        if user is None:
            return "user {} not exists".format(user_name)
        
        user.delete()
    
    return "user {} delete success".format(user_name)