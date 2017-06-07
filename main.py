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
  return uploaded_files
@app.route('/populate_jstree')
def populate_jstree():
  rootNode = util_prepare_nodes()
  
  
if __name__ == '__main__':
  app.run()


