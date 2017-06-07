import os
import re
import subprocess

def util_process_pdf_file(pdfPath):
	(path, pdfname) = os.path.split(pdfPath)
	originPath, newfileName = extract_countryName_year(pdfPath)
	subprocess.call('mv ' + originPath + ' ' + util_get_txt_dir()+newfileName, shell=True)

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
			get_all_dir_and_file(parentNode, filePath)
			rootNode['children'].append(parentNode)
		if os.path.isfile(filePath):
			print file +' is a file'
			node = get_jstree_template(file, False)
			node['id'] = filePath			
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
		"icon" : "static/folder_icon.png",
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
