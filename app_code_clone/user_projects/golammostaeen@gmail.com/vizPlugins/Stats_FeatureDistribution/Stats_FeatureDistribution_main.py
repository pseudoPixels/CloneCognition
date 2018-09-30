

import matplotlib
#matplotlib.use('Agg')
import numpy as np
import matplotlib.pyplot as plt
plt.switch_backend('agg')
import pandas as pd

import platform



import seaborn as sns

import warnings
warnings.filterwarnings('ignore')



# with open(csv_dataset_path) as module_1_inp:
# 	lines = module_1_inp.readlines()
#
# #only read the first line (in case it has multiples)
# csv_dataset_path = lines[0]

dataset = pd.read_csv(csv_dataset_path)


final_train = dataset



plt.figure(figsize=(15,7))
ax = sns.kdeplot(final_train[feature][final_train.validated == 1], color="darkturquoise", shade=True)
sns.kdeplot(final_train[feature][final_train.validated == 0], color="lightcoral", shade=True)


plt.legend(['True Positive', 'False Positive'])
plt.title('Density Plot of ' + feature)
ax.set(xlabel=feature)
plt.xlim(-10,85)





tmpFileName = feature_distribution.split('/')
tmpFileName = tmpFileName[len(tmpFileName)-1]

tmpFilePath = "/home/ubuntu/Webpage/app_code_clone/static/img/" + tmpFileName + ".png"

ax.get_figure().savefig(tmpFilePath)




with open(feature_distribution, "w+") as thisModuleOutput:
    thisModuleOutput.write("<HTML><body>")
    thisModuleOutput.write("<img src='http://p2irc-cloud.usask.ca/app_code_clone/static/img/" + tmpFileName + ".png'/>")
    thisModuleOutput.write("</body></HTML>")






