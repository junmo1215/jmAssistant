# coding = UTF8

import os
import imp
import json
import sqlite3

DB_NAME = "db/core.db"

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
            if not callable(func):
                continue

            param = {}
            param_names = func.__code__.co_varnames
            for i in range(func.__code__.co_argcount):
                param[param_names[i]] = {}
            str_params = str(param).replace("'", '"')
            # print(file_name, function_name, str_params)
            result.append((file_name, function_name, str_params))
    
    return result

def main():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    check_table_sql = "SELECT name FROM sqlite_master WHERE type = 'table' AND name = 'services';"

    create_db_sql = """
    CREATE TABLE `services` (
        `service_name`	TEXT NOT NULL,
        `function_name`	TEXT NOT NULL,
        `params`	TEXT NOT NULL
    );
    """

    insert_sql = """
    INSERT INTO `services`(`service_name`, `function_name`, `params`)
    VALUES(?, ?, ?);
    """

    cur.execute(check_table_sql)
    if not cur.fetchall():
        cur.executescript(create_db_sql)
    cur.executemany(insert_sql, get_all_func())
    conn.commit()
    conn.close()

if __name__ == "__main__":
    main()