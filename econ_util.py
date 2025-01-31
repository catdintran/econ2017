import os
import re
import subprocess
import zipfile
import json
from werkzeug import secure_filename
from itertools import islice

def global_countryCodes():
	global countryCodes
        with open(util_get_countryCodes(), 'rb') as json_data:
             countryCodes = json.load(json_data)

def util_process_idList(fileList):
	# clean tmp/ b4 moving files to folder
	subprocess.call('rm -rf', shell=True)
	# mv requested files to tmp/
	for file in fileList:
		subprocess.call('mv ' + file + ' ' + util_get_tmp_dir(), shell=True)
	fileZip = zipfile.ZipFile(util_get_tmp_dir()+'file.zip', 'w')
	zipdir(util_get_tmp_dir(), fileZip)

def util_process_pdf_file(pdfPath):
	'''
	1/save pdf file to correct folder
	2/xpdf to txt to txt/
	3/extract countryName--year to use as new folder name
	4/process xpdf to html
	5/extract pageNum and save new files to parsed/
	'''
	(path, pdfname) = os.path.split(pdfPath)
	newfileName = extract_countryName_year(pdfPath)	
	
	# change pdf filename to newfilename
	newpdfPath = util_get_pdf_dir()+newfileName.replace('.txt','.pdf')
	subprocess.call('mv ' + pdfPath + ' ' + newpdfPath, shell=True)
	# process pdf file to html/ and parsed/
	process_pdftohtml(newpdfPath)
	
def process_pdftohtml(pdfPath):
	filename = pdfPath.split('/')[-1].replace('.pdf', '')
	filename = filename.replace('.txt', '')
	output = util_get_html_dir() + filename
	
	# convert pdf to html folder
	subprocess.call(util_xpdftohtml() + ' ' + pdfPath + ' ' + output, shell=True)
	# get *.html from new input file and process with page matching fileName
	htmlList = [f for f in os.listdir(output) if '.html' in f]
	for html in htmlList:
		parse_page_number(output + '/' + html)

def parse_page_number(htmlPath):
	folderName = htmlPath.split('/')[-2]	
	output = util_get_parsed_dir() + 'parsed_'+folderName 
	pageNum = extract_page_number(htmlPath)
	print 'processed %s' % htmlPath
	print 'pageNum = %s' % pageNum
	# create a folder inside parsed/ to store new set of html files
	check_if_not_exist(output)
	# copy from html/ to parsed/ with new page file name
	subprocess.call('cp ' + htmlPath + ' ' + output+'/'+'%s_parsed_page%s.html'%(folderName,pageNum), shell=True)
	
def extract_page_number(htmlPath):
	'''
	pageNum is stored in last 3 lines in html file
	reversed open file to read from bottom
	using islice to get last 3 lines for memory optimization
	'''
	lines = islice(reversed(open(htmlPath, 'rb').readlines()), 1,3)
	for l in lines:		
             	num = re.findall('color:#000000;">(\d+ ?)</span>', l)            	
		if num:		
     			return num[0].split()[0]
	     	else:
			continue
	return ''
	
def extract_countryName_year(pdfPath):
	filename = pdfPath.split('/')[-1].replace('.pdf', '')
	print 'Start extracting countryName for pdfFile %s' % filename
	
	# load the json file which contains {'code' : 'countryNameYear'}
	global_countryCodes()
	
	# the upload fileName is code and use it to get value from countryCodes
	if filename in countryCodes:
		print '%s is in countryCodes' % filename
		print 'getting countryName from countryCodes'
		newFileName = countryCodes[filename]
		# remove special characters in filename
		newFileName = secure_filename(newFileName)
		print 'After extracting from countryCodes, newFileName will be %s' % newFileName

	
		# convert pdf to text file using the extracted countryName as fileName
		output = util_get_txt_dir() + newFileName
		print util_xpdftotext() + ' ' + pdfPath + ' ' + output
		subprocess.call(util_xpdftotext() + ' ' + pdfPath + ' ' + output, shell=True)
		return newFileName
	else:
		print 'failed extracting from countryCodes proceed to algo extracting'
		# save pdf to txt file for extracting
		output = util_get_txt_dir() + filename
		
		subprocess.call(util_xpdftotext() + ' ' + pdfPath + ' ' + output, shell=True)
				
		with open(output, 'rb') as fp:
			lp = fp.readlines()
			fileName = ''
			docDate = ''
			for i, line in enumerate(lp):
				print 'iterate over line#:%s' % str(i)
				print line
				if i == 0:
					# print(line.replace('\n', ''))
					print 'getting docDate'
					print line
					docDate = line.replace('\n', '')
				if i in range(2, 4):
					print 'gettiing countryName'
					print line
				if i in range(2, 4) and 'IMF' not in line:
					# make sure line is not an empty line
					if line.strip():
						line = line.replace('\n', '').replace('\'S', '').replace('\xad', '')
						#line = line.replace('\'S', '')
						#line = line.replace('\xad', '')
						print 'gettiing countryName'
						print line
						fileName = line + '--' + docDate
						fileName = fileName.replace(' ', '_') + '.txt'
				if i > 4:
					break
		if fileName:			
			print 'After extracting countryName, filename will become %s' % fileName		
		else:
			fileName = extract_countryName_year_2nd(output)
			
			
		# change txt file to newfilename
		fileName = secure_filename(fileName)
		subprocess.call('mv ' + output + ' ' + util_get_txt_dir()+fileName, shell=True)			
		
		return fileName
	
def extract_countryName_year_2nd(txtFile):
	'''
	Due to different format of some pdf files
	2nd attempt to extract country--year from txt file.
	Will add 3rd, 4th .... if necessary
	'''
	print 'Starting extract_countryName_year 2nd try'
	with open(txtFile, 'rb') as f:
		lines = f.readlines()
		fileName = ''
		countryName = ''
		for i, l in enumerate(lines):
			if 0 < i < 20:
			#	country_year = re.findall( r'^(.*): (\d{4}) .*', str(l))
				country_year = re.findall( r'^(.*): (.*) ', str(l))
				if country_year:
					print 'Found match in the follwing line:'
					print l
					text = str(l).split(':')
					countryName = text[0].replace(' ', '_')
        				year = re.findall(r' (\d{4}) ', text[1])
					if year:
						fileName = countryName + '--' + year[0]					
					break
	if fileName:
		print 'After extracting countryName, filename will become %s' % fileName
		return fileName
	else:
		return extract_countryName_year_3rd(txtFile, countryName)
	
def extract_countryName_year_3rd(txtFile, foundCountryName):
	'''
	Due to different format of some pdf files
	3rd attempt to extract country--year from txt file.
	Will add 3rd, 4th .... if necessary
	'''
	print 'Starting extract_countryName_year 3rd try'
	with open(txtFile, 'rb') as f:
		lines = f.readlines()
		fileName = ''
		for i, l in enumerate(lines):
			if 0 < i < 10:		
				found = re.search(r'\d{4} Article IV Consultation', str(l))
				if found:
					text = str(l)
					countryName = re.split(r'\d{4}', text)[0].strip().replace(' ', '_').upper()
					year = re.findall(r'\d{4}', text)[0]
					if year:
						fileName = countryName+ '--' + year
					else:	
						fileName = countryName
					break					
	if fileName:
		print 'After extracting countryName, filename will become %s' % fileName
		return fileName
	else:
		fileName = foundCountryName
		return fileName
		#raise Exception('Encounter a different format, need to revise extracting algo')
	
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
	# sort folders/files in natural sorted format 
	allFiles = sorted(os.listdir(parentPath), key=natural_keys)
		
	for file in allFiles:
		filePath = parentPath+'/'+file
		if os.path.isdir(filePath):
			parentNode = get_jstree_template(file, False)
			parentNode['icon'] = "static/folder_icon.png"
			get_all_dir_and_file(parentNode, filePath)
			rootNode['children'].append(parentNode)
		if os.path.isfile(filePath):
			node = get_jstree_template(file, False)			
			node['id'] = filePath		
			node['icon'] = "static/file_icon.png"
			rootNode['children'].append(node)
#	print rootNode
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

def util_get_countryCodes():
	return '/home/catdt_datascience/app/countryCodes.json'

def get_immediate_subdirectories(a_dir):
    return [name for name in os.listdir(a_dir)
            if os.path.isdir(os.path.join(a_dir, name))]

def check_if_not_exist(directory):
	if not os.path.exists(directory):
                os.makedirs(directory)
	return directory

def atoi(text):
    	return int(text) if text.isdigit() else text

def natural_keys(text):
    	'''
    	alist.sort(key=natural_keys) sorts in human order
    	http://nedbatchelder.com/blog/200712/human_sorting.html
    	(See Toothy's implementation in the comments)
    	'''
	return [ atoi(c) for c in re.split('(\d+)', text) ]

def zipdir(path, zip):
    path = os.path.abspath(path)
    for root, dirs, files in os.walk(path):
        dest_dir = root.replace(os.path.dirname(path), '', 1)
        for file in files:
		if '.zip' not in file:
            		zip.write(os.path.join(root, file), arcname=os.path.join(dest_dir, file))
	
