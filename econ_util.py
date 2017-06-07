import os
import re
import subprocess

def util_prepare_nodes():
	rootNode = prepare_rootNode()
	util_get_pdf_dir()
	util_get_txt_dir()
	util_get_html_dir()
	util_get_parsed_dir()
	present_dirs = [util_get_save_data_dir()+ dir for dir in  get_immediate_subdirectories(util_get_save_data_dir())]
	print present_dirs
	for dir in present_dirs:
		parentName = dir.split('/')[-1]
		print 'iterating present_dirs'
		print parentName
		parentNode = get_jstree_template(parentName, False)
		print parentNode
		sub_dirs = get_immediate_subdirectories(dir)
		if len(sub_dirs) > 0:
			childNode = prepare_subdirs_node(dir, sub_dirs)
			parentNode['children'].append(childNode)
			print childNode
		else:
			fileArray = [dir + f for f in os.listdir(dir)]
			childNode = get_children_Node(fileArray)
			parentNode['children'].append(childNode)
			print childNode
		rootNode['children'].append(parentNode)
	return rootNode
			
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
