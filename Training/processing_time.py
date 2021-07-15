data=data = pd.read_csv("/content/demo_ISCX.csv")
num_records, num_features = data.shape
print("there are {} flow records with {} feature dimension".format(num_records, num_features))
import keras
data = data.rename(columns=lambda x: x.strip())
print('stripped column names')
print(data.keys)
data=Normalize_data(data)
data=pd.DataFrame(data).to_numpy()
data=select_features(data)
data=split_sequences_timesteps_data(data,8)
print(data.shape)
import time
model =keras.models.load_model('/content/cnn+lstmlayer_model1.hdf5')
model.load_weights("/content/checkpoint-60.hdf5")
start_time = time.time()
pred = model.predict_classes(data)
print("--- %s seconds ---" % (time.time() - start_time))
print(pred)
