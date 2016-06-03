import db
import encryption
import getpass
import pinyin

def run():
    db.init()
    instr = input('Search input(q/Q for quit):')
    while instr.upper() != 'Q':
        getwebsite(instr)
        instr = input('Search input(q/Q for quit):')
        
    db.close()

def getwebsite(instr):
    if instr.upper() == 'NEWPWD':
        newpwd()
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
        num = input('press number for show:')
        if num.isnumeric():
            names = db.getnamelist(list[int(num)][0])
        else:
            return
    select(names)

def select(list):
    if len(list) ==0:
        return
    encryption.show(list[0][0], list[0][1])
    if len(list) ==1:
        return
    if len(list) == 2:
        encryption.show(list[1][0], list[1][1])
        return
    for i in range(1, len(list)):
        print(str(i) + ' :' + list[i][0])
    num = input('press number for show:')
    if num.isnumeric():
        encryption.show(list[int(num)][0], list[int(num)][1])
    
def newpwd():
    webname = input('Input website name?');
    if webname.upper() == 'Q':
        return
    websiteid, isnew = db.addwebsite(webname)
    if not isnew:
        instr = input('show ' + webname + '? a/A for continue add:')
        if instr.upper() != 'A':
            getwebsite(webname)
    for i in range(0,100):
        if i == 0:
            defstr = 'username'
        else:
            defstr = 'pwd' + str(i)
        key = input("The " + str(i) + ' Info name :' + defstr + '?')
        if key == '':
            key = defstr
        if key.upper() == 'Q':
            return
        if i == 0:
            val = input('Input the value: \r\n')
        else:
            val = getpass.getpass('Input the value: \r\n')
        db.addnamepwd(websiteid, key, val)
        


if __name__ == '__main__':
    run()