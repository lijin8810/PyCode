import random

def getpwd():
    s = input("请输入想要的密码结构，A表示大小写字母，0代表数字，?代表符号，如‘aa000000’等：")
    return getpwd1(s)

def getpwd1(fstr):
    pwd = ''
    init()
    for a in fstr:
        if a.upper() == 'A':
            pwd = pwd + geta()
        if a == '0':
            pwd = pwd + get0()
        if a == '?' or a == '？':
            pwd = pwd + getothers()
    return pwd

def geta():
    return random.sample('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz', 1)[0]

def get0():
    return random.sample('1234567890', 1)[0]

def getothers():
    return random.sample("~!@#$%^&*()_+=-`{}|:<>?/.,;'[]\\\'", 1)[0]

def init():
    s = input("请随意的敲击键盘，产生随机的字符做为种子发生器：")
    random.seed(s)

