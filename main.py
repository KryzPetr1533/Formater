import requests
import xlsxwriter

name = 'file'
# Create a workbook (exel file) and add a worksheet (table).
workbook = xlsxwriter.Workbook(name + '.xlsx')
worksheet = workbook.add_worksheet()

# Some data (this is test version) we want to write to the worksheet.
response = requests.get('http://catalog.data.gov/api/3/action/package_list')
response = response.json()

# print(*response.items(), sep = '\n')
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
# worksheet.write(row, 0, 'Total')
# worksheet.write(row, 1, '=SUM(B1:B4)')

workbook.close()



from PyQt5 import uic
from PyQt5.QtWidgets import QApplication
import os

Form, Window = uic.loadUiType("gui.ui")
app = QApplication([])
window = Window()
form = Form()
form.setupUi(window)
window.show()

def start_click():
    print("click start with URL: " + form.lineEdit.text())
form.startButton.clicked.connect(start_click)


def continue_click():
    print("click continue with format: " + form.comboBox.currentText())
form.continueButton.clicked.connect(continue_click)

app.exec_()
