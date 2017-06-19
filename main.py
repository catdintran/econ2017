from flask import Flask, render_template, request, jsonify, send_from_directory, send_file
from werkzeug import secure_filename
from econ_util import *
from nltk_econ import *
from random import randint
import ast
import os

app = Flask(__name__)



@app.route('/')
def index():
  v=randint(0,9999)
  sourceList = get_source_list()
  return render_template('index.html',version=v, sources=sourceList)  

@app.route('/upload', methods=['POST'])
def upload():
  uploaded_files = request.files.getlist("file[]")
  
  for f in uploaded_files:
    filename = secure_filename(f.filename) 

    f.save(util_get_pdf_dir() + filename)
    errorList = []
    try:
      util_process_pdf_file(util_get_pdf_dir() + filename)
    except Exception:
      errorList.append(filename)
  return render_template('index.html',version=randint(0,9999), sources=get_source_list(), pdfError=errorList) 

@app.route('/download', methods=['POST'])
def download():
    idList = request.form.get('idList').decode("utf-8").split(',')    
    print 'calling download'
    print 'calling download'
    print idList
    if len(idList) > 1:
      util_process_idList(idList)
      return send_from_directory(util_get_tmp_dir(), 'file.zip', as_attachment=True)
    else:      
      filePath, filename = os.path.split(idList[0])
      return send_from_directory(filePath, filename, as_attachment=True)
    
  
@app.route('/populate_jstree')
def populate_jstree():
  print 'calling /populate_jstree'
  rootNode = util_prepare_nodes()
  return jsonify(rootNode)
 
@app.route('/display_file', methods=['POST'])
def display_file():
  print 'calling /display_file'
  filePath = request.json['id']
  if '.pdf' in filePath:
     return 'Can Not View pdf at this moment.'
  else:
     return send_file(filePath)

def get_source_list():
  return [e.replace('.pdf', '') for e in os.listdir(util_get_pdf_dir())]

'''
  else:
    with open(filePath, 'r') as f:
      text = f.read().replace('\n', '')
    print text
    return text
'''

'''
@app.route('/nltk_textPreprocess', methods=['POST'])
def nltk_textPreprocess():
    
    filePath =  util_get_txt_dir() + request.json['id'] + '.txt'
    return jsonify(nltk_econ.textPreprocess(filePath))
'''   
if __name__ == '__main__':
  app.run()


