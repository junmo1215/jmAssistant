# coding = UTF8

import os
import random

from pony.orm import commit, db_session, select

import globalVariable
from core.common import interface_function, read_json_data
from entity.restaurantEntity import Restaurant

@interface_function
def install(with_data=None):
    if with_data is None:
        return

    restaurant_datas = read_json_data("restaurant.json")

    with db_session:
        for restaurant in restaurant_datas["Restaurant"]:
            if Restaurant.get(**restaurant) is None:
                Restaurant(**restaurant)

@interface_function
def uninstall():
    # 这里使用drop table之后似乎单元测试不能通过，不知道是不是在sqlite里面记录了什么表格相关的信息
    # Restaurant.drop_table(with_all_data=True)
    with db_session:
        for restaurant in Restaurant.select():
            restaurant.delete()

@interface_function
def add_restaurant(name):
    assert name is not None and name != "", "restaurant name is empty"
    with db_session:
        if Restaurant.get(name=name) is None:
            Restaurant(name=name)
        else:
            return "restaurant {} already in database".format(name)

    return "restaurant {} added success".format(name)

@interface_function
def choose():
    with db_session:
        restaurants = list(Restaurant.select())
        # print(restaurants, type(restaurants))
    assert len(restaurants) > 0, "no restaurant in database"

    random.shuffle(restaurants)
    return restaurants[0].name
