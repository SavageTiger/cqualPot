import sqlite3
import uuid
import shutil

class Sqlite:

    __connection = None,
    __tables     = []
    __lastQuery  = ''

    def __init__(self):
        randomId = str(uuid.uuid4())

        shutil.copy('database_template/fake.db', 'tmp/' + randomId + '.sqlite')

        self.__connection = sqlite3.connect('tmp/' + randomId + '.sqlite')
        self.__tables     = self.__connection.execute('SELECT name FROM sqlite_master WHERE type=\'table\'').fetchall()

    def guessTable(self):
        # Look in the middle of the query
        for table in self.__tables:
            if self.__lastQuery.lower().find(' ' + table[0] + ' ') > 0:
                return table[0]

        # Look at the end of the query
        for table in self.__tables:
            if self.__lastQuery.lower().find(' ' + table[0]) > 0:
                return table[0]

        return ''

    def executeQuery(self, query: str):
        query = query.strip()

        # Sqlite has no SET support, so lets just ignore it for now
        if query.upper()[0:3] == 'SET':
            return []

        self.__lastQuery = query

        result = self.__connection.execute(query)

        return result.fetchall()

