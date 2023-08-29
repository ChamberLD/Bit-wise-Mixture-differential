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
 3 proc:     Right = 2^(-inf)
 3 proc: randRight = 2^(-inf)
 4 proc:     Right = 2^(1.000000)
 4 proc: randRight = 2^(-inf)
 5 proc:     Right = 2^(-inf)
 5 proc: randRight = 2^(-inf)
 6 proc:     Right = 2^(-inf)
 6 proc: randRight = 2^(-inf)
 7 proc:     Right = 2^(-inf)
 7 proc: randRight = 2^(-inf)
 8 proc:     Right = 2^(-inf)
 8 proc: randRight = 2^(-inf)
 9 proc:     Right = 2^(-inf)
 9 proc: randRight = 2^(-inf)
 10 proc:     Right = 2^(-inf)
 10 proc: randRight = 2^(-inf)
 11 proc:     Right = 2^(-inf)
 11 proc: randRight = 2^(-inf)
 12 proc:     Right = 2^(0.000000)
 12 proc: randRight = 2^(-inf)
 13 proc:     Right = 2^(0.000000)
 13 proc: randRight = 2^(-inf)
 14 proc:     Right = 2^(-inf)
 14 proc: randRight = 2^(-inf)
 15 proc:     Right = 2^(-inf)
 15 proc: randRight = 2^(-inf)
 16 proc:     Right = 2^(-inf)
 16 proc: randRight = 2^(-inf)
 17 proc:     Right = 2^(-inf)
 17 proc: randRight = 2^(-inf)
 18 proc:     Right = 2^(-inf)
 18 proc: randRight = 2^(-inf)
 19 proc:     Right = 2^(-inf)
 19 proc: randRight = 2^(-inf)
 20 proc:     Right = 2^(2.000000)
 20 proc: randRight = 2^(-inf)
 21 proc:     Right = 2^(-inf)
 21 proc: randRight = 2^(-inf)
 22 proc:     Right = 2^(-inf)
 22 proc: randRight = 2^(-inf)
 23 proc:     Right = 2^(-inf)
 23 proc: randRight = 2^(-inf)
 24 proc:     Right = 2^(-inf)
 24 proc: randRight = 2^(-inf)
 25 proc:     Right = 2^(-inf)
 25 proc: randRight = 2^(-inf)
 26 proc:     Right = 2^(-inf)
 26 proc: randRight = 2^(-inf)
 27 proc:     Right = 2^(-inf)
 27 proc: randRight = 2^(-inf)
 28 proc:     Right = 2^(-inf)
 28 proc: randRight = 2^(-inf)
 29 proc:     Right = 2^(-inf)
 29 proc: randRight = 2^(-inf)
 30 proc:     Right = 2^(-inf)
 30 proc: randRight = 2^(-inf)
 31 proc:     Right = 2^(3.000000)
 31 proc: randRight = 2^(-inf)
 32 proc:     Right = 2^(-inf)
 32 proc: randRight = 2^(-inf)
 33 proc:     Right = 2^(-inf)
 33 proc: randRight = 2^(-inf)
 34 proc:     Right = 2^(-inf)
 34 proc: randRight = 2^(-inf)
 35 proc:     Right = 2^(-inf)
 35 proc: randRight = 2^(-inf)
 36 proc:     Right = 2^(-inf)
 36 proc: randRight = 2^(-inf)
 37 proc:     Right = 2^(-inf)
 37 proc: randRight = 2^(-inf)
 38 proc:     Right = 2^(-inf)
 38 proc: randRight = 2^(-inf)
 39 proc:     Right = 2^(-inf)
 39 proc: randRight = 2^(-inf)
 40 proc:     Right = 2^(-inf)
 40 proc: randRight = 2^(-inf)
 41 proc:     Right = 2^(-inf)
 41 proc: randRight = 2^(-inf)
 42 proc:     Right = 2^(-inf)
 42 proc: randRight = 2^(-inf)
 43 proc:     Right = 2^(-inf)
 43 proc: randRight = 2^(-inf)
 44 proc:     Right = 2^(-inf)
 44 proc: randRight = 2^(-inf)
 45 proc:     Right = 2^(-inf)
 45 proc: randRight = 2^(-inf)
 46 proc:     Right = 2^(4.000000)
 46 proc: randRight = 2^(-inf)
 47 proc:     Right = 2^(-inf)
 47 proc: randRight = 2^(-inf)
 48 proc:     Right = 2^(-inf)
 48 proc: randRight = 2^(-inf)
 49 proc:     Right = 2^(-inf)
 49 proc: randRight = 2^(-inf)
 50 proc:     Right = 2^(2.000000)
 50 proc: randRight = 2^(-inf)
 51 proc:     Right = 2^(-inf)
 51 proc: randRight = 2^(-inf)
 52 proc:     Right = 2^(6.569856)
 52 proc: randRight = 2^(-inf)
 53 proc:     Right = 2^(3.321928)
 53 proc: randRight = 2^(-inf)
 54 proc:     Right = 2^(1.584963)
 54 proc: randRight = 2^(-inf)
 55 proc:     Right = 2^(-inf)
 55 proc: randRight = 2^(-inf)
 56 proc:     Right = 2^(-inf)
 56 proc: randRight = 2^(-inf)
 57 proc:     Right = 2^(-inf)
 57 proc: randRight = 2^(-inf)
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
