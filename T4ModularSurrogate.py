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