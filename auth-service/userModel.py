import sys
from typing import Tuple
import psycopg2
import os
from passlib.hash import bcrypt

#connect to database postgres
def connectToPostgres():
    try:
        conn = psycopg2.connect(
            dbname=os.environ.get('DBNAME'), 
            user=os.environ.get('DBUSER'), 
            password=os.environ.get('DBPASSWORD'), 
            host=os.environ.get('DBHOST'), 
            port=os.environ.get('DBPORT')
        )
        return conn
    except:
        return None

def hashPassword(password):
    return bcrypt.using(rounds=13).hash(password)

def checkPasswordInDatabase(username, password):
    conn = connectToPostgres()
    if conn is None:
        return (False, None)

    cur = conn.cursor()
    cur.execute("SELECT password, superadmin FROM \"user\" WHERE login = %s", [username])
    if cur.rowcount == 0:
        return (False, None)
    else:
        hashedPassword = cur.fetchone()[0]
        hashedPassword = hashedPassword.strip()
        return (bcrypt.using(rounds=13).verify(password, hashedPassword), cur.fetchone()[1])

def hashAndRegisterUser(login, password):
    conn = connectToPostgres()
    if conn is None:
        return False
    hashedPassword = hashPassword(password)
    cur = conn.cursor()
    try:
        cur.execute("INSERT INTO \"user\" (login, password, superadmin) VALUES (%s, %s, false)", (login, hashedPassword))
        conn.commit()
        return True
    except:
        print(sys.exc_info()[0])
        return False