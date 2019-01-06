# coding = UTF8

import os
from flask import Flask, request, render_template, url_for, redirect
import globalVariable
import config
from core.common import get_function
from core.invoke_services import run_command

website = Flask(__name__, root_path="web/", static_folder=os.path.join(config.root_path, "web", "static"))
website.debug = config.is_debug_mode

website.register_blueprint(
    get_function("./service/register.py", "register_page"),
    url_prefix='/service'
)

wechat = get_function("./interface/wechat.py", "wechat")
website.add_url_rule('/wechat_bot', '/wechat_bot', wechat, methods=['GET','POST'])

@website.route("/", methods=['GET'])
def index():
    return redirect(config.jump_page)

@website.route('/command/hi',methods=['GET'])
def hi():
    return render_template('index.html')

@website.route('/command/<token>/<str_command>',methods=['GET', 'POST'])
def run_cmd(token, str_command):
    user = get_user(token)
    if user == None:
        return "login first"
    
    globalVariable.gContext["from_user"] = user
    return run_command(str_command)

def get_user(token):
    if token == "password":
        return config.admin
    return None

def main():
    website.run(
        host=config.WechatBotConfig.host,
        port=config.WechatBotConfig.port
    )
