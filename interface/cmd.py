# coding = UTF8

from core.invoke_services import run_command

def main():
    while True:
        cmd = input(">>> ").strip()
        if cmd == "":
            continue
        resp = run_command(cmd)
        print(resp)
