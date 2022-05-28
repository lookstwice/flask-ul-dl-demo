# importing the required libraries
import os
import csv
import xlsxwriter

import pandas as pd
import pdfkit

from flask import Flask, render_template, request, send_file
from werkzeug.utils import secure_filename


#initialising the flask app
app = Flask(__name__)
app_settings = os.getenv('APP_SETTINGS')
app.config.from_object(app_settings)

# upload and test file paths
base_path = os.path.join(os.environ.get("HOME"), "ul_dl_demo")
xlsx_file_path = os.path.join(base_path, "download_demo.xlsx")
pdf_file_path = os.path.join(base_path, "download_demo.pdf")

# Creating the upload folder
if not os.path.exists(base_path):
    os.mkdir(base_path)

# set the default upload destination
app.config['UPLOAD_FOLDER'] = base_path

# Note: xlswriter can handle formatting the column width
def generate_xlsx():
    # Create a workbook and add a worksheet.
    workbook = xlsxwriter.Workbook(xlsx_file_path)
    worksheet = workbook.add_worksheet()

    bold = workbook.add_format({'bold': True})

    # Some data we want to write to the worksheet.
    data = (
        ["658954", "HEB CC CHOCOLATE & CHERRIES", 10],
        ["142989", "CC NEAPOLITAN 1/2 GAL", 5],
        ["700048", "BOMB POP ORIGINAL 24CT", 1]
    )

    cell_num = 1

    worksheet.write(f"A{cell_num}", "UPC", bold) # Column A
    worksheet.write(f"B{cell_num}", "ITEM", bold) # Column B
    worksheet.write(f"C{cell_num}", "QUANTITY", bold) # Column C

    cell_num += 1

    # Iterate over the data and write it out row by row.
    for upc, item, quantity in (data):
        worksheet.write(f"A{cell_num}", upc) # Column A
        worksheet.write(f"B{cell_num}", item) # Column B
        worksheet.write(f"C{cell_num}", quantity) # Column C
        cell_num += 1

    workbook.close()

def generate_pdf():
    temp_html = os.path.join(base_path, "temp.html")
    df = pd.read_excel(xlsx_file_path)
    df.to_html(temp_html)
    pdfkit.from_file(temp_html, pdf_file_path)

# displaying the HTML template at the home url
@app.route('/')
def index():
   return render_template('index.html')

# Sending the file to the user
@app.route('/download')
def download():
   return render_template('download.html')

@app.route('/upload', methods = ['GET', 'POST'])
def upload():
    return render_template('upload.html')

@app.route('/downloadxlsx')
def download_xlsx():
    generate_xlsx()
    return send_file(xlsx_file_path, as_attachment=True)

@app.route('/downloadpdf')
def download_pdf():
    generate_xlsx()
    generate_pdf()
    return send_file(pdf_file_path, as_attachment=True)

@app.route('/uploader', methods = ['GET', 'POST'])
def uploader():
   if request.method == 'POST': # check if the method is post
      f = request.files['file'] # get the file from the files object
      file_path = os.path.join(app.config['UPLOAD_FOLDER'] ,secure_filename(f.filename))
      f.save(file_path)
      if os.path.exists(file_path):
          msg = f"UPLOAD SUCCESS: {file_path}"
      else:
          msg = "UPLOAD FAILURE"
      return f'{msg}' # Display message after uploading

if __name__ == '__main__':
   # app.run() # running the flask app
   app.run(host="0.0.0.0", debug=True)
