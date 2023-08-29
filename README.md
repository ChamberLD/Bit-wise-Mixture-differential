# Bit-wise-Mixture-differential
All code used in paper "Bit-wise Mixture Differential Cryptanalysis and Its Application to SIMON" and the contents of the attachment

## SIMON
The SIMON folder contains the code for the automated search of SIMON's Mixture Differential Distinguisher for 5 versions.

By adjusting the function's parameter 1 and parameter 2 it is possible to find mixture differential trails with probability less than or equal to parameter 2 for different numbers of rounds.

`gen_objectfuntion_Constraint(9, 34)` //round， probability

`pycryptosat.Solver(threads=1)` //adjusting the number of CPU cores used

To run our codes preinstallation is SAT for solving constraint programming problems. You can run the code in the background on a linux system using the following command:

`nohup python SIMONXXX.py &`

output:
```
L_1r_0_c2:  False  L_1r_0_c1:  False  L_1r_0_c0:  False
R_1r_0_c2:  False  R_1r_0_c1:  False  R_1r_0_c0:  False
######################    AND运算   ########################
SR1_1r_0_c2:  True  SR1_1r_0_c1:  False  SR1_1r_0_c0:  True
SR8_1r_0_c2:  False  SR8_1r_0_c1:  False  SR8_1r_0_c0:  False
aftAnd_1r_0_c2:  False  aftAnd_1r_0_c1:  False  aftAnd_1r_0_c0:  False
ProaftAnd_1r_0_ph:  False  ProaftAnd_1r_0_pl:  True
...
...
L_23r_17_c2:  False  L_23r_17_c1:  True  L_23r_17_c0:  True
L_23r_18_c2:  False  L_23r_18_c1:  False  L_23r_18_c0:  False
L_23r_19_c2:  False  L_23r_19_c1:  False  L_23r_19_c0:  False
L_23r_20_c2:  False  L_23r_20_c1:  False  L_23r_20_c0:  False
L_23r_21_c2:  False  L_23r_21_c1:  True  L_23r_21_c0:  True
L_23r_22_c2:  False  L_23r_22_c1:  False  L_23r_22_c0:  False
L_23r_23_c2:  False  L_23r_23_c1:  False  L_23r_23_c0:  False
L_23r_24_c2:  False  L_23r_24_c1:  False  L_23r_24_c0:  False
L_23r_25_c2:  False  L_23r_25_c1:  False  L_23r_25_c0:  False
L_23r_26_c2:  False  L_23r_26_c1:  False  L_23r_26_c0:  False
L_23r_27_c2:  False  L_23r_27_c1:  False  L_23r_27_c0:  False
L_23r_28_c2:  False  L_23r_28_c1:  False  L_23r_28_c0:  False
L_23r_29_c2:  False  L_23r_29_c1:  False  L_23r_29_c0:  False
L_23r_30_c2:  False  L_23r_30_c1:  False  L_23r_30_c0:  False
L_23r_31_c2:  False  L_23r_31_c1:  False  L_23r_31_c0:  False
142
```


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

## attachment
in this 
