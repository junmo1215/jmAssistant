# coding = UTF8

# 封装接口函数，用这个装饰器和其他的函数区分
def interface_function(func):
    def wrapper(*args, **kw):
        return func(*args, **kw)
    wrapper.is_interface_function = True
    wrapper.co_varnames = func.__code__.co_varnames
    wrapper.co_argcount = func.__code__.co_argcount
    return wrapper
