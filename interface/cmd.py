# coding = UTF8

from core.invoke_services import run_command

import globalVariable

def main():
    while True:
        cmd = input(">>> ").strip()
        globalVariable.init()
        globalVariable.gContext["from_user"] = "junmo"
        if cmd == "":
            continue
        resp = run_command(cmd)
        print(resp)
