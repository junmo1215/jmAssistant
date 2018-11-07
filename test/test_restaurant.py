# coding = UTF8

import numpy as np

from nose.tools import with_setup, raises
from service.restaurant import install, uninstall, add_restaurant, choose, vote, scores_to_priority, list_all

@with_setup(install, uninstall)
def test_base():
    add_restaurant("asdf")
    for i in range(10):
        add_restaurant(str(i))
    choose()
    # print(list_all())

@raises(Exception)
@with_setup(install, uninstall)
def test_error():
    uninstall()
    choose()

@with_setup(install, uninstall)
def test_priotity():
    restaurants = {
        '0': 5,
        '1': 9,
        '2': 4,
        '3': 2,
        '4': 3
    }

    names = []
    scores = []
    for name, score in restaurants.items():
        names.append(name)
        scores.append(score)

        add_restaurant(name)
        # 减去初始分数默认值5分
        vote(name, score - 5)

    p = scores_to_priority(scores)

    # 概率和应该为1
    assert abs(1 - np.sum(p)) < 0.01
    # 概率与分数正相关
    assert p[1] > p[0] > p[2] > p[4] > p[3]
    # 5分与6分4分的差距 大于3分与2分的差距
    assert p[0] - p[2] > p[4] - p[3]

    count = 1000
    stat = {'0': 0, '1': 0, '2': 0, '3': 0, '4': 0}
    for i in range(count):
        choose_name = choose()
        stat[choose_name] += 1

    for i in range(5):
        # 对比实际测试的几率跟概率的差值应该小于5%
        # 测试10000次大概5秒左右，应该主要是读数据库太慢了
        # 降低测试次数，增大允许的误差为5%，实际测试超过2%的都不太多
        assert abs(stat[str(i)] / count - p[i]) < 0.05

