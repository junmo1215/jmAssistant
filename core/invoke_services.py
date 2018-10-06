# coding = UTF8

import imp
import json
import sqlite3

DB_NAME = "db/core.db"
PARAMS_SPLIT_PATTERN = " "

def invoke(service_name, function_name, params=None):
    """
    调用指定服务的指定功能

    service_name：服务的名称，对应的.py文件必须要放在service/文件夹下，如果有class，class的名称需要与service_name名称相同
    function: 功能名称
    params: 参数
    """
    service = imp.load_source(service_name, 'service/{}.py'.format(service_name))
    func = eval("service.{}".format(function_name))
    # 解析成json格式的参数
    params = parse_parameters(service_name, function_name, params)

    try:
        return func(**params)
    except Exception as e:
        return "[error]" + str(e)

def parse_parameters(service_name, function_name, params):
    """
    将字符串形式的params转变成json格式，最后的结果可以直接通过func(**params)的形式调用指定的功能
    params可以是None代表所有参数都是默认值
    如果有多个参数使用PARAMS_SPLIT_PATTERN分隔不同的参数

    目前的做法是按照顺序依次往后面的参数中填充
    """
    assert params is None or type(params) == str

    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("SELECT params FROM services WHERE service_name = '{}' and function_name = '{}';".format(service_name, function_name))
    # 读取指定功能需要填充的参数
    param_format = cur.fetchone()[0]

    # 将传进来的参数转换成list
    if params is not None:
        list_params = params.split(PARAMS_SPLIT_PATTERN)
    else:
        list_params = []

    index = param_format.find("{}")
    while index >= 0:
        # print(param_format)
        # 目前每个参数只能是null或者是字符串，字符串都使用双引号
        if len(list_params) > 0:
            item = list_params[0]
            list_params.remove(item)
            item = '"{}"'.format(item)
        else:
            item = "null"
        param_format = param_format[:index + 2].replace("{}", item) + param_format[index+2:]
        index = param_format.find("{}")

    json_params = json.loads(param_format)
    if json_params is None:
        return {}
    return json_params

def response(string):
    return ""
