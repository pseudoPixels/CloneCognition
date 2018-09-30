from app_code_clone import app_code_clone
from flask import render_template



from flask import Flask,render_template,jsonify, g, redirect, url_for, session
from io import StringIO
import sys
import subprocess
import tempfile
from flask import request
import os
import uuid



import xml.etree.ElementTree as ET
#import BeautifulSoup

#for couch db...
from couchdb.design import ViewDefinition
from flaskext.couchdb import CouchDBManager




views_by_txl_user = ViewDefinition('hello', 'findEmailAndDocID', '''
	function (doc) {
		if (doc.the_doc_type == 'txl_user') {
			emit(doc.user_email, doc._id)
		};
	}
	''')




views_by_txl_project_authors = ViewDefinition('hello', 'findTXLProjectAuthors', '''
	function (doc) {
		if (doc.the_doc_type == 'txl_project') {
			emit(doc.author, doc._id)
		};
	}
	''')


views_by_txl_project_shared_members = ViewDefinition('hello', 'findTXLProjectSharedMembers', '''
	function (doc) {
		if (doc.the_doc_type == 'txl_project') {
			emit(doc.shared_with, doc._id)
		};
	}
	''')

views_by_app_code_clone_user = ViewDefinition('hello', 'appCodeClonefindEmailAndDocID', '''
	function (doc) {
		if (doc.the_doc_type == 'app_code_clone_user') {
			emit(doc.user_email, doc._id)
		};
	}
	''')



from flask import current_app as app


app = Flask(__name__)
app.config.update(
    COUCHDB_SERVER='http://localhost:5984',
    COUCHDB_DATABASE='plantphenotype',
	MAX_CONTENT_LENGTH=30000000
)

manager = CouchDBManager()
with app.app_context():
	manager.setup(app)
	#manager.add_viewdef([views_by_txl_user, views_by_txl_project_authors, views_by_txl_project_shared_members])
	manager.add_viewdef([views_by_app_code_clone_user])
	manager.sync(app)





import glob




from flaskext.couchdb import Document, TextField, FloatField, DictField, Mapping, ListField
from datetime import datetime

@app_code_clone.route('/cloneCognition')
def cloneCognition():

	return render_template('index_cloneValidationFramework.html')



@app_code_clone.route('/app_code_clone_request_user_access')
def app_code_clone_request_user_access():
	return render_template('app_code_clone_request_user_access.html')




@app_code_clone.route('/app_code_clone_process_user_access_request', methods=['POST'])
def app_code_clone_process_user_access_request():
	user_email = request.form['code_clone_reg_email']
	user_name = request.form['code_clone_reg_name']
	user_password = request.form['code_clone_reg_password']


	row = (views_by_app_code_clone_user(g.couch))[user_email]


	if not row:
		new_code_clone_user = AppCodeClone_User()
		new_code_clone_user.user_email = user_email
		new_code_clone_user.user_password = user_password
		new_code_clone_user.user_full_name = user_name
		new_code_clone_user.store()

		projectRoot = 'app_code_clone/user_projects/'
		os.makedirs(projectRoot + user_email)
		return jsonify({'response_code': 'OK'})
	else:
		return jsonify({'response_code': 'USER_ALREADY_EXISTS'})







@app_code_clone.route('/app_code_clone_login')
def app_code_clone_login():
	return render_template('app_code_clone_login.html')






@app_code_clone.route('/app_code_clone_varify_user', methods=['POST'])
def app_code_clone_varify_user():
	# get user credentials
	app_code_clone_login_email = request.form['app_code_clone_login_email']
	app_code_clone_login_password = request.form['app_code_clone_login_password']
	# return redirect(url_for('myProjects'))

	row = (views_by_app_code_clone_user(g.couch))[app_code_clone_login_email]

	this_app_code_clone_user = ''
	if not row:
		return redirect(url_for('app_code_clone.app_code_clone_login'))
	else:
		this_app_code_clone_user = AppCodeClone_User.load(list(row)[0].value)

	if this_app_code_clone_user.user_email != app_code_clone_login_email or this_app_code_clone_user.user_password != app_code_clone_login_password:
		return redirect(url_for('app_code_clone.app_code_clone_login'))
	else:
		# first_name = p2irc_user.first_name
		# last_name = p2irc_user.last_name
		# email = p2irc_user.email
		session['app_code_clone_user_email'] = this_app_code_clone_user.user_email
		return redirect(url_for('app_code_clone.machine_learning_validation'))

	#return render_template('app_code_clone_login.html')
















class AppCodeClone_User(Document):
	user_email = TextField()
	user_password = TextField()
	user_full_name = TextField()
	the_doc_type = TextField(default='app_code_clone_user')











@app_code_clone.route('/manual_validation')
def manual_validation():

	thisUser = 'golammostaeen@gmail.com'
	projectRoot = 'app_code_clone/user_projects/'

	#list_of_file_for_validation = os.listdir(projectRoot + thisUser + '/' )
	list_of_file_for_validation = [os.path.basename(x) for x in glob.glob(projectRoot + thisUser + '/' + '*.xml')]


	return render_template('manual_validation.html', list_of_file_for_validation = list_of_file_for_validation)







@app_code_clone.route('/machine_learning_validation')
def machine_learning_validation():

	thisUser = 'golammostaeen@gmail.com'
	projectRoot = 'app_code_clone/user_projects/'

	#list_of_file_for_validation = os.listdir(projectRoot + thisUser + '/' )
	list_of_file_for_validation = [os.path.basename(x) for x in glob.glob(projectRoot + thisUser + '/' + '*.xml')]

	list_of_validated_clone_files = [os.path.basename(x) for x in glob.glob(projectRoot + thisUser + '/' + '*.mlValidated')]


	return render_template('machine_learning_validation.html', list_of_file_for_validation = list_of_file_for_validation, list_of_validated_clone_files=list_of_validated_clone_files)






@app_code_clone.route('/ml_auto_validate_clone_file', methods=['POST'])
def ml_auto_validate_clone_file():

	projectRoot = 'app_code_clone/user_projects/'
	thisUser = request.form['theUser']
	theCloneFile = request.form['theCloneFile']
	validationThreshold = 0.5

	mlValidation_output_file = theCloneFile+'.mlValidated'



	tree2 = ET.parse(projectRoot+thisUser+'/'+theCloneFile)
	root = tree2.getroot()
	totalClonePairs = len(root)

	mlValidationCount = 0

	if os.path.exists(projectRoot+thisUser+'/'+mlValidation_output_file) == True:
		#response_code = 'FILE_ALREADY_EXIST'
		mlValidationCount = sum(1 for line in open(projectRoot+thisUser+'/'+mlValidation_output_file))
	else:
		new_file = open(projectRoot+thisUser+'/'+mlValidation_output_file, "w")
		new_file.close()


	for aCloneIndex in range(mlValidationCount, totalClonePairs):
		fragment_1_path, fragment_1_startline, fragment_1_endline, fragment_1_clone, fragment_2_path, fragment_2_startline, fragment_2_endline, fragment_2_clone, clones_validated, total_clones = get_next_clone_pair_for_validation(
			thisUser, theCloneFile, '.mlValidated')


		true_probability = app_code_clone_getValidationScore(fragment_1_clone, fragment_2_clone, 'java')

		with open(projectRoot+thisUser+'/'+mlValidation_output_file, "a") as validationFile:
			if true_probability >=validationThreshold:
				validationFile.write('true' + ',' + fragment_1_path +','+ fragment_1_startline +','+ fragment_1_endline+','+fragment_2_path+','+fragment_2_startline+','+fragment_2_endline + '\n')
			else:
				validationFile.write(
					'false' + ',' + fragment_1_path + ',' + fragment_1_startline + ',' + fragment_1_endline + ',' + fragment_2_path + ',' + fragment_2_startline + ',' + fragment_2_endline + '\n')



	return jsonify({'status': 'Done'})


	#list_of_file_for_validation = os.listdir(projectRoot + thisUser + '/' )
	#list_of_file_for_validation = [os.path.basename(x) for x in glob.glob(projectRoot + thisUser + '/' + '*.xml')]


	#return render_template('machine_learning_validation.html', list_of_file_for_validation = list_of_file_for_validation)






@app_code_clone.route('/get_clone_validation_statistics', methods=['POST'])
def get_clone_validation_statistics():

	projectRoot = 'app_code_clone/user_projects/'
	thisUser = request.form['theUser']
	theCloneFile = request.form['theCloneFile']
	validationFileType = request.form['validationFileType']

	mlValidation_output_file = theCloneFile + validationFileType

	with open(projectRoot + thisUser + '/' + mlValidation_output_file, "r") as validationFile:
		validationResponseLines = validationFile.readlines()

	totalClones = len(validationResponseLines)
	trueCount = 0

	for aValidationLine in validationResponseLines:
		aResponse = aValidationLine.split(',')[0]
		if aResponse=='true':
			trueCount = trueCount + 1



	return jsonify({'trueClones': trueCount, 'totalClonePairs': totalClones})








@app_code_clone.route('/srv_get_next_clone_pair_for_validation', methods=['POST'])
def srv_get_next_clone_pair_for_validation():
	# getting the example program name

	projectRoot = 'app_code_clone/user_projects/'
	thisUser = request.form['theUser']
	theCloneFile = request.form['theCloneFile']
	#theValidationFile = theCloneFile + '.validated'

	# tree2 = ET.parse(projectRoot+thisUser+'/'+theCloneFile)
	# root = tree2.getroot()
    #
	# nextCloneIndex = 0
    #
	# if os.path.exists(projectRoot+thisUser+'/'+theValidationFile) == True:
	# 	#response_code = 'FILE_ALREADY_EXIST'
	# 	nextCloneIndex = sum(1 for line in open(projectRoot+thisUser+'/'+theValidationFile))
	# else:
	# 	new_file = open(projectRoot+thisUser+'/'+theValidationFile, "w")
	# 	new_file.close()
    #
    #
    #
	fragment_1_path, fragment_1_startline, fragment_1_endline, fragment_1_clone, fragment_2_path, fragment_2_startline, fragment_2_endline, fragment_2_clone, clones_validated, total_clones  = get_next_clone_pair_for_validation(
		thisUser, theCloneFile)


	# soup = ''
	# with open(projectRoot+thisUser+'/'+theCloneFile) as fp:
	# 	soup = BeautifulSoup(fp, 'lxml')
    #
    #
	# clones = soup.find_all('clone')





	return jsonify({'fragment_1_path': fragment_1_path,
					'fragment_1_startline': fragment_1_startline,
					'fragment_1_endline':fragment_1_endline,
				    'fragment_1_clone':fragment_1_clone,

					'fragment_2_path': fragment_2_path,
					'fragment_2_startline': fragment_2_startline,
					'fragment_2_endline': fragment_2_endline,
					'fragment_2_clone': fragment_2_clone,

					'clones_validated': clones_validated,
					'total_clones': total_clones
					})




def saveManualValidationResponse(theUser, theValidationFile, response, fragment_1_path, fragment_1_start_line, fragment_1_end_line, fragment_2_path, fragment_2_start_line, fragment_2_end_line):
	projectRoot = 'app_code_clone/user_projects/'

	with open(projectRoot+theUser+'/'+theValidationFile, "a") as validationFile:
		validationFile.write(response + ',' + fragment_1_path +','+ fragment_1_start_line +','+ fragment_1_end_line+','+fragment_2_path+','+fragment_2_start_line+','+fragment_2_end_line + '\n')








def get_next_clone_pair_for_validation(theUser, cloneFile, validationFileExt='.validated'):
	# getting the example program name

	projectRoot = 'app_code_clone/user_projects/'
	thisUser = theUser
	theCloneFile = cloneFile
	theValidationFile = theCloneFile + validationFileExt

	tree2 = ET.parse(projectRoot+thisUser+'/'+theCloneFile)
	root = tree2.getroot()

	nextCloneIndex = 0

	if os.path.exists(projectRoot+thisUser+'/'+theValidationFile) == True:
		#response_code = 'FILE_ALREADY_EXIST'
		nextCloneIndex = sum(1 for line in open(projectRoot+thisUser+'/'+theValidationFile))
	else:
		new_file = open(projectRoot+thisUser+'/'+theValidationFile, "w")
		new_file.close()

	#fragment_1_path, fragment_1_startline, fragment_1_endline, fragment_1_clone, fragment_2_path, fragment_2_startline, fragment_2_endline, fragment_2_clone, number_of_validated_clones, total_clones
	return root[nextCloneIndex][0].attrib['file'], root[nextCloneIndex][0].attrib['startline'], root[nextCloneIndex][0].attrib['endline'], root[nextCloneIndex][1].text, root[nextCloneIndex][2].attrib['file'], root[nextCloneIndex][2].attrib['startline'], root[nextCloneIndex][2].attrib['endline'],root[nextCloneIndex][3].text, nextCloneIndex+1, len(root)
	#return 	root[nextCloneIndex][1].text, root[nextCloneIndex][3].text












@app_code_clone.route('/save_manual_clone_validation_res_and_get_new_clone_pair', methods=['POST'])
def save_manual_clone_validation_res_and_get_new_clone_pair():

	thisUser = request.form['theUser']
	theCloneFile= request.form['theCloneFile']
	manual_validation_response= request.form['manual_validation_response']

	fragment_1_path= request.form['fragment_1_path']
	fragment_1_start_line= request.form['fragment_1_start_line']
	fragment_1_end_line= request.form['fragment_1_end_line']

	fragment_2_path= request.form['fragment_2_path']
	fragment_2_start_line= request.form['fragment_2_start_line']
	fragment_2_end_line= request.form['fragment_2_end_line']






	# getting the example program name
	#manual_validation_response = 'true'



	theValidationFile = theCloneFile + '.validated'



	saveManualValidationResponse(thisUser, theValidationFile, manual_validation_response, fragment_1_path, fragment_1_start_line, fragment_1_end_line, fragment_2_path, fragment_2_start_line, fragment_2_end_line)

	fragment_1_path, fragment_1_startline, fragment_1_endline, fragment_1_clone, fragment_2_path, fragment_2_startline, fragment_2_endline, fragment_2_clone, clones_validated, total_clones = get_next_clone_pair_for_validation(thisUser, theCloneFile)


	#
	#
	#
	#
    #
	# tree2 = ET.parse(projectRoot+thisUser+'/'+theCloneFile)
	# root = tree2.getroot()
    #
	# nextCloneIndex = 0
    #
	# if os.path.exists(projectRoot+thisUser+'/'+theValidationFile) == True:
	# 	#response_code = 'FILE_ALREADY_EXIST'
	# 	nextCloneIndex = sum(1 for line in open(projectRoot+thisUser+'/'+theValidationFile))
	# else:
	# 	new_file = open(projectRoot+thisUser+'/'+theValidationFile, "w")
	# 	new_file.close()





	# soup = ''
	# with open(projectRoot+thisUser+'/'+theCloneFile) as fp:
	# 	soup = BeautifulSoup(fp, 'lxml')
    #
    #
	# clones = soup.find_all('clone')





	# txl_source = str(txl_source, 'utf-8')
	return jsonify({'fragment_1_path': fragment_1_path,
					'fragment_1_startline': fragment_1_startline,
					'fragment_1_endline':fragment_1_endline,
				    'fragment_1_clone':fragment_1_clone,

					'fragment_2_path': fragment_2_path,
					'fragment_2_startline': fragment_2_startline,
					'fragment_2_endline': fragment_2_endline,
					'fragment_2_clone': fragment_2_clone,

					'clones_validated': clones_validated,
					'total_clones': total_clones
					})








from flask import  request
from werkzeug import secure_filename

@app_code_clone.route('/upload_new_clone_file', methods = ['GET', 'POST'])
def upload_new_clone_file():
	file = request.files['file']
	projectDir = request.form['userID']
	file.save(os.path.join('app_code_clone/user_projects/'+projectDir, secure_filename(file.filename)))
	return "Ajax file upload success"

















@app_code_clone.route('/txln', methods=['POST'])
def txln():
	# getting the txl and the input file to parse
	txl_source = request.form['txl_source']
	input_to_parse = request.form['input_to_parse']

	# generate a unique random file name for preventing conflicts
	fileName = str(uuid.uuid4())
	txl_source_file = 'app_txl_cloud/txl_tmp_file_dir/' + fileName + '.txl'

	fileName = str(uuid.uuid4())
	input_to_parse_file = 'app_txl_cloud/txl_tmp_file_dir/' + fileName + '.txt'

	# write submitted txl and input to corresponding files
	with open(txl_source_file, "w") as fo:
		fo.write(txl_source)

	with open(input_to_parse_file, "w") as fo:
		fo.write(input_to_parse)

	# parsing
	p = subprocess.Popen(['/usr/local/bin/txl', '-Dapply', txl_source_file, input_to_parse_file], stdout=subprocess.PIPE,
						 stderr=subprocess.PIPE)
	# p = subprocess.Popen(['ls'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	out, err = p.communicate()

	# once done remove the file
	#os.remove(txl_source_file)
	#os.remove(input_to_parse_file)

	# preparing the log file for better readabilty...
	# err = err.replace('\n','<br>') #add new line for html
	err = str(err,'utf-8')
	out = str(out,'utf-8')
	err = err.replace(txl_source_file, 'YOUR_TXL_FILE')
	err = err.replace(input_to_parse_file, 'YOUR_INPUT_FILE')

	return jsonify({'txl_log': err, 'txl_output': out})










@app_code_clone.route('/load_example_txl_programn', methods=['POST'])
def load_example_txl_programn():
	# getting the example program name
	example_name = request.form['txl_example_program_name']

	txl_example_program_dir = 'app_txl_cloud/txl_sources/examples/'

	file_location = txl_example_program_dir + example_name + '/' + example_name

	txl_source = ''
	with open(file_location + '.txl', 'r') as f:
		for line in f:
			txl_source = txl_source + line

	input_to_parse = ''
	with open(file_location + '.txt', 'r') as f:
		for line in f:
			input_to_parse = input_to_parse + line

	# txl_source = str(txl_source, 'utf-8')
	return jsonify({'example_txl_source': txl_source, 'input_to_parse': input_to_parse})















########################################################################################################################
########################################################################################################################
########################################################################################################################
#############################  MACHINE LEARNING MODEL ##################################################################
########################################################################################################################
########################################################################################################################
########################################################################################################################


import pickle
import pybrain


def app_code_clone_getValidationScore(sourceCode1,sourceCode2,lang='java' ):


	#load the trained Neural Net
	fileObject = open('/home/ubuntu/Webpage/pybrain/trainedNetwork', 'rb')
	loaded_fnn = pickle.load(fileObject, encoding='latin1')

	type1sim_by_line, type2sim_by_line, type3sim_by_line = app_code_clone_similaritiesNormalizedByLine(sourceCode1,sourceCode2,lang)
	type1sim_by_token, type2sim_by_token, type3sim_by_token = app_code_clone_similaritiesNormalizedByToken(sourceCode1,sourceCode2,lang)


	#type2sim_by_line, type2sim_by_line, type3sim_by_line, type1sim_by_token, type2sim_by_token, type3sim_by_token
	#network_prediction = loaded_fnn.activate([0.2,0.5,0.6,0.1,0.3,0.7])
	network_prediction = loaded_fnn.activate([type2sim_by_line, type2sim_by_line, type3sim_by_line, type1sim_by_token, type2sim_by_token, type3sim_by_token])

	#out = {'false_clone_probability_score':network_prediction[0], 'true_clone_probability_score':network_prediction[1]}


	#return jsonify({'error_msg': 'None', 'log_msg': 'Preprocessing Source Codes...\nNormalizing Source Codes...\nCalculating Similarities...\nDone.','output': out})

	#true_clone_probability_score
	return network_prediction[1]


def app_code_clone_execTxl(txlFilePath, sourceCode, lang, saveOutputFile=False):
	# get an unique file name for storing the code temporarily
	fileName = str(uuid.uuid4())
	sourceFile = '/home/ubuntu/Webpage/txl_tmp_file_dir/' + fileName + '.txt'

	# write submitted source code to corresponding files
	with open(sourceFile, "w") as fo:
		fo.write(sourceCode)

	# get the required txl file for feature extraction
	# txlPath = '/home/ubuntu/Webpage/txl_features/txl_features/java/PrettyPrint.txl'

	# do the feature extraction by txl
	p = subprocess.Popen(['/usr/local/bin/txl', '-Dapply', txlFilePath, sourceFile], stdout=subprocess.PIPE,
						 stderr=subprocess.PIPE)
	out, err = p.communicate()

	# convert to utf-8 format for easier readibility
	out = str(out, 'utf-8')
	err = str(err, 'utf-8')

	err = err.replace(sourceFile, 'YOUR_SOURCE_FILE')
	err = err.replace(txlFilePath, 'REQUIRED_TXL_FILE')

	# once done remove the temp file
	os.remove(sourceFile)

	if saveOutputFile == False:
		return out, err
	else:
		outputFileLocation = str(uuid.uuid4())
		outputFileLocation = '/home/ubuntu/Webpage/txl_tmp_file_dir/' + outputFileLocation + '.txt'
		with open(outputFileLocation, "w") as fo:
			fo.write(out)

		return outputFileLocation, out, err







def app_code_clone_getCodeCloneSimilarity(sourceCode1, sourceCode2, lang, txlFilePath):
	saveOutputFile = True
	outputFileLocation1, out1, err1 = app_code_clone_execTxl(txlFilePath, sourceCode1, lang, saveOutputFile)
	outputFileLocation2, out2, err2 = app_code_clone_execTxl(txlFilePath, sourceCode2, lang, saveOutputFile)

	p = subprocess.Popen(['/usr/bin/java', '-jar', '/home/ubuntu/Webpage/txl_tmp_file_dir/calculateCloneSimilarity.jar',
						  outputFileLocation1, outputFileLocation2], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	similarityValue, err = p.communicate()

	similarityValue = str(similarityValue, 'utf-8')
	similarityValue = similarityValue.replace('\n', '')
	err = str(err, 'utf-8')

	# once done remove the temp files
	os.remove(outputFileLocation1)
	os.remove(outputFileLocation2)

	return similarityValue



def app_code_clone_similaritiesNormalizedByLine(sourceCode1, sourceCode2, lang):
	# getting the txl and the input file to parse
	# sourceCode1 = request.form['sourceCode_1']
	# sourceCode2 = request.form['sourceCode_2']
	# lang = request.form['lang']

	txlFilePath = '/home/ubuntu/Webpage/txl_features/txl_features/java/PrettyPrint.txl'
	type1sim_by_line = app_code_clone_getCodeCloneSimilarity(sourceCode1, sourceCode2, lang, txlFilePath)

	txlFilePath = '/home/ubuntu/Webpage/txl_features/txl_features/java/normalizeLiteralsToDefault.txl'
	type2sim_by_line = app_code_clone_getCodeCloneSimilarity(sourceCode1, sourceCode2, lang, txlFilePath)

	txlFilePath = '/home/ubuntu/Webpage/txl_features/txl_features/java/normalizeLiteralsToZero.txl'
	type3sim_by_line = app_code_clone_getCodeCloneSimilarity(sourceCode1, sourceCode2, lang, txlFilePath)

	#out = {'type_1_similarity_by_line': type1sim_by_line, 'type_2_similarity_by_line': type2sim_by_line,
	#	   'type_3_similarity_by_line': type3sim_by_line}

	#return jsonify({'error_msg': 'None',
	#				'log_msg': 'Preprocessing Source Codes...\nNormalizing Source Codes...\nCalculating Similarities...\nDone.',
	#				'output': out})

	return type1sim_by_line, type2sim_by_line, type3sim_by_line



def app_code_clone_similaritiesNormalizedByToken(sourceCode1, sourceCode2, lang):
	# getting the txl and the input file to parse
	# sourceCode1 = request.form['sourceCode_1']
	# sourceCode2 = request.form['sourceCode_2']
	# lang = request.form['lang']

	txlFilePath = '/home/ubuntu/Webpage/txl_features/txl_features/java/consistentRenameIdentifiers.txl'
	type1sim_by_token = app_code_clone_getCodeCloneSimilarity(sourceCode1, sourceCode2, lang, txlFilePath)

	txlFilePath = '/home/ubuntu/Webpage/txl_features/txl_features/java/normalizeLiteralsToZero.txl'
	type2sim_by_token = app_code_clone_getCodeCloneSimilarity(sourceCode1, sourceCode2, lang, txlFilePath)

	txlFilePath = '/home/ubuntu/Webpage/txl_features/txl_features/java/normalizeLiteralsToZero.txl'
	type3sim_by_token = app_code_clone_getCodeCloneSimilarity(sourceCode1, sourceCode2, lang, txlFilePath)

	# out = {'type_1_similarity_by_token': type1sim_by_token, 'type_2_similarity_by_token': type2sim_by_token,
	# 	   'type_3_similarity_by_token': type3sim_by_token}
    #
	# return jsonify({'error_msg': 'None',
	# 				'log_msg': 'Preprocessing Source Codes...\nNormalizing Source Codes...\nCalculating Similarities...\nDone.',
	# 				'output': out})

	return type1sim_by_token, type2sim_by_token, type3sim_by_token



























@app_code_clone.route('/cloneviz')
def cloneViz():

	thisUser = 'golammostaeen@gmail.com'
	projectRoot = 'app_code_clone/user_projects/'



	list_of_validated_clone_files = [os.path.basename(x) for x in glob.glob(projectRoot + thisUser + '/' + '*.mlValidated')]
	list_of_viz_plugins = os.listdir(projectRoot + thisUser + '/vizPlugins')
	list_of_viz_outputs = [os.path.basename(x) for x in glob.glob(projectRoot + thisUser + '/vizOutputs/' + '*.html')]


	return render_template('cloneviz.html', list_of_validated_clone_files=list_of_validated_clone_files, list_of_viz_plugins= list_of_viz_plugins, list_of_viz_outputs=list_of_viz_outputs)




def getModuleCodes(path):
	sourceCode = ''
	with open(path) as f:
		for line in f:
			sourceCode = sourceCode + line

	return sourceCode


@app_code_clone.route('/get_viz_plugin_details', methods=['POST'])
def get_viz_plugin_details():
	p_module_key = request.form['p_module_key']

	thisUser = 'golammostaeen@gmail.com'
	projectRoot = 'app_code_clone/user_projects/'


	# module = ''
	# for row in views_by_pipeline_module(g.couch):
	#	if row.key == p_module_key: #'rgb2gray'
	#		module = PipelineModule.load(row.value)

	# moduleSourceCode_main = getModuleCodes(module.code_link_main)
	# moduleSourceCode_settings = getModuleCodes(module.code_link_settings)
	# moduleSourceCode_html = getModuleCodes(module.code_link_html)


	modulesPath = projectRoot + thisUser + '/vizPlugins/'

	# moduleSourceCode_main = getModuleCodes(modulesPath+'biodatacleaning/biodatacleaning_main.py')
	# moduleSourceCode_settings = getModuleCodes(modulesPath+'biodatacleaning/biodatacleaning_settings.py')
	# moduleSourceCode_html = getModuleCodes(modulesPath+'biodatacleaning/biodatacleaning_html.txt')


	#moduleSourceCode_main = getModuleCodes(modulesPath + p_module_key + '/' + p_module_key + '_main.py')
	#moduleSourceCode_html = getModuleCodes(modulesPath + p_module_key + '/' + p_module_key + '_html.txt')


	moduleSourceCode_main = getModuleCodes(modulesPath+p_module_key+'/'+p_module_key+'_main.py')
	moduleSourceCode_settings = getModuleCodes(modulesPath+p_module_key+'/'+p_module_key+'_settings.py')
	moduleSourceCode_html = getModuleCodes(modulesPath+p_module_key+'/'+p_module_key+'_html.txt')
	module_documentation = getModuleCodes(modulesPath+p_module_key+'/'+p_module_key+'_doc.txt')





	return jsonify({ 'module_name':p_module_key,#module.module_name,
	'documentation': module_documentation,#module.documentation,
	'moduleSourceCode_settings': moduleSourceCode_settings,
	'moduleSourceCode_main': moduleSourceCode_main,
	'moduleSourceCode_html': moduleSourceCode_html})






@app_code_clone.route('/execVizPlugin', methods=['POST'])
def execVizPlugin():
	program = request.form['textarea_source_code']
	# program = 'for i in range(3):\n    print("Python is cool")'


	old_stdout = sys.stdout
	redirected_output = sys.stdout = StringIO()
	exec (program)
	sys.stdout = old_stdout

	#output = getModuleCodes('/home/ubuntu/Webpage/app_code_clone/static/SP1_fastqc.html')

	return jsonify({'output': 'ok'})







#list of workflow outputs
@app_code_clone.route('/cloneViz_get_workflow_outputs_list/',  methods=['POST'])
def cloneViz_get_workflow_outputs_list():
	workflow_id = request.form['workflow_id'] #the unique workflow name
	workflow_outputs_list = os.listdir("/home/ubuntu/Webpage/app_code_clone/user_projects/golammostaeen@gmail.com/")
	return jsonify({'workflow_outputs_list':workflow_outputs_list})


#list of workflow outputs
@app_code_clone.route('/cloneViz_get_viz_output_list/',  methods=['POST'])
def cloneViz_get_viz_output_list():


	thisUser = 'golammostaeen@gmail.com'
	projectRoot = 'app_code_clone/user_projects/'

	workflow_id = request.form['workflow_id'] #the unique workflow name
	workflow_outputs_list = [os.path.basename(x) for x in glob.glob(projectRoot + thisUser + '/vizOutputs/' + '*.html')]
	return jsonify({'workflow_outputs_list':workflow_outputs_list})






@app_code_clone.route('/cloneViz_load_output_for_visualization', methods=['POST'])
def cloneViz_load_output_for_visualization():
	fileName= request.form['fileName']


	output = getModuleCodes('app_code_clone/user_projects/golammostaeen@gmail.com/vizOutputs/'+ fileName)



	return jsonify({'output': output})



























