# coding = UTF8

import os

def init():
    global gContext, root_path
    gContext = {}
    root_path = os.path.dirname(os.path.realpath(__file__))

init()
