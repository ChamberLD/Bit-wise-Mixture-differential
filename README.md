# Bit-wise-Mixture-differential
All code used in paper "Bit-wise Mixture Differential Cryptanalysis and Its Application to SIMON" and the contents of the attachment

## SIMON
The SIMON folder contains the code for the automated search of SIMON's Mixture Differential Distinguisher for 5 versions.

By adjusting the function's parameter 1 and parameter 2 it is possible to find mixture differential trails with probability less than or equal to parameter 2 for different numbers of rounds.

`gen_objectfuntion_Constraint(9, 34)` //round， probability

`pycryptosat.Solver(threads=1)` //adjusting the number of CPU cores used

To run our codes preinstallation is SAT for solving constraint programming problems. You can run the code in the background on a linux system using the following command:

`nohup python SIMONXXX.py &`


## verify
In folder verify, we verified the obtained mixture differential trails under multip keys.
