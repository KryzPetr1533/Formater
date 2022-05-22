import requests
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication
import os
import pandas as pd

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
            raise Exception("status_code not equal 200!")
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
    except Exception as err:
        print(err)

form.continueButton.clicked.connect(continue_click)
app.exec_()