from protocol import Constants

import sqlite3
import uuid
import shutil
import json

class Sqlite:

    __connection       = None,
    __tables           = []
    __lastQuery        = ''
    __variables        = []
    __selectedDatabase = ''
    __expectedColumns  = None

    def __init__(self, selectedDatabase: str):
        randomId = str(uuid.uuid4())

        shutil.copy('database_template/fake.db', 'tmp/' + randomId + '.sqlite')

        self.__connection = sqlite3.connect('tmp/' + randomId + '.sqlite')

        self.__variables        = json.load(open('database_template/variables.json', 'r'))
        self.__tables           = self.__connection.execute('SELECT name FROM sqlite_master WHERE type=\'table\'').fetchall()
        self.__selectedDatabase = selectedDatabase

    def getColumnDefinitions(self):
        # SQLite has really limited field type support. So lets just assume 255 varchar and 8 byte longs.
        types  = { 'TEXT': Constants.FIELD_TYPE_VARCHAR, 'INTEGER': Constants.FIELD_TYPE_LONG, 'NUMERIC': Constants.FIELD_TYPE_LONG }
        length = { 'TEXT': 255, 'INTEGER': 8, 'NUMERIC': 8 }

        definition = []

        if self.__expectedColumns != None:
            columns = self.__expectedColumns

            # Reset
            self.__expectedColumns = None
        else:
            columns = self.__connection.execute('PRAGMA table_info(' + self.guessTable() + ')').fetchall()

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

    def resolveVariable(self, query: str):
        for variableKey in self.__variables:
            if query.find(variableKey) > 0:
                self.__expectedColumns = [(0, variableKey, 'TEXT')]

                return [[ self.__variables[variableKey] ]]

        return ''

    def handleShow(self, query: str):
        # SHOW DATABASES
        if query.upper().find('DATABASES') > 0:
            self.__expectedColumns = [(0, 'Database', 'TEXT')]

            if self.__selectedDatabase == '':
                selectedDatabase = 'Honeypot' # Todo, make configurable
            else:
                selectedDatabase = self.__selectedDatabase

            if selectedDatabase.upper() == 'MYSQL':
                return [['mysql']]
            else:
                return [['mysql'], [selectedDatabase]]

        return []

    def executeQuery(self, query: str):
        query = query.strip()

        print ('Q:' + query)

        self.__lastQuery = query

        # Sqlite has no SET support, so lets just ignore it for now
        # TODO implement internal updateVariable
        if query.upper()[0:3] == 'SET':
            return []

        if query.upper()[0:4] == 'SHOW':
            return self.handleShow(query)

        # Crudely simulate variable request response
        if query.find('@@') > 0 and self.resolveVariable(query) != '':
            return self.resolveVariable(query)

        try:
            result = self.__connection.execute(query)

            return result.fetchall()
        except sqlite3.Error as e:
            print ('ERROR: ' + query) # TODO: Move to logger

            return e


