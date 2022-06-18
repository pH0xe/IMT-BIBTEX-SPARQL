import logging
import time
import psycopg2
import os
from psycopg2 import OperationalError
from psycopg2.extras import RealDictCursor
from werkzeug.utils import secure_filename
from typing import Union

from HttpMessage import OPERATIONAL_ERROR, UNEXPECTED_ERROR


class DataBaseManager:
    def __init__(self):
        self.db = None
        self.cursor = None
        self.logger = logging.getLogger('bibtexToRDF')

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
            self.logger.error(OPERATIONAL_ERROR.format(e))
            return False
        except Exception as e:
            self.logger.error(UNEXPECTED_ERROR.format(e))
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
            req = f'INSERT INTO bibfile (uploaddate, name, size, contenttype, data) VALUES ({upload_date}, \'{filename}\', {size}, \'{contenttype}\', {psycopg2.Binary(data)})'
            self.cursor.execute(req)
            return True, data
        except Exception as e:
            self.logger.error(e)
            return False, None

    def commit_upload(self):
        self.db.commit()

    def commit_upload(self):
        self.db.rollback()

    def get_data_by_id(self, id) -> Union[bytes, None]:
        self.cursor.execute("select data from bibfile where id = {0}".format(id))
        result_set = self.cursor.fetchone()
        if result_set is not None:
            data = result_set['data']
            if data is not None:
                return bytes(data)
        return None
