#%%
"""
First of all several functions are defined to create the samples (Latin Hypercube Sampling) and the connection HYSYS-python (HysysConnection(object)).
Then, samples are randomly generated and ordered, so HYSYS feasibility is improved.
Finally, the connection is created and samples are simulated. The results are eventually exported to an Excel file through a pandas DataFrame.
"""
### Functions to create the Sampling data ###

import numpy as np
import matplotlib.pyplot as plt
import array


def latin_hypercube_normalized(d,n):
  "Normalized values from 0-1"
  lower_limits = np.arange(0,n)/n
  upper_limits = np.arange(1,n+1)/n      

  points = np.random.uniform(low=lower_limits, high=upper_limits, size=[d,n]).T
   
  for i in range(0,d):
    np.random.shuffle(points[:,i])
  return points


def latin_hypercube_sampling(LOW,UP,p,d):
  "Values from upper to lower limits"
  for i in range(0,d):
    p[:,i]=p[:,i]*(UP[i]-LOW[i])+LOW[i]
  return p


#pip install cognite-sdk

import numpy as np
import pandas as pd
import win32com.client
import os
import time
import datetime as dt
from datetime import datetime
from datetime import timedelta 
from cognite.client import CogniteClient
from pathlib import Path
from win32com.client import makepy 
import matplotlib.pyplot as plt
import sys

class HysysConnection(object):
    ''' All the functions related to Hysys communication '''
    #Open Hysys Case
    def __init__(self,filepath,Hysyspath):
        '''
        Set all the global variables and do the convertion for C classes to Python language.
        The CLSID may be wrong because this script was written for Unisim in case is wrong we can look for the good ones
        '''
        try:
            self.casepath = filepath
            self.uniapp = win32com.client.Dispatch("HYSYS.Application.NewInstance")
            self.simcase = self.uniapp.SimulationCases.Open(filepath)
            ## Call to Hysys backdor class on the register
            self.BackDoor=makepy.gencache.GetClassForCLSID("{11FE7386-A1D1-4E47-B46A-8A09A7CE5EB2}")
            # Define class for FixedDataTables, Datatalbe and VarDefinition lybraries
            self.FixedDataTables = makepy.gencache.GetClassForCLSID("{4DEF63F0-103B-11D1-A455-00A0C923285C}")
            self.DataTable = makepy.gencache.GetClassForCLSID("{FE57ADBD-5DFA-46DA-B205-423FBF3799AA}")
            self.VarDefinition = makepy.gencache.GetClassForCLSID("{B37CCBF0-E29E-11D0-A418-00A0C923285C}")
            sys.argv = ["makepy", Hysyspath]
            makepy.main ()
            return
        except:
            assert self.simcase is not None, "Hysys Case is null"
            HysysConnection.KillHysys(self.simcase)

    def OpenCase(self):
        ''' Open Hysys case & Activate the select case '''
        self.uniapp.Visible = False
        self.simcase.Activate()
        return [self.simcase,self.uniapp]

    def KillHysys(self,simCase = ''):
        ''' Kill Hysys at the end of the run or when something goes wrong '''
        if self.simcase != '': 
            self.simcase.Close(False)
        return self.uniapp.Quit()   
                    
    def ReadDataTable(self,TableName):
        ''' Read Information from Process data table and convert it to a python dictionary'''
        # Look for the Process Data Table of the Hysys case
        DataTables = self.FixedDataTables(self.simcase.DataTables)
        ProcessDataTable = self.DataTable(DataTables.Item(TableName))
        ProcessDataTable.StartTransfer()
        vd = ProcessDataTable.GetAllVarDefinitions()  
        # Extract all Tags info and save it into a dict
        DataTable = {}
        idict = {}
        Values = []
        for x,value in enumerate(vd):
            vd = self.VarDefinition(value)  
            idict[vd.Tag] = vd              
            Values.append(vd.Variable.GetValue())
        ProcessDataTable.EndTransfer()  
        DataTable[TableName] = idict
        return DataTable, Values

    def WriteTagsDataTable(self, TableDict,Values,dataTableName):
        '''Write all tags to selected process data table'''
    
        # Write all the values back to the ProcessDataTable 
        DataTables = self.FixedDataTables(self.simcase.DataTables)
        ProcessDataTable = self.DataTable(DataTables.Item(dataTableName))
        ProcessDataTable.StartTransfer()
        getvalues = ProcessDataTable.GetAllValues()
        for iDataTable in TableDict:
            tempDict = TableDict[iDataTable]
            dictindex = 0
            for Tag in tempDict.values():
                vd = self.VarDefinition(Tag)    
                if (vd.accessMode == 3 or vd.accessMode == 2):                  #Write and Write/Read
                    if not(np.isnan(Values[dictindex])):
                        vd.Variable.SetValue(Values[dictindex], vd.Units) 
                dictindex +=1
        ProcessDataTable.EndTransfer()

    def Reset(self): 
        ''' Resets the Hysys simulation from a script previously defined'''
        self.uniapp.PlayScript(r'C:\Users\vdi.eebe\Desktop\TFG-main\ResetColumnPython.scp')
        return True

    def Run(self): 
        ''' Runs the Hysys simulation from a script previously defined'''
        self.uniapp.PlayScript(r'C:\Users\vdi.eebe\Desktop\TFG-main\RunColumnPython.scp')
        'This sleep is just to let the optimizer calculate, it can be checked also with a While loop'
        #time.sleep(5) 
        return True

    def Calculate(self): 
        ''' Call to Hysys optimizer '''
        # References to BackDoor Variables
        PropPkgBd = self.BackDoor(self.simcase)
        PropPkgBd.SendBackDoorMessage('Optimizer.300:Execute')
        'This sleep is jut to let the optimizer calculate, it can be checked also with a While loop'
        time.sleep(7) 
        return True

#%% Create the sampling points.
#Define the upper and lower intervals for each variable. Remember that each position "i" in vectors LOW and UP matches each variable "i" in array p.
Inputs = ['NT_T5', 'D_T5', 'RR_T5']
UP  = [18, 130 , 1.5]
LOW = [10, 70, 1]

n = 10000     #Number of samples that are required
d = len(UP)   #Number of inputs that are required

#The array "p" is normalized between 0-1.
p = latin_hypercube_normalized(d,n)

#The array "q" is not normalized. These are the sampling points. 
q = latin_hypercube_sampling(LOW,UP,p,d)
q[:,0]=q[:,0].astype(int)                           #Always keep the first input  NT (number of trays) as a natural number (int).
#%% Plot the sampling points to check everything is random
x=2
y=1

#Figure
plt.figure(figsize=[10,10])
plt.xlim([LOW[x],UP[x]])
plt.ylim([LOW[y],UP[y]])
plt.xlabel(Inputs[x])
plt.ylabel(Inputs[y])
plt.scatter(q[:,x], q[:,y], c='r', s=10)

#Create the grid so the position of the points is the one desired (just one point per column and row).
for i in np.arange(LOW[x], UP[x], 1/n*(UP[x]-LOW[x])):
  plt.axvline(i, linewidth=0.01)
for i in np.arange(LOW[y], UP[y], 1/n*(UP[y]-LOW[y])):
  plt.axhline(i, linewidth=0.01)

plt.show()

#%%
q= sorted(sorted(sorted(q,key=lambda x: x[1]),key=lambda x: -x[2]),key=lambda x: -x[0])   #Though the sample is random, the points are sorted to reduce HYSYS hysteresis
#%% Sample the data points

filepath   =r'C:\Users\vdi.eebe\Desktop\TFG-main\PE.hsc'  # HYSYS simulation
Hysyspath =r'C:\Program Files\AspenTech\Aspen HYSYS V12.0\hysys.tlb'  # HYSYS program file location

obj = HysysConnection(filepath,Hysyspath)
obj.OpenCase()
#%%
TableDict, Values = obj.ReadDataTable('ProcData1')
#%%
from datetime import datetime
start_time = datetime.now()
Results = []
Counter = 0
NaNs = 0
for x in q:
    obj.WriteTagsDataTable(TableDict,x,'ProcData1')
    obj.Run()
    Result, Values = obj.ReadDataTable('ProcData1')
    Results.append(Values)
    Counter = Counter + 1
    if Values[4] == -32767.0: #Check if the first column has converged, if it has not, reset and run a new example.
        obj.Reset() 
        NaNs += 1
    print('Number of samples:',Counter)
    print('Unfeasible samples:',NaNs)
end_time = datetime.now()
print(NaNs)

import csv 
  
# field names  
fields = list(Result[list(Result.keys())[0]].keys())
   
# data rows of csv file  
rows = Results

with open('Model', 'w') as f: 
    # using csv.writer method from CSV package 
    write = csv.writer(f) 
    write.writerow(fields) 
    write.writerows(rows) 

Data_Model  = Results

print('Time:0', end_time-start_time)

#%% 
#Results

"""
Variables with units of time are read in sec, disregarding if they are in another unit (such as h) on HYSYS.
"""

tags = list(Result[list(Result.keys())[0]].keys())
Results=pd.DataFrame(Results)
Results.columns = tags
#Save the data into Book1.xlsx 
Results.to_excel(r'C:\Users\vdi.eebe\Desktop\TFG-main\Book1.xlsx')