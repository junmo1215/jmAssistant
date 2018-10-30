# coding = UTF8

from flask import Flask

from interface import cmd, wechat
import config
from core.common import get_function

INTERFACE = config.interface_mode

def start_web_site():
    website = Flask(__name__)
    website.debug = config.is_debug_mode

    # for i in []:
    wechat = get_function("./interface/wechat.py", "wechat")
    # wechat = eval("from interface.wechat import wechat as w")
    website.add_url_rule('/wechat_bot', '/wechat_bot', wechat, methods=['GET','POST'])

    website.run(
        host=config.WechatBotConfig.host,
        port=config.WechatBotConfig.port
    )

def main():
    start_web_site()
    if INTERFACE == 'cmd':
        cmd.main()
    elif INTERFACE == 'wechat':
        wechat.main()

if __name__ == "__main__":
    main()
