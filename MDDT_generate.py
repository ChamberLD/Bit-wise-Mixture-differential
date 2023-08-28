"""
Function: MDDT generation for & operation
Date: 2022/02/25
Author: Zehan Wu
Contact:
"""

import sys
import numpy as np
import pandas as pd
#输入混合差分模式变量进行编码
c2_c1_c0 = ["000","111","100","010","001","011","101","110"]
d2_d1_d0 = ["000","111","100","010","001","011","101","110"]

al3_al2_al1_al0 = np.arange(4)
bl3_bl2_bl1_bl0 = np.arange(4)
ar3_ar2_ar1_ar0 = np.arange(4)
br3_br2_br1_br0 = np.arange(4)



print('#############################################')
################################################################################
Truth_table = pd.DataFrame(np.full((64,8),0))
#列名与行名
Truth_table.columns = ["000","111","100","010","001","011","101","110"]
Truth_table.index = ["000 000","000 111","000 100","000 010","000 001","000 011","000 101","000 110",
                     "111 000","111 111","111 100","111 010","111 001","111 011","111 101","111 110",
                     "100 000","100 111","100 100","100 010","100 001","100 011","100 101","100 110",
                     "010 000","010 111","010 100","010 010","010 001","010 011","010 101","010 110",
                     "001 000","001 111","001 100","001 010","001 001","001 011","001 101","001 110",
                     "011 000","011 111","011 100","011 010","011 001","011 011","011 101","011 110",
                     "101 000","101 111","101 100","101 010","101 001","101 011","101 101","101 110",
                     "110 000","110 111","110 100","110 010","110 001","110 011","110 101","110 110",]
#print(Truth_table)
print("#############################################")

#########################################################################################
#############对所有的混合输入差分模式进行遍历操作,生成真值表###################################
#########################################################################################
index = 0
for i in range(0,8):
    al3_al2_al1_al0[0] = 0
    bl3_bl2_bl1_bl0[0] = 1
    for m in range(0, 3):
        if c2_c1_c0[i][m] == "1":
            al3_al2_al1_al0[m + 1] = al3_al2_al1_al0[0] ^ 1
            bl3_bl2_bl1_bl0[m + 1] = bl3_bl2_bl1_bl0[0] ^ 1
        else:
            al3_al2_al1_al0[m + 1] = al3_al2_al1_al0[0]
            bl3_bl2_bl1_bl0[m + 1] = bl3_bl2_bl1_bl0[0]
    for j in range(0,8):
        ar3_ar2_ar1_ar0[0] = 0
        br3_br2_br1_br0[0] = 1
        for k in range(0,3):
            if d2_d1_d0[j][k] == "1":
                ar3_ar2_ar1_ar0[k + 1] = ar3_ar2_ar1_ar0[0] ^ 1
                br3_br2_br1_br0[k + 1] = br3_br2_br1_br0[0] ^ 1
            else:
                ar3_ar2_ar1_ar0[k + 1] = ar3_ar2_ar1_ar0[0]
                br3_br2_br1_br0[k + 1] = br3_br2_br1_br0[0]
        print(c2_c1_c0[i]+" & " +d2_d1_d0[j]+":")
        ao3_ao2_ao1_ao0_4 = np.arange(4)
        ao3_ao2_ao1_ao0_3 = np.arange(4)
        ao3_ao2_ao1_ao0_2 = np.arange(4)
        ao3_ao2_ao1_ao0_1 = np.arange(4)
        for n in range(0, 4):
            ao3_ao2_ao1_ao0_4[n] = al3_al2_al1_al0[n] and ar3_ar2_ar1_ar0[n]
            ao3_ao2_ao1_ao0_3[n] = al3_al2_al1_al0[n] and br3_br2_br1_br0[n]
            ao3_ao2_ao1_ao0_2[n] = bl3_bl2_bl1_bl0[n] and ar3_ar2_ar1_ar0[n]
            ao3_ao2_ao1_ao0_1[n] = bl3_bl2_bl1_bl0[n] and br3_br2_br1_br0[n]
        for s in range(1,5):
            locals()['e2_e1_e0_' + str(s)] = np.arange(3)
            for p in range(1,4):
                if (locals()['ao3_ao2_ao1_ao0_'+str(s)])[0] == (locals()['ao3_ao2_ao1_ao0_'+str(s)])[p]:
                    locals()['e2_e1_e0_'+str(s)][p-1] = 0
                else:
                    locals()['e2_e1_e0_' + str(s)][p-1] = 1
            print(locals()['e2_e1_e0_' + str(s)])
            #000
            if (locals()['e2_e1_e0_' + str(s)][0]) == 0 and (locals()['e2_e1_e0_' + str(s)][1]) == 0 and (locals()['e2_e1_e0_' + str(s)][2]) == 0 :
                Truth_table.iloc[index][0] = Truth_table.iloc[index][0] + 1
            #111
            if (locals()['e2_e1_e0_' + str(s)][0]) == 1 and (locals()['e2_e1_e0_' + str(s)][1]) == 1 and (locals()['e2_e1_e0_' + str(s)][2]) == 1:
                Truth_table.iloc[index][1] = Truth_table.iloc[index][1] + 1
            #100
            if (locals()['e2_e1_e0_' + str(s)][0]) == 1 and (locals()['e2_e1_e0_' + str(s)][1]) == 0 and (locals()['e2_e1_e0_' + str(s)][2]) == 0:
                Truth_table.iloc[index][2] = Truth_table.iloc[index][2] + 1
            #010
            if (locals()['e2_e1_e0_' + str(s)][0]) == 0 and (locals()['e2_e1_e0_' + str(s)][1]) == 1 and (locals()['e2_e1_e0_' + str(s)][2]) == 0:
                Truth_table.iloc[index][3] = Truth_table.iloc[index][3] + 1
            #001
            if (locals()['e2_e1_e0_' + str(s)][0]) == 0 and (locals()['e2_e1_e0_' + str(s)][1]) == 0 and (locals()['e2_e1_e0_' + str(s)][2]) == 1:
                Truth_table.iloc[index][4] = Truth_table.iloc[index][4] + 1
            #011
            if (locals()['e2_e1_e0_' + str(s)][0]) == 0 and (locals()['e2_e1_e0_' + str(s)][1]) == 1 and (locals()['e2_e1_e0_' + str(s)][2]) == 1:
                Truth_table.iloc[index][5] = Truth_table.iloc[index][5] + 1
            #101
            if (locals()['e2_e1_e0_' + str(s)][0]) == 1 and (locals()['e2_e1_e0_' + str(s)][1]) == 0 and (locals()['e2_e1_e0_' + str(s)][2]) == 1:
                Truth_table.iloc[index][6] = Truth_table.iloc[index][6] + 1
            #110
            if (locals()['e2_e1_e0_' + str(s)][0]) == 1 and (locals()['e2_e1_e0_' + str(s)][1]) == 1  and (locals()['e2_e1_e0_' + str(s)][2]) == 0:
                Truth_table.iloc[index][7] = Truth_table.iloc[index][7] + 1
        index = index + 1
#展示真值表的所有行
pd.set_option('display.max_rows', None)
print("#####################################################")
print("Truth_table: ")
print(Truth_table)
print("#####################################################"
      "#####################################################")
####################################################################################
################生成c2,c1,c0,d2,d1,d0,e2,e1,e0,ph,pl的11维可行点集####################
####################################################################################
Feasible_point = []
print("Feasible_point:  ")
for i in range(0,64):
    for j in range(0,8):
        if Truth_table.iloc[i][j] == 1:
            c2 = int(Truth_table.index[i][0]); c1 = int(Truth_table.index[i][1]); c0 = int(Truth_table.index[i][2])
            d2 = int(Truth_table.index[i][4]); d1 = int(Truth_table.index[i][5]); d0 = int(Truth_table.index[i][6])
            e2 = int(Truth_table.columns[j][0]); e1 = int(Truth_table.columns[j][1]); e0 = int(Truth_table.columns[j][2])
            ph = 1; pl = 0
            Feasible_point.append([c2,c1,c0,d2,d1,d0,e2,e1,e0,ph,pl])
            print([c2, c1, c0, d2, d1, d0, e2, e1, e0, ph, pl])
        if Truth_table.iloc[i][j] == 2:
            c2 = int(Truth_table.index[i][0]); c1 = int(Truth_table.index[i][1]); c0 = int(Truth_table.index[i][2])
            d2 = int(Truth_table.index[i][4]); d1 = int(Truth_table.index[i][5]); d0 = int(Truth_table.index[i][6])
            e2 = int(Truth_table.columns[j][0]); e1 = int(Truth_table.columns[j][1]); e0 = int(Truth_table.columns[j][2])
            ph = 0; pl = 1
            Feasible_point.append([c2, c1, c0, d2, d1, d0, e2, e1, e0, ph, pl])
            print([c2, c1, c0, d2, d1, d0, e2, e1, e0, ph, pl])
        if Truth_table.iloc[i][j] == 4:
            c2 = int(Truth_table.index[i][0]); c1 = int(Truth_table.index[i][1]); c0 = int(Truth_table.index[i][2])
            d2 = int(Truth_table.index[i][4]); d1 = int(Truth_table.index[i][5]); d0 = int(Truth_table.index[i][6])
            e2 = int(Truth_table.columns[j][0]); e1 = int(Truth_table.columns[j][1]); e0 = int(Truth_table.columns[j][2])
            ph = 0; pl = 0
            Feasible_point.append([c2, c1, c0, d2, d1, d0, e2, e1, e0, ph, pl])
            print([c2, c1, c0, d2, d1, d0, e2, e1, e0, ph, pl])
#########################################

array = np.array(Feasible_point)
df = pd.DataFrame(array)
df.to_csv('Feasible_point.csv')

