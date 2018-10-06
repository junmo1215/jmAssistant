# coding = UTF8

from nose.tools import with_setup
from jmAssistant.core.invoke_services import invoke, PARAMS_SPLIT_PATTERN

def test_base():
    names = ["alice", "bob"]
    assert invoke("hello", "hi", names[0]) == "hi, alice"
    assert invoke("hello", "hi") == "hi, anonymous"
    assert invoke("hello", "hi", PARAMS_SPLIT_PATTERN.join(names)) == "hi, alice, bob" 

def test_invoke_restaurant():
    assert invoke("restaurant", "install") is None
    assert invoke("restaurant", "add_restaurant", "aaa") is None
    assert invoke("restaurant", "choose") == "aaa"
