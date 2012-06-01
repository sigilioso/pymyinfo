# -*- coding: utf-8 -*-

"""
db_timer_manager.py

A simple Database manager for MySQLdb to easily run queries and keep the 
database connection opened for a while. 
"""

import MySQLdb
from MySQLdb.cursors import DictCursor
from threading import Timer
from contextlib import contextmanager

class DatabaseTimerManager(object):
    """
    Class which represents a MySQL manager defined to to run queries and keep
    the database connection opened for some time in order to execute subsequent
    queries.
    """
    def __init__(self, host, user, password, connection_time=10,
            cursorclass=DictCursor):
        """
        args:
            `host`: host for the database connection.
            `user`: user for the database connection.
            `password`: for the database connection.
            `connection_time`: (default 20) the amount of time which the MySQL 
                connection will be kept opened after executing a query.
            `cursorclass`: the MySQLdb cursor class to be used.
        """
        self.__host = host
        self.__user = user
        self.__password = password
        self.cursorclass = cursorclass
        self.__db = None
        self.__timer = Timer(connection_time, self.__close)

    def __connect(self):
        """
        Stablish the database connection.
        """
        self.__db = MySQLdb.connect(host=self.__host, user=self.__user,
                passwd=self.__password, cursorclass=self.cursorclass)

    def __close(self):
        """
        Close the database connection.
        """
        self.__db.close()

    def __start_timer(self):
        """
        Creates a new timer and starts it in order to close the database 
        connection when it reaches its end.
        """
        self.__timer = Timer(self.__timer.interval, self.__close)
        self.__timer.start()

    @contextmanager
    def execute(self, *args, **kwargs):
        """
        Execute a query by means of MySQLdb and yields its results (see
        [MySQLdb Documentation](http://mysql-python.sourceforge.net/MySQLdb.html)
        for details. The connection to the database is kept opened for the
        specified time.
        """
        if self.__db and self.__db.open:
            # Cancel the timer if the db connection is opened
            self.__timer.cancel()
        else :
            # If not, just connect
            self.__connect()
        cursor = self.__db.cursor()
        cursor.execute(*args, **kwargs)
        yield cursor
        # Start the timer again
        self.__start_timer()

