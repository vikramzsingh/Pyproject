# Database connectivity for all function

import pymysql


def connect_to_database():
    conn=pymysql.connect(host="localhost", port=3306, user="root", passwd="", db="pyproject", autocommit=True)
    cur=conn.cursor()
    return cur

def check_photo(userid):
    conn=pymysql.connect(host="localhost", port=3306, user="root", passwd="", db="pyproject", autocommit=True) #connection
    cur=conn.cursor() # create cursor
    sql="select * from photodata where userid='"+userid+"'" #valid sql stmt
    cur.execute(sql) #execute stmt
    n=cur.rowcount
    photo="no"
    if(n==1):
        row=cur.fetchone()
        photo=row[1]
    return photo
