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
df = pd.read_excel('/content/drive/MyDrive/TFG/DADES/T4_T5.xlsx') #Read excel file

pd.set_option('display.max_columns', None) #Display all columns
df.head() 
df.describe() #Check for constant values (std close to 0)

df = df.drop(['Unnamed: 0', 'P_T5', 'P_T4', 'X_BTTMS_T4'], axis=1)  #Drop the output variable columns where the value doesn't change or the information is redundant.

NaNs = df['BUTENE'].isin([-32767.0000]).sum(axis=0) #Count the number of NaNs
print('Uncoverged examples:', NaNs)

df = shuffle(df) #shuffle all the samples
ths = df.shape[0]*8//10 #define the threshold
#%% Normalization

scaler = StandardScaler()
scaler.fit(df.iloc[:ths,:]) #Take only yhe training set
df = pd.DataFrame(scaler.transform(df), columns=df.columns, index=df.index)
df.boxplot(figsize=(50,15)) #Check normalization was applied correctly

#%% Build the surrogate (ANN)

x_train = df.iloc[:ths,:6]
x_test = df.iloc[ths:,:6]

y_train = df.iloc[:ths,6:]
y_test = df.iloc[ths:,6:]

hidden_units = [3, 6, 8] #Define the values of the hidden units that you want to study
neur_comb = list(itertools.product(hidden_units, repeat = 2)) #Create a list of tuples containing all the permutations 
hid_units=[]
for q in range(len(neur_comb)): #Create a list with all the permutations
    hid_units.append(neur_comb[q][0])
    hid_units.append(neur_comb[q][1])

inputs = keras.Input(shape=(len(x_train.columns)), name='Input layer') #Define the input unit

mymodels = {}
History = {}
preds = {}
mse_values = []
list_dicts_mse = []

for names in range(0,len(hid_units)//2): #Create a dictionary of names for the different 
  mse_name = {}
  list_dicts_mse.append(mse_name)

epochs = 35
batch_size = 300
k=0

for count, num_units in enumerate(hid_units): #Generate X models (as many as hidden units permutions, per hidden layers)
    if k <len(hid_units):
      features = layers.Dense(hid_units[k], activation="relu", name='first_hidden_layer')(inputs) #First hidden layer
      features = layers.Dense(hid_units[k+1], activation="relu", name='second_hidden_layer')(features) #Second hidden layer
      
      outputs = layers.Dense(len(y_train.columns), activation="linear", name="Output_layer")(features) #Output layer

      model_i = "Model {0}".format(count+1) #Model names
      mymodels[model_i] = keras.Model(inputs=inputs, outputs=outputs) # Save the i model
      #mymodels["model{0}".format(count)].summary() --> print a summary
      mymodels[model_i].compile(loss='mean_squared_error', optimizer='adam', metrics=["mae", 'mse'])  # Compile the i model
      print('')
      print(model_i)
      print('')
      History_i = "History{0}".format(count) # History names
      History[History_i] = mymodels[model_i].fit(x_train, y_train, epochs=epochs, batch_size=batch_size, validation_split=0.2) #Fit the i model and store it in i history
      print('')
      print('Evaluate (test set)')
      mymodels[model_i].evaluate(x_test, y_test) #Evaluate i model
      print('')
      preds_i = "preds{0}".format(count) #Preds names
      preds[preds_i] = mymodels[model_i].predict(x_test) #Predict the i model
      print('')

      for col in range(0,len(y_test.columns)): #Evaluate each output variable for the i model using mse and store it into a dictionary 
        mse_i = "mse_{0}".format(col+1)
        mse_value1 = mean_squared_error(y_test.iloc[:,col], preds[preds_i][:,col])
        list_dicts_mse[count][mse_i] = mse_value1
      print('')
      k +=2

      #Plot the training vs validation loss for the i model
      fig, (ax1) = plt.subplots(nrows=1, ncols=1, figsize = (15, 8))
      ax1.plot(History[History_i].history['loss'])
      ax1.plot(History[History_i].history['val_loss'])
      ax1.set_title(model_i + ' loss', size=20)
      ax1.set_ylabel('Loss', size=16)
      ax1.set_xlabel('Epoch', size=16)
      ax1.set_xticks(range(0, epochs+1, 4))
      ax1.legend(['Train', 'Validation'], loc='upper right', fontsize=20)
      ax1.tick_params(axis='both',labelsize=15)
      print('')

df_mse = pd.DataFrame.from_records(list_dicts_mse) #Store the mse values for each output of the i model into a dataframe
df_mse_trans = df_mse.T