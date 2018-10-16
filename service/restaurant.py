# coding = UTF8

import os
import random

from pony.orm import commit, db_session, select

from core.common import interface_function
from entity.restaurantEntity import Restaurant

@interface_function
def install():
    pass

@interface_function
def uninstall():
    # 这里使用drop table之后似乎单元测试不能通过，不知道是不是在sqlite里面记录了什么表格相关的信息
    # Restaurant.drop_table(with_all_data=True)
    with db_session:
        for restaurant in Restaurant.select():
            restaurant.delete()

@interface_function
def add_restaurant(name):
    assert name is not None and name != ""
    with db_session:
        Restaurant(name=name)
        commit()

    return "restaurant {} added success".format(name)

@interface_function
def choose():
    with db_session:
        restaurants = list(Restaurant.select())
        # print(restaurants, type(restaurants))
    random.shuffle(restaurants)
    return restaurants[0].name
