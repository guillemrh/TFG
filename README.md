# End of degree project.

## Abstract 

One of the main problems when performing chemical process simulations is the large computational load and the high execution time required due to the complexity of these systems. This is especially problematic in the current paradigm, where the connection of these simulations could contribute to the identification of opportunities for industrial symbiosis and thus accelerate the transition towards a circular economy. Particularly promising in this context are new models, called surrogate models, which can simplify the simulation task itself, reducing its time and computational burden.

In this paper, a methodology will be developed to apply surrogate models using machine learning algorithms, namely those known as artificial neural networks. First, the lack of sufficient literature data to train the surrogate models will lead us to simulate the polyethylene pyrolysis process with Aspen HYSYS. Subsequently, two alternatives will be studied to develop surrogate methods for this simulation. In the first, the process will be treated as a holistic system, so a single surrogate model representing the entire process will be developed. In the second alternative, the process will be treated in modules (sequentially), so as many surrogate models will be developed as modules are carried out in the process. In this second alternative, the surrogate models will be connected sequentially, so that some of the output variables predicted by one model will be used as input variables for the model of the next module. Finally, both alternatives will be compared according to the time and accuracy they achieve.

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

