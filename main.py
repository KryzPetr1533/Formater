import requests
import mysql.connector
import sqlite3
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication
import os
import pandas as pd

from mysql.connector import Error

Form, Window = uic.loadUiType("gui.ui")
app = QApplication([])
window = Window()
form = Form()
form.setupUi(window)
window.show()

# https://catalog.data.gov/api/3/action/package_show?id=cms-lidar-data-for-forested-areas-in-paragominas-para-brazil-2012-2014
# https://catalog.data.gov/api/3/action/package_show?id=active-control-of-tailored-laminates
# https://catalog.data.gov/api/3/action/package_show?id=water-quality-total-organic-carbon-removal

def start_click():
    print("click start")

    # form.startButton.clicked.connect(start_click)


def continue_click():
    global cursor
    try:
        url = form.lineEdit.text()
        name_file = 'file' + form.comboBox.currentText()
        response = requests.get(url)
        if response.status_code != 200:
            raise Exception
        response = response.json()
        if form.comboBox.currentText() == '.xlsx':
            data_frame = pd.json_normalize(response['result'])
            data_frame.to_excel(name_file)
        print(
            "Successful exported data from " +
            form.lineEdit.text() +
            " to Excel .xlsx file!")
        if form.comboBox.currentText() == ".csv":
            data_frame = pd.json_normalize(response['result'])
            data_frame.to_csv(name_file)
        print(
            "Successful exported data from " +
            form.lineEdit.text() +
            " to CSV .csv file!")
    except Error as err:
        print(err)


if form.comboBox.currentText() == "MySQL":

    mysql_host = "localhost"
    mysql_database = "test"
    mysql_port = 3306
    mysql_username = "root"
    mysql_password = "adminadmin"
    mysql_table = "result"
    connection = None
    try:
        if form.comboBox.currentText() == "MySQL":
            connection = mysql.connector.connect(
                host=mysql_host,
                port=mysql_port,
                database=mysql_database,
                user=mysql_username,
                password=mysql_password)
        if connection.is_connected():
            cursor = connection.cursor()
            sql_delete = 'DROP TABLE IF EXISTS ' + mysql_table
            cursor.execute(sql_delete)

            row = 0
            count_args = 0
            sql_create = 'CREATE TABLE ' + mysql_table + ' ('
            sql_list = []
            for items in response['result']['results']:
                sql_newline = 'INSERT ' + mysql_table + ' VALUES ('
                sql_value = []
                for name, data in items.items():
                    if not isinstance(
                            data, list) and not isinstance(
                            data, dict) and data is not None:
                        if row == 0:
                            sql_create += name + ' TEXT,'
                            count_args += 1
                        else:
                            sql_newline += '%s,'
                            sql_value.append(data)
                sql_list.append([sql_newline[:-1] + ')', sql_value])
                row += 1
            cursor.execute(sql_create[:-1] + ')')
            for list1 in sql_list:
                if len(list1[1]) > 0:
                    cursor.execute(list1[0], list1[1])
            connection.commit()
    except Error as e:
        print(e)
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
    print(
        "Successful exported data from " +
        form.lineEdit.text() +
        " to MySQL DataBase!")
if form.comboBox.currentText() == "SQLite (.db)":
    connection = None
    try:
        connection = sqlite3.connect("database.db")
        sql_table = 'database'
        if connection:
            cursor = connection.cursor()
            sql_delete = 'DROP TABLE IF EXISTS ' + sql_table
            cursor.execute(sql_delete)

            row = 0
            count_args = 0
            sql_create = 'CREATE TABLE ' + sql_table + ' ('
            sql_list = []
            for items in response['result']['results']:
                sql_newline = 'INSERT INTO ' + sql_table + ' VALUES ('
                sql_value = []
                for name, data in items.items():
                    if not isinstance(
                            data, list) and not isinstance(
                            data, dict) and data is not None:
                        if row == 0:
                            sql_create += name + ' TEXT,'
                            count_args += 1
                        else:
                            sql_newline += '?,'
                            sql_value.append(data)
                sql_list.append([sql_newline[:-1] + ')', sql_value])
                row += 1
            cursor.execute(sql_create[:-1] + ')')
            for list1 in sql_list:
                if len(list1[1]) > 0:
                    cursor.execute(list1[0], list1[1])
            connection.commit()
    except Error as e:
        print(e)
    finally:
        if connection:
            cursor.close()
            connection.close()
    print(
        "Successful exported data from " +
        form.lineEdit.text() +
        " to SQLite DataBase!")

form.continueButton.clicked.connect(continue_click)
app.exec_()
