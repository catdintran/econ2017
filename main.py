from flask import Flask, render_template, request, jsonify
from werkzeug import secure_filename
from econ_util import *
from random import randint

app = Flask(__name__)



@app.route('/')
def index():
  v=randint(0,9)
  return render_template('index.html',version=v)  

@app.route('/upload', methods=['POST'])
def upload():
  uploaded_files = request.files.getlist("file[]")
  
  for f in uploaded_files:
    filename = secure_filename(f.filename)
    f.save(util_get_pdf_dir() + filename)
  return render_template('index.html',version=randint(0,9))  

@app.route('/populate_jstree')
def populate_jstree():
  print 'calling /populate_jstree'
  rootNode = util_prepare_nodes()
  return jsonify(rootNode)
  
if __name__ == '__main__':
  app.run()


