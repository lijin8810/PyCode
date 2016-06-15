import rsa
import os
import pyperclip
import getpass
import db

PubFilename = ".\pub.pem"
PrivFilename = ".\priv.pem"
CodeList = []

def show(str1, str2):
    privkey = getprivkey()
    pwd = rsa.decrypt(str2, privkey).decode()
    return pwd

def hide(str1, str2):
    pubkey = getpubkey()
    return rsa.encrypt(str2.encode(encoding='utf-8'), pubkey)


def getpubkey():
    pub = db.getRSAPub()
    if pub == '':
        createkeys()
        return rsa.PublicKey.load_pkcs1(db.getRSAPub())
    else:
        return rsa.PublicKey.load_pkcs1(pub)

def getprivkey():
    priv = db.getRSAPriv()
    if priv == '':
        createkeys()
        priv = db.getRSAPriv()
    getcode()
    i = 1
    for index in CodeList:
        priv = priv[0:index] + chr(ord((priv[index])) - i) + priv[index + 1 :]
        i = i + 1
    print(priv)
    try:
        return rsa.PrivateKey.load_pkcs1(priv)
    except:
        return None

def getcode():
    if len(CodeList) <= 0:
        code = getpass.getpass("请输入此程序的运行密码：\r\n")
        for c in code:
            index = ord(c)
            CodeList.append(index)
    return CodeList

def createkeys():
    (pubkey, privkey) = rsa.newkeys(1024)
    pub = pubkey.save_pkcs1().decode()
    priv = privkey.save_pkcs1().decode()
    code = getpass.getpass("请输入此程序的密码，此密码将保护您的资料不被他人破解，请记住这唯一的密码：\r\n")
    print(priv)
    while len(code) < 6:
        print("密码太短，不足以保护您的隐私。")
        code = getpass.getpass("请输入此程序的密码，此密码将保护您的资料不被他人破解，请记住这唯一的密码：\r\n")
    i = 1
    for c in code:
        priv = priv[0:ord(c)] + chr(ord((priv[ord(c)])) + i) + priv[ord(c) + 1 :]
        i = i + 1
    print(priv)
    
    db.addRSAKey(pub, priv)    
    