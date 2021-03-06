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

df = df.drop(['Unnamed: 0', 'P_T5', 'P_T4', 'X_BTTMS_T4'], axis=1)  #Drop the output variable columns where the value doesn't change or the information is redundant.

NaNs = df['BUTENE'].isin([-32767.0000]).sum(axis=0) #Count the number of NaNs
print('Uncoverged examples:', NaNs)

df = shuffle(df) #shuffle all the samples
ths = df.shape[0]*8//10 #define the threshold

df1 = df.iloc[ths:,4:7] #Save the input points for the test set of the next surrogate (which will be related to the output points of this surrogate)
df = df.drop(df.iloc[:, 13:21],axis = 1) #Drop the input/output variables of distillation column T5

df = df.drop(['Unnamed: 0', 'P_T4', 'NT_T5',  'RR_T5',  'D_T5', 'X_BTTMS_T4'], axis=1) #Drop temperature and pressure columns since the value doesn't change
#%% Normalization

scaler = StandardScaler()
scaler.fit(df.iloc[:ths,:]) #Take only yhe training set
df = pd.DataFrame(scaler.transform(df), columns=df.columns, index=df.index)
df.boxplot(figsize=(50,15)) #Check normalization was applied correctly

#%% Build the surrogate (ANN)
x_train = df.iloc[:ths,:3]
x_test = df.iloc[ths:,:3]

y_train = df.iloc[:ths,3:]
y_test = df.iloc[ths:,3:]

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
mset4 = []
for col in range(0,len(y_test.columns)):
        mse_value1 = mean_squared_error(y_test.iloc[:,col], preds[:,col])
        mset5.append(mse_value1)


preds = model.predict(x_test) #predicted outputs 
df2 = pd.DataFrame(preds) #Store into a dataframe
df2.columns = list(y_test) #Change column names (get same as y_test)
