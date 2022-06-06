import logging
import time
import psycopg2
import os
from psycopg2 import OperationalError
from psycopg2.extras import RealDictCursor
from werkzeug.utils import secure_filename


class DataBaseManager:
    def __init__(self):
        self.db = None
        self.cursor = None
    
    def connect_to_postgres(self) -> bool:
        try:
            self.db = psycopg2.connect(
                host=os.environ.get('POSTGRESQL_HOST'), 
                port=os.environ.get('POSTGRESQL_PORT'),
                dbname=os.environ.get('POSTGRESQL_DB'), 
                user=os.environ.get('POSTGRESQL_USERNAME'), 
                password=os.environ.get('POSTGRESQL_PASSWORD')
            )
            self.cursor = self.db.cursor(cursor_factory=RealDictCursor)
            return True
        except OperationalError as e:
            print("Operational error: " + str(e))
            return False
        except Exception as e:
            print("error a ala connexion")
            return False

    def select_all_file(self) -> list[tuple]:
        self.cursor.execute("SELECT id, uploaddate, name FROM bibfile order by uploaddate desc")
        return self.cursor.fetchall()

    def upload_file(self, file) -> tuple[bool, bytes]:
        try:
            upload_date = int(time.time())
            filename = secure_filename(file.filename)
            contenttype = file.mimetype
            data = file.read()
            size = len(data)
            self.cursor.execute("INSERT INTO bibfile (uploaddate, name, size, contenttype, data) VALUES (%s, %s, %s, %s, %s)", (upload_date, filename, size, contenttype,  data))
            self.db.commit()
            return True, data
        except Exception as e:
            logging.ERROR(e)
            return False, None

    def get_data_by_id(self, id) -> bytes | None:
        self.cursor.execute("select data from bibfile where id = {0}".format(id))
        result_set = self.cursor.fetchone()
        if result_set is not None:
            data = result_set['data']
            if data is not None:
                return bytes(data)
        return None