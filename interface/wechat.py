# coding = UTF8

from flask import Flask,request
from time import time
import xml.etree.ElementTree as et
import hashlib

import globalVariable
from config import WechatBotConfig, is_debug_mode
from core.invoke_services import run_command

app = Flask(__name__)
app.debug = is_debug_mode

response_text_format = "<xml><ToUserName><![CDATA[{}]]></ToUserName><FromUserName><![CDATA[{}]]></FromUserName><CreateTime>{}</CreateTime><MsgType><![CDATA[text]]></MsgType><Content><![CDATA[{}]]></Content></xml>"

def wechat_authority(request):
    """
    验证请求是否是微信发出的
    """
    token = WechatBotConfig.token
    data = request.args
    signature = data.get('signature', '')
    timestamp = data.get('timestamp', '')
    nonce = data.get('nonce', '')
    list = [token, timestamp, nonce]
    list.sort()
    s = list[0] + list[1] + list[2]
    hascode = hashlib.sha1(s.encode('utf-8')).hexdigest()
    return hascode == signature

@app.route('/wechat_bot',methods=['GET','POST'])
def wechat():
    globalVariable.init()
    # get和post请求都要验证请求来源，debug模式除外
    if app.debug == False and wechat_authority(request) == False:
        return ""

    if request.method == 'GET':
        echostr = request.args.get('echostr','')
        return echostr

    if request.method == 'POST':
        xmldata = request.data
        # print("")
        # print(xmldata)
        xml_rec = et.fromstring(xmldata)

        ToUserName = xml_rec.find('ToUserName').text
        fromUser = xml_rec.find('FromUserName').text
        MsgType = xml_rec.find('MsgType').text
        Content = xml_rec.find('Content').text
        globalVariable.gContext["from_user"] = fromUser
        resp = run_command(Content)
        # MsgId = xml_rec.find('MsgId').text

        return response_text_format.format(fromUser, ToUserName, int(time()), resp)

def main():
    app.run(host=WechatBotConfig.host, port=80)
