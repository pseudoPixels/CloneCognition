

import matplotlib
#matplotlib.use('Agg')
import numpy as np
import matplotlib.pyplot as plt
plt.switch_backend('agg')
import pandas as pd



import warnings
warnings.filterwarnings('ignore')



# with open(csv_dataset_path) as module_1_inp:
# 	lines = module_1_inp.readlines()
#
# #only read the first line (in case it has multiples)
# csv_dataset_path = lines[0]

dataset = pd.read_csv(csv_dataset_path)

# import pip
# r = pip.main(['install', 'scikit-learn'])
#
# print ("=================================")
# print (r)
# print ("=================================")



# Fitting Kernel SVM to the Training set
from sklearn.svm import SVC
classifier = SVC(kernel = kernel_type, random_state = 0)


#cols = [featureSet]
X = dataset[featureSet]
y = dataset[target]



# Applying k-Fold Cross Validation
from sklearn.model_selection import cross_val_score
accuracies = cross_val_score(estimator = classifier, X=X , y=y , cv = n)


with open(SVM_classification_stats, "w+") as thisModuleOutput:
    thisModuleOutput.write("SVM:\n========================================\n")
    thisModuleOutput.write("Classification Accuracy: " + str( round(accuracies.mean()*100,2) ) +  " %" )


#print("Logistic Regression:\n Accuracy:", accuracies.mean(), "+/-", accuracies.std(),"\n")





