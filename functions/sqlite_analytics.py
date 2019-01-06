import os
import sqlite3
import argparse
from sqlite3 import Error

from datetime import datetime as dt

class UrlViews:
    def __init__(self):
        sqlite_file = "../dbase/url_views.db"

        self.curdir = os.path.dirname(os.path.realpath(__file__))
        self.sqlite_file = os.path.join(self.curdir, sqlite_file)
        self.conn = None
        self.create_connection()

    def create_connection(self):
        """ create a database connection to the SQLite database
            specified by db_file
        :param db_file: database file
        :return: Connection object or None
        """
        try:
            self.conn = sqlite3.connect(self.sqlite_file)
            self.conn.row_factory = sqlite3.Row  #for getting the colnames!
        except Error as e:
            print("create_connection: {}".format(e))
        return None

    def create_table(self):
        table_create = '''CREATE TABLE IF NOT EXISTS `pageviews` (id integer PRIMARY KEY, 
                          `page` TEXT, 
                          `view_id` integer, 
                          `ga:uniquePageviews` integer DEFAULT 1, 
                          `ga:pageviews` integer DEFAULT 1,
                          `lastupdate` timestamp )'''
        try:
            self.conn.execute(table_create)
        except Error as e:
            print("create_table: {}".format(e))

        table_unique = '''CREATE UNIQUE INDEX idx_positions_page ON `pageviews` (page);'''
        try:
            self.conn.execute(table_unique)
        except Error as e:
            print("table_unique: {}".format(e))

    def drop_table(self):
        table_create = '''DROP TABLE IF EXISTS `pageviews`'''
        try:
            self.conn.execute(table_create)
        except Error as e:
            print("create_table: {}".format(e))

    def get_last_row(self):
        sql = '''SELECT `page`, `view_id`, `ga:uniquePageviews`, `ga:pageviews`, `lastupdate` FROM `pageviews` 
                 ORDER BY url DESC LIMIT 1'''
        try:
            cur = self.conn.cursor()
            cur.execute(sql)

            return cur.fetchone()
        except Error as e:
            print("get_last_row: {}".format(e))

    def get_views_from_page(self, fields):
        try:
            sql = '''SELECT `page`, `view_id`, `ga:uniquePageviews`, `ga:pageviews`, `lastupdate` 
                     FROM `pageviews` WHERE `page` = ? and `lastupdate` > ?'''

            cur = self.conn.cursor()
            cur.execute(sql, fields)
            return cur.fetchone()

        except Error as e:
            print("get_row: {}".format(e))

    def get_views_from_view_id(self, fields):
        try:
            sql = '''SELECT `page`, `view_id`, `ga:uniquePageviews`, `ga:pageviews`, `lastupdate` 
                     FROM `pageviews` 
                     WHERE `view_id` = ?
                     ORDER BY `ga:uniquePageviews` DESC 
                     LIMIT ?'''

            cur = self.conn.cursor()
            cur.execute(sql, fields)
            return cur.fetchone()

        except Error as e:
            print("get_row: {}".format(e))

    def replace_row(self, fields):
        try:
            sql = '''REPLACE INTO `pageviews` (`page`,`view_id`,`ga:uniquePageviews`, `ga:pageviews`, `lastupdate`)
                     VALUES(?, ?, ?, ?, ?);'''

            cur = self.conn.cursor()
            cur.execute(sql, fields)
            self.conn.commit()
        except Error as e:
            print("insert_row: {}".format(e))

    def close_conn(self):
        try:
            self.conn.close()
        except Error as e:
            print("close_conn: {}".format(e))


if __name__ == "__main__":
    now = int(dt.utcnow().strftime("%s"))
    infourhours = now+14400

    page_path = '2018/12/01/01-12-2018-image-resize-python-automation-script.html'
    view_id = '10374727'

    s = UrlViews()

    '''
    easy helper to create, destroy or get data from database
    '''
    parser = argparse.ArgumentParser(
        description='''Welcome to this helpfile. ''',
        epilog="""Thats all folks!""")
    parser.add_argument('-dd', '--dropDatabase', help='Drop Database', required=False, type=str)
    parser.add_argument('-cd', '--createDatabase', help='Create Database', required=False, type=str)
    parser.add_argument('-id', '--insertData', help='Insert Data', required=False, type=str)
    parser.add_argument('-gd', '--getData', help='get Data', required=False, type=str)
    args = parser.parse_args()

    if args.dropDatabase is not None and args.dropDatabase.lower() in ('yes', 'true', 't', 'y', '1'):
        s.drop_table()

    if args.createDatabase is not None and args.createDatabase.lower() in ('yes', 'true', 't', 'y', '1'):
        s.create_table()

    if args.insertData is not None and args.insertData.lower() in ('yes', 'true', 't', 'y', '1'):
        fields = [page_path, view_id, 45, 55, now]
        s.replace_row(fields)

    if args.getData is not None and args.getData.lower() in ('yes', 'true', 't', 'y', '1'):
        fields = [page_path, view_id]
        row = s.get_views_from_page(fields)
        print(row.keys())
        print(dict(row))
