import os
import re
import subprocess
from itertools import islice

def util_process_pdf_file(pdfPath):
	(path, pdfname) = os.path.split(pdfPath)
	originPath, newfileName = extract_countryName_year(pdfPath)
	# change txt file to newfilename
	subprocess.call('mv ' + originPath + ' ' + util_get_txt_dir()+newfileName, shell=True)
	# change pdf filename to newfilename
	newpdfPath = util_get_pdf_dir()+newfileName
	subprocess.call('mv ' + pdfPath + ' ' + newpdfPath, shell=True)
	# process pdf file to html/ and parsed/
	process_pdftohtml(newpdfPath)
	
def process_pdftohtml(pdfPath):
	filename = pdfPath.split('/')[-1].replace('.txt', '')	
	output = util_get_html_dir() + filename
	
	# convert pdf to html folder
	subprocess.call(util_xpdftohtml() + ' ' + pdfPath + ' ' + output, shell=True)
	htmlList = [f for f in os.listdir(output) if '.html' in f]
	for html in htmlList:
		parse_page_number(output + '/' + html)

def parse_page_number(htmlPath):
	folderName = htmlPath.split('/')[-2]	
	output = util_get_parsed_dir() + folderName 
	pageNum = extract_page_number(htmlPath)
	subprocess.call('cp ' + htmlPath + ' ' + output+'/'+'%s_parsed_page%s.html'%(folderName,pageNum), shell=True)
	
def extract_page_number(htmlPath):
	#a = islice(reversed(open(f).readlines()), 1,3)
	lines = islice(reversed(open(htmlPath, 'rb').readlines()), 1,4)
	for l in lines:
             num = re.findall('color:#000000;">(\d+ ?)</span>', l)
             if num:
     		return num[0].split()
	     else:
		return ''     
	
def extract_countryName_year(pdfPath):
	filename = pdfPath.split('/')[-1].replace('.pdf', '')		
	output = util_get_txt_dir() + filename
	
	# convert pdf to text file
	subprocess.call(util_xpdftotext() + ' ' + pdfPath + ' ' + output, shell=True)
	
	with open(output, 'rb') as fp:
		lp = fp.readlines()
        	fileName = ''
        	docDate = ''
		for i, line in enumerate(lp):
			print 'iterate over txt file'
			print line
			if i == 0:
			   	# print(line.replace('\n', ''))
				docDate = line.replace('\n', '')
			if i in range(2, 4) and 'IMF' not in line:
              			# make sure line is not an empty line
                		if line.strip():
					line = line.replace('\n', '')
					line = line.replace('\'S', '')
					
                    			fileName = line + '--' + docDate
					fileName = fileName.replace(' ', '_') + '.txt'
            		if i > 4:
                		break
			print 'extracted fileName'
			print fileName
	return output, fileName
def util_prepare_nodes():
	rootNode = prepare_rootNode()
	util_get_pdf_dir()
	util_get_txt_dir()
	util_get_html_dir()
	util_get_parsed_dir()
	
	rootNode = get_all_dir_and_file(rootNode, util_get_save_data_dir())
	return rootNode

def get_all_dir_and_file(rootNode, parentPath):
	'''
	recursively pass rootNode and rootPath to param
	retrieve all dirs and files within rootPath to generate jstree node
	'''
#	(path, parentname) = os.path.split(parentPath) 
	print 'we are in %s now' % parentPath
	allFiles = os.listdir(parentPath)
	print 'get all files within %s' % parentPath
	print allFiles
	
	for file in allFiles:
		filePath = parentPath+'/'+file
   		print file
		if os.path.isdir(filePath):
			print file +' is a dir'			
			parentNode = get_jstree_template(file, False)
			parentNode['icon'] = "static/folder_icon.png"
			get_all_dir_and_file(parentNode, filePath)
			rootNode['children'].append(parentNode)
		if os.path.isfile(filePath):
			print file +' is a file'
			node = get_jstree_template(file, False)			
			node['id'] = filePath		
			node['icon'] = "static/file_icon.png"
			rootNode['children'].append(node)
	print rootNode
	return rootNode

def prepare_rootNode():
	rootNode = get_jstree_template("root", True)
	rootNode['icon'] = "//jstree.com/tree.png"
	return rootNode	

def get_jstree_template(rootName, stateBool):
	return {
		"id" : rootName,
              "text" : rootName,
              "state" : {"opened" : stateBool },
              "children" : []
	}

def util_xpdftohtml():
	return '/home/catdt_datascience/app/xpdfbin-linux-3.04/bin64/pdftohtml'
def util_xpdftotext():
	return '/home/catdt_datascience/app/xpdfbin-linux-3.04/bin64/pdftotext'

def util_get_home_dir():
	return '/home/catdt_datascience/app/'

def util_get_pdf_dir():
	directory=check_if_not_exist('/home/catdt_datascience/app/saved_data/pdf/')
	return directory

def util_get_html_dir():
	directory=check_if_not_exist('/home/catdt_datascience/app/saved_data/html/')
        return directory
        
def util_get_parsed_dir():
        directory=check_if_not_exist('/home/catdt_datascience/app/saved_data/parsed/')
        return directory
	
def util_get_txt_dir():
        directory=check_if_not_exist('/home/catdt_datascience/app/saved_data/txt/')        
        return directory
	
def util_get_tmp_dir():
        directory = check_if_not_exist('/home/catdt_datascience/app/saved_data/tmp/')
	return directory

def util_get_save_data_dir():
        directory = check_if_not_exist('/home/catdt_datascience/app/saved_data/')
	return directory
def get_immediate_subdirectories(a_dir):
    return [name for name in os.listdir(a_dir)
            if os.path.isdir(os.path.join(a_dir, name))]

def check_if_not_exist(directory):
	if not os.path.exists(directory):
                os.makedirs(directory)
	return directory
