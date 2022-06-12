# End of degree project.

## Abstract 

One of the main problems when simulating chemical processes is the large computational load and the high execution time required due to the complexity of these systems. This fact has given rise to new models, called surrogate models, that can simplify the same task, reducing time and computational load. In the present work, a methodology will be developed to apply substitution methods using autonomous learning algorithms, known as artificial neural networks. Two alternatives will be studied to develop surrogate models, which will be evaluated according to time and accuracy. In the first one, the process will be treated as a holistic, so that a single surrogate model representing the whole process will be developed. In the second, the process will be treated by modules (sequentially), so that as many surrogate models will be developed as there are modules in the process. In this second alternative, the surrogate models will be connected sequentially, so that some of the output variables predicted by one model will be used as input variables for the next model. Since I did not have enough data of a chemical process to train the surrogate models, a polyethylene pyrolysis process will be simulated with Aspen HYSYS.

## Files

## Datasets:

"T4_T5.xlsx": Result of sampling distillation columns T4 and T5 (from PE2.hsc, in HYSYS simulations folder) as a holistic. Contains 10000 sampling points, with both input (NT, RR, D_Flow for each column) and output variables.

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

"PE.hsc" : Same as PE.hsc, but it is ready to generate data from distillation columns T4 and T5 as a holistic.

