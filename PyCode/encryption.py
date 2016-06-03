import rsa
import os
import pyperclip

PubFilename = ".\pub.pem"
PrivFilename = ".\priv.pem"

def show(str1, str2):
    privkey = getprivkey()
    pwd = rsa.decrypt(str2, privkey).decode()
    pyperclip.copy(pwd)
    print(str1 + "成功复制到粘贴板。")

def hide(str1, str2):
    pubkey = getpubkey()
    return rsa.encrypt(str2.encode(encoding='utf-8'), pubkey)


def getpubkey():
    if not os.path.isfile(PubFilename):
        createkeys()
    with open(PubFilename) as publickfile:
        p = publickfile.read()
        pubkey = rsa.PublicKey.load_pkcs1(p)
    return pubkey

def getprivkey():
    if not os.path.isfile(PrivFilename):
        createkeys()
    with open(PrivFilename) as privfile:
        p = privfile.read()
        privkey = rsa.PrivateKey.load_pkcs1(p)
    return privkey

def createkeys():
    (pubkey, privkey) = rsa.newkeys(1024)
    pub = pubkey.save_pkcs1().decode()
    pubfile = open(PubFilename, "w+")
    pubfile.writelines(pub)
    pubfile.close()
    
    priv = privkey.save_pkcs1().decode()
    privfile = open(PrivFilename, "w+")
    privfile.writelines(priv)
    privfile.close()
    
    