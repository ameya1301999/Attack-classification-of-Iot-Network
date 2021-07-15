from __future__ import print_function
from sklearn.model_selection import train_test_split
import pandas as pd
import numpy as np
np.random.seed(1337)  # for reproducibility
from keras.preprocessing import sequence
from keras.utils import np_utils
from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation, Embedding
from keras.layers import LSTM, SimpleRNN, GRU,Conv1D,MaxPool1D,Flatten
from keras.datasets import imdb
from keras.utils.np_utils import to_categorical
from sklearn.metrics import (precision_score, recall_score,f1_score, accuracy_score,mean_squared_error,mean_absolute_error)
from sklearn import metrics
from sklearn.preprocessing import Normalizer
import h5py
from keras import callbacks
from keras.callbacks import ModelCheckpoint, EarlyStopping, ReduceLROnPlateau, CSVLogger
import matplotlib.pyplot as plt
import tensorflow as tf




data,labels=load_data()
labels=encode_label_values(labels)
data=Normalize_data(data)
#print(len(sel_cols))
data=select_features(data)

#data,labels=split_sequences_timesteps(data,labels,5)
print(data.shape)
X_train, X_test, y_train, y_test = train_test_split(data,labels, test_size=0.2,random_state=1)

X_train = np.reshape(X_train, (X_train.shape[0],X_train.shape[1],1))
X_test = np.reshape(X_test, (X_test.shape[0],X_test.shape[1],1))

batch_size = 30
#n_steps=4

# 1. define the network
model = Sequential()
model.add(Conv1D(filters=64, kernel_size=3, activation='relu', input_shape=(21,1)))
model.add(Conv1D(filters=64, kernel_size=5, activation='relu'))
model.add(MaxPool1D(pool_size=2))
model.add(LSTM(70,activation='relu'))
model.add(Dropout(0.1))
#model.add(Flatten())
#model.add(Dense(50))
#model.add(Dropout(0.2))
model.add(Dense(1,activation='sigmoid'))
print(model.summary())

opt=tf.keras.optimizers.Adam(learning_rate=0.0001)
# try using different optimizers and different optimizer configs
model.compile(loss='binary_crossentropy',optimizer=opt,metrics=['accuracy'])
checkpointer = callbacks.ModelCheckpoint(filepath="/content/checkpoint1-{epoch:02d}.hdf5", verbose=1, save_best_only=True, monitor='loss')
csv_logger = CSVLogger('/content/training_set_dnnanalysis.csv',separator=',', append=False)
history=model.fit(X_train, y_train, validation_split=0.25,  batch_size=batch_size, epochs=300, callbacks=[checkpointer,csv_logger])
plt.plot(history.history['accuracy'])
plt.plot(history.history['val_accuracy'])
plt.title('model accuracy')
plt.ylabel('accuracy')
plt.xlabel('epoch')
plt.legend(['train', 'test'], loc='upper left')
plt.savefig('/content/accuraccy_43_2.png')
plt.show()
plt.plot(history.history['loss'])
plt.plot(history.history['val_loss'])
plt.title('model loss')
plt.ylabel('loss')
plt.xlabel('epoch')
plt.legend(['train', 'test'], loc='upper left')
plt.savefig('/content/loss_43_2.png')
plt.show()
model.save("/content/cnn+lstmlayer_43_2_features.hdf5")