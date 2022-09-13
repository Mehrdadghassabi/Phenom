import sqlite3
import sys

def insert(i,m,lang):
    try:
        c.execute(f'insert into NOTES ([index],[message]) values ({i},"{m}")')
        conn.commit()
        if(lang=='en'):
            print('Operation done successfully')
        else:
            print("عملیات با موفقیت انجام شد")
    except:
        if(lang=='en'):
            print("There is a note with this index")
        else:
            print("یک یادداشت با این شاخص وجود دارد")

def find(i,lang):
    row=c.execute(f'select [index], [message] from NOTES where [index]={i}')
    i=0
    for r in row:
        i+=1
        print(r[1])
    if(i==0):
        if(lang=='en'):
            print('There is no note with this index')
        else:
            print("هیچ یادداشتی با این شاخص وجود ندارد")

def findall(lang):
    row = c.execute(f'select [index], [message] from NOTES')
    i = 0
    for r in row:
        i += 1
        print("-"+r[1])
    if (i == 0):
        if(lang=='en'):
            print('There is no note')
        else:
            print("هیچ یادداشتی وجود ندارد")

def delete(i,lang):
    c.execute(f'delete from NOTES where [index]={i}')
    conn.commit()
    if(lang=='en'):
        print('Operation done successfully')
    else:
        print("عملیات با موفقیت انجام شد")

conn=sqlite3.connect('notes.db')
c=conn.cursor()
arg=sys.argv[1]
if(arg=="insert"):
    insert(int(sys.argv[2]),str(sys.argv[3]),str(sys.argv[4]))
elif(arg=="find"):
    find(int(sys.argv[2]),str(sys.argv[3]))
elif(arg=="delete"):
    delete(int(sys.argv[2]),str(sys.argv[3]))
elif(arg=="findall"):
    findall(str(sys.argv[1]))
conn.close()
