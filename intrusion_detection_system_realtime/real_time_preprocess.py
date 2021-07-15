import numpy as np
import pandas as pd
import tensorflow as tf
def read_realtime_data(data):
    data = pd.read_csv(data)
    data = data.rename(columns=lambda x: x.strip())
    return data.values
def split_sequences_realtime(data,time_steps):
    X=[]
    for i in range(len(data)):
        end_ix = i + time_steps
        if end_ix > len(data)+1:
            break
        seq_x= data[i:end_ix - 1]
        X.append(seq_x)

    return np.asarray(X)
def Normalize_data(data):
    data = data.astype(np.float32)

    eps = 1e-15

    mean_i=np.array([8.8796191e+03, 4.8749166e+00, 4.5727744e+00, 9.3946344e+02, 5.3853564e+02,
           1.6482671e+02, 2.1490726e+02, 2.7355850e+03, 1.6718775e+01, 1.2301730e+03,
           1.5396521e+07, 2.5406095e+06, 5.1952080e+06, 1.2994340e+07, 1.1152272e+02,
           1.6482671e+02, 8.9053687e+02, 4.8749166e+00, 9.3946344e+02, 4.2475830e+03,
           3.3114974e+00])
    max_i=np.array([6.553200e+04 ,1.932000e+03, 2.942000e+03 ,1.830120e+05, 1.168000e+04,
                   3.867000e+03, 6.692645e+03, 1.168000e+04, 1.460000e+03, 8.194660e+03,
                   1.200000e+08, 1.200000e+08 ,7.670000e+07, 1.200000e+08 ,3.939600e+04,
                   3.867000e+03 ,5.800500e+03 ,1.932000e+03 ,1.830120e+05 ,6.553500e+04,
                   1.931000e+03])
    min_i=np.array([0., 1., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 1., 0., 0., 0.])

    r = max_i - min_i + eps
    data = (data - mean_i) / r  # zero centered

    # deal with missing features -1
    #data[mask] = 0
    return data
def select_features(data):
  data=data[:,[0,2,3,4,6,8,9,10,11,13,20,21,22,23,34,53,54,61,62,65,67]]
  return data

def pre_process_raw_data(data,time_steps):
    #data=read_realtime_data(data)
    data = Normalize_data(data)
    data=np.array(data).reshape(1,21,1)
    data=tf.convert_to_tensor(data)

    #data = pd.DataFrame(data).to_numpy()
    #data = select_features(data)
    #data = split_sequences_realtime(data, 5)
    return data