# coding = UTF8

from core.common import interface_function

@interface_function
def hi(name1=None, name2=None):
    if name1 is None and name2 is None:
        return "hi, anonymous"

    names = []
    if name1 is not None:
        names.append(name1)
    if name2 is not None:
        names.append(name2)
    return "hi, {}".format(", ".join(names))
    # if type(name1) == str:
    #     return "hi, {}".format(name)
    # elif type(name) == list:
    #     return "hi, {}".format(", ".join(name))
    # else:
    #     raise ValueError(name, "parameter should be str or list")
