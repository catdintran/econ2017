from flask import Flask, render_template, request, jsonify
from werkzeug import secure_filename
from econ_util import *
from random import randint

app = Flask(__name__)



@app.route('/')
def index():
  v=randint(0,9)
  return render_template('index.html',version=v)  

@app.route('/upload')
def upload():
  uploaded_files = request.files.getlist("file[]")
  print uploaded_files
  for f in uploaded_files:
    print type(f)
  return uploaded_files

@app.route('/populate_jstree')
def populate_jstree():
  print 'calling /populate_jstree'
  rootNode = util_prepare_nodes()
  return jsonify(rootNode)
  
if __name__ == '__main__':
  app.run()


