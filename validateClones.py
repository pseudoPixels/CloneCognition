########################################################################################################################
########################################################################################################################
########################################################################################################################
#############################  MACHINE LEARNING MODEL ##################################################################
########################################################################################################################
########################################################################################################################
########################################################################################################################


import pickle
import pybrain
from io import StringIO
import sys
import subprocess
import tempfile
import os
import uuid
import glob
import xml.etree.ElementTree as ET

def app_code_clone_getValidationScore(sourceCode1,sourceCode2,lang='java' ):


	#load the trained Neural Net
	fileObject = open('pybrain/trainedNetwork', 'rb')
	loaded_fnn = pickle.load(fileObject)

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
	sourceFile = 'txl_tmp_file_dir/' + fileName + '.txt'

	# write submitted source code to corresponding files
	with open(sourceFile, "w") as fo:
		#encode in unicode so that the program does not crash when strange unicode characters are encountered
		fo.write(sourceCode.encode('utf-8'))

	# get the required txl file for feature extraction
	# txlPath = '/home/ubuntu/Webpage/txl_features/txl_features/java/PrettyPrint.txl'

	# do the feature extraction by txl
	p = subprocess.Popen(['/usr/local/bin/txl', '-Dapply', txlFilePath, sourceFile], stdout=subprocess.PIPE,
						 stderr=subprocess.PIPE)
	out, err = p.communicate()

	# convert to utf-8 format for easier readibility
	#out = str(out, 'utf-8')
	#err = str(err, 'utf-8')

	out = str(out)
	err = str(err)

	err = err.replace(sourceFile, 'YOUR_SOURCE_FILE')
	err = err.replace(txlFilePath, 'REQUIRED_TXL_FILE')

	# once done remove the temp file
	os.remove(sourceFile)

	if saveOutputFile == False:
		return out, err
	else:
		outputFileLocation = str(uuid.uuid4())
		outputFileLocation = 'txl_tmp_file_dir/' + outputFileLocation + '.txt'
		with open(outputFileLocation, "w") as fo:
			#encode in unicode so that the program does not crash when strange unicode characters are encountered
			fo.write(out.encode('utf-8'))

		return outputFileLocation, out, err







def app_code_clone_getCodeCloneSimilarity(sourceCode1, sourceCode2, lang, txlFilePath):
	saveOutputFile = True
	outputFileLocation1, out1, err1 = app_code_clone_execTxl(txlFilePath, sourceCode1, lang, saveOutputFile)
	outputFileLocation2, out2, err2 = app_code_clone_execTxl(txlFilePath, sourceCode2, lang, saveOutputFile)

	p = subprocess.Popen(['/usr/bin/java', '-jar', 'txl_tmp_file_dir/calculateCloneSimilarity.jar',
						  outputFileLocation1, outputFileLocation2], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	similarityValue, err = p.communicate()

	#similarityValue = str(similarityValue, 'utf-8')
	similarityValue = str(similarityValue)
	similarityValue = similarityValue.replace('\n', '')
	#err = str(err, 'utf-8')
	err = str(err)


	# once done remove the temp files
	os.remove(outputFileLocation1)
	os.remove(outputFileLocation2)

	return similarityValue



def app_code_clone_similaritiesNormalizedByLine(sourceCode1, sourceCode2, lang):
	# getting the txl and the input file to parse
	# sourceCode1 = request.form['sourceCode_1']
	# sourceCode2 = request.form['sourceCode_2']
	# lang = request.form['lang']

	txlFilePath = 'txl_features/txl_features/java/PrettyPrint.txl'
	type1sim_by_line = app_code_clone_getCodeCloneSimilarity(sourceCode1, sourceCode2, lang, txlFilePath)

	txlFilePath = 'txl_features/txl_features/java/normalizeLiteralsToDefault.txl'
	type2sim_by_line = app_code_clone_getCodeCloneSimilarity(sourceCode1, sourceCode2, lang, txlFilePath)

	txlFilePath = 'txl_features/txl_features/java/normalizeLiteralsToZero.txl'
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

	txlFilePath = 'txl_features/txl_features/java/consistentRenameIdentifiers.txl'
	type1sim_by_token = app_code_clone_getCodeCloneSimilarity(sourceCode1, sourceCode2, lang, txlFilePath)

	txlFilePath = 'txl_features/txl_features/java/normalizeLiteralsToZero.txl'
	type2sim_by_token = app_code_clone_getCodeCloneSimilarity(sourceCode1, sourceCode2, lang, txlFilePath)

	txlFilePath = 'txl_features/txl_features/java/normalizeLiteralsToZero.txl'
	type3sim_by_token = app_code_clone_getCodeCloneSimilarity(sourceCode1, sourceCode2, lang, txlFilePath)

	# out = {'type_1_similarity_by_token': type1sim_by_token, 'type_2_similarity_by_token': type2sim_by_token,
	# 	   'type_3_similarity_by_token': type3sim_by_token}
    #
	# return jsonify({'error_msg': 'None',
	# 				'log_msg': 'Preprocessing Source Codes...\nNormalizing Source Codes...\nCalculating Similarities...\nDone.',
	# 				'output': out})

	return type1sim_by_token, type2sim_by_token, type3sim_by_token








def get_next_clone_pair_for_validation(cloneFile, theValidationFile, validationFileExt='.validated'):
	# getting the example program name
	theCloneFile = cloneFile
	#theValidationFile = theCloneFile + validationFileExt

	tree2 = ET.parse(cloneFile)
	root = tree2.getroot()

	nextCloneIndex = 0

	if os.path.exists(theValidationFile) == True:
		#response_code = 'FILE_ALREADY_EXIST'
		nextCloneIndex = sum(1 for line in open(theValidationFile))
	else:
		new_file = open(theValidationFile, "w")
		new_file.close()

	#fragment_1_path, fragment_1_startline, fragment_1_endline, fragment_1_clone, fragment_2_path, fragment_2_startline, fragment_2_endline, fragment_2_clone, number_of_validated_clones, total_clones
	return root[nextCloneIndex][0].attrib['file'], root[nextCloneIndex][0].attrib['startline'], root[nextCloneIndex][0].attrib['endline'], root[nextCloneIndex][1].text, root[nextCloneIndex][2].attrib['file'], root[nextCloneIndex][2].attrib['startline'], root[nextCloneIndex][2].attrib['endline'],root[nextCloneIndex][3].text, nextCloneIndex+1, len(root)











def main():
	validationThreshold = float(sys.argv[1])
	inputCloneDir = sys.argv[2]
	outDir = sys.argv[3]


	list_of_file_for_validation = [x for x in glob.glob(inputCloneDir + '/' + '*.xml')]


	OVERALL_TRUE_CLONES = 0
	OVERALL_CLONE_PAIRS = 0

	print 'Starting Validation...'
	progress = 0



	cloneFilesCounts = len(list_of_file_for_validation)
	for aCloneFile in list_of_file_for_validation:
		print 'Validation Progress : ' + str(progress*100/cloneFilesCounts) + '%'

		cloneFileBaseName = os.path.basename(aCloneFile)
		mlValidation_output_file = outDir + '/' + cloneFileBaseName + '.mlValidated'


		mlValidationCount = 0

		if os.path.exists(mlValidation_output_file) == True:
			#response_code = 'FILE_ALREADY_EXIST'
			mlValidationCount = sum(1 for line in open(mlValidation_output_file))
		else:
			new_file = open(mlValidation_output_file, "w")
			new_file.close()

		tree2 = ET.parse(aCloneFile)
		root = tree2.getroot()
		totalClonePairs = len(root)


		for aCloneIndex in range(mlValidationCount, totalClonePairs):
			fragment_1_path, fragment_1_startline, fragment_1_endline, fragment_1_clone, fragment_2_path, fragment_2_startline, fragment_2_endline, fragment_2_clone, clones_validated, total_clones = get_next_clone_pair_for_validation(
				aCloneFile, mlValidation_output_file)
			OVERALL_CLONE_PAIRS = OVERALL_CLONE_PAIRS + 1

			true_probability = app_code_clone_getValidationScore(fragment_1_clone, fragment_2_clone, 'java')

			with open(mlValidation_output_file, "a") as validationFile:
				if true_probability >=validationThreshold:
					validationFile.write('true' + ',' + fragment_1_path +','+ fragment_1_startline +','+ fragment_1_endline+','+fragment_2_path+','+fragment_2_startline+','+fragment_2_endline + '\n')
					OVERALL_TRUE_CLONES = OVERALL_TRUE_CLONES + 1
				else:
					validationFile.write(
						'false' + ',' + fragment_1_path + ',' + fragment_1_startline + ',' + fragment_1_endline + ',' + fragment_2_path + ',' + fragment_2_startline + ',' + fragment_2_endline + '\n')

		progress = progress + 1

	print 'Done'

	print '##############################################'
	print '           CLONE VALIDATION STATS             '
	print '##############################################'


	print 'Total Clone Pairs Validated: ' + str(OVERALL_CLONE_PAIRS)
	print 'Predicted True Positive Clones: ' + str(OVERALL_TRUE_CLONES)
	print 'Predicted False Positive Clones: ' + str(OVERALL_TRUE_CLONES - OVERALL_TRUE_CLONES)
	print 'Predicted Precision: ' + str(OVERALL_TRUE_CLONES/OVERALL_CLONE_PAIRS)


	with open(outDir+'/'+'__CLONE_VALIDATION_STATS.txt', "a") as cloneValidationStats:
		cloneValidationStats.write('Total Clone Pairs Validated: ' + str(OVERALL_CLONE_PAIRS) + '\n')
		cloneValidationStats.write('Predicted True Positive Clones: ' + str(OVERALL_TRUE_CLONES) + '\n')
		cloneValidationStats.write('Predicted False Positive Clones: ' + str(OVERALL_CLONE_PAIRS - OVERALL_TRUE_CLONES) + '\n')
		cloneValidationStats.write('Predicted Precision: ' + str(OVERALL_TRUE_CLONES/OVERALL_CLONE_PAIRS) + '\n')




if __name__ == "__main__":
	main()





































