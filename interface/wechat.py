# coding = UTF8

from flask import Flask,request
from time import time
import xml.etree.ElementTree as et
import hashlib

from config import WechatBotConfig

app = Flask(__name__)
# app.debug = True

response_text_format = "<xml><ToUserName><![CDATA[%s]]></ToUserName><FromUserName><![CDATA[%s]]></FromUserName><CreateTime>%s</CreateTime><MsgType><![CDATA[text]]></MsgType><Content><![CDATA[%s]]></Content></xml>"

@app.route('/wechat_bot',methods=['GET','POST'])
def wechat():
    if request.method == 'GET':
        token = WechatBotConfig.token
        data = request.args
        signature = data.get('signature','')
        timestamp = data.get('timestamp','')
        nonce = data.get('nonce','')
        echostr = data.get('echostr','')

        list = [token, timestamp, nonce]
        list.sort()

        s = list[0] + list[1] + list[2]

        hascode = hashlib.sha1(s.encode('utf-8')).hexdigest()

        if hascode == signature:
            return echostr
        else:
            return ""

    if request.method == 'POST':
        xmldata = request.data
        # print(xmldata)
        xml_rec = et.fromstring(xmldata)

        ToUserName = xml_rec.find('ToUserName').text
        fromUser = xml_rec.find('FromUserName').text
        MsgType = xml_rec.find('MsgType').text
        Content = xml_rec.find('Content').text
        MsgId = xml_rec.find('MsgId').text

        return response_text_format.format(fromUser, ToUserName, int(time()), Content)


def main():
    app.run(host=WechatBotConfig.host, port=80)
