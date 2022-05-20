import requests
import xlsxwriter
import csv
import mysql.connector
import sqlite3
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication
import os

from mysql.connector import Error

Form, Window = uic.loadUiType("gui.ui")
app = QApplication([])
window = Window()
form = Form()
form.setupUi(window)
window.show()


# url = 'http://catalog.data.gov/api/3/action/package_list'

def start_click():
    print("click start")


# form.startButton.clicked.connect(start_click)

def continue_click():
    global cursor
    url = form.lineEdit.text()
    name = 'file'
    # Some data (this is test version) we want to write to save.
    response = requests.get(url)
    response = response.json()
    # print(*response.items(), sep = '\n')
    if form.comboBox.currentText() == ".xlsx":
        # Create a workbook (exel file) and add a worksheet (table).
        workbook = xlsxwriter.Workbook(name + '.xlsx')
        worksheet = workbook.add_worksheet()
        # Start from the first cell. Rows and columns are zero indexed.
        row = 0
        col = 0
        width = 20
        for items in response['result']['results']:
            col = 0
            for name, data in items.items():
                if type(data) is not list and type(data) is not dict and data is not None:
                    if row == 0:
                        worksheet.write(row, col, name, workbook.add_format({'bold': 1}))
                    else:
                        worksheet.write(row, col, data)
                    # Adjust the column width.
                    worksheet.set_column(row, col, width)
                    col += 1
            row += 1
        # Iterate over the data and write it out row by row.
        # # Write a total using a formula.
        workbook.close()
        print("Successful exported data from " + form.lineEdit.text() + " to Excel .xlsx file!")
    if form.comboBox.currentText() == ".csv":
        with open(name + '.csv', 'w', newline='') as csvfile:
            worksheet = csv.writer(csvfile, quotechar='|', quoting=csv.QUOTE_MINIMAL)
            row = 0
            for items in response['result']['results']:
                string = []
                for name, data in items.items():
                    if type(data) is not list and type(data) is not dict and data is not None:
                        if row == 0:
                            string += [name]
                        else:
                            string += [data]

                worksheet.writerow(string)
                row += 1
        print("Successful exported data from " + form.lineEdit.text() + " to CSV .csv file!")
    if form.comboBox.currentText() == "MySQL":

        mysql_host = "localhost"
        mysql_database = "test"
        mysql_port = 3306
        mysql_username = "root"
        mysql_password = "adminadmin"
        mysql_table = "result"
        connection = None
        try:
            if (form.comboBox.currentText() == "MySQL"):
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
                        if type(data) is not list and type(data) is not dict and data is not None:
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
            if (connection.is_connected()):
                cursor.close()
                connection.close()
        print("Successful exported data from " + form.lineEdit.text() + " to MySQL DataBase!")
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
                        if type(data) is not list and type(data) is not dict and data is not None:
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
        print("Successful exported data from " + form.lineEdit.text() + " to SQLite DataBase!")


form.continueButton.clicked.connect(continue_click)
app.exec_()
