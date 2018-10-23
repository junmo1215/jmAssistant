# coding = UTF8

from core.invoke_services import run_command

import globalVariable
import config
from entity.coreEntity import User
from pony.orm import db_session

def main():
    while True:
        cmd = input(">>> ").strip()
        globalVariable.gContext["from_user"] = config.admin
        if cmd == "":
            continue
        resp = run_command(cmd)
        print(resp)
