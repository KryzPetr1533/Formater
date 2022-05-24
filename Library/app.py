from PyQt5 import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from .index import click_func

class App(QWidget):
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

    self.btn_submit.pressed.connect(self.click)

  def click(self):
    click_func(self)

  def show_popup_error(self):
    QMessageBox.about(self, "Error", "Something went wrong..")