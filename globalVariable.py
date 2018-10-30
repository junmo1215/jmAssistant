# coding = UTF8

import os

inited = False

def init():
    global gContext, root_path
    gContext = {}
    root_path = os.path.dirname(os.path.realpath(__file__))

#     init_web_site()

# def init_web_site():
#     global website
#     website = Flask(__name__)
#     website.debug = is_debug_mode

#     # for i in []:
#     wechat = get_function("./interface/wechat.py", "wechat")
#     # wechat = eval("from interface.wechat import wechat as w")
#     website.add_url_rule('/wechat_bot', '/wechat_bot', wechat, methods=['GET','POST'])

#     website.run()
#     # website.run(host=WechatBotConfig.host, port=80)

if inited == False:
    init()
    inited = True
