import db
import encryption
import getpass
import pinyin
import pyperclip
import os
import password

def welcome():
    f = open('welcome.txt', 'r')
    print('\r'.join(f.readlines()))
    return

def run():
    if db.init() :
        welcome()
        encryption.createkeys()
    encryption.getpubkey()
    encryption.getcode()
    instr = input('请输入关键字进行搜索(q/Q退出；newpwd添加新的密码项):')
    while instr.upper() != 'Q':
        getwebsite(instr)
        instr = input('请输入关键字进行搜索：')
        
    db.close()

def getwebsite(instr):
    if instr.upper() == 'NEWPWD':
        newpwd()
        return
    if instr.upper() == 'RANDOMPWD':
        print(password.getpwd())
        return
    if instr == '':
        return
    list = db.search(instr)
    if len(list) == 0:
        return
    elif len(list) == 1:
        names = db.getnamelist(list[0][0])
    else:
        for i in range(0, len(list)):
            print(str(i) + ' :' + list[i][1])
        num = input('请输入项目前的序号查看:')
        if num.isnumeric():
            names = db.getnamelist(list[int(num)][0])
        else:
            return
    select(names)

def select(list):
    if len(list) ==0:
        return
    print(list[0][0] + ":" + encryption.show(list[0][0], list[0][1]))
    if len(list) ==1:
        return
    if len(list) == 2:
        pwd = encryption.show(list[1][0], list[1][1])
        pyperclip.copy(pwd)
        print(list[1][0] + "成功复制到粘贴板。")
        return
    for i in range(1, len(list)):
        print(str(i) + ' :' + list[i][0])
    num = input('请输入项目前的序号查看:')
    if num.isnumeric():
        pwd = encryption.show(list[int(num)][0], list[int(num)][1])
        pyperclip.copy(pwd)
        print(list[int(num)][0] + "成功复制到粘贴板。")
    
def newpwd():
    webname = input('请输入网站或应用程序名字：');
    if webname.upper() == 'Q':
        return
    websiteid, isnew = db.addwebsite(webname)
    if not isnew:
        instr = input('此名字已经存在，回车键查看（输入a/A向此网站添加密码项:')
        if instr.upper() != 'A':
            getwebsite(webname)
    for i in range(0,100):
        if i == 0:
            defstr = '用户名'
        else:
            defstr = '密码' + str(i)
        key = input("要录入“" + defstr + "”吗？回车键确认，输入其他修改名称：")
        if key == '':
            key = defstr
        if key.upper() == 'Q':
            return
        if i == 0:
            val = input('请输入' + defstr + ': \r\n')
        else:
            val = getpass.getpass('请输入' + defstr + ': \r\n')
        db.addnamepwd(websiteid, key, val)
        


if __name__ == '__main__':
    run()