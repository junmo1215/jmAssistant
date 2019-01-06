# coding = UTF8

from flask import Flask,request
from time import time
import xml.etree.ElementTree as et
import hashlib

import globalVariable
# from globalVariable import website
from config import WechatBotConfig, is_debug_mode
from core.invoke_services import run_command
from entity.coreEntity import User
from pony.orm import db_session

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

# @website.route('/wechat_bot',methods=['GET','POST'])
def wechat():
    # get和post请求都要验证请求来源，debug模式除外
    if is_debug_mode == False and wechat_authority(request) == False:
        return ""

    if request.method == 'GET':
        echostr = request.args.get('echostr','')
        return echostr

    if request.method == 'POST':
        xmldata = request.data
        # print("")
        # print(xmldata)
        xml_rec = et.fromstring(xmldata)

        to_user_name = xml_rec.find('ToUserName').text
        from_user_name = xml_rec.find('FromUserName').text
        msg_type = xml_rec.find('MsgType').text
        content = xml_rec.find('Content').text

        with db_session:
            from_user = User.get(wechat_open_id=from_user_name)
        if from_user is None:
            resp = "you are unregistered, contact admin to register"
        else:
            globalVariable.gContext["from_user"] = from_user.name
            resp = run_command(content)
        # MsgId = xml_rec.find('MsgId').text

        return response_text_format.format(from_user_name, to_user_name, int(time()), resp)
