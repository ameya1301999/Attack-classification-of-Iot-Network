#from data_load_preprocess import load_data,read_data,encode_label_values
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.preprocessing import LabelEncoder, OneHotEncoder
import warnings
warnings.filterwarnings("ignore")
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.metrics import confusion_matrix

data,labels=load_data()

labels=encode_label_values(labels.astype(str))
labels= pd.to_numeric(labels, errors='coerce')
print(labels.shape)
labels=labels.reshape(225745,1)
#data=np.append(data,labels,axis=1)
d= pd.DataFrame(data)

def feature_correlation(d):
  corr=d.corr()
  print(d.shape)
  sns.heatmap(corr)
  columns = np.full((corr.shape[0],), True, dtype=bool)
  for i in range(corr.shape[0]):
     for j in range(i+1, corr.shape[0]):
         if corr.iloc[i,j] >= 0.9:
             if columns[j]:
                 columns[j] = False

  selected_columns = d.columns[columns]
  data_sel_columns = d[selected_columns]
  return selected_columns,data_sel_columns



import statsmodels.api as sm





def backwardElimination(x, Y, sl, columns):
    numVars = len(x[0])
    for i in range(0, numVars):
        regressor_OLS = sm.OLS(Y, x).fit()
        maxVar = max(regressor_OLS.pvalues).astype(float)
        if maxVar > sl:
            for j in range(0, numVars - i):
                if (regressor_OLS.pvalues[j].astype(float) == maxVar):
                    x = np.delete(x, j, 1)
                    columns = np.delete(columns, j)
                    
    print(regressor_OLS.summary())
    return x, columns

def plot_feature_distribution(data,result):
  fig = plt.figure(figsize = (20, 25))
  j = 0
  for i in data.columns:
      plt.subplot(11, 4, j+1)
      j += 1
      sns.distplot(data[i][result['Attack']==0], color='g', label = 'benign')
      sns.distplot(data[i][result['Attack']==1], color='r', label = 'DDOS')
      plt.legend(loc='best')
  fig.suptitle('Attack Ddos')
  fig.tight_layout()
  fig.subplots_adjust(top=0.95)
  plt.show()
  plt.savefig("feature_distribution_of_selected_features.png")

selected_columns,data_sel_columns=feature_correlation(d)
print(len(selected_columns.values))

#selected_columns = selected_columns[0:len(selected_columns)].values
SL = 0.05
data_modeled, selected_columns = backwardElimination(data_sel_columns.values,labels, SL, selected_columns)
print(len(selected_columns))
result = pd.DataFrame()
labels=labels.reshape(225745)
result['Attack'] =labels
data = pd.DataFrame(data = data_modeled, columns = selected_columns)
plot_feature_distribution(data,result)



