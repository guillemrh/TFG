'''
                            Test 1 for the                     
                    Aspen HYSYS - Python interface 
                    for spreadsheets connection
Author: Edgar Ivan Sanchez Medina
Email: sanchez@mpi-magdeburg.mpg.de
-------------------------------------------------------------------------------
Date:   05/01/2020
This is a test file for the Aspen HYSYS - Python connection using a flowsheet 
with multiple units.
'''
from Read_Spreadsheets.Hysys_connection import Aspen_connection

# 1.0 Data of the Aspen HYSYS file
File         = 'PE.hsc'
Spreadsheets = ('SS_Compressors', 'SS_HeatExchangers', 'SS_Valves', 'SS_Columns')
Units        = ('HX1', 'HX2', 'HX3', 'HX4', 'HX5',
                'K1', 'K2', 'K3',
                'T1', 'T2', 'T3', 'T4', 'T5',
                'V1', 'V2', 'V3', 'V4')

# 2.0 Perform connection
Test_1      = Aspen_connection(File, Spreadsheets, Units)
Compressors     = Test_1.SS['SS_Compressors']
Input_pressure_K1  = Compressors.Cell(0,1)      #Object: Cell(Column,Row) starting from 0,0
Output_pressure_K1  = Compressors.Cell(1,1)
ori_press     = Input_pressure_K1.CellValue     #Value of the defined object

print(ori_press)