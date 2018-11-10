# coding = UTF8

import os
import imp
import json
import functools
import globalVariable

# 封装接口函数，用这个装饰器和其他的函数区分
# 接口函数只能有这一个装饰器，并且不能再增加其他装饰器
def interface_function(original_function=None, key_words=[]):
    def wrapper(function):
        # print(function)
        @functools.wraps(function)
        def _wrapper(*args, **kwargs):
            return function(*args, **kwargs)

        _wrapper.is_interface_function = True
        _wrapper.key_words = key_words

        _wrapper.co_varnames = function.__code__.co_varnames
        _wrapper.co_argcount = function.__code__.co_argcount
        return _wrapper

    if original_function is None:
        return wrapper

    return wrapper(original_function)

def read_json_data(file_name, dir_path = None):
    """
    读取指定目录下的json文件，返回json对象
    数据文件默认目录为 project_root/datas/
    没有找到文件返回 {}
    """
    if dir_path is None:
        dir_path = os.path.join(globalVariable.root_path, "datas")

    file_path = os.path.join(dir_path, file_name)
    if os.path.exists(file_path) == False:
        return {}

    with open(file_path, "r", encoding="UTF8") as f:
        data = json.load(f)

    return data

def get_function(file_path, function_name):
    # 取出文件名字作为module名称
    service_name = os.path.basename(file_path)[:-3]
    service = imp.load_source(service_name, file_path)
    func = eval("service.{}".format(function_name))
    return func
