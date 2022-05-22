import requests
import mysql.connector
import sqlite3
from PyQt5 import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import sys
import pandas as pd

from mysql.connector import Error


def start_click():
    print("click start")

    # form.startButton.clicked.connect(start_click)


def normilize_url(url_name):
    url_name = url_name.split('/')[3]

    return 'https://catalog.data.gov/api/3/action/package_show?id=' + url_name


class Example(QWidget):

    def __init__(self):
        QWidget.__init__(self)
        self.setWindowTitle("Formater")

        # url
        self.url_label = QLabel("URL", self)
        self.url_label.setAlignment(Qt.AlignCenter)
        self.url_text = QLineEdit(self)
        self.url_text.setAlignment(Qt.AlignCenter)

        # file name
        self.file_label = QLabel("File name", self)
        self.file_label.setAlignment(Qt.AlignCenter)
        self.file_text = QLineEdit(self)
        self.file_text.setAlignment(Qt.AlignCenter)

        # Availible formats
        self.formats_label = QLabel("Availible formats", self)
        self.formats_label.setAlignment(Qt.AlignCenter)
        self.formats_text = QLabel(".xlsx, .csv, MySQL, SQLite (.db)")
        self.formats_text.setAlignment(Qt.AlignCenter)

        # title of settings
        self.sql_title = QLabel("SQL settings", self)
        self.sql_title.setAlignment(Qt.AlignCenter)

        # mysql_host
        self.mysql_host_label = QLabel("mysql_host", self)
        self.mysql_host_label.setAlignment(Qt.AlignCenter)
        self.mysql_host_text = QLineEdit(self)
        self.mysql_host_text.setAlignment(Qt.AlignCenter)

        # mysql_database
        self.mysql_database_label = QLabel("mysql_database", self)
        self.mysql_database_label.setAlignment(Qt.AlignCenter)
        self.mysql_database_text = QLineEdit(self)
        self.mysql_database_text.setAlignment(Qt.AlignCenter)

        # mysql_port
        self.mysql_port_label = QLabel("mysql_port", self)
        self.mysql_port_label.setAlignment(Qt.AlignCenter)
        self.mysql_port_text = QLineEdit(self)
        self.mysql_port_text.setAlignment(Qt.AlignCenter)

        # mysql_username
        self.mysql_username_label = QLabel("mysql_username", self)
        self.mysql_username_label.setAlignment(Qt.AlignCenter)
        self.mysql_username_text = QLineEdit(self)
        self.mysql_username_text.setAlignment(Qt.AlignCenter)

        # mysql_password
        self.mysql_password_label = QLabel("mysql_password", self)
        self.mysql_password_label.setAlignment(Qt.AlignCenter)
        self.mysql_password_text = QLineEdit(self)
        self.mysql_password_text.setAlignment(Qt.AlignCenter)

        # mysql_table
        self.mysql_table_label = QLabel("mysql_table", self)
        self.mysql_table_label.setAlignment(Qt.AlignCenter)
        self.mysql_table_text = QLineEdit(self)
        self.mysql_table_text.setAlignment(Qt.AlignCenter)

        # avaliable list
        self.list_label = QLabel("Save as", self)
        self.list_label.setAlignment(Qt.AlignCenter)
        self.available_list = [".xlsx", ".csv", "MySQL", "SQLite (.db)"]
        self.combo_box = QComboBox(self)
        self.combo_box.addItems(self.available_list)

        self.btn_submit = QPushButton("Continue", self)

        # all includes
        self.layout = QGridLayout()
        self.layout.addWidget(self.url_label, 0, 0)
        self.layout.addWidget(self.url_text, 0, 1)
        self.layout.addWidget(self.file_label, 2, 0)
        self.layout.addWidget(self.file_text, 2, 1)
        self.layout.addWidget(self.formats_label, 4, 0)
        self.layout.addWidget(self.formats_text, 4, 1)
        self.layout.addWidget(self.list_label, 6, 0)
        self.layout.addWidget(self.combo_box, 6, 1)
        self.layout.addWidget(self.sql_title, 8, 0)
        self.layout.addWidget(self.mysql_host_label, 9, 0)
        self.layout.addWidget(self.mysql_host_text, 9, 1)
        self.layout.addWidget(self.mysql_database_label, 10, 0)
        self.layout.addWidget(self.mysql_database_text, 10, 1)
        self.layout.addWidget(self.mysql_port_label, 11, 0)
        self.layout.addWidget(self.mysql_port_text, 11, 1)
        self.layout.addWidget(self.mysql_username_label, 12, 0)
        self.layout.addWidget(self.mysql_username_text, 12, 1)
        self.layout.addWidget(self.mysql_password_label, 13, 0)
        self.layout.addWidget(self.mysql_password_text, 13, 1)
        self.layout.addWidget(self.mysql_table_label, 14, 0)
        self.layout.addWidget(self.mysql_table_text, 14, 1)
        self.layout.addWidget(self.btn_submit, 18, 1)

        self.setLayout(self.layout)
        self.show()

        self.btn_submit.pressed.connect(self.continue_click)

    def continue_click(self):
        global cursor
        try:
            file_name = self.file_text.text()
            url = normilize_url(self.url_text.text())
            name_file = file_name + self.combo_box.currentText()
            response = requests.get(url)

            if response.status_code != 200:
                raise Exception("status_code not equal 200!")

            response = response.json()

            if self.combo_box.currentText() == '.xlsx':
                data_frame = pd.json_normalize(response['result'])
                data_frame.to_excel(name_file)
                print("Successful exported data from " + self.file_text.text() + " to Excel .xlsx file!")

            if self.combo_box.currentText() == ".csv":
                data_frame = pd.json_normalize(response['result'])
                data_frame.to_csv(name_file)
                print("Successful exported data from " + self.file_text.text() + " to CSV .csv file!")

            if self.combo_box.currentText() == "MySQL":
                try:
                    mysql_host = self.mysql_host_text.text()
                    mysql_database = self.mysql_database_text.text()
                    mysql_port = int(self.mysql_port_text.text())
                    mysql_username = self.mysql_username_text.text()
                    mysql_password = self.mysql_password.text()
                    mysql_table = self.mysql_table.text()
                    connection = None
                    
                    if self.combo_box.currentText() == "MySQL":
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
                            if len(list1[1]) > 0:
                                cursor.execute(list1[0], list1[1])
                        connection.commit();
                except Error as e:
                    print(e)
                    self.show_popup_error(self)
                finally:
                    if connection.is_connected():
                        connection.close()
                print("Successful exported data from " + self.file_text.text() + " to MySQL DataBase!")

            if self.combo_box.currentText() == "SQLite (.db)":
                connection = None
                try:
                    connection = sqlite3.connect(file_name + ".db")
                    sql_table = 'database'

                    if connection:
                        cursor = connection.cursor()
                        sql_delete = 'DROP TABLE IF EXISTS ' + sql_table
                        cursor.execute(sql_delete)

                        sql_create = 'CREATE TABLE ' + sql_table + ' ('
                        sql_list = []
                        data_frame = pd.json_normalize(response['result']);
                        i = 0
                        for string in data_frame.columns.values:
                            sql_create += '\'' + string + '\'' + ' TEXT,'
                            i+=1
                        cursor.execute(sql_create[:-1] + ')')

                        sql_newline = 'INSERT INTO ' + sql_table + ' VALUES ('
                        sql_value = []
                        t = 0
                        while t < i:
                            sql_newline += '?,'
                            sql_value.append(str(data_frame.iloc[0][t]))
                            t+=1

                        sql_list.append([sql_newline[:-1] + ')', sql_value])
                        for list1 in sql_list:
                            if len(list1[1]) > 0:
                                cursor.execute(list1[0], list1[1])

                        connection.commit()
                except Error as e:
                    print(e)
                    self.show_popup_error(self)

                finally:
                    if connection:
                        cursor.close()
                        connection.close()

                print("Successful exported data from " + self.file_text.text() + " to SQLite DataBase!")

        except Exception as err:
            print(err)
            self.show_popup_error()

    def show_popup_error(self):
        QMessageBox.about(self, "Error", "Something went wrong..")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())
