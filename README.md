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

To run distinguisher verification code, preinstallation is MPI. To test the 9-round mixture differential trails on SIMON32, firstly compile:

`mpicxx SIMON3264_Quadruple_MPI_RNG.cpp SIMON3264.cpp --std=c++11 -Wall -O3 -o SIMON32_9r`

then run:

`mpirun -np 8 ./SIMON32_9r`

output:
 ```
 Quaries on each process = 2^(32.000000)
 0 proc:     Right = 2^(-inf)
 0 proc: randRight = 2^(-inf)
 1 proc:     Right = 2^(-inf)
 1 proc: randRight = 2^(-inf)
 2 proc:     Right = 2^(-inf)
 2 proc: randRight = 2^(-inf)
...
 58 proc:     Right = 2^(-inf)
 58 proc: randRight = 2^(-inf)
 59 proc:     Right = 2^(1.000000)
 59 proc: randRight = 2^(-inf)
 60 proc:     Right = 2^(-inf)
 60 proc: randRight = 2^(-inf)
 61 proc:     Right = 2^(0.000000)
 61 proc: randRight = 2^(-inf)
 62 proc:     Right = 2^(-inf)
 62 proc: randRight = 2^(-inf)
 63 proc:     Right = 2^(-inf)
 63 proc: randRight = 2^(-inf)

                              Total queries = 2^(38.000000) 
SIMON32:     Number of total right quadruples = 2^(7.199672)
           Probability of right quadruples  = 2^(-30.8003)
 RandPerm: Number of total right quadruples = 2^(-inf)
            Probability of right quadruples = 2^(-inf)
 time on clock(): 4593.67
 ```
