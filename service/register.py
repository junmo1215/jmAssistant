# coding = UTF8

import os
from flask import Blueprint, render_template, abort

import config
from core.common import interface_function
from pony.orm import db_session
from entity.coreEntity import User

register_page = Blueprint('register_page', __name__,
                        template_folder='templates',
                        root_path=os.path.join(config.root_path, "web"))

@register_page.route("/register")
def register():
    return render_template("register.html")

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