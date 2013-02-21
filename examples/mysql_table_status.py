#!/usr/bin/python
"""
Collects information about a specified
tables (matched by a condition) in a
selected DB (average values).

Configuration is in ./db.yaml. Sample:
---
db_params:
    host: localhost
    user: dbuser
    db: dbname
    passwd: 'dbpassword'
    use_unicode: False
    charset: utf8
    unix_socket: /var/run/mysqld/mysqld.sock
table: '%MyTable%'
---
"""
import MySQLdb
import yaml
import string
from probebase.app import AppBuilder
from time import time


class MySQLConnector:
    def __init__(self, params):
        self.connection = MySQLdb.connect(**params)

    def __del__(self):
        self.connection.close()

    def execute(self, query):
        cursor = self.connection.cursor()
        cursor.execute(query)
        rows = cursor.fetchall()
        cursor.close()
        for row in rows:
            yield row


class DB(object):
    def __init__(self):
        config = yaml.safe_load(open("db.yaml", 'r'))
        mysql_params = config['db_params']
        self.keys = ["dbstat.%s.%s"\
          % (config['table'].translate(string.maketrans("%", "_")), metric)
          for metric in ["avg_rows", "avg_data_length", "avg_index_length"]]
        self.query = "show table status like '%s'" % config['table']
        self.connector = MySQLConnector(mysql_params)

    def get_status(self):
        status = self.connector.execute(self.query)
        values = ((rows, data_length, index_length)
          for (name, engine, version, row_format, rows, avg_row_length,\
            data_length, max_data_length, index_length, data_free,\
            auto_increment, create_time, update_time, check_time,\
            collation, checksum, create_options, comment)
          in status)
        avg_values = [sum(series) / len(series) for series in zip(*values)]
        return ((key, value, int(time()))
            for key, value in zip(self.keys, avg_values))


DATA_BASE = DB()


def probe_status():
    return DATA_BASE.get_status()

AppBuilder(probe_status).create().launch()
