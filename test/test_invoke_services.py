# coding = UTF8

from nose.tools import with_setup
from core.invoke_services import invoke, PARAMS_SPLIT_PATTERN

from globalVariable import gContext
import config

def setup():
    gContext["from_user"] = config.admin

@with_setup(setup)
def test_base():
    names = ["alice", "bob"]
    assert invoke("hello", "hi", names[0]) == "hi, alice"
    assert invoke("hello", "hi") == "hi, anonymous"
    assert invoke("hello", "hi", PARAMS_SPLIT_PATTERN.join(names)) == "hi, alice, bob" 

@with_setup(setup)
def test_invoke_restaurant():
    assert invoke("restaurant", "uninstall") is None
    assert invoke("restaurant", "install") is None
    assert invoke("restaurant", "add_restaurant", "aaa") == "restaurant aaa added success"
    assert invoke("restaurant", "choose") == "aaa"
    assert invoke("restaurant", "uninstall") is None
