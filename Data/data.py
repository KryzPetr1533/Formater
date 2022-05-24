import mysql.connector
import sqlite3
from mysql.connector import Error
import pandas as pd

def sql_parser(self, response):
  try:
    mysql_host = self.mysql_host_text.text()
    mysql_database = self.mysql_database_text.text()
    mysql_port = int(self.mysql_port_text.text())
    mysql_username = self.mysql_username_text.text()
    mysql_password = self.mysql_password_text.text()
    mysql_table = self.mysql_table_text.text()
    connection = None

    connection = mysql.connector.connect(
      host = mysql_host,
      port = mysql_port,
      database = mysql_database,
      user = mysql_username,
      password = mysql_password
    )

    if (connection.is_connected()):
      cursor = connection.cursor()
      sql_delete = 'DROP TABLE IF EXISTS ' + mysql_table
      cursor.execute(sql_delete)

      sql_create = 'CREATE TABLE ' + mysql_table + ' ('
      sql_list = []
      data_frame = pd.json_normalize(response['result']);
      i = 0

      for string in data_frame.columns.values:
        sql_create += '`' + string + '`' + ' TEXT,'
        i += 1
      cursor.execute(sql_create[:-1] + ')')
      sql_newline = 'INSERT INTO ' + mysql_table + ' VALUES ('
      sql_value = []
      t = 0
      while t < i:
        sql_newline += '%s,'
        sql_value.append(str(data_frame.iloc[0][t]))
        t += 1

      sql_list.append([sql_newline[:-1] + ')', sql_value])
      
      for list1 in sql_list:
        if (len(list1[1]) > 0):
          cursor.execute(list1[0], list1[1])
      connection.commit()
  except Error as e:
    print(e)
    self.show_popup_error(self)
  finally:
    if (connection.is_connected()):
      connection.close()
  print("Successful exported data from " + self.file_text.text() + " to MySQL DataBase!")

def db_parser(self, file_name, response):
  connection = None

  try:
    connection = sqlite3.connect(file_name + ".db")
    sql_table = 'database'

    if (connection):
      cursor = connection.cursor()
      sql_delete = 'DROP TABLE IF EXISTS ' + sql_table
      cursor.execute(sql_delete)

      sql_create = 'CREATE TABLE ' + sql_table + ' ('
      sql_list = []
      data_frame = pd.json_normalize(response['result']);
      i = 0

      for string in data_frame.columns.values:
        sql_create += '\'' + string + '\'' + ' TEXT,'
        i += 1
      cursor.execute(sql_create[:-1] + ')')

      sql_newline = 'INSERT INTO ' + sql_table + ' VALUES ('
      sql_value = []
      t = 0
      while t < i:
        sql_newline += '?,'
        sql_value.append(str(data_frame.iloc[0][t]))
        t += 1

      sql_list.append([sql_newline[:-1] + ')', sql_value])
      for list1 in sql_list:
        if (len(list1[1]) > 0):
          cursor.execute(list1[0], list1[1])

      connection.commit()
  except Error as e:
    print(e)
    self.show_popup_error(self)

  finally:
    if (connection):
      cursor.close()
      connection.close()

  print("Successful exported data from " + self.file_text.text() + " to SQLite DataBase!")