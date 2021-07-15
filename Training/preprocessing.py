import numpy as np
from glob import glob
import pandas as pd
from sklearn.preprocessing import LabelEncoder, OneHotEncoder, MinMaxScaler,Normalizer


def read_data():
    data = pd.read_csv("/content/Friday-WorkingHours-Afternoon-DDos.pcap_ISCX (1).csv")
    num_records, num_features = data.shape
    print("there are {} flow records with {} feature dimension".format(num_records, num_features))

    data = data.rename(columns=lambda x: x.strip())
    print('stripped column names')
    print(data.keys)
    return data

def load_data():
    data =read_data()
    print(data.info())
    df_label = data['Label']
    data = data.drop(columns=['Label'])
    print('dropped bad columns')
   
    data["Flow Bytes/s"] = pd.to_numeric(data["Flow Bytes/s"], errors='coerce')
    data["Flow Packets/s"] = pd.to_numeric(data["Flow Packets/s"], errors='coerce')
    
    m = data.loc[data['Flow Bytes/s'] != np.inf, 'Flow Bytes/s'].max()
    data['Flow Bytes/s'].replace(np.inf,m,inplace=True)
    m = data.loc[data['Flow Packets/s'] != np.inf, 'Flow Packets/s'].max()
    data['Flow Packets/s'].replace(np.inf,m,inplace=True)
    data.replace([np.inf, -np.inf],np.nan, inplace=True)
    nan_count = data.isnull().sum().sum()
    nan_count1 = df_label.isnull().sum().sum()
   
    #data["FIN Flag Count"] = pd.to_numeric(data["FIN Flag Count"], errors='coerce')
   
    print('There are {} nan entries'.format(nan_count))
   
    
    
    if nan_count > 0:
        data.fillna(data.mean(), inplace=True)
        print('filled NAN')
    if nan_count1 > 0:
        #data.fillna(data.mean(), inplace=True)
        print('nan exists')
   
    
    
    #data = data.astype(float).apply(pd.to_numeric)
    
    assert data.isnull().sum().sum() == 0, "There should not be any NaN"
    assert df_label.isnull().sum().sum() == 0, "There should not be any nan in labels"
    X = data.values
    
    return (X,df_label)

def encode_label_values(df_label):
    le = LabelEncoder()
    df_label = le.fit_transform(df_label)
    print(list(le.classes_))
    #df_label.unique()
    return df_label
def split_sequences_timesteps(X_train,Y_train,n_steps):
    X,y=[],[]
    for i in range(len(X_train)):
        end_ix=i+n_steps
        if end_ix>len(X_train):
            break
        seq_x,seq_y=X_train[i:end_ix-1],Y_train[end_ix-1]
        X.append(seq_x)
        y.append(seq_y)
    return np.array(X),np.array(y)
def split_sequences_timesteps_data(X_realtime,n_steps):
    X,y=[],[]
    for i in range(len(X_realtime)):
        end_ix=i+n_steps
        if end_ix>len(X_realtime):
            break
        seq_x=X_realtime[i:end_ix-1]
        X.append(seq_x)
        
    return np.array(X)

def Normalize_data(data):
    data = data.astype(np.float32)

    eps = 1e-15

    mask = data == -1
    data[mask] = 0
    mean_i = np.mean(data, axis=0)
    print(mean_i)
    min_i = np.min(data, axis=0)  # to leave -1 (missing features) values as is and exclude in normilizing
    print(min_i)
    max_i = np.max(data, axis=0)
    print(max_i)
    #scaler = Normalizer().fit(data)
    #trainX = scaler.transform(data)
    r = max_i - min_i + eps
    data = (data - mean_i) / r  # zero centered

    # deal with missing features -1
    data[mask] = 0
    return data
def select_features(data):
  data=data[:,[0,2,3,4,6,8,9,10,11,13,20,21,22,23,34,53,54,61,62,65,67]]
  return data
d,c=load_data()
data=select_features(d)
data=Normalize_data(data)

#print(d[0],"\n",d[2],"\n",d[3],"\n",d[4],"\n",d[6],"\n",d[8],"\n",d[9],"\n",d[10],"\n",d[11],"\n",d[13],"\n",d[20],"\n",d[21],"\n",d[22],"\n",d[23],"\n",d[34],"\n",d[53],"\n",d[54],"\n",d[61],"\n",d[62],"\n",d[65],"\n",d[67])



 
