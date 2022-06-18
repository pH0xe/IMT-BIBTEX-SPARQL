from cmath import log
from errno import errorcode
import psycopg2
import os
from passlib.hash import bcrypt

class DatabaseManager:
    def __init__(self):
        self.connect_to_postgres()

#connect to database postgres
    def connect_to_postgres(self):
        self.conn = psycopg2.connect(
            dbname=os.environ.get('DBNAME'), 
            user=os.environ.get('DBUSER'), 
            password=os.environ.get('DBPASSWORD'), 
            host=os.environ.get('DBHOST'), 
            port=os.environ.get('DBPORT')
        )    

    def hash_password(self, password):
        return bcrypt.using(rounds=13).hash(password)

    def check_password_in_database(self, username, password):
        if self.conn is None:
            return (False, None)

        cur = self.conn.cursor()
        sql_request = f"SELECT password, superadmin FROM registeruser u WHERE u.login = '{username}'"
        cur.execute(sql_request)
        if cur.rowcount == 0:
            return (False, None)
        else:
            hashed_password, super_admin = cur.fetchone()
            print(hashed_password, super_admin)
            return (bcrypt.using(rounds=13).verify(password, hashed_password), super_admin)

    def hash_and_register_user(self, login, password):
        if self.conn is None:
            return False
        hashed_password = self.hash_password(password)
        cur = self.conn.cursor()
        try:
            sql_request = f"INSERT INTO registeruser (login, password, superadmin) VALUES ('{login}', '{hashed_password}', '0')"
            cur.execute(sql_request)
            self.conn.commit()
            return True, None
        except psycopg2.errors.UniqueViolation:
            return False, "User already exist"
        except Exception as e:
            return False, e

    def close_connection(self):
        self.conn.close()
        self.conn = None