# importing the required libraries
import os
import csv
from flask import Flask, render_template, request, send_file
from werkzeug.utils import secure_filename

#initialising the flask app
app = Flask(__name__)

# upload and test file paths
base_path = os.path.join(os.environ.get("HOME"), "Downloads", "ul_dl_demo")
file_path = os.path.join(base_path, "download_demo.csv")

# Creating the upload folder
if not os.path.exists(base_path):
    os.mkdir(base_path)

# set the default upload destination
app.config['UPLOAD_FOLDER'] = base_path

# Note: xlswriter can handle formatting the column width
def generate_csv():
    with open(file_path, 'w') as csvfile:
        filewriter = csv.writer(csvfile, delimiter=',',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
        filewriter.writerow(['Name', 'Title'])
        filewriter.writerow(['Joe', 'Team Lead'])
        filewriter.writerow(['Derek', 'Software Developer'])
        filewriter.writerow(['Steve', 'Software Developer'])
        filewriter.writerow(['Paul', 'Manager'])

# displaying the HTML template at the home url
@app.route('/')
def index():
   return render_template('index.html')

# Sending the file to the user
@app.route('/download')
def download():
   return render_template('download.html')

@app.route('/upload', methods = ['GET', 'POST'])
def uploadfile():
    return render_template('upload.html')

@app.route('/foo')
def foo():
    generate_csv()
    return send_file(file_path, as_attachment=True)

@app.route('/bar', methods = ['GET', 'POST'])
def bar():
   if request.method == 'POST': # check if the method is post
      f = request.files['file'] # get the file from the files object
      file_path = os.path.join(app.config['UPLOAD_FOLDER'] ,secure_filename(f.filename))
      f.save(file_path)
      if os.path.exists(file_path):
          msg = "UPLOAD SUCCESS"
      else:
          msg = "UPLOAD FAILURE"
      return f'{msg}' # Display message after uploading

if __name__ == '__main__':
   app.run() # running the flask app
