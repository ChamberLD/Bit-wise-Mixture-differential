
from time import process_time
import multiprocessing
from util import *
import random

###############################################################################
######################SiMON算法加密流程#########################################
###############################################################################
def key_schedule(k, m, z, r):
    size = WS * m
    keys = [(k >> (WS * (i))) & (2 ** WS - 1) if i < m else None for i in range(r)]
    for i in range(m, r):
        tmp = rotr(keys[i - 1], 3)
        if m == 4: tmp ^= keys[i - 3]
        tmp ^= rotr(tmp, 1)
        keys[i] = (2 ** WS - 1 - keys[i - m]) ^ 3 ^ tmp ^ ((z >> ((61 - (i - m)) % 62)) & 1)
    return keys


def round_function(w1, w2, key):
    """Round function"""
    #return的顺序也是return Lin，Rin
    return w2 ^ (rotl(w1, 1) & rotl(w1, 8)) ^ rotl(w1, 2) ^ key, w1


#block是SIMON算法的输入
def simon(block, keys=[], rounds=0):
    if not len(keys):
        keys = key_schedule(MASTER_KEY, 4, Z, ROUNDS)
    if rounds == 0:
        return simon(block, keys, ROUNDS)
    w1 = block >> WS            #w1是Lin,>>是按位运算符
    w2 = block % (1 << WS)      #w2是Rin
    for r in range(rounds):
        w1, w2 = round_function(w1, w2, keys[r])
    return w1 << WS | w2


##########################################################################
#生成轮密钥
keys = key_schedule(0x1b1a1918131211100b0a090803020100, 4, Z, ROUNDS)
print(hex(simon(7308050733459598965, keys, ROUNDS)))


#########################################################################
##############SIMON混合差分路径验证########################################
#########################################################################
def verify():
    seed = "01"
    tmp = {}

    #Mixture_input_pattern   0  1   2.....                                            19 20                               31    33                                                 50                              61    63
    Mixture_input_pattern = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                             0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                             0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,]
    count = 0

    for i in range(pow(2, 25)):     #生成2^20组四元组
        # 存放随机生成明文的每个比特的值,先生成一个随机明文
        plaintext = []
        for k in range(64):  # 明文为64比特
            plaintext.append(random.choice(seed))
        tmp["P_1"] = ''.join(plaintext)
        plaintext_2 = []
        plaintext_3 = []
        plaintext_4 = []
        for j in range(0, 64):
            if Mixture_input_pattern[j] == 0:  # 生成P_2
                plaintext_2.append(tmp["P_1"][j])
            else:
                plaintext_2.append(str(1 - int(tmp["P_1"][j])))
            if Mixture_input_pattern[j + 64] == 0:  # 生成P_3
                plaintext_3.append(tmp["P_1"][j])
            else:
                plaintext_3.append(str(1 - int(tmp["P_1"][j])))
            if Mixture_input_pattern[j + 128] == 0:  # 生成P_3
                plaintext_4.append(tmp["P_1"][j])
            else:
                plaintext_4.append(str(1 - int(tmp["P_1"][j])))
        tmp["P_2"] = ''.join(plaintext_2)
        tmp["P_3"] = ''.join(plaintext_3)
        tmp["P_4"] = ''.join(plaintext_4)
        # 判断明文四元组P1,P2,P3,P4的混合差分模式,逐比特进行判定
        tmp["P_1_int"] = 0
        tmp["P_2_int"] = 0
        tmp["P_3_int"] = 0
        tmp["P_4_int"] = 0
        for m in range(0, 64):
            if tmp["P_1"][m] == "1":
                tmp["P_1_int"] = tmp["P_1_int"] + pow(2, 63-m)
            if tmp["P_2"][m] == "1":
                tmp["P_2_int"] = tmp["P_2_int"] + pow(2, 63-m)
            if tmp["P_3"][m] == "1":
                tmp["P_3_int"] = tmp["P_3_int"] + pow(2, 63-m)
            if tmp["P_4"][m] == "1":
                tmp["P_4_int"] = tmp["P_4_int"] + pow(2, 63-m)
        #对明文P1,P2,P3,P4进行加密,得到C1,C2,C3,C4
        for n in range(1, 5):
            tmp["C_" + str(n)] = bin(simon(tmp["P_" + str(n) + "_int"], keys, ROUNDS))
            #生成的字符串中带了0b,利用切片的方式将0b去掉,只保留后面的每一位的二进制表示
            tmp["C_" + str(n)] = tmp["C_" + str(n)][-(len(tmp["C_" + str(n)])-2):]
            if len(tmp["C_" + str(n)]) != 64:
                s_zero = ''
                for s in range(64-len(tmp["C_" + str(n)])):
                    s_zero = s_zero + '0'
                tmp["C_" + str(n)] = s_zero + tmp["C_" + str(n)]
        #获取密文C1,C2,C3,C4的混合差分模式
        for t in range(0, 64):
            # 生成c2
            if tmp["C_1"][t] != tmp["C_2"][t]:
                tmp["Ciphertext_" + str(t) + "_c2"] = 1
            else:
                tmp["Ciphertext_" + str(t) + "_c2"] = 0
            # 生成c1
            if tmp["C_1"][t] != tmp["C_3"][t]:
                tmp["Ciphertext_" + str(t) + "_c1"] = 1
            else:
                tmp["Ciphertext_" + str(t) + "_c1"] = 0
            # 生成c0
            if tmp["C_1"][t] != tmp["C_4"][t]:
                tmp["Ciphertext_" + str(t) + "_c0"] = 1
            else:
                tmp["Ciphertext_" + str(t) + "_c0"] = 0
        # print('#################################################')
        #与给定的高概率混合差分路径比较,记录满足高概率混合差分路径的明文四元组P1,P2,P3,P4以及对应的密文四元组C1,C2,C3,C4, 给定的6轮高概率混合差分路径见文件
        #其中0-31为L, 32-63为R, 比对密文的混合差分模式
        if (tmp["Ciphertext_0_c2"] == 0 and tmp["Ciphertext_0_c1"] == 0 and tmp["Ciphertext_0_c0"] == 0 and
            tmp["Ciphertext_1_c2"] == 0 and tmp["Ciphertext_1_c1"] == 0 and tmp["Ciphertext_1_c0"] == 0 and
            tmp["Ciphertext_2_c2"] == 0 and tmp["Ciphertext_2_c1"] == 0 and tmp["Ciphertext_2_c0"] == 0 and
            tmp["Ciphertext_3_c2"] == 0 and tmp["Ciphertext_3_c1"] == 0 and tmp["Ciphertext_3_c0"] == 0 and
            tmp["Ciphertext_4_c2"] == 0 and tmp["Ciphertext_4_c1"] == 0 and tmp["Ciphertext_4_c0"] == 0 and
            tmp["Ciphertext_5_c2"] == 0 and tmp["Ciphertext_5_c1"] == 0 and tmp["Ciphertext_5_c0"] == 0 and
            tmp["Ciphertext_6_c2"] == 0 and tmp["Ciphertext_6_c1"] == 0 and tmp["Ciphertext_6_c0"] == 0 and
            tmp["Ciphertext_7_c2"] == 0 and tmp["Ciphertext_7_c1"] == 0 and tmp["Ciphertext_7_c0"] == 0 and
            tmp["Ciphertext_8_c2"] == 0 and tmp["Ciphertext_8_c1"] == 0 and tmp["Ciphertext_8_c0"] == 0 and
            tmp["Ciphertext_9_c2"] == 0 and tmp["Ciphertext_9_c1"] == 0 and tmp["Ciphertext_9_c0"] == 0 and
            tmp["Ciphertext_10_c2"] == 0 and tmp["Ciphertext_10_c1"] == 0 and tmp["Ciphertext_10_c0"] == 0 and
            tmp["Ciphertext_11_c2"] == 0 and tmp["Ciphertext_11_c1"] == 0 and tmp["Ciphertext_11_c0"] == 1 and
            tmp["Ciphertext_12_c2"] == 0 and tmp["Ciphertext_12_c1"] == 0 and tmp["Ciphertext_12_c0"] == 0 and
            tmp["Ciphertext_13_c2"] == 0 and tmp["Ciphertext_13_c1"] == 0 and tmp["Ciphertext_13_c0"] == 0 and
            tmp["Ciphertext_14_c2"] == 0 and tmp["Ciphertext_14_c1"] == 0 and tmp["Ciphertext_14_c0"] == 0 and
            tmp["Ciphertext_15_c2"] == 0 and tmp["Ciphertext_15_c1"] == 0 and tmp["Ciphertext_15_c0"] == 0 and
            tmp["Ciphertext_16_c2"] == 0 and tmp["Ciphertext_16_c1"] == 0 and tmp["Ciphertext_16_c0"] == 0 and
            tmp["Ciphertext_17_c2"] == 0 and tmp["Ciphertext_17_c1"] == 0 and tmp["Ciphertext_17_c0"] == 0 and
            tmp["Ciphertext_18_c2"] == 0 and tmp["Ciphertext_18_c1"] == 0 and tmp["Ciphertext_18_c0"] == 0 and
            tmp["Ciphertext_19_c2"] == 0 and tmp["Ciphertext_19_c1"] == 0 and tmp["Ciphertext_19_c0"] == 1 and
            tmp["Ciphertext_20_c2"] == 0 and tmp["Ciphertext_20_c1"] == 0 and tmp["Ciphertext_20_c0"] == 0 and
            tmp["Ciphertext_21_c2"] == 0 and tmp["Ciphertext_21_c1"] == 0 and tmp["Ciphertext_21_c0"] == 0 and
            tmp["Ciphertext_22_c2"] == 0 and tmp["Ciphertext_22_c1"] == 0 and tmp["Ciphertext_22_c0"] == 0 and
            tmp["Ciphertext_23_c2"] == 0 and tmp["Ciphertext_23_c1"] == 0 and tmp["Ciphertext_23_c0"] == 0 and
            tmp["Ciphertext_24_c2"] == 0 and tmp["Ciphertext_24_c1"] == 0 and tmp["Ciphertext_24_c0"] == 0 and
            tmp["Ciphertext_25_c2"] == 0 and tmp["Ciphertext_25_c1"] == 0 and tmp["Ciphertext_25_c0"] == 0 and
            tmp["Ciphertext_26_c2"] == 0 and tmp["Ciphertext_26_c1"] == 0 and tmp["Ciphertext_26_c0"] == 0 and
            tmp["Ciphertext_27_c2"] == 0 and tmp["Ciphertext_27_c1"] == 0 and tmp["Ciphertext_27_c0"] == 0 and
            tmp["Ciphertext_28_c2"] == 0 and tmp["Ciphertext_28_c1"] == 0 and tmp["Ciphertext_28_c0"] == 0 and
            tmp["Ciphertext_29_c2"] == 0 and tmp["Ciphertext_29_c1"] == 0 and tmp["Ciphertext_29_c0"] == 0 and
            tmp["Ciphertext_30_c2"] == 0 and tmp["Ciphertext_30_c1"] == 0 and tmp["Ciphertext_30_c0"] == 0 and
            tmp["Ciphertext_31_c2"] == 0 and tmp["Ciphertext_31_c1"] == 0 and tmp["Ciphertext_31_c0"] == 0 and
            tmp["Ciphertext_32_c2"] == 0 and tmp["Ciphertext_32_c1"] == 0 and tmp["Ciphertext_32_c0"] == 0 and
            tmp["Ciphertext_33_c2"] == 0 and tmp["Ciphertext_33_c1"] == 0 and tmp["Ciphertext_33_c0"] == 0 and
            tmp["Ciphertext_34_c2"] == 0 and tmp["Ciphertext_34_c1"] == 0 and tmp["Ciphertext_34_c0"] == 0 and
            tmp["Ciphertext_35_c2"] == 0 and tmp["Ciphertext_35_c1"] == 0 and tmp["Ciphertext_35_c0"] == 0 and
            tmp["Ciphertext_36_c2"] == 0 and tmp["Ciphertext_36_c1"] == 0 and tmp["Ciphertext_36_c0"] == 0 and
            tmp["Ciphertext_37_c2"] == 0 and tmp["Ciphertext_37_c1"] == 0 and tmp["Ciphertext_37_c0"] == 0 and
            tmp["Ciphertext_38_c2"] == 0 and tmp["Ciphertext_38_c1"] == 0 and tmp["Ciphertext_38_c0"] == 0 and
            tmp["Ciphertext_39_c2"] == 0 and tmp["Ciphertext_39_c1"] == 0 and tmp["Ciphertext_39_c0"] == 0 and
            tmp["Ciphertext_40_c2"] == 0 and tmp["Ciphertext_40_c1"] == 0 and tmp["Ciphertext_40_c0"] == 0 and
            tmp["Ciphertext_41_c2"] == 0 and tmp["Ciphertext_41_c1"] == 0 and tmp["Ciphertext_41_c0"] == 0 and
            tmp["Ciphertext_42_c2"] == 0 and tmp["Ciphertext_42_c1"] == 0 and tmp["Ciphertext_42_c0"] == 0 and
            tmp["Ciphertext_43_c2"] == 0 and tmp["Ciphertext_43_c1"] == 0 and tmp["Ciphertext_43_c0"] == 0 and
            tmp["Ciphertext_44_c2"] == 0 and tmp["Ciphertext_44_c1"] == 0 and tmp["Ciphertext_44_c0"] == 0 and
            tmp["Ciphertext_45_c2"] == 0 and tmp["Ciphertext_45_c1"] == 0 and tmp["Ciphertext_45_c0"] == 1 and
            tmp["Ciphertext_46_c2"] == 0 and tmp["Ciphertext_46_c1"] == 0 and tmp["Ciphertext_46_c0"] == 0 and
            tmp["Ciphertext_47_c2"] == 0 and tmp["Ciphertext_47_c1"] == 0 and tmp["Ciphertext_47_c0"] == 0 and
            tmp["Ciphertext_48_c2"] == 0 and tmp["Ciphertext_48_c1"] == 0 and tmp["Ciphertext_48_c0"] == 0 and
            tmp["Ciphertext_49_c2"] == 0 and tmp["Ciphertext_49_c1"] == 0 and tmp["Ciphertext_49_c0"] == 1 and
            tmp["Ciphertext_50_c2"] == 0 and tmp["Ciphertext_50_c1"] == 0 and tmp["Ciphertext_50_c0"] == 0 and
            tmp["Ciphertext_51_c2"] == 0 and tmp["Ciphertext_51_c1"] == 0 and tmp["Ciphertext_51_c0"] == 0 and
            tmp["Ciphertext_52_c2"] == 0 and tmp["Ciphertext_52_c1"] == 0 and tmp["Ciphertext_52_c0"] == 0 and
            tmp["Ciphertext_53_c2"] == 0 and tmp["Ciphertext_53_c1"] == 0 and tmp["Ciphertext_53_c0"] == 1 and
            tmp["Ciphertext_54_c2"] == 0 and tmp["Ciphertext_54_c1"] == 0 and tmp["Ciphertext_54_c0"] == 0 and
            tmp["Ciphertext_55_c2"] == 0 and tmp["Ciphertext_55_c1"] == 0 and tmp["Ciphertext_55_c0"] == 0 and
            tmp["Ciphertext_56_c2"] == 0 and tmp["Ciphertext_56_c1"] == 0 and tmp["Ciphertext_56_c0"] == 0 and
            tmp["Ciphertext_57_c2"] == 0 and tmp["Ciphertext_57_c1"] == 0 and tmp["Ciphertext_57_c0"] == 0 and
            tmp["Ciphertext_58_c2"] == 0 and tmp["Ciphertext_58_c1"] == 0 and tmp["Ciphertext_58_c0"] == 0 and
            tmp["Ciphertext_59_c2"] == 0 and tmp["Ciphertext_59_c1"] == 0 and tmp["Ciphertext_59_c0"] == 0 and
            tmp["Ciphertext_60_c2"] == 0 and tmp["Ciphertext_60_c1"] == 0 and tmp["Ciphertext_60_c0"] == 0 and
            tmp["Ciphertext_61_c2"] == 0 and tmp["Ciphertext_61_c1"] == 0 and tmp["Ciphertext_61_c0"] == 0 and
            tmp["Ciphertext_62_c2"] == 0 and tmp["Ciphertext_62_c1"] == 0 and tmp["Ciphertext_62_c0"] == 0 and
            tmp["Ciphertext_63_c2"] == 0 and tmp["Ciphertext_63_c1"] == 0 and tmp["Ciphertext_63_c0"] == 0):
            count = count + 1
    print(count)


if __name__ == "__main__":
    # 创建进程池，最大进程数为4
    pool = multiprocessing.Pool(processes=32)
    for i in range(32):
        pool.apply_async(verify)

    pool.close()

    pool.join()

    print("All tasks completed")


