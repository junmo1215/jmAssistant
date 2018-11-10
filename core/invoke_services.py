# coding = UTF8

import imp
import json
import traceback
from pony.orm import db_session, select

import globalVariable
from entity.coreEntity import Service, User, KeyWord

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
        traceback.print_exc()
        return "[error]" + str(e)

def parse_parameters(service_name, function_name, params):
    """
    将字符串形式的params转变成json格式，最后的结果可以直接通过func(**params)的形式调用指定的功能
    params可以是None代表所有参数都是默认值
    如果有多个参数使用PARAMS_SPLIT_PATTERN分隔不同的参数

    目前的做法是按照顺序依次往后面的参数中填充
    params按照空格区分，所以单个params里面不能有空格
    """
    assert params is None or type(params) == str

    with db_session:
        # service = select(s for s in Service if s.service_name == service_name and s.function_name == function_name)[:]
        # assert len(service) == 1
        # service = service[0]

        service = Service.get(service_name=service_name, function_name=function_name)
        assert service is not None

        # 读取指定功能需要填充的参数
        param_format = service.params

    # 将传进来的参数转换成list
    if params is not None and params != "":
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
            if item == "":
                continue
            item = '"{}"'.format(item)
        else:
            item = "null"
        param_format = param_format[:index + 2].replace("{}", item) + param_format[index+2:]
        index = param_format.find("{}")

    # print(param_format)
    json_params = json.loads(param_format)
    if json_params is None:
        return {}
    return json_params

# 验证用户是否有某个功能的权限
@db_session
def authority_user_right(service_name, function_name, user_name=None):
    if user_name is None:
        user_name = globalVariable.gContext["from_user"]

    user = User.get(name=user_name)
    if user is None:
        return False

    service = Service.get(service_name=service_name, function_name=function_name)
    # return (service is not None) and (service in user.services)
    return service in user.services

def run_command(command):
    """
    这个函数保证没有跑出异常，在调用服务过程中的异常会转变为字符串返回
    """
    service_name = ""
    function_name = ""
    params = ""

    with db_session:
        for key_word in list(KeyWord.select()):
            # print(key_word)
            if command.find(key_word.key_word) >= 0:
                # service_name, function_name = function.split(" ")[:2]
                service_name = key_word.service.service_name
                function_name = key_word.service.function_name
                params = command[len(key_word.key_word):].strip()
                break

    if service_name == "" or function_name == "":
        return "permission delay"

    if authority_user_right(service_name, function_name) == False:
        return "permission delay"

    # print(service_name, function_name, params)
    return invoke(service_name, function_name, params)
