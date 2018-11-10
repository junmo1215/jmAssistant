# coding = UTF8

import os
import imp
import json
# import inspect

from pony.orm import commit, db_session, select
from entity.coreEntity import Service, User, KeyWord
import globalVariable
from core.common import read_json_data

def get_all_func():
    """
    获取所有服务的名称和参数等信息，存入数据库中
    service中的功能不能以双下划线__开头，并且文件需要放在service文件夹中
    """
    result = []
    for file_name in os.listdir("service"):
        if file_name.startswith("__") or file_name.endswith(".py") is False:
            continue

        # 去掉.py的后缀，数据库中直接使用去掉后缀的文件名当做service名称
        file_name = file_name[:-3]
        service = imp.load_source(file_name, 'service/{}.py'.format(file_name))
        for function_name in dir(service):
            if function_name.startswith("__"):
                continue
            
            func = eval("service.{}".format(function_name))
            
            # if not inspect.isfunction(func):
            #     continue

            # 由于在文件中会import一些函数进来，比较难区分是接口函数还是第三方库中引入的，因此给接口函数打上了interface_function标签。目前通过有没有这个标签来判断
            try:
                if func.is_interface_function:
                    print(function_name, func.key_words)
            except:
                # print(function_name, False)
                continue

            # 执行每个服务的install函数
            if function_name == "install":
                func(with_data=True)

            # 解析接口函数的参数信息
            param = {}
            param_names = func.co_varnames
            for i in range(func.co_argcount):
                param[param_names[i]] = {}
            str_params = str(param).replace("'", '"')
            # print(file_name, function_name, str_params)
            result.append((file_name, function_name, str_params, func.key_words))

    return result

@db_session
def add_user_and_rights():
    core = read_json_data("core.json")
    service_user = core.get("Service_User", {})
    # with db_session:
    for user in core.get("User", []):
        user_entity = User.get(**user)
        if user_entity is None:
            user_entity = User(**user)

        if user_entity.name not in service_user:
            continue
        
        for service in service_user[user_entity.name]:
            service_entity = Service.get(**service)
            if service_entity in user_entity.services:
                continue

            user_entity.services.add(service_entity)

def main():
    # 将接口函数信息加入到数据库中
    services = get_all_func()
    # # print(services)
    with db_session:
        for service_name, function_name, params, key_words in services:
            # 如果存在就不插入
            service = Service.get(service_name=service_name, function_name=function_name)

            if service is None:
                service = Service(
                    service_name = service_name,
                    function_name = function_name,
                    params = params
                )

            # 增加每个服务接口对应的关键字
            for key_word in key_words:
                if KeyWord.get(key_word=key_word) is not None:
                    continue

                KeyWord(
                    key_word = key_word,
                    service = service
                )

    # 将用户信息加入数据库中
    # 包含用户和相关的权限
    add_user_and_rights()

    # commit()

if __name__ == "__main__":
    main()
