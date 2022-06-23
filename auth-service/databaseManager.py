from cmath import log
from errno import errorcode
import psycopg2
import os
from passlib.hash import bcrypt


def init_db():
    """
    Initialize the database at first launch
    """
    dm = DatabaseManager()
    if dm.user_exist("admin"):
        print("Admin user already exists")
        return
    print("Creating admin user")
    dm.insert_admin()

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

    def change_password_in_db(self, username, current_password, new_password):
        if self.conn is None:
            return False, "Connection to database failed"
        
        if not  self.user_exist(username):
            return False, "User doesn't exist"
        
        if not self.check_password_in_database(username, current_password):
            return False, "Wrong current password"
        
        hashed_password = self.hash_password(new_password)
        cur = self.conn.cursor()
        try:
            sql_request = f"UPDATE registeruser SET password = '{hashed_password}' WHERE login = '{username}'"
            cur.execute(sql_request)
            self.conn.commit()
            return True, 'Password changed'
        except Exception as e:
            return False, str(e)
        
    def user_exist(self, login):
        if self.conn is None:
            return False

        cur = self.conn.cursor()
        sql_request = f"SELECT password FROM registeruser u WHERE u.login = '{login}'"
        cur.execute(sql_request)
        if cur.rowcount == 0:
            return False
        return True
    
    def is_super_admin(self, id):
        if self.conn is None:
            return False

        cur = self.conn.cursor()
        sql_request = f"SELECT superadmin FROM registeruser u WHERE u.id = '{id}'"
        cur.execute(sql_request)
        if cur.rowcount == 0:
            return False
        return cur.fetchone()[0] == 1

    def insert_admin(self):
        hashed_password = self.hash_password(os.environ.get('ADMIN_PASSWORD'))
        req = f"insert into registeruser (login, password, superadmin) values ('admin', '{hashed_password}', '1')"
        cur = self.conn.cursor()
        cur.execute(req)
        self.conn.commit()
    
    def remove_user(self, id):
        if self.conn is None:
            return False
        cur = self.conn.cursor()
        sql_request = f"DELETE FROM registeruser WHERE id = '{id}'"
        cur.execute(sql_request)
        self.conn.commit()
        return True

    def close_connection(self):
        self.conn.close()
        self.conn = None