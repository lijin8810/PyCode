import sqlite3
import uuid
import pinyin
import encryption

conn = sqlite3.connect('.\code.db')
cr = conn.cursor()

def getRSAPub():
    cr.execute("select pub from rsa ")
    list = cr.fetchall()
    if len(list) > 0:
        return list[0][0]
    else:
        return ''

def getRSAPriv():
    cr.execute("select priv from rsa ")
    list = cr.fetchall()
    if len(list) > 0:
        return list[0][0]
    else:
        return ''

def addRSAKey(pub, priv):
    uid = uuid.uuid4().hex
    cr.execute("insert into rsa(uuid, pub, priv) values (?,?,?)",(uid, pub, priv,))
    conn.commit()
    return

def addnamepwd(websiteid, name, val):
    cr.execute("select uuid from namepwd where websiteid = ? and name = ? ", (websiteid, name,))
    list = cr.fetchall()
    if len(list) > 0:
        if input('Already exists, update now?').upper() == 'Y':
            cr.execute("update namepwd set val = ? where websiteid = ? and name = ?", (val, websiteid, name,))
            conn.commit()
            return
    uid = uuid.uuid4().hex
    val = encryption.hide(name, val)
    cr.execute("insert into namepwd (uuid, websiteid, name, val, seq) values (?,?,?,?, (select max(seq) + 1 from namepwd where  websiteid = ?))", (uid, websiteid, name, val, websiteid,))
    conn.commit()
    return

def addwebsite(webname):
    cr.execute("select uuid from website where website = ?", (webname,))
    list = cr.fetchall()
    if len(list) > 0:
        return list[0][0], False
    uid = uuid.uuid4().hex
    inputcode = input('inputcode?')
    py = "".join(pinyin.getpy(webname))
    cr.execute("insert into website (uuid, website, py, inputcode) values (?,?,?,?)", (uid, webname, py, inputcode,))
    conn.commit()
    return uid, True

def search(str):
    str = '%' + str + '%'
    cr.execute("select uuid, website from website where inputcode like ? or py like ? or website like ?", (str,str,str,))
    return cr.fetchall()

def getnamelist(websiteid):
    cr.execute("select name, val from namepwd where websiteid = ? order by seq asc", (websiteid,))
    return cr.fetchall()

def init():
    isFirstRun = False
    cr.execute("select name from sqlite_master where name = 'dbver'")
    var = cr.fetchall()
    if var == []:
        isFirstRun = True
        initdb()
    cr.execute("select ver from dbver where dbname = 'code'")
    var = cr.fetchall()
    updatedb(var[0][0])
    return isFirstRun

def initdb():
    sql = ["create table dbver(dbname varchar(32), ver int)",\
        "insert into dbver(dbname, ver) values ('code', 1)"]
    for str in sql:
        cr.execute(str)
    conn.commit()
        
def updatedb(ver):
    f = open(".\DBSQL.sql", 'r')
    sql = f.readlines()
    f.close()
    for i in range(ver - 1, len(sql)):
        cr.execute(sql[i])
    cr.execute("update dbver set ver = ? where dbname = 'code'", (len(sql) + 1,))
    conn.commit()
    return

def close():
    conn.commit()
    cr.close()
    conn.close()