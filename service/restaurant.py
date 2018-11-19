# coding = UTF8

import os
import random
import numpy as np

from pony.orm import commit, db_session, select

import globalVariable
from core.common import interface_function, read_json_data
from entity.restaurantEntity import Restaurant

INIT_SCORE = 5
MAX_SCORE = 10
MIN_SCORE = 0

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

@interface_function(key_words=["增加餐馆"])
def add_restaurant(name, user_name=None):
    assert name is not None and name != "", "restaurant name is empty"

    if user_name is None:
        user_name = globalVariable.gContext["from_user"]

    with db_session:
        if Restaurant.get(user_name=user_name, name=name) is None:
            Restaurant(user_name=user_name, name=name, score=5)
        else:
            return "restaurant {} already in database".format(name)

    return "restaurant {} added success".format(name)

@interface_function(key_words=["删除餐馆"])
def remove_restaurant(name, user_name=None):
    assert name is not None and name != "", "restaurant name is empty"

    if user_name is None:
        user_name = globalVariable.gContext["from_user"]

    with db_session:
        restaurant = Restaurant.get(user_name=user_name, name=name)
        if restaurant is not None:
            restaurant.delete()
            return "restaurant {} remove success".format(name)
        else:
            return "restaurant {} not exists".format(name)

def softmax(scores):
    scores -= np.max(scores)
    return np.exp(scores) / np.sum(np.exp(scores))

def sigmoid(scores):
    return 1 / (1 + np.exp(-scores))

def scores_to_priority(scores):
    """
    根据得分获得每个元素的概率
    分数在0到10之间，所有元素概率和为1
    """
    scores = np.array(scores)
    return softmax(sigmoid(scores - INIT_SCORE))

@interface_function(key_words=["吃啥", "吃什么"])
def choose(user_name = None):
    if user_name is None:
        user_name = globalVariable.gContext["from_user"]

    with db_session:
        restaurants = list(Restaurant.select(lambda r: r.user_name == user_name))
        # print(restaurants, type(restaurants))
    assert len(restaurants) > 0, "no restaurant in database"

    names = []
    scores = []
    for restaurant in restaurants:
        names.append(restaurant.name)
        scores.append(restaurant.score)

    # p的结果类似 [0.3, 0.2, 0.4, 0.1]
    # np.sum(p[:i+1])的值依次是 0.3 0.5 0.9 1
    # 随机一个0到1之间的小数，依次跟sum从左到右比较
    # 遇到第一个大于等于随机数的索引就是餐厅名字的索引
    p = scores_to_priority(scores)
    random_value = random.random()
    for i in range(len(restaurants)):
        if random_value <= np.sum(p[:i+1]):
            return names[i]

@interface_function(key_words=["餐馆打分"])
def vote(name, score, user_name=None):
    try:
        score = int(score)
    except:
        return "score should be int"

    if user_name is None:
        user_name = globalVariable.gContext["from_user"]

    with db_session:
        restaurant = Restaurant.get(user_name=user_name, name=name)
        assert restaurant is not None, "restaurant not found"

        old_score = restaurant.score
        old_score += score

        # 分数限制在0到10之间
        # 防止计算概率的时候过于不均匀
        if old_score > MAX_SCORE:
            old_score = MAX_SCORE
        elif old_score < MIN_SCORE:
            old_score = MIN_SCORE

        restaurant.score = old_score

    return "now score of {} is {}".format(name, old_score)

@interface_function(key_words=["餐馆列表"])
def list_all(user_name=None):
    if user_name is None:
        user_name = globalVariable.gContext["from_user"]

    results = []
    with db_session:
        restaurants = Restaurant.select(lambda r: r.user_name == user_name)

        for restaurant in restaurants:
            results.append("{}\t{}".format(restaurant.name, restaurant.score))

    return "\n".join(results)


