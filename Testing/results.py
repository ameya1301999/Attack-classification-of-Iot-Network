import keras
import seaborn as sns
from sklearn.metrics import plot_confusion_matrix
import matplotlib.pyplot as plt
import time
from mlxtend.plotting import plot_confusion_matrix
#print(X_test.shape)
#X_train, X_test, y_train, y_test = train_test_split(data,labels, test_size=0.3,shuffle=True,random_state=5)
model=keras.models.load_model('/content/cnn+lstmlayer_43_2_features.hdf5')
model.load_weights("/content/checkpoint1-98.hdf5")
start_time = time.time()
pred = model.predict_classes(X_test)
print("\n\n\n")
print("--- The processing time is %s seconds ---" % (time.time() - start_time))
print("\n\n\n")
proba = model.predict_proba(X_test)
np.savetxt("cnn+lstmpredicted.txt", pred)
np.savetxt("cnn+lstmprobability.txt", proba)

accuracy = accuracy_score(y_test, pred)
recall = recall_score(y_test, pred , average="binary")
precision = precision_score(y_test, pred , average="binary")
f1 = f1_score(y_test, pred, average="binary")


print("----------------------------------------------")
print("accuracy")
print("%.3f" %accuracy)
print("precision")
print("%.3f" %precision)
print("recall")
print("%.3f" %recall)
print("f1score")
print("%.3f" %f1)
print("...............................................")
kappa = cohen_kappa_score(y_test, pred)
print('Cohens kappa: %f' % kappa)
# ROC AUC
auc = roc_auc_score(y_test, pred)
print('ROC AUC: %f' % auc)
# confusion matrix
print("...........the confusion matrix is as follows...........")
matrix = confusion_matrix(y_test,pred)
print(matrix)
variance=np.var(proba)
sse=np.mean((np.mean(proba)-y_test)**2)
bias=sse-variance
print("........................................................")
print("The variance is %.3f" %variance)
print("The bias is %.3f" %bias)
class_names=['BENIGN','DDOS']
f = sns.heatmap(matrix, annot=True)
figure = f.get_figure()    
figure.savefig('/content/confusion_matrix.png', dpi=400)