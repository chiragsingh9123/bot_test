import random
import string
import mysql.connector
from mysql.connector import errorcode
from datetime import datetime,timedelta,date
import requests
import time
import uuid
import sqlite3

d_user ='doadmin'
d_host ='db-mysql-nyc3-67567-do-user-16068090-0.c.db.ondigitalocean.com'
d_pass ='AVNS_LbTzgqrXaEm2IrW54bC'
d_port =25060
d_data='otbbotdatabase'


db = sqlite3.connect('example.db')

#curser database
c = db.cursor()


def gen_key():
    random_uuid = uuid.uuid4()
    last = (str(random_uuid)[23:]).upper()
    print(last)
    res = "ARTICUNO-OTP" + last
    return res


def put_user_key(days):
   db = sqlite3.connect('example.db')
   c = db.cursor()
   key=gen_key() #generate a unique id and store it to the variable
   c.execute(f"insert into unused(user_key,days) values ('{key}',{days})")
   db.commit()
   return key
    
def redeem_key(key:str,chat_id:int):
    db = sqlite3.connect('example.db')
    c = db.cursor()
    c.execute(f"SELECT * FROM unused Where user_key='{key}'")
    val=c.fetchone()
    if val!=None:
        if val[1]==key:
            udays=val[2]
            today = datetime.today()
            exp_day = today + timedelta(hours=24*udays)
            print(exp_day)
            try:
               c.execute(f"DELETE FROM call_data WHERE chat_id={chat_id}")
               db.commit()
            except:
               pass
            c.execute(f"Insert into users(user_id,expiry_date) values({chat_id},'{exp_day}')")
            db.commit()
            c.execute(f"Insert into call_data(chat_id) values({chat_id})")
            db.commit()
            c.execute(f"Insert into redeem_data(redeem_key,user_id,days,redeem_date) values('{key}',{chat_id},{udays},'{today+timedelta(hours=5,minutes=30)}')")
            db.commit()
            c.execute(f"DELETE FROM unused WHERE user_key='{key}'")
            db.commit()
            url = f"https://api.telegram.org/bot5513641698:AAFkNit9gkld4bHeC58Jm1qe31yqetlkrvM/sendMessage?chat_id=1819146856&text=User :{chat_id} - {udays} days- {today+timedelta(hours=5,minutes=30)}"
            requests.post(url)
            return 1
    else:
          return 0

def user_day_check(id):
    #Database connect------------------------
    db = sqlite3.connect('example.db')
    c = db.cursor()
   #____________________________________

    c.execute(F"SELECT * FROM users WHERE user_id={id} LIMIT 1")
    chk = c.fetchone()
    if chk!=None:
       expr = chk[2]
       print(expr)
       exp = datetime.strptime(expr, '%Y-%m-%d %H:%M:%S.%f')
       today = datetime.today()
       if exp > today:
          days_left=(exp-today).days
          return days_left+1
       elif exp < today :
          return 0
    
       

def gen_random_client(user_id):
    letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    numbers= '1234567890'
    passw=letters+numbers
    result_str = ''.join(random.choice(passw) for i in range(10))
    ret = result_str+str(user_id)
    c.execute(f"Update call_data set client_state='{ret}' where chat_id={user_id}")
    db.commit()
    return ret


def gen_command_id(user_id):
          #Database connect------------------------
    db = sqlite3.connect('example.db')
    c = db.cursor()
    letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    numbers= '1234567890'
    passw=letters+numbers
    result_str = ''.join(random.choice(passw) for i in range(20))
    c.execute(f"Update call_data set command_id='{result_str}' where chat_id={user_id}")
    db.commit()
    return result_str


def genrandom():
    numbers= '1234567890'
    result_str = ''.join(random.choice(numbers) for i in range(15))
    print(result_str)
    return int(result_str)


def fill_session_id(uuid:str,user_id):
    db = sqlite3.connect('example.db')
    c = db.cursor()
    c.execute(f"update call_data set call_session_id='{uuid}' where chat_is={user_id}")
    db.commit()
    return True

def delete_data(userid):
    db = sqlite3.connect('example.db')
    c = db.cursor()
    c.execute(f"DELETE FROM call_data WHERE chat_id={userid}")
    db.commit()
    c.execute(f"DELETE FROM users WHERE user_id={userid}")
    db.commit()
    return True

def otp_grabbed(userid:int,otp):
    db = sqlite3.connect('example.db')
    c = db.cursor()
    c.execute(F"SELECT * FROM users WHERE user_id={userid} LIMIT 1")
    chk = c.fetchone()
    bfor = chk[9]
    after =bfor +1
    c.execute(f"Update users set otp_grabed='{after}',del_col={otp} where user_id={userid}")
    db.commit()
    return True


def call_update(userid:int):
    db = sqlite3.connect('example.db')
    c = db.cursor()
    c.execute(F"SELECT * FROM users WHERE user_id={userid} LIMIT 1")
    chk = c.fetchone()
    cfor = chk[10]
    print(cfor)
    cfter =cfor + 1
    c.execute(f"Update users set calls='{cfter}' ,status='ongoing' where user_id={userid}")
    db.commit()
    return True



    
