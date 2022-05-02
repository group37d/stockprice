import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import matplotlib.pyplot as plt

# Input data files are available in the "../input/" directory.
# For example, running this (by clicking run or pressing Shift+Enter) will list the files in the input directory

import os
print(os.listdir("/content/drive/MyDrive/FPT"))

dataset_train = pd.read_csv("/content/drive/MyDrive/FPT/newfpttrain.csv")

dataset_train

dataset_train.info()

trainset = dataset_train.iloc[:,1:2].values

trainset

from sklearn.preprocessing import MinMaxScaler
sc = MinMaxScaler(feature_range = (0,1))
training_scaled = sc.fit_transform(trainset)

training_scaled

x_train = []
y_train = []

for i in range(60,498):
    x_train.append(training_scaled[i-60:i, 0])
    y_train.append(training_scaled[i,0])
x_train,y_train = np.array(x_train),np.array(y_train)

x_train.shape

x_train = np.reshape(x_train, (x_train.shape[0],x_train.shape[1],1))

from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from keras.layers import Dropout

regressor = Sequential()
regressor.add(LSTM(units = 50,return_sequences = True,input_shape = (x_train.shape[1],1)))

regressor.add(Dropout(0.2))

regressor.add(LSTM(units = 50,return_sequences = True))
regressor.add(Dropout(0.2))

regressor.add(LSTM(units = 50,return_sequences = True))
regressor.add(Dropout(0.2))

regressor.add(LSTM(units = 50))
regressor.add(Dropout(0.2))

regressor.add(Dense(units = 1))

regressor.compile(optimizer = 'adam',loss = 'mean_squared_error')

regressor.fit(x_train,y_train,epochs = 100, batch_size = 32)

dataset_test =pd.read_csv("/content/drive/MyDrive/FPT/fpt-test.csv")

real_stock_price = dataset_test.iloc[:,1:2].values

dataset_total = pd.concat((dataset_train['<OpenFixed>'],dataset_test['<OpenFixed>']),axis = 0)
dataset_total

dataset_total.dropna()

inputs = dataset_total[len(dataset_total) - len(dataset_test)-60:].values
inputs

inputs = inputs.reshape(-1,1)

inputs

inputs = sc.transform(inputs)
inputs.shape

x_test = []
for i in range(60,390):
    x_test.append(inputs[i-60:i,0])

x_test = np.array(x_test)
x_test.shape

x_test = np.reshape(x_test, (x_test.shape[0],x_test.shape[1],1))
x_test.shape

predicted_price = regressor.predict(x_test)

predicted_price = sc.inverse_transform(predicted_price)
predicted_price

plt.plot(real_stock_price,color = 'red', label = 'Real Price')
plt.plot(predicted_price, color = 'blue', label = 'Predicted Price')
plt.title('FPT Stock Price Prediction')
plt.xlabel('Time')
plt.ylabel('FPT Stock Price')
plt.legend()
plt.show()
