from flask import Flask, render_template, request
from werkzeug import secure_filename
from econ_util import *

app = Flask(__name__)



@app.route('/')
def index():
  return render_template('index.html')  

@app.route('/upload')
def upload():
  uploaded_files = request.files.getlist("file[]")
  print uploaded_files
  for f in uploaded_files:
    print type(f)
  return render_template('index.html') 

if __name__ == '__main__':
  app.run()


