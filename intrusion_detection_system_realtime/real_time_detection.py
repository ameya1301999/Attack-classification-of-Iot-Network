import keras
import tensorflow as tf
#import tflite_runtime.interpreter as tflite
import sys
import os
import config
import csv
import time
import numpy as np
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
#tf.logging.set_verbosity(tf.logging.ERROR)
from  real_time_preprocess import read_realtime_data,split_sequences_realtime,pre_process_raw_data
#filepaths  = [os.path.join(config.folderpath, name) for name in os.listdir(config.folderpath)]
print("\n\n\n\n")
print(">>>>>>>>LOADING>>>>>>>>>>",end='\r')
time.sleep(4)

def get_model():
    model = keras.models.load_model('C:\\Users\Indian\PycharmProjects\intrusion_detection_system_realtime\CNN+lstm_model\cnn+lstmlayer_21_1step_features.hdf5')
    model.load_weights("C:\\Users\Indian\PycharmProjects\intrusion_detection_system_realtime\CNN+lstm_model\checkpoint1-98_1step.hdf5")
    return model



def predict(data):
    data=pre_process_raw_data(data,config.time_steps)
    print("data_shape",data.shape)
    model=get_model()
    predicted_values=(model.predict(data))
    return predicted_values

    '''interpreter = tflite.Interpreter(model_path=)
    #interpreter = tf.lite.Interpreter(model_path="C:\\Users\Indian\PycharmProjects\intrusion_detection_system_realtime\checkpoint_21.tflite")
    interpreter.allocate_tensors()

# Get input and output tensors.
    input_details = interpreter.get_input_details()
    print(input_details)
    output_details = interpreter.get_output_details()

# Test the model on random input data.

    interpreter.set_tensor(input_details[0]['index'],data)

    interpreter.invoke()

# The function `get_tensor()` returns a copy of the tensor data.
# Use `tensor()` in order to get a pointer to the tensor.
    output_data = interpreter.get_tensor(output_details[0]['index'])
    return output_data'''

def traffic_congestion(predicted_values):
    congestion_pkt_cnt_indvidual_csv_file=0

    for i in predicted_values:
        if(i==0):
            congestion_pkt_cnt_indvidual_csv_file+=1
    config.traffic_congestion_pkt_cnt+=congestion_pkt_cnt_indvidual_csv_file
    print("congestion_cnt",config.traffic_congestion_pkt_cnt)
    config.pkt_total_cnt+=len(predicted_values)
    config.percent_traffic_congestion=(config.traffic_congestion_pkt_cnt/config.pkt_total_cnt)*100
    return config.percent_traffic_congestion


'''def analyze_files():
    per_traffic_congestion=0
    for data in filepaths:
      print("analyzing files.............",end='\r')

      print("\n\n\n")
      file = open(data)
      reader = csv.reader(file)
      lines= len(list(reader))

      print(".......Number of flows generated......",lines)
      print("\n\n\n")

      predicted_values=predict(data)
      per_traffic_congestion=traffic_congestion(predicted_values)
      print(".........traffic_congestion = %d........",per_traffic_congestion)
    if(per_traffic_congestion>0):
        print("!!!!!!WARNING!!!!!!",end='\r')
        print("THE SYSTEM IS UNDER DOS ATTACK")
    else:
        print("\n\n\n")
        print(".............System is operating in normal condition...............")


#analyze_files()
'''










