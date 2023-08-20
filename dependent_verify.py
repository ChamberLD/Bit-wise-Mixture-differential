"""
Function: verify  AND operantion dependent inputs
Date: 2022/03/27
Author: Zehan Wu
Contact:
"""
import sys
import numpy as np
import pandas as pd
import csv
#验证MDDT中因为bit移位带来的影响
#定义输入差分模式Mixture_pattern
Mixture_pattern = ['000', '111', '100', '010', '001', '011', '101', '110']
bin = [0, 1]
#count1用于记录有多少种22模式,count2用于记录22模式种有多少种是有依赖的
count1 = 0
count2 = 0

#遍历输入差分a0
for i in range(0, 8):
    a0 = Mixture_pattern[i]
    for j in range(0, 8):
        a1 = Mixture_pattern[j]
        for k in range(0, 8):      #确定某一组a0,a1,a2
            a2 = Mixture_pattern[k]
            print('a0:  %s' % a0)
            print('a1:  %s' % a1)
            print('a2:  %s' % a2)
            x_0_0 = 0                       #x_0_0表示四元组中第一组的第0比特
            # 首先计算x_1_0, x_2_0, x_3_0, 比特0的四元组
            if a0[0] == '0':  # x_1_0
                x_1_0 = 0
            else:
                x_1_0 = 1
            if a0[1] == '0':  # x_2_0
                x_2_0 = 0
            else:
                x_2_0 = 1
            if a0[2] == '0':  # x_3_0
                x_3_0 = 0
            else:
                x_3_0 = 1
            #用一个字典来记录每一个小循环中β1和β2的值
            dict = {}
            print("################### β1 ##################")
            for m in range(0, 2):
                x_0_1 = bin[m]           #x_0_1表示四元组中第一组的第1比特
                #计算相应的混合差分模式
                #计算x_1_1, x_2_1, x_3_1,  比特1的四元组
                if a1[0] == '0':   #x_1_1
                    x_1_1 = bin[m]
                else:
                    x_1_1 = 1-bin[m]
                if a1[1] == '0':   #x_2_1
                    x_2_1 = bin[m]
                else:
                    x_2_1 = 1-bin[m]
                if a1[2] == '0':   #x_3_1
                    x_3_1 = bin[m]
                else:
                    x_3_1 = 1-bin[m]
                #根据得到的各个明文组的值来计算&值，用And_0_01, AND_1_01, AND_2_01, AND_3_01来表示具体的&值
                And_0_01 = x_0_0 & x_0_1
                And_1_01 = x_1_0 & x_1_1
                And_2_01 = x_2_0 & x_2_1
                And_3_01 = x_3_0 & x_3_1
                #计算输出混合差分，用diff_out来表示, diff_out是个三元码
                if And_0_01 == And_1_01:    #计算c2
                    diff_out_c2 = '0'
                else:
                    diff_out_c2 = '1'
                if And_0_01 == And_2_01:    #计算c1
                    diff_out_c1 = '0'
                else:
                    diff_out_c1 = '1'
                if And_0_01 == And_3_01:    #计算c0
                    diff_out_c0 = '0'
                else:
                    diff_out_c0 = '1'
                diff_out = diff_out_c2 + diff_out_c1 + diff_out_c0
                dict["diff_β1_1_" + str(m)] = diff_out      #这个表示β1的第一个袋子里的取值
                print(diff_out)
                #记录一下β1有几种混合差分模式，方便后面进行比对
            if dict["diff_β1_1_0"] == dict["diff_β1_1_1"]:
                count_1_1 = 1           #count_1_1 表示β1的第一类取值的个数、
            else:
                count_1_1 = 2
            print("################### β2 ##################")
            for n in range(0, 2):
                x_0_2 = bin[n]              #x_0_2表示四元组中的第2比特
                # 计算x_1_2, x_2_2, x_3_2,  比特2的四元组
                if a2[0] == '0':  # x_1_2
                    x_1_2 = bin[n]
                else:
                    x_1_2 = 1-bin[n]
                if a2[1] == '0':  # x_2_2
                    x_2_2 = bin[n]
                else:
                    x_2_2 = 1-bin[n]
                if a2[2] == '0':  # x_3_2
                    x_3_2 = bin[n]
                else:
                    x_3_2 = 1-bin[n]
                # 根据得到的各个明文组的值来计算&值，用And_0_02, AND_1_02, AND_2_02, AND_3_02来表示具体的&值
                And_0_02 = x_0_0 & x_0_2
                And_1_02 = x_1_0 & x_1_2
                And_2_02 = x_2_0 & x_2_2
                And_3_02 = x_3_0 & x_3_2
                # 计算输出混合差分，用diff_out来表示, diff_out是个三元码
                if And_0_02 == And_1_02:  # 计算c2
                    diff_out_c2 = '0'
                else:
                    diff_out_c2 = '1'
                if And_0_02 == And_2_02:  # 计算c1
                    diff_out_c1 = '0'
                else:
                    diff_out_c1 = '1'
                if And_0_02 == And_3_02:  # 计算c0
                    diff_out_c0 = '0'
                else:
                    diff_out_c0 = '1'
                diff_out = diff_out_c2 + diff_out_c1 + diff_out_c0
                dict["diff_β2_1_" + str(n)] = diff_out          ##这个表示β2的第一个袋子里的取值
                print(diff_out)
            # 记录一下β2有几种混合差分模式，方便后面进行比对
            if dict["diff_β2_1_0"] == dict["diff_β2_1_1"]:
                count_2_1 = 1  # count_2_1 表示β2的第一类取值的个数、
            else:
                count_2_1 = 2
            x_0_0 = 1                                       #x_0_0 = 1  比特的另一种取值#################################
            # 首先计算x_1_0, x_2_0, x_3_0, 比特0的四元组
            if a0[0] == '0':  # x_1_0
                x_1_0 = 1
            else:
                x_1_0 = 0
            if a0[1] == '0':  # x_2_0
                x_2_0 = 1
            else:
                x_2_0 = 0
            if a0[2] == '0':  # x_3_0
                x_3_0 = 1
            else:
                x_3_0 = 0
            print("################### β1 ##################")
            for s in range(0, 2):
                x_0_1 = bin[s]
                #计算相应的混合差分模式
                # 计算x_1_1, x_2_1, x_3_1,  比特1的四元组
                if a1[0] == '0':  # x_1_1
                    x_1_1 = bin[s]
                else:
                    x_1_1 = 1-bin[s]
                if a1[1] == '0':  # x_2_1
                    x_2_1 = bin[s]
                else:
                    x_2_1 = 1-bin[s]
                if a1[2] == '0':  # x_3_1
                    x_3_1 = bin[s]
                else:
                    x_3_1 = 1-bin[s]
                # 根据得到的各个明文组的值来计算&值，用And_0_01, AND_1_01, AND_2_01, AND_3_01来表示具体的&值
                And_0_01 = x_0_0 & x_0_1
                And_1_01 = x_1_0 & x_1_1
                And_2_01 = x_2_0 & x_2_1
                And_3_01 = x_3_0 & x_3_1
                # 计算输出混合差分，用diff_out来表示, diff_out是个三元码
                if And_0_01 == And_1_01:  # 计算c2
                    diff_out_c2 = '0'
                else:
                    diff_out_c2 = '1'
                if And_0_01 == And_2_01:  # 计算c1
                    diff_out_c1 = '0'
                else:
                    diff_out_c1 = '1'
                if And_0_01 == And_3_01:  # 计算c0
                    diff_out_c0 = '0'
                else:
                    diff_out_c0 = '1'
                diff_out = diff_out_c2 + diff_out_c1 + diff_out_c0
                dict["diff_β1_2_" + str(s)] = diff_out          #这个表示β1的第二个袋子里的取值
                print(diff_out)
            # 记录一下β1有几种混合差分模式，方便后面进行比对
            if dict["diff_β1_2_0"] == dict["diff_β1_2_1"]:
                count_1_2 = 1  # count_1_2 表示β1的第二类取值的个数、
            else:
                count_1_2 = 2
            print("################### β2 ##################")
            for t in range(0, 2):
                x_0_2 = bin[t]
                #计算相应的混合差分模式
                # 计算x_1_2, x_2_2, x_3_2,  比特2的四元组
                if a2[0] == '0':  # x_1_2
                    x_1_2 = bin[t]
                else:
                    x_1_2 = 1-bin[t]
                if a2[1] == '0':  # x_2_2
                    x_2_2 = bin[t]
                else:
                    x_2_2 = 1-bin[t]
                if a2[2] == '0':  # x_3_2
                    x_3_2 = bin[t]
                else:
                    x_3_2 = 1-bin[t]
                # 根据得到的各个明文组的值来计算&值，用And_0_02, AND_1_02, AND_2_02, AND_3_02来表示具体的&值
                And_0_02 = x_0_0 & x_0_2
                And_1_02 = x_1_0 & x_1_2
                And_2_02 = x_2_0 & x_2_2
                And_3_02 = x_3_0 & x_3_2
                # 计算输出混合差分，用diff_out来表示, diff_out是个三元码
                if And_0_02 == And_1_02:  # 计算c2
                    diff_out_c2 = '0'
                else:
                    diff_out_c2 = '1'
                if And_0_02 == And_2_02:  # 计算c1
                    diff_out_c1 = '0'
                else:
                    diff_out_c1 = '1'
                if And_0_02 == And_3_02:  # 计算c0
                    diff_out_c0 = '0'
                else:
                    diff_out_c0 = '1'
                diff_out = diff_out_c2 + diff_out_c1 + diff_out_c0
                dict["diff_β2_2_" + str(t)] = diff_out      #表示β2的第二个袋子的值
                print(diff_out)
            # 记录一下β2有几种混合差分模式，方便后面进行比对
            if dict["diff_β2_2_0"] == dict["diff_β2_2_1"]:
                count_2_2 = 1  # count_2_2 表示β2的第一类取值的个数、
            else:
                count_2_2 = 2
            ###################计算两个β1，β2的两个袋子中分别有几种值，因为只有1，2，4三种值
            count_1 = 2
            count_2 = 2
            #若比特对应的四个值都不想等，则count_1和count_2都赋值为4
            x = [dict["diff_β1_1_0"], dict["diff_β1_1_1"], dict["diff_β1_2_0"], dict["diff_β1_2_1"]]
            k1 = len(set(x))        #集合中不保留重复元素，可以判断四个值是否完全相同
            k2 = len(x)
            if k1 == k2:
                count_1 = 4
            y = [dict["diff_β2_1_0"], dict["diff_β2_1_1"], dict["diff_β2_2_0"], dict["diff_β2_2_1"]]
            k3 = len(set(y))
            k4 = len(y)
            if k3 == k4:
                count_2 = 4
            #若比特对应的四个值都相等，则count_1和count_2都赋值为1
            if dict["diff_β1_1_0"] == dict["diff_β1_1_1"] == dict["diff_β1_2_0"] == dict["diff_β1_2_1"]:
                count_1 = 1
            if dict["diff_β2_1_0"] == dict["diff_β2_1_1"] == dict["diff_β2_2_0"] == dict["diff_β2_2_1"]:
                count_2 = 1
            print('########################################'
                  '########################################'
                  '######################', count_1, count_2 )

            # 根据依赖的分布情况，生成存在依赖的差分的可行的传播模式
            #根据count_1与count_2的值来判断可行的传播模式
            if count_1 == 1 and count_2 == 1:       #1-1
                print(a0, a1, a2, dict["diff_β1_1_0"], dict["diff_β2_1_0"], 0)          #最后的0表示当前差分传播模式不存在依赖
                output_list = list(a0 + a1 + a2 + dict["diff_β1_1_0"] + dict["diff_β2_1_0"] + "0")
                # 将可行的依赖差分传播模式写入CSV文件中
                with open("dependent_And.csv", "a+", newline="") as csvfile:
                    writer = csv.writer(csvfile)
                    # 将每行写入
                    writer.writerow(output_list)
            if count_1 == 1 and count_2 == 2:       #1-2
                print(a0, a1, a2, dict["diff_β1_1_0"], dict["diff_β2_1_0"], 0)
                print(a0, a1, a2, dict["diff_β1_2_0"], dict["diff_β2_2_0"], 0)
                output_list_1 = list(a0 + a1 + a2 + dict["diff_β1_1_0"] + dict["diff_β2_1_0"] + "0")
                output_list_2 = list(a0 + a1 + a2 + dict["diff_β1_2_0"] + dict["diff_β2_2_0"] + "0")
                # 将可行的依赖差分传播模式写入CSV文件中
                with open("dependent_And.csv", "a+", newline="") as csvfile:
                    writer = csv.writer(csvfile)
                    # 将每行写入
                    writer.writerow(output_list_1)
                    writer.writerow(output_list_2)
            if count_1 == 2 and count_2 == 1:       #2-1
                print(a0, a1, a2, dict["diff_β1_1_0"], dict["diff_β2_1_0"], 0)
                print(a0, a1, a2, dict["diff_β1_2_0"], dict["diff_β2_2_0"], 0)
                output_list_1 = list(a0 + a1 + a2 + dict["diff_β1_1_0"] + dict["diff_β2_1_0"] + "0")
                output_list_2 = list(a0 + a1 + a2 + dict["diff_β1_2_0"] + dict["diff_β2_2_0"] + "0")
                # 将可行的依赖差分传播模式写入CSV文件中
                with open("dependent_And.csv", "a+", newline="") as csvfile:
                    writer = csv.writer(csvfile)
                    # 将每行写入
                    writer.writerow(output_list_1)
                    writer.writerow(output_list_2)
            if count_1 == 2 and count_2 == 2:   #2-2
                count1 = count1 + 1
                #2-2中存在有差分依赖性和无差分依赖性两种情况
                if dict["diff_β1_1_0"] == dict["diff_β1_1_1"]:      #有差分依赖性，有两种传播模式不能取
                    count2 = count2 + 1
                    print(a0, a1, a2, dict["diff_β1_1_0"], dict["diff_β2_1_0"], 1)
                    print(a0, a1, a2, dict["diff_β1_2_0"], dict["diff_β2_2_0"], 1)
                    output_list_1 = list(a0 + a1 + a2 + dict["diff_β1_1_0"] + dict["diff_β2_1_0"] + "1")
                    output_list_2 = list(a0 + a1 + a2 + dict["diff_β1_2_0"] + dict["diff_β2_2_0"] + "1")
                    # 将可行的依赖差分传播模式写入CSV文件中
                    with open("dependent_And.csv", "a+", newline="") as csvfile:
                        writer = csv.writer(csvfile)
                        # 将每行写入
                        writer.writerow(output_list_1)
                        writer.writerow(output_list_2)
                else:
                    print(a0, a1, a2, dict["diff_β1_1_0"], dict["diff_β2_1_0"], 0)
                    print(a0, a1, a2, dict["diff_β1_1_0"], dict["diff_β2_1_1"], 0)
                    print(a0, a1, a2, dict["diff_β1_1_1"], dict["diff_β2_1_0"], 0)
                    print(a0, a1, a2, dict["diff_β1_1_1"], dict["diff_β2_1_1"], 0)
                    output_list_1 = list(a0 + a1 + a2 + dict["diff_β1_1_0"] + dict["diff_β2_1_0"] + "0")
                    output_list_2 = list(a0 + a1 + a2 + dict["diff_β1_1_0"] + dict["diff_β2_1_1"] + "0")
                    output_list_3 = list(a0 + a1 + a2 + dict["diff_β1_1_1"] + dict["diff_β2_1_0"] + "0")
                    output_list_4 = list(a0 + a1 + a2 + dict["diff_β1_1_1"] + dict["diff_β2_1_1"] + "0")
                    # 将可行的依赖差分传播模式写入CSV文件中
                    with open("dependent_And.csv", "a+", newline="") as csvfile:
                        writer = csv.writer(csvfile)
                        # 将每行写入
                        writer.writerow(output_list_1)
                        writer.writerow(output_list_2)
                        writer.writerow(output_list_3)
                        writer.writerow(output_list_4)
            if count_1 == 2 and count_2 == 4:   #2-4
                print(a0, a1, a2, dict["diff_β1_1_0"], dict["diff_β2_1_0"], 0)
                print(a0, a1, a2, dict["diff_β1_1_0"], dict["diff_β2_1_1"], 0)
                print(a0, a1, a2, dict["diff_β1_1_1"], dict["diff_β2_1_0"], 0)
                print(a0, a1, a2, dict["diff_β1_1_1"], dict["diff_β2_1_1"], 0)
                print(a0, a1, a2, dict["diff_β1_2_0"], dict["diff_β2_2_0"], 0)
                print(a0, a1, a2, dict["diff_β1_2_0"], dict["diff_β2_2_1"], 0)
                print(a0, a1, a2, dict["diff_β1_2_1"], dict["diff_β2_2_0"], 0)
                print(a0, a1, a2, dict["diff_β1_2_1"], dict["diff_β2_2_1"], 0)
                output_list_1 = list(a0 + a1 + a2 + dict["diff_β1_1_0"] + dict["diff_β2_1_0"] + "0")
                output_list_2 = list(a0 + a1 + a2 + dict["diff_β1_1_0"] + dict["diff_β2_1_1"] + "0")
                output_list_3 = list(a0 + a1 + a2 + dict["diff_β1_1_1"] + dict["diff_β2_1_0"] + "0")
                output_list_4 = list(a0 + a1 + a2 + dict["diff_β1_1_1"] + dict["diff_β2_1_1"] + "0")
                output_list_5 = list(a0 + a1 + a2 + dict["diff_β1_2_0"] + dict["diff_β2_2_0"] + "0")
                output_list_6 = list(a0 + a1 + a2 + dict["diff_β1_2_0"] + dict["diff_β2_2_1"] + "0")
                output_list_7 = list(a0 + a1 + a2 + dict["diff_β1_2_1"] + dict["diff_β2_2_0"] + "0")
                output_list_8 = list(a0 + a1 + a2 + dict["diff_β1_2_1"] + dict["diff_β2_2_1"] + "0")
                # 将可行的依赖差分传播模式写入CSV文件中
                with open("dependent_And.csv", "a+", newline="") as csvfile:
                    writer = csv.writer(csvfile)
                    # 将每行写入
                    writer.writerow(output_list_1)
                    writer.writerow(output_list_2)
                    writer.writerow(output_list_3)
                    writer.writerow(output_list_4)
                    writer.writerow(output_list_5)
                    writer.writerow(output_list_6)
                    writer.writerow(output_list_7)
                    writer.writerow(output_list_8)
            if count_1 == 4 and count_2 == 2:   #4-2
                print(a0, a1, a2, dict["diff_β1_1_0"], dict["diff_β2_1_0"], 0)
                print(a0, a1, a2, dict["diff_β1_1_1"], dict["diff_β2_1_0"], 0)
                print(a0, a1, a2, dict["diff_β1_1_0"], dict["diff_β2_1_1"], 0)
                print(a0, a1, a2, dict["diff_β1_1_1"], dict["diff_β2_1_1"], 0)
                print(a0, a1, a2, dict["diff_β1_2_0"], dict["diff_β2_2_0"], 0)
                print(a0, a1, a2, dict["diff_β1_2_1"], dict["diff_β2_2_0"], 0)
                print(a0, a1, a2, dict["diff_β1_2_0"], dict["diff_β2_2_1"], 0)
                print(a0, a1, a2, dict["diff_β1_2_1"], dict["diff_β2_2_1"], 0)
                output_list_1 = list(a0 + a1 + a2 + dict["diff_β1_1_0"] + dict["diff_β2_1_0"] + "0")
                output_list_2 = list(a0 + a1 + a2 + dict["diff_β1_1_1"] + dict["diff_β2_1_0"] + "0")
                output_list_3 = list(a0 + a1 + a2 + dict["diff_β1_1_0"] + dict["diff_β2_1_1"] + "0")
                output_list_4 = list(a0 + a1 + a2 + dict["diff_β1_1_1"] + dict["diff_β2_1_1"] + "0")
                output_list_5 = list(a0 + a1 + a2 + dict["diff_β1_2_0"] + dict["diff_β2_2_0"] + "0")
                output_list_6 = list(a0 + a1 + a2 + dict["diff_β1_2_1"] + dict["diff_β2_2_0"] + "0")
                output_list_7 = list(a0 + a1 + a2 + dict["diff_β1_2_0"] + dict["diff_β2_2_1"] + "0")
                output_list_8 = list(a0 + a1 + a2 + dict["diff_β1_2_1"] + dict["diff_β2_2_1"] + "0")
                # 将可行的依赖差分传播模式写入CSV文件中
                with open("dependent_And.csv", "a+", newline="") as csvfile:
                    writer = csv.writer(csvfile)
                    # 将每行写入
                    writer.writerow(output_list_1)
                    writer.writerow(output_list_2)
                    writer.writerow(output_list_3)
                    writer.writerow(output_list_4)
                    writer.writerow(output_list_5)
                    writer.writerow(output_list_6)
                    writer.writerow(output_list_7)
                    writer.writerow(output_list_8)
            if count_1 == 4 and count_2 == 4:   #4-4,这李一定存在差分
                print(a0, a1, a2, dict["diff_β1_1_0"], dict["diff_β2_1_0"], 1)
                print(a0, a1, a2, dict["diff_β1_1_0"], dict["diff_β2_1_1"], 1)
                print(a0, a1, a2, dict["diff_β1_1_1"], dict["diff_β2_1_0"], 1)
                print(a0, a1, a2, dict["diff_β1_1_1"], dict["diff_β2_1_1"], 1)
                print(a0, a1, a2, dict["diff_β1_2_0"], dict["diff_β2_2_0"], 1)
                print(a0, a1, a2, dict["diff_β1_2_0"], dict["diff_β2_2_1"], 1)
                print(a0, a1, a2, dict["diff_β1_2_1"], dict["diff_β2_2_0"], 1)
                print(a0, a1, a2, dict["diff_β1_2_1"], dict["diff_β2_2_1"], 1)
                output_list_1 = list(a0 + a1 + a2 + dict["diff_β1_1_0"] + dict["diff_β2_1_0"] + "1")
                output_list_2 = list(a0 + a1 + a2 + dict["diff_β1_1_0"] + dict["diff_β2_1_1"] + "1")
                output_list_3 = list(a0 + a1 + a2 + dict["diff_β1_1_1"] + dict["diff_β2_1_0"] + "1")
                output_list_4 = list(a0 + a1 + a2 + dict["diff_β1_1_1"] + dict["diff_β2_1_1"] + "1")
                output_list_5 = list(a0 + a1 + a2 + dict["diff_β1_2_0"] + dict["diff_β2_2_0"] + "1")
                output_list_6 = list(a0 + a1 + a2 + dict["diff_β1_2_0"] + dict["diff_β2_2_1"] + "1")
                output_list_7 = list(a0 + a1 + a2 + dict["diff_β1_2_1"] + dict["diff_β2_2_0"] + "1")
                output_list_8 = list(a0 + a1 + a2 + dict["diff_β1_2_1"] + dict["diff_β2_2_1"] + "1")
                # 将可行的依赖差分传播模式写入CSV文件中
                with open("dependent_And.csv", "a+", newline="") as csvfile:
                    writer = csv.writer(csvfile)
                    # 将每行写入
                    writer.writerow(output_list_1)
                    writer.writerow(output_list_2)
                    writer.writerow(output_list_3)
                    writer.writerow(output_list_4)
                    writer.writerow(output_list_5)
                    writer.writerow(output_list_6)
                    writer.writerow(output_list_7)
                    writer.writerow(output_list_8)
            print('########################################'
                  '########################################'
                  '########################################')
            print(count1)
            print(count2)



