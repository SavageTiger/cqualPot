from protocol import Constants

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

    def getColumnDefinitions(self):
        # SQLite has really limited field type support. So lets just assume 255 varchar and 8 byte longs.
        types      = { 'TEXT': Constants.FIELD_TYPE_VARCHAR, 'INTEGER': Constants.FIELD_TYPE_LONG, 'NUMERIC': Constants.FIELD_TYPE_LONG }
        length     = { 'TEXT': 255, 'INTEGER': 8, 'NUMERIC': 8 }

        definition = []
        columns    = self.__connection.execute('PRAGMA table_info(' + self.guessTable() + ')').fetchall()

        for c in columns:
            definition.append({
                'name'   : c[1],
                'type'   : types[c[2]],
                'length' : length[c[2]]
            })

        return definition


    def guessTable(self):
        # TODO: dbname.tablename
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

        try:
            result = self.__connection.execute(query)
        except sqlite3.Error as e:
            print ('ERROR: ' + query) # TODO: Move to logger

        return result.fetchall()

