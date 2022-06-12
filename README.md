# End of degree project.

## Abstract 

One of the main problems when simulating chemical processes is the large computational load and the high execution time required due to the complexity of these systems. This fact has given rise to new models, called surrogate models, that can simplify the same task, reducing time and computational load. In the present work, a methodology is developed to build surrogate models using machine learning algorithms, such as artificial neural networks. Two alternatives are studied to develop surrogate models, which are evaluated according to time and accuracy. In the first one, the process is treated as a holistic system, so that a single surrogate model is developed for the whole process. In the second one, the process is treated by modules (sequentially), a surrogate model is developed for every module in the process. In this second alternative, the surrogate models are connected sequentially, so that some of the output variables predicted by one model are used as input variables for the next model. Since I did not have enough data of a chemical process to train the surrogate models, a polyethylene pyrolysis process is simulated with Aspen HYSYS.

## Files

## Datasets

"T4_T5.xlsx": Result of sampling distillation columns T4 and T5 (from PE2.hsc, in HYSYS simulations folder) as a holistic system. Contains 10000 sampling points, with both input (NT, RR, D_Flow for each column) and output variables.

"Book1.xlsx": Empty .xlsx file, used to store the data generated using the Python scripts.

## Python scripts

"1_Column.py" : Connection HYSYS - Python and sampling of the data using Latin Hypercube Sampling. Contains the necessary functions to generate data from 1 single distillation column.

"2_Columns.py" : Same as 1_Column.py, but used to generate data from 2 single distillation column (sequentially, i.e., bottoms of T4 = Feed of T5).

"X_Columns.py" : Same as 2_Column.py, but can generate data from multiple (X) distillation columns (sequentially).

## Folders

## HYSYS scripts

"RunColumn4Python.SCP" : Simulates the click of the "Run" button of distillation column T4 in Aspen HYSYS. This is used to make the distillation column converge when introducing a new sampling point.

"ResetColumn4Python.SCP" : Simulates the click of the "Reset" button of distillation column T4 in Aspen HYSYS. This is used when the distillation column does not converge.

"OkCompT5.SCP" : Simulates the click of the "Ok" button of the compositions window for stream 17 (feed T5). This is used when building a modular surrogate.

## HYSYS simulations

"PE.hsc" : Complete simulation process for a waste polyethylene pyrolysis, ready to be connected with Python to generate data from distillation column T5.

"PE.hsc" : Same as PE.hsc, but it is ready to generate data from distillation columns T4 and T5 as a holistic system.

