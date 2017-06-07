import os
import re
import subprocess

def util_prepare_nodes():
	rootNode = prepare_rootNode()
	util_get_pdf_dir()
	util_get_txt_dir()
	util_get_html_dir()
	util_get_parsed_dir()
	
	rootNode = get_all_dir_and_file(rootNode, util_get_save_data_dir())
	return rootNode

def get_all_dir_and_file(rootNode, parentPath):
	(path, parentname) = os.path.split(parentPath) 
	print 'we are in %s now' % parentPath
	allFiles = os.listdir(parentPath)
	print 'get all files within saved_data'
	print allFiles
	
	for file in allFiles:
		filePath = parentPath+file
   		print file
		if os.path.isdir(filePath):
			print file +' is a dir'
			
			parentNode = get_jstree_template(file, False)
			get_all_dir_and_file(parentNode, filePath)
			rootNode['children'].append(parentNode)
		if os.path.isfile(filePath):
			print file +' is a file'
			node = get_jstree_template(file, False)
			node['id'] = parentPath+file
			rootNode['children'].append(node)
	print rootNode
	return rootNode
'''
def prepare_subdirs_node(path, sub_dirs):
	sub_dirs = [path+dir for dir in sub_dirs]
	nodeList = []
	for dir in sub_dirs:
		dirName = dir.split('/')[-1]
		fileArray = [dir + f for f in os.listdir(dir)]
		parentNode = get_jstree_template(dirName, False)
		parentNode['children'] = get_children_Node(fileArray)
		nodeList.append(parentNode)
	return nodeList
		
def get_children_Node(fileArray):
	nodeList = []
	for f in fileArray:
		(filepath, filename) = os.path.split(f)
		node = get_jstree_template(filename, False)
		node['id'] = f
		nodeList.append(node)
	return nodeList
'''
def prepare_rootNode():
	rootNode = get_jstree_template("root", True)
	rootNode['icon'] = "//jstree.com/tree.png"
	return rootNode	

def get_jstree_template(rootName, stateBool):
	return {
		"id" : rootName,
              "text" : rootName,
              "state" : {"opened" : stateBool },
		"icon" : "glyphicon glyphicon-flash",
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
