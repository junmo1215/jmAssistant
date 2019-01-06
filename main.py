# coding = UTF8

from interface import cmd, web
import config

INTERFACE = config.interface_mode

def main():
    web.main()
    if INTERFACE == 'cmd':
        cmd.main()

if __name__ == "__main__":
    main()
