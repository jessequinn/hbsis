'''

Simple python script to convert the city list from http://bulk.openweathermap.org/sample/ to a sqlite database.

'''

# from __future__ import unicode_literals
# from builtins import str  #  pip install future
import json
import sqlite3
from sqlite3 import Error


def create_connection(db):
    '''

    Create a database connection to the SQLite database specified by db.

    :param db: database file
    :return: Connection object or None

    '''

    try:
        conn = sqlite3.connect(db)
        return conn
    except Error as e:
        print(e)

    return None


def create_table(conn, create_table_sql):
    '''

    Create a table from the create_table_sql statement.

    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:

    '''

    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)


def insert_city(conn, keys):
    '''

    Insert city info.

    :param conn: Connection object
    :param keys: data
    :return:

    '''

    try:
        # SQL insert
        sql = '''INSERT INTO cities VALUES (?,?,?)'''

        c = conn.cursor()
        c.execute(sql, keys)
    except Error as e:
        print(e)


def main():
    database = "city.list.db"

    sql_create_cities_table = '''
    CREATE TABLE IF NOT EXISTS cities (
    id integer PRIMARY KEY, 
    name text NOT NULL,
    country text NOT NULL);'''

    # load json file that contains all cities
    # available from http://bulk.openweathermap.org/sample/
    cities = json.load(open("city.list.json"))

    # sqlite database
    conn = create_connection(database)

    with conn:
        # create cities table
        create_table(conn, sql_create_cities_table)

        # ignore coordinates
        columns = ["id", "name", "country"]

        # tuple of city info passed to sql
        for c in cities:
            # keys = tuple(u"{}".format(c[i]) if isinstance(c[i], str) else c[i] for i in columns)
            keys = tuple(c[i] for i in columns)

            # json contains continents as well
            if keys[2] != '':
                insert_city(conn, keys)


if __name__ == '__main__':
    main()
