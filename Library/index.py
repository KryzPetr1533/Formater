import requests

from Formater.Data.data import *
from .data_parser import *

def normilize_url(url_name):
  url_name = url_name.split('/')[3]

  return 'https://catalog.data.gov/api/3/action/package_show?id=' + url_name

def click_func(self):
  global cursor
  try:
    file_name = "../Output/" + self.file_text.text()
    url = normilize_url(self.url_text.text())
    name_file = file_name + self.combo_box.currentText()
    response = requests.get(url)

    if (response.status_code != 200):
      raise Exception("status_code not equal 200!")

    response = response.json()

    if (self.combo_box.currentText() == '.xlsx'):
      xlsx_parser(self, response, name_file)

    if (self.combo_box.currentText() == ".csv"):
      scv_parser(self, response, name_file)

    if (self.combo_box.currentText() == "MySQL"):
      sql_parser(self, response)

    if (self.combo_box.currentText() == "SQLite (.db)"):
      db_parser(self, file_name, response)

  except Exception as err:
    print(err)
    self.show_popup_error()