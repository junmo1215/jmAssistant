# coding = UTF8

"""
this file is all same with config.py but without value
when run with it, should fist rename this file to config.py and set config value
"""

class WechatBotConfig:
    # 微信公众号页面的token，用来验证请求是否的确来自腾讯服务器
    token = ""
    # 搭载腾讯公众号自动响应机器人的机器ip，不带端口号
    host = ""

# 接受指令的接口模式
# 目前支持
# cmd：使用本地控制台进行交互
# wechat：微信公众号，需要有微信公众号并且配置运行服务器信息WechatBotConfig
interface_mode = "cmd"

# 是否是调试模式
# 调试模式下不验证消息来源
is_debug_mode = False
