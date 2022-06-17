from T4ModularSurrogate import *
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import mean_squared_error
from sklearn.utils import shuffle
from sklearn.preprocessing import StandardScaler
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.layers import Dense, Activation, Dropout
import itertools

sns.set_theme()

#%%Preprocessing/cleaning
df = pd.read_excel('T4_T5.xlsx') #Read excel file

pd.set_option('display.max_columns', None) #Display all columns
df.head() 
df.describe() #Check for constant values (std close to 0)
df = df.drop(df.iloc[:, 7:13],axis = 1) #Drop the outputs from column T4

#Drop temperature and pressure columns since the value doesn't change + other unuseful variables
df = df.drop(['Unnamed: 0', 'P_T5', 'NT_T4',  'RR_T4',  'D_T4', 'X_BTTMS_T4', 'M_BUTENE'], axis=1) 

df2 = df2.iloc[:,6:] #retrieve the useful variables from module surrogate T4 

#Count the number of NaNs
NaNs = df['BUTENE'].isin([-32767.0000]).sum(axis=0)
print('Uncoverged examples:', NaNs)

#Delete rows with NaNs
df = df[df['BUTENE'] != -32767.0000]
df = shuffle(df)

ths = df.shape[0]*8//10
df.iloc[ths:,:3] = df1.iloc[:,:3] #Change the NT, RR, D sampling points for the ones stored after shuffling in modular surrogate T4
#%% Normalization

scaler = StandardScaler()
scaler.fit(df.iloc[:ths,:]) #Take only yhe training set
df = pd.DataFrame(scaler.transform(df), columns=df.columns, index=df.index)
df.boxplot(figsize=(50,15)) #Check normalization was applied correctly

#%% Build the surrogate (ANN)
x_train = df.iloc[:ths,:6]
x_test = df.iloc[ths:,:3]
x_test[['M_BTTMS_T4', 'X_BUTENE_BTTMS_T4', 'X_CYCLOPENTANE_BTTMS_T4']] = df2.values #use the predicted outputs from the surrogate T4

y_train = df.iloc[:ths,6:]
y_test = df.iloc[ths:,6:]

inputs = keras.Input(shape=(len(x_train.columns),), name='Input layer')
features = layers.Dense(8, activation="relu", name='first_hidden_layer')(inputs)
features = layers.Dense(8, activation="relu", name='second_hidden_layer')(features)
outputs = layers.Dense(len(y_train.columns), activation="linear", name="Output_layer")(features)

model = keras.Model(inputs=inputs, outputs=outputs)

model.compile(loss='mean_squared_error', optimizer='adam', metrics=['mse'])

epochs = 50
batch_size = 300

history = model.fit(x_train, y_train, epochs=epochs, batch_size=batch_size, validation_split=0.2)

model.evaluate(x_test, y_test)

#Plot the loss for the training and validation sets.
fig, (ax1) = plt.subplots(nrows=1, ncols=1, figsize = (15, 8))

ax1.plot(history.history['loss'])
ax1.plot(history.history['val_loss'])
ax1.set_title('T4 model loss', size=20)
ax1.set_ylabel('Loss', size=16)
ax1.set_xlabel('Epoch', size=16)
ax1.set_xticks(range(0, epochs+1, 4))
ax1.set_yticks(np.arange(0, 1.2, step=0.1))
ax1.legend(['Train', 'Validation'], loc='upper right', fontsize=20)
ax1.tick_params(axis='both',labelsize=15)

#Evaluate each output independently
preds = model.predict(x_test)
mset5 = []
for col in range(0,len(y_test.columns)):
        mse_value1 = mean_squared_error(y_test.iloc[:,col], preds[:,col])
        mset5.append(mse_value1)
