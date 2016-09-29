import sqlite3
import uuid
import shutil

class Sqlite:

    __connection = None

    def __init__(self):
        randomId = str(uuid.uuid4())

        shutil.copy('database_template/fake.db', 'tmp/' + randomId + '.sqlite')

        self.__connection = sqlite3.connect('tmp/' + randomId + '.sqlite')

    def executeQuery(self, query: str):
        query = query.strip()

        # Sqlite has no SET support, so lets just ignore it for now
        if query.upper()[0:3] == 'SET':
            return []

        result = self.__connection.execute(query)

        return result.fetchall()

