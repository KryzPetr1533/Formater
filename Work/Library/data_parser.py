import pandas as pd

def xlsx_parser(self, response, name_file):
  data_frame = pd.json_normalize(response['result'])
  data_frame.to_excel(name_file)
  print("Successful exported data from " + self.file_text.text() + " to Excel .xlsx file!")

def scv_parser(self, response, name_file):
  data_frame = pd.json_normalize(response['result'])
  data_frame.to_csv(name_file)
  print("Successful exported data from " + self.file_text.text() + " to CSV .csv file!")
