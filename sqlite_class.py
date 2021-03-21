"""Modified from original on: https://gist.github.com/goldsborough/c973d934f620e16678bf """

import sqlite3
import logging


class Database:


    def __init__(self, name=None):
        
        self.conn = None
        self.cursor = None

        if name:
            self.open(name)


    def open(self,name):
        
        try:
            self.conn = sqlite3.connect(name)
            self.cursor = self.conn.cursor()
            message = "Opened Database: " + name
            logging.debug(message)

        except sqlite3.Error as e:
            message = "Error connecting to: " + name + e
            logging.error(message)


    def close(self):
        
        if self.conn:
            self.conn.commit()
            self.cursor.close()
            self.conn.close()
        message = "Database Closed"
        logging.debug(message)


    def __enter__(self):
        
        return self


    def __exit__(self,exc_type,exc_value,traceback):
        
        self.close()

    def get(self,table,columns,limit=None):

        query = "SELECT {0} from {1};".format(columns,table)
        self.cursor.execute(query)

        # fetch data
        rows = self.cursor.fetchall()

        return rows[len(rows)-limit if limit else 0:]



    def write(self,table,columns,data):
        
        query = "INSERT INTO {0} ({1}) VALUES ({2});".format(table,columns,data)

        self.cursor.execute(query)


    def query(self,sql_query):
        
        try:
            self.cursor.execute(sql_query)
            logging.info(f"Executed: {sql_query}")
            
        except sqlite3.Error as e:
            logging.error(f"Error '{e}'' while executing '{sql_query}'")

    def query_many(self,sql_query,data):
        
        try:
            self.cursor.executemany(sql_query, data)
            logging.info(f"Executed: {sql_query}")

        except sqlite3.Error as e:
            logging.error(f"Error '{e}'' while executing '{sql_query}'")


    def read_query(self, sql_query):

        try:
            self.cursor.execute(sql_query)
            result = self.cursor.fetchall()
            logging.info(f"Executed: '{sql_query}'")

            return result

        except sqlite3.Error as e:            
            logging.critical(f"The error: '{e}' occurred.")


