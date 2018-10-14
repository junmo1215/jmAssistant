# coding = UTF8

from interface import cmd, wechat

INTERFACE = "cmd"

def main():
    if INTERFACE == 'cmd':
        cmd.main()
    elif INTERFACE == 'wechat':
        wechat.main()

if __name__ == "__main__":
    main()
