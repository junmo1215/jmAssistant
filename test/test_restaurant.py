# coding = UTF8

from nose.tools import *
from jmAssistant.service.restaurant import install, uninstall, add_restaurant, choose

@with_setup(install, uninstall)
def test_base():
    add_restaurant("asdf")
    for i in range(10):
        add_restaurant(str(i))
    print(choose())

