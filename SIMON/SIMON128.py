"""
Function: Model SIMON algorithm and find Mixture differential distinguishers
Date: 2022/03/06
Author: Zehan Wu
Contact:
"""

import pycryptosat
import time
from time import process_time


##############################################################################################
#定义SIMON算法模型中的变量，一共应该有7个状态，因此应该定义7个状态的bit的混合差分变量模式，还需要带上轮数
##############################################################################################
#每一轮的输入bit的混合差分模式,分为左侧输入和右侧输入
def genVars_Round(r):
    return ['L_'+str(r)+'r_'+str(i) for i in range(64)] + ['R_'+str(r)+'r_'+str(i) for i in range(64)]

#每一轮的左移1位的bit的混合差分模式
def genVars_SR1_Round(r):
    return ['SR1_'+str(r)+'r_'+str(i) for i in range(64)]

#每一轮的左移2位的bit的混合差分模式
def genVars_SR2_Round(r):
    return ['SR2_'+str(r)+'r_'+str(i) for i in range(64)]

#每一轮的左移8位的bit的混合差分模式
def genVars_SR8_Round(r):
    return ['SR8_'+str(r)+'r_'+str(i) for i in range(64)]

#每一轮的＆运算之后的bit的混合差分模式
def genVars_aftAnd_Round(r):
    return ['aftAnd_'+str(r)+'r_'+str(i) for i in range(64)]

#每一轮的第一次异或后的bit的混合差分模式
def genVars_aftXOR1_Round(r):
    return ['aftXOR1_'+str(r)+'r_'+str(i) for i in range(64)]

#每一轮的and操作后的混合差分概率变量
def genVars_ProaftAnd_Round(r):
    return ['ProaftAnd_'+str(r)+'r_'+str(i) for i in range(64)]

#生成每一轮需要的copy变量，copy变量在传递约束方面是很有用的
def genVars_Copy_Round(r, k):
    return ['Copy_'+str(k)+'_'+str(r)+'r_'+str(i) for i in range(64)]

#生成每一轮需要的概率变量ph的copy变量
def genVars_PCopy_Round():
    #用p_number来表示概率变量的下标
    global  p_number
    return ['PCopy_'+str(i) for i in range(p_number, p_number+64)]

####################################################################################
####################################################################################
#定义向SAT模型中添加clause（CNF约束）的函数
####################################################################################
dict = {}
def gen_AndCNF_Constraint(a, b, c, d):
    global number
    for i in range(0, 64):
        dict[c[i] + str("_c2")] = number; number = number + 1
        dict[c[i] + str("_c1")] = number; number = number + 1
        dict[c[i] + str("_c0")] = number; number = number + 1
        dict[d[i] + str("_ph")] = number; number = number + 1
        dict[d[i] + str("_pl")] = number; number = number + 1
        solver.add_clause([dict[a[i] + str("_c2")], dict[a[i] + str("_c1")], dict[a[i] + str("_c0")], dict[b[i] + str("_c2")], dict[b[i] + str("_c1")], dict[b[i] + str("_c0")], -dict[d[i] + str("_pl")]])  #c2+c1+c0+d2+d1+d0+pl'
        solver.add_clause([dict[a[i] + str("_c2")], dict[b[i] + str("_c2")], -dict[c[i] + str("_c2")]])   #c2+d2+e2'
        solver.add_clause([dict[a[i] + str("_c1")], dict[b[i] + str("_c1")], -dict[c[i] + str("_c1")]])  # c1+d1+e1'
        solver.add_clause([dict[a[i] + str("_c0")], dict[b[i] + str("_c0")], -dict[c[i] + str("_c0")]])  # c0+d0+e0'
        solver.add_clause([-dict[a[i] + str("_c2")], dict[a[i] + str("_c1")], -dict[a[i] + str("_c0")], dict[c[i] + str("_c2")], -dict[c[i] + str("_c1")], -dict[c[i] + str("_c0")]])  # c2'+c1+c0'+e2+e1'+e0'
        solver.add_clause([-dict[a[i] + str("_c2")], -dict[a[i] + str("_c1")], dict[a[i] + str("_c0")], dict[c[i] + str("_c2")], -dict[c[i] + str("_c1")], -dict[c[i] + str("_c0")]])  # c2'+c1'+c0+e2+e1'+e0'
        solver.add_clause([-dict[b[i] + str("_c2")], dict[b[i] + str("_c1")], -dict[b[i] + str("_c0")], dict[c[i] + str("_c2")], -dict[c[i] + str("_c1")], -dict[c[i] + str("_c0")]])  # d2'+d1+d0'+e2+e1'+e0'
        solver.add_clause([-dict[b[i] + str("_c2")], -dict[b[i] + str("_c1")], dict[b[i] + str("_c0")], dict[c[i] + str("_c2")], -dict[c[i] + str("_c1")], -dict[c[i] + str("_c0")]])  # d2'+d1'+d0+e2+e1'+e0'
        solver.add_clause([dict[b[i] + str("_c2")], -dict[b[i] + str("_c1")], -dict[b[i] + str("_c0")], -dict[c[i] + str("_c2")], dict[c[i] + str("_c1")], -dict[c[i] + str("_c0")]])  # d2+d1'+d0'+e2'+e1+e0'
        solver.add_clause([dict[a[i] + str("_c2")], -dict[a[i] + str("_c1")], -dict[a[i] + str("_c0")], -dict[c[i] + str("_c2")], dict[c[i] + str("_c1")], -dict[c[i] + str("_c0")]])  # c2+c1'+c0'+e2'+e1+e0'
        solver.add_clause([-dict[a[i] + str("_c2")], -dict[a[i] + str("_c1")], dict[a[i] + str("_c0")], -dict[c[i] + str("_c2")], dict[c[i] + str("_c1")], -dict[c[i] + str("_c0")]])  # c2'+c1'+c0+e2'+e1+e0'
        solver.add_clause([-dict[b[i] + str("_c2")], -dict[b[i] + str("_c1")], dict[b[i] + str("_c0")], -dict[c[i] + str("_c2")], dict[c[i] + str("_c1")], -dict[c[i] + str("_c0")]])  # d2'+d1'+d0+e2'+e1+e0'
        solver.add_clause([dict[b[i] + str("_c2")], -dict[b[i] + str("_c1")], -dict[b[i] + str("_c0")], -dict[c[i] + str("_c2")], -dict[c[i] + str("_c1")], dict[c[i] + str("_c0")]])  # d2+d1'+d0'+e2'+e1'+e0
        solver.add_clause([-dict[b[i] + str("_c2")], dict[b[i] + str("_c1")], -dict[b[i] + str("_c0")], -dict[c[i] + str("_c2")], -dict[c[i] + str("_c1")], dict[c[i] + str("_c0")]])  # d2'+d1+d0'+e2'+e1'+e0
        solver.add_clause([dict[a[i] + str("_c2")], -dict[a[i] + str("_c1")], -dict[a[i] + str("_c0")], -dict[c[i] + str("_c2")], -dict[c[i] + str("_c1")], dict[c[i] + str("_c0")]])  # c2+c1'+c0'+e2'+e1'+e0
        solver.add_clause([-dict[a[i] + str("_c2")], dict[a[i] + str("_c1")], -dict[a[i] + str("_c0")], -dict[c[i] + str("_c2")], -dict[c[i] + str("_c1")], dict[c[i] + str("_c0")]])  # c2'+c1+c0'+e2'+e1'+e0
        solver.add_clause([dict[a[i] + str("_c2")], dict[a[i] + str("_c0")], -dict[b[i] + str("_c2")], dict[c[i] + str("_c2")], -dict[c[i] + str("_c0")]])  # c2+c0+d2'+e2+e0'
        solver.add_clause([dict[a[i] + str("_c1")], dict[a[i] + str("_c0")], -dict[b[i] + str("_c1")], dict[c[i] + str("_c1")], -dict[c[i] + str("_c0")]])  # c1+c0+d1'+e1+e0'
        solver.add_clause([-dict[a[i] + str("_c2")], dict[b[i] + str("_c2")], dict[b[i] + str("_c0")], dict[c[i] + str("_c2")], -dict[c[i] + str("_c0")]])  # c2'+d2+d0+e2+e0'
        solver.add_clause([-dict[a[i] + str("_c1")], dict[b[i] + str("_c1")], dict[b[i] + str("_c0")], dict[c[i] + str("_c1")], -dict[c[i] + str("_c0")]])  # c1'+d1+d0+e1+e0'
        solver.add_clause([dict[a[i] + str("_c2")], dict[a[i] + str("_c1")], -dict[b[i] + str("_c2")], dict[c[i] + str("_c2")], -dict[c[i] + str("_c1")]])  # c2+c1+d2'+e2+e1'
        solver.add_clause([dict[a[i] + str("_c1")], dict[a[i] + str("_c0")], -dict[b[i] + str("_c0")], -dict[c[i] + str("_c1")], dict[c[i] + str("_c0")]])  # c1+c0+d0'+e1'+e0
        solver.add_clause([-dict[a[i] + str("_c2")], dict[b[i] + str("_c2")], dict[b[i] + str("_c1")], dict[c[i] + str("_c2")], -dict[c[i] + str("_c1")]])  # c2'+d2+d1+e2+e1'
        solver.add_clause([-dict[a[i] + str("_c0")], dict[b[i] + str("_c1")], dict[b[i] + str("_c0")], -dict[c[i] + str("_c1")], dict[c[i] + str("_c0")]])  # c0'+d1+d0+e1'+e0
        solver.add_clause([dict[a[i] + str("_c2")], dict[a[i] + str("_c1")], -dict[b[i] + str("_c1")], -dict[c[i] + str("_c2")], dict[c[i] + str("_c1")]])  # c2+c1+d1'+e2'+e1
        solver.add_clause([dict[a[i] + str("_c2")], dict[a[i] + str("_c0")], -dict[b[i] + str("_c0")], -dict[c[i] + str("_c2")], dict[c[i] + str("_c0")]])  # c2+c0+d0'+e2'+e0
        solver.add_clause([-dict[a[i] + str("_c1")], dict[b[i] + str("_c2")], dict[b[i] + str("_c1")], -dict[c[i] + str("_c2")], dict[c[i] + str("_c1")]])  # c1'+d2+d1+e2'+e1
        solver.add_clause([-dict[a[i] + str("_c0")], dict[b[i] + str("_c2")], dict[b[i] + str("_c0")], -dict[c[i] + str("_c2")], dict[c[i] + str("_c0")]])  # c0'+d2+d0+e2'+e0
        solver.add_clause([-dict[a[i] + str("_c2")], dict[a[i] + str("_c1")], -dict[a[i] + str("_c0")], dict[b[i] + str("_c2")], -dict[b[i] + str("_c1")], -dict[b[i] + str("_c0")], dict[c[i] + str("_c2")], dict[c[i] + str("_c1")], dict[c[i] + str("_c0")]])  # c2'+c1+c0'+d2+d1'+d0'+e2+e1+e0
        solver.add_clause([-dict[a[i] + str("_c2")], -dict[a[i] + str("_c1")], dict[a[i] + str("_c0")], dict[b[i] + str("_c2")], -dict[b[i] + str("_c1")], -dict[b[i] + str("_c0")], dict[c[i] + str("_c2")], dict[c[i] + str("_c1")], dict[c[i] + str("_c0")]])  # c2'+c1'+c0+d2+d1'+d0'+e2+e1+e0
        solver.add_clause([dict[a[i] + str("_c2")], -dict[a[i] + str("_c1")], -dict[a[i] + str("_c0")], -dict[b[i] + str("_c2")], dict[b[i] + str("_c1")], -dict[b[i] + str("_c0")], dict[c[i] + str("_c2")], dict[c[i] + str("_c1")], dict[c[i] + str("_c0")]])  # c2+c1'+c0'+d2'+d1+d0'+e2+e1+e0
        solver.add_clause([-dict[a[i] + str("_c2")], -dict[a[i] + str("_c1")], dict[a[i] + str("_c0")], -dict[b[i] + str("_c2")], dict[b[i] + str("_c1")], -dict[b[i] + str("_c0")], dict[c[i] + str("_c2")], dict[c[i] + str("_c1")], dict[c[i] + str("_c0")]])  # c2'+c1'+c0+d2'+d1+d0'+e2+e1+e0
        solver.add_clause([dict[a[i] + str("_c2")], -dict[a[i] + str("_c1")], -dict[a[i] + str("_c0")], -dict[b[i] + str("_c2")], -dict[b[i] + str("_c1")], dict[b[i] + str("_c0")], dict[c[i] + str("_c2")], dict[c[i] + str("_c1")], dict[c[i] + str("_c0")]])  # c2+c1'+c0'+d2'+d1'+d0+e2+e1+e0
        solver.add_clause([-dict[a[i] + str("_c2")], dict[a[i] + str("_c1")], -dict[a[i] + str("_c0")], -dict[b[i] + str("_c2")], -dict[b[i] + str("_c1")], dict[b[i] + str("_c0")], dict[c[i] + str("_c2")], dict[c[i] + str("_c1")], dict[c[i] + str("_c0")]])  # c2'+c1+c0'+d2'+d1'+d0+e2+e1+e0
        solver.add_clause([-dict[d[i] + str("_ph")], -dict[d[i] + str("_pl")]])  # ph'+pl'
        solver.add_clause([-dict[b[i] + str("_c0")], dict[d[i] + str("_ph")], dict[d[i] + str("_pl")]])  # d0'+ph+pl
        solver.add_clause([-dict[b[i] + str("_c1")], dict[d[i] + str("_ph")], dict[d[i] + str("_pl")]])  # d1'+ph+pl
        solver.add_clause([-dict[a[i] + str("_c0")], -dict[b[i] + str("_c1")], dict[b[i] + str("_c0")], -dict[d[i] + str("_pl")]])  # c0'+d1'+d0+pl'
        solver.add_clause([-dict[a[i] + str("_c1")], dict[b[i] + str("_c1")], -dict[b[i] + str("_c0")], -dict[d[i] + str("_pl")]])  # c1'+d1+d0'+pl'
        solver.add_clause([-dict[b[i] + str("_c2")], dict[d[i] + str("_ph")], dict[d[i] + str("_pl")]])  # d2'+ph+pl
        solver.add_clause([-dict[a[i] + str("_c2")], dict[b[i] + str("_c2")], -dict[b[i] + str("_c1")], -dict[d[i] + str("_pl")]])  # c2'+d2+d1'+pl'
        solver.add_clause([dict[b[i] + str("_c2")], dict[b[i] + str("_c1")], dict[b[i] + str("_c0")], -dict[d[i] + str("_ph")]])  # d2+d1+d0+ph'
        solver.add_clause([-dict[a[i] + str("_c1")], dict[a[i] + str("_c0")], -dict[b[i] + str("_c0")], -dict[d[i] + str("_pl")]])  # c1'+c0+d0'+pl'
        solver.add_clause([dict[a[i] + str("_c1")], -dict[a[i] + str("_c0")], -dict[b[i] + str("_c1")], -dict[d[i] + str("_pl")]])  # c1+c0'+d1'+pl'
        solver.add_clause([-dict[a[i] + str("_c0")], -dict[b[i] + str("_c2")], dict[b[i] + str("_c0")], -dict[d[i] + str("_pl")]])  # c0'+d2'+d0+pl'
        solver.add_clause([dict[a[i] + str("_c2")], dict[a[i] + str("_c1")], dict[a[i] + str("_c0")], -dict[d[i] + str("_ph")]])  # c2+c1+c0+ph'
        solver.add_clause([dict[a[i] + str("_c2")], -dict[a[i] + str("_c0")], -dict[b[i] + str("_c2")], -dict[d[i] + str("_pl")]])  # c2+c0'+d2'+pl'
        solver.add_clause([-dict[a[i] + str("_c0")], dict[d[i] + str("_ph")], dict[d[i] + str("_pl")]])  # c0'+ph+pl
        solver.add_clause([-dict[a[i] + str("_c1")], -dict[a[i] + str("_c0")], -dict[b[i] + str("_c1")], -dict[b[i] + str("_c0")], -dict[c[i] + str("_c1")], dict[c[i] + str("_c0")]])  # c1'+c0'+d1'+d0'+e1'+e0
        solver.add_clause([-dict[a[i] + str("_c1")], -dict[a[i] + str("_c0")], -dict[b[i] + str("_c1")], -dict[b[i] + str("_c0")], dict[c[i] + str("_c1")], -dict[c[i] + str("_c0")]])  # c1'+c0'+d1'+d0'+e1+e0'
        solver.add_clause([-dict[a[i] + str("_c2")], -dict[a[i] + str("_c0")], -dict[b[i] + str("_c2")], -dict[b[i] + str("_c0")], dict[c[i] + str("_c2")], -dict[c[i] + str("_c0")]])  # c2'+c0'+d2'+d0'+e2+e0'
        solver.add_clause([-dict[a[i] + str("_c2")], dict[a[i] + str("_c0")], -dict[b[i] + str("_c0")], -dict[d[i] + str("_pl")]])  # c2'+c0+d0'+pl'
        solver.add_clause([-dict[a[i] + str("_c2")], -dict[a[i] + str("_c1")], -dict[b[i] + str("_c2")], -dict[b[i] + str("_c1")], -dict[c[i] + str("_c2")], dict[c[i] + str("_c1")]])  # c2'+c1'+d2'+d1'+e2'+e1
        solver.add_clause([-dict[a[i] + str("_c2")], -dict[a[i] + str("_c0")], -dict[b[i] + str("_c2")], -dict[b[i] + str("_c0")], -dict[c[i] + str("_c2")], dict[c[i] + str("_c0")]])  # c2'+c0'+d2'+d0'+e2'+e0
        solver.add_clause([-dict[a[i] + str("_c2")], -dict[a[i] + str("_c1")], -dict[b[i] + str("_c2")], -dict[b[i] + str("_c1")], dict[c[i] + str("_c2")], -dict[c[i] + str("_c1")]])  # c2'+c1'+d2'+d1'+e2+e1'
        solver.add_clause([-dict[a[i] + str("_c2")], -dict[a[i] + str("_c1")], -dict[a[i] + str("_c0")], -dict[b[i] + str("_c2")], -dict[b[i] + str("_c1")], -dict[b[i] + str("_c0")], dict[d[i] + str("_pl")]])  # c2'+c1'+c0'+d2'+d1'+d0'+pl
        solver.add_clause([-dict[a[i] + str("_c1")], -dict[b[i] + str("_c2")], dict[b[i] + str("_c1")], -dict[d[i] + str("_pl")]])  # c1'+d2'+d1+pl'
        solver.add_clause([-dict[a[i] + str("_c1")], dict[d[i] + str("_ph")], dict[d[i] + str("_pl")]])  # c1'+ph+pl
        solver.add_clause([-dict[a[i] + str("_c2")], dict[b[i] + str("_c2")], -dict[b[i] + str("_c0")], -dict[d[i] + str("_pl")]])  # c2'+d2+d0'+pl'
        solver.add_clause([-dict[a[i] + str("_c2")], dict[a[i] + str("_c1")], dict[a[i] + str("_c0")], dict[b[i] + str("_c1")], dict[b[i] + str("_c0")], dict[d[i] + str("_pl")]])  # c2'+c1+c0+d1+d0+pl
        solver.add_clause([-dict[a[i] + str("_c2")], dict[a[i] + str("_c1")], -dict[b[i] + str("_c1")], -dict[d[i] + str("_pl")]])  # c2'+c1+d1'+pl'
        solver.add_clause([dict[a[i] + str("_c2")], -dict[a[i] + str("_c1")], -dict[b[i] + str("_c2")], -dict[d[i] + str("_pl")]])  # c2+c1'+d2'+pl'
        solver.add_clause([-dict[a[i] + str("_c2")], -dict[a[i] + str("_c1")], dict[a[i] + str("_c0")], -dict[b[i] + str("_c2")], -dict[b[i] + str("_c1")], dict[b[i] + str("_c0")], dict[d[i] + str("_pl")]])  # c2'+c1'+c0+d2'+d1'+d0+pl
        solver.add_clause([-dict[a[i] + str("_c2")], dict[a[i] + str("_c1")], -dict[a[i] + str("_c0")], -dict[b[i] + str("_c2")], dict[b[i] + str("_c1")], -dict[b[i] + str("_c0")], dict[d[i] + str("_pl")]])  # c2'+c1+c0'+d2'+d1+d0'+pl
        solver.add_clause([dict[a[i] + str("_c2")], -dict[a[i] + str("_c1")], -dict[a[i] + str("_c0")], dict[b[i] + str("_c2")], -dict[b[i] + str("_c1")], -dict[b[i] + str("_c0")], dict[d[i] + str("_pl")]])  # c2+c1'+c0'+d2+d1'+d0'+pl
        solver.add_clause([dict[a[i] + str("_c2")], dict[a[i] + str("_c0")], dict[b[i] + str("_c2")], dict[b[i] + str("_c0")], -dict[d[i] + str("_ph")]])  # c2+c0+d2+d0+ph'
        solver.add_clause([dict[a[i] + str("_c2")], dict[a[i] + str("_c1")], dict[b[i] + str("_c2")], dict[b[i] + str("_c1")], -dict[d[i] + str("_ph")]])  # c2+c1+d2+d1+ph'


def gen_XORCNF_Constraint(a, b, c):
    global number
    for i in range(0, 64):
        dict[c[i] + str("_c2")] = number; number = number + 1
        dict[c[i] + str("_c1")] = number; number = number + 1
        dict[c[i] + str("_c0")] = number; number = number + 1
        solver.add_clause([-dict[a[i] + str("_c0")], -dict[b[i] + str("_c0")], -dict[c[i] + str("_c0")]])   # c0'+d0'+e0'
        solver.add_clause([dict[a[i] + str("_c0")], dict[b[i] + str("_c0")], -dict[c[i] + str("_c0")]])     # c0+d0+e0'
        solver.add_clause([-dict[a[i] + str("_c1")], -dict[b[i] + str("_c1")], -dict[c[i] + str("_c1")]])     # c1'+d1'+e1'
        solver.add_clause([dict[a[i] + str("_c1")], dict[b[i] + str("_c1")], -dict[c[i] + str("_c1")]])     # c1+d1+e1'
        solver.add_clause([-dict[a[i] + str("_c2")], -dict[b[i] + str("_c2")], -dict[c[i] + str("_c2")]])   #c2'+d2'+e2'
        solver.add_clause([dict[a[i] + str("_c2")], dict[b[i] + str("_c2")], -dict[c[i] + str("_c2")]])     #c2+d2+e2'
        solver.add_clause([dict[a[i] + str("_c0")], -dict[b[i] + str("_c0")], dict[c[i] + str("_c0")]])      #c0+d0'+e0
        solver.add_clause([dict[a[i] + str("_c1")], -dict[b[i] + str("_c1")], dict[c[i] + str("_c1")]])     #c1+d1'+e1
        solver.add_clause([dict[a[i] + str("_c2")], -dict[b[i] + str("_c2")], dict[c[i] + str("_c2")]])     #c2+d2'+e2
        solver.add_clause([-dict[a[i] + str("_c0")], dict[b[i] + str("_c0")], dict[c[i] + str("_c0")]])     #c0'+d0+e0
        solver.add_clause([-dict[a[i] + str("_c1")], dict[b[i] + str("_c1")], dict[c[i] + str("_c1")]])      #c1'+d1+e1
        solver.add_clause([-dict[a[i] + str("_c2")], dict[b[i] + str("_c2")], dict[c[i] + str("_c2")]])      #c2'+d2+e2


#定义copy操作的CNF约束,copy操作即输入bit和输出bit的混合差分模式完全相等
def gen_CopyCNF_Constraint(a, b):
    global number
    for i in range(0, 64):
        dict[b[i] + str("_c2")] = number; number = number + 1
        dict[b[i] + str("_c1")] = number; number = number + 1
        dict[b[i] + str("_c0")] = number; number = number + 1
        solver.add_clause([dict[a[i] + str("_c0")], -dict[b[i] + str("_c0")]])      #in0+out0'
        solver.add_clause([dict[a[i] + str("_c1")], -dict[b[i] + str("_c1")]])      #in1+out1'
        solver.add_clause([dict[a[i] + str("_c2")], -dict[b[i] + str("_c2")]])       #in2+out2'
        solver.add_clause([-dict[a[i] + str("_c0")], dict[b[i] + str("_c0")]])      #in0'+out0
        solver.add_clause([-dict[a[i] + str("_c1")], dict[b[i] + str("_c1")]])      #in1'+out1
        solver.add_clause([-dict[a[i] + str("_c2")], dict[b[i] + str("_c2")]])      #in2'+out2


#定义概率变量ph的copy操作的CNF,概率变量的COPY操作和上面的copy操作的不同点在于，上面是三元，这个是一元的
def gen_PhCopyCNF_Constraint(a, b):
    global number
    for i in range(0, 64):
        dict[b[i]] = number; number = number + 1
        solver.add_clause([dict[a[i] + str("_ph")], -dict[b[i]]])          #ph+ph_copy'
        solver.add_clause([-dict[a[i] + str("_ph")], dict[b[i]]])          #ph'+ph_copy


#定义概率变量pl的copy操作的CNF
def gen_PlCopyCNF_Constraint(a, b):
    global number
    for i in range(0, 64):
        dict[b[i]] = number; number = number + 1
        solver.add_clause([dict[a[i] + str("_pl")], -dict[b[i]]])          #pl+pl_copy'
        solver.add_clause([-dict[a[i] + str("_pl")], dict[b[i]]])          #pl'+pl_copy


#定义bit的循环左移,将相应的bit的混合差分模式赋给循环左移后的bit,k表示循环左移位数，其实主要的功能是让不同的变量名在SAT中指向同一变量，这样约束就不会混乱
def shift_left(a, b, k):
    if k == 1:
        for i in range(0, 64):
            dict[b[(i - 1)%64] + str("_c2")] = dict[a[i] + str("_c2")]
            dict[b[(i - 1)%64] + str("_c1")] = dict[a[i] + str("_c1")]
            dict[b[(i - 1)%64] + str("_c0")] = dict[a[i] + str("_c0")]
    elif k == 2:
        for i in range(0, 64):
            dict[b[(i - 2) % 64] + str("_c2")] = dict[a[i] + str("_c2")]
            dict[b[(i - 2) % 64] + str("_c1")] = dict[a[i] + str("_c1")]
            dict[b[(i - 2) % 64] + str("_c0")] = dict[a[i] + str("_c0")]
    else:
        for i in range(0, 64):
            dict[b[(i - 8) % 64] + str("_c2")] = dict[a[i] + str("_c2")]
            dict[b[(i - 8) % 64] + str("_c1")] = dict[a[i] + str("_c1")]
            dict[b[(i - 8) % 64] + str("_c0")] = dict[a[i] + str("_c0")]

#定义一个函数，用于在dict中添加相应的值，方便添加约束用
def insert_dict(a):
    global number
    for i in range(0, 64):
        dict[a[i] + str("_c2")] = number; number = number + 1
        dict[a[i] + str("_c1")] = number; number = number + 1
        dict[a[i] + str("_c0")] = number; number = number + 1


#生成目标函数的约束
def gen_objectfuntion_Constraint(r, w):
    global number
    n = r*64*3
    dict["S_1_1"] = number; number = number + 1
    solver.add_clause([-dict["PCopy_1"], dict["S_1_1"]])                                           #x1'+S_1_1
    for j in range(2, w+1):
        dict["S_1_" + str(j)] = number; number = number + 1
        solver.add_clause([-dict["S_1_" + str(j)]])                                                #S1,j'
    for i in range(2, n):
        dict["S_" + str(i) + "_1"] = number; number = number + 1
        solver.add_clause([-dict["PCopy_" + str(i)], dict["S_" + str(i) + "_1"]])                 #xi'+S_i_1
        solver.add_clause([-dict["S_" + str(i-1) + "_1"], dict["S_" + str(i) + "_1"]])            #S_i-1_1'+S_i_1
        for k in range(2, w+1):
            dict["S_" + str(i) + "_" + str(k)] = number; number = number + 1
            solver.add_clause([-dict["PCopy_" + str(i)], -dict["S_" + str(i-1) + "_" + str(k-1)], dict["S_" + str(i) + "_" + str(k)]])   #xi'+S_i-1_j-1'+S_i_j
            solver.add_clause([-dict["S_" + str(i-1) + "_" + str(k)], dict["S_" + str(i) + "_" + str(k)]])                      #S_i-1_j'+S_i_j
        solver.add_clause([-dict["PCopy_" + str(i)], -dict["S_" + str(i-1) + "_" + str(w)]])            #xi'+S_i-1_k'
    solver.add_clause([-dict["PCopy_" + str(n)], -dict["S_" + str(n-1) + "_" + str(w)]])   #xn'+S_n-1_k'


#添加SIMON算法and运算的差分因为移位产生的约束（差分依赖性约束）
def gen_rotation_Constraint(a, b, c):
    global number
    for i in range(0, 64):
        with open('dependent_Constraint.txt', 'r') as file:
            file = file.read().splitlines()
            length = len(file)
            for m in range(0, length):
                line_split = file[m].split("+")
                constraint = []
                for j in range(0, len(line_split)):
                    # 添加ax相关约束
                    if line_split[j] == "αx_c2":
                        constraint.append("dict[a[i] + str(\"_c2\")]")
                    if line_split[j] == "αx_c1":
                        constraint.append("dict[a[i] + str(\"_c1\")]")
                    if line_split[j] == "αx_c0":
                        constraint.append("dict[a[i] + str(\"_c0\")]")
                    if line_split[j] == "αx_c2'":
                        constraint.append("-dict[a[i] + str(\"_c2\")]")
                    if line_split[j] == "αx_c1'":
                        constraint.append("-dict[a[i] + str(\"_c1\")]")
                    if line_split[j] == "αx_c0'":
                        constraint.append("-dict[a[i] + str(\"_c0\")]")
                    # 添加ay相关约束
                    if line_split[j] == "αy_c2":
                        constraint.append("dict[b[i] + str(\"_c2\")]")
                    if line_split[j] == "αy_c1":
                        constraint.append("dict[b[i] + str(\"_c1\")]")
                    if line_split[j] == "αy_c0":
                        constraint.append("dict[b[i] + str(\"_c0\")]")
                    if line_split[j] == "αy_c2'":
                        constraint.append("-dict[b[i] + str(\"_c2\")]")
                    if line_split[j] == "αy_c1'":
                        constraint.append("-dict[b[i] + str(\"_c1\")]")
                    if line_split[j] == "αy_c0'":
                        constraint.append("-dict[b[i] + str(\"_c0\")]")
                    # 添加az相关约束
                    if line_split[j] == "αz_c2":
                        constraint.append("dict[a[(i+57)%64] + str(\"_c2\")]")
                    if line_split[j] == "αz_c1":
                        constraint.append("dict[a[(i+57)%64] + str(\"_c1\")]")
                    if line_split[j] == "αz_c0":
                        constraint.append("dict[a[(i+57)%64] + str(\"_c0\")]")
                    if line_split[j] == "αz_c2'":
                        constraint.append("-dict[a[(i+57)%64] + str(\"_c2\")]")
                    if line_split[j] == "αz_c1'":
                        constraint.append("-dict[a[(i+57)%64] + str(\"_c1\")]")
                    if line_split[j] == "αz_c0'":
                        constraint.append("-dict[a[(i+57)%64] + str(\"_c0\")]")
                    # 添加βxy相关约束
                    if line_split[j] == "βxy_c2":
                        constraint.append("dict[c[i] + str(\"_c2\")]")
                    if line_split[j] == "βxy_c1":
                        constraint.append("dict[c[i] + str(\"_c1\")]")
                    if line_split[j] == "βxy_c0":
                        constraint.append("dict[c[i] + str(\"_c0\")]")
                    if line_split[j] == "βxy_c2'":
                        constraint.append("-dict[c[i] + str(\"_c2\")]")
                    if line_split[j] == "βxy_c1'":
                        constraint.append("-dict[c[i] + str(\"_c1\")]")
                    if line_split[j] == "βxy_c0'":
                        constraint.append("-dict[c[i] + str(\"_c0\")]")
                    # 添加βxz相关约束
                    if line_split[j] == "βxz_c2":
                        constraint.append("dict[c[(i+57)%64] + str(\"_c2\")]")
                    if line_split[j] == "βxz_c1":
                        constraint.append("dict[c[(i+57)%64] + str(\"_c1\")]")
                    if line_split[j] == "βxz_c0":
                        constraint.append("dict[c[(i+57)%64] + str(\"_c0\")]")
                    if line_split[j] == "βxz_c2'":
                        constraint.append("-dict[c[(i+57)%64] + str(\"_c2\")]")
                    if line_split[j] == "βxz_c1'":
                        constraint.append("-dict[c[(i+57)%64] + str(\"_c1\")]")
                    if line_split[j] == "βxz_c0'":
                        constraint.append("-dict[c[(i+57)%64] + str(\"_c0\")]")
                constraint_real = []
                for k in range(0, len(constraint)):
                    constraint_real.append(eval(constraint[k]))
                solver.add_clause(constraint_real)

#定义一个简单的两个比特变量机型异或运算时候的函数(主要是用于约束输入混合差分模式的约束）
def gen_XORCNF_input(a, b):
    global number
    for i in range(0, 64):
        dict[a[i] + str("_e2")] = number; number = number + 1
        dict[a[i] + str("_e1")] = number; number = number + 1
        dict[a[i] + str("_e0")] = number; number = number + 1
        dict[b[i] + str("_e2")] = number; number = number + 1
        dict[b[i] + str("_e1")] = number; number = number + 1
        dict[b[i] + str("_e0")] = number; number = number + 1
        #先对L_1r_k_e2/e1/e0添加约束
        #L_1r_i_e2的约束，主要是和c2和c1的关系
        solver.add_clause([-dict[a[i] + str("_c2")], -dict[a[i] + str("_c1")], -dict[a[i] + str("_e2")]])  # c2'+c1'+e2'
        solver.add_clause([dict[a[i] + str("_c2")], dict[a[i] + str("_c1")], -dict[a[i] + str("_e2")]])    # c2+c1+e2'
        solver.add_clause([dict[a[i] + str("_c2")], -dict[a[i] + str("_c1")], dict[a[i] + str("_e2")]])    # c2+c1'+e2
        solver.add_clause([-dict[a[i] + str("_c2")], dict[a[i] + str("_c1")], dict[a[i] + str("_e2")]])    # c2'+c1+e2
        #L_1r_i_e1的约束，主要是和c2和c0的关系
        solver.add_clause([-dict[a[i] + str("_c2")], -dict[a[i] + str("_c0")], -dict[a[i] + str("_e1")]])  # c2'+c0'+e1'
        solver.add_clause([dict[a[i] + str("_c2")], dict[a[i] + str("_c0")], -dict[a[i] + str("_e1")]])  # c2+c0+e1'
        solver.add_clause([dict[a[i] + str("_c2")], -dict[a[i] + str("_c0")], dict[a[i] + str("_e1")]])  # c2+c0'+e1
        solver.add_clause([-dict[a[i] + str("_c2")], dict[a[i] + str("_c0")], dict[a[i] + str("_e1")]])  # c2'+c0+e1
        # L_1r_i_e0的约束，主要是和c1和c0的关系
        solver.add_clause([-dict[a[i] + str("_c1")], -dict[a[i] + str("_c0")], -dict[a[i] + str("_e0")]])  # c1'+c0'+e0'
        solver.add_clause([dict[a[i] + str("_c1")], dict[a[i] + str("_c0")], -dict[a[i] + str("_e0")]])  # c1+c0+e0'
        solver.add_clause([dict[a[i] + str("_c1")], -dict[a[i] + str("_c0")], dict[a[i] + str("_e0")]])  # c1+c0'+e0
        solver.add_clause([-dict[a[i] + str("_c1")], dict[a[i] + str("_c0")], dict[a[i] + str("_e0")]])  # c1'+c0+e0
        #对R_1r_k_e2/e1/e0添加约束
        # R_1r_i_e2的约束，主要是和c2和c1的关系
        solver.add_clause([-dict[b[i] + str("_c2")], -dict[b[i] + str("_c1")], -dict[b[i] + str("_e2")]])  # c2'+c1'+e2'
        solver.add_clause([dict[b[i] + str("_c2")], dict[b[i] + str("_c1")], -dict[b[i] + str("_e2")]])  # c2+c1+e2'
        solver.add_clause([dict[b[i] + str("_c2")], -dict[b[i] + str("_c1")], dict[b[i] + str("_e2")]])  # c2+c1'+e2
        solver.add_clause([-dict[b[i] + str("_c2")], dict[b[i] + str("_c1")], dict[b[i] + str("_e2")]])  # c2'+c1+e2
        #R_1r_i_e1的约束，主要是和c2和c0的关系
        solver.add_clause([-dict[b[i] + str("_c2")], -dict[b[i] + str("_c0")], -dict[b[i] + str("_e1")]])  # c2'+c0'+e1'
        solver.add_clause([dict[b[i] + str("_c2")], dict[b[i] + str("_c0")], -dict[b[i] + str("_e1")]])  # c2+c0+e1'
        solver.add_clause([dict[b[i] + str("_c2")], -dict[b[i] + str("_c0")], dict[b[i] + str("_e1")]])  # c2+c0'+e1
        solver.add_clause([-dict[b[i] + str("_c2")], dict[b[i] + str("_c0")], dict[b[i] + str("_e1")]])  # c2'+c0+e1
        # R_1r_i_e0的约束，主要是和c1和c0的关系
        solver.add_clause([-dict[b[i] + str("_c1")], -dict[b[i] + str("_c0")], -dict[b[i] + str("_e0")]])  # c1'+c0'+e0'
        solver.add_clause([dict[b[i] + str("_c1")], dict[b[i] + str("_c0")], -dict[b[i] + str("_e0")]])  # c1+c0+e0'
        solver.add_clause([dict[b[i] + str("_c1")], -dict[b[i] + str("_c0")], dict[b[i] + str("_e0")]])  # c1+c0'+e0
        solver.add_clause([-dict[b[i] + str("_c1")], dict[b[i] + str("_c0")], dict[b[i] + str("_e0")]])  # c1'+c0+e0


start_time = process_time()


number = 1
p_number = 1
#定义求解器
solver = pycryptosat.Solver(threads=32)
#主循环,这里的循环次数是想要找的混合差分区分器的轮数
for i in range(1, 33):
    Lin = genVars_Round(i)[0:64]
    Rin = genVars_Round(i)[64:128]
    SR1 = genVars_SR1_Round(i)
    SR2 = genVars_SR2_Round(i)
    SR8 = genVars_SR8_Round(i)
    aft_And = genVars_aftAnd_Round(i)
    Pro_aftAnd = genVars_ProaftAnd_Round(i)
    aft_XOR = genVars_aftXOR1_Round(i)
    #生成copy变量
    Copy1 = genVars_Copy_Round(i, 1)
    Copy2 = genVars_Copy_Round(i, 2)
    Copy3 = genVars_Copy_Round(i, 3)
    Copy4 = genVars_Copy_Round(i, 4)
    #生成Pcopy变量,用于后续添加目标函数约束，Pcopy1和Pcopy2是ph的复制变量，Pcopy3是pl的复制变量
    PCopy1 = genVars_PCopy_Round()
    for k in range(1, 65):
        p_number = p_number + 1
    PCopy2 = genVars_PCopy_Round()
    for k in range(1, 65):
        p_number = p_number + 1
    PCopy3 = genVars_PCopy_Round()
    for k in range(1, 65):
        p_number = p_number + 1
    #在生成约束前，先在字典中给Lin,Rin分配相应的位置,分轮次，第一轮不需要，后续轮次的Lin和Rin由前一轮生成
    if i == 1:
        insert_dict(Lin)
        insert_dict(Rin)
    else:
        gen_CopyCNF_Constraint(genVars_Round(i-1)[0:64], Rin)
    #生成copy变量需要添加相关约束
    gen_CopyCNF_Constraint(Lin, Copy1)
    gen_CopyCNF_Constraint(Lin, Copy2)
    gen_CopyCNF_Constraint(Lin, Copy3)
    gen_CopyCNF_Constraint(Lin, Copy4)
    #在进行And操作前，先进行移位操作
    shift_left(Copy1, SR1, 1)
    shift_left(Copy2, SR8, 8)
    shift_left(Copy3, SR2, 2)
    #生成每一轮每一个bit对应的and约束
    gen_AndCNF_Constraint(SR1, SR8, aft_And, Pro_aftAnd)

    #添加每一个bit对应三元组的依赖混合差分的约束
    gen_rotation_Constraint(SR1, SR8, aft_And)


    #生成概率变量ph的copy变量
    gen_PhCopyCNF_Constraint(Pro_aftAnd, PCopy1)
    gen_PhCopyCNF_Constraint(Pro_aftAnd, PCopy2)
    #生成概率变量pl的copy变量
    gen_PlCopyCNF_Constraint(Pro_aftAnd, PCopy3)
    #生成每一轮每一个bit对应的第一次XOR约束
    gen_XORCNF_Constraint(aft_And, Rin, aft_XOR)
    #生成每一轮每一个bit对应的第二次XOR约束,用下一轮的Lin来作为XOR操作的输出
    gen_XORCNF_Constraint(aft_XOR, SR2, genVars_Round(i+1)[0:64])

    # 添加输入混合差分模式的有关约束,先添加异或变量的有关约束，
    if i == 1:
        gen_XORCNF_input(Lin, Rin)

gen_objectfuntion_Constraint(32, 384)
#添加一个非平凡解约束，保证Lin不全为0
solver.add_clause([dict["L_1r_0_c2"], dict["L_1r_0_c1"], dict["L_1r_0_c0"],
                   dict["L_1r_1_c2"], dict["L_1r_1_c1"], dict["L_1r_1_c0"],
                   dict["L_1r_2_c2"], dict["L_1r_2_c1"], dict["L_1r_2_c0"],
                   dict["L_1r_3_c2"], dict["L_1r_3_c1"], dict["L_1r_3_c0"],
                   dict["L_1r_4_c2"], dict["L_1r_4_c1"], dict["L_1r_4_c0"],
                   dict["L_1r_5_c2"], dict["L_1r_5_c1"], dict["L_1r_5_c0"],
                   dict["L_1r_6_c2"], dict["L_1r_6_c1"], dict["L_1r_6_c0"],
                   dict["L_1r_7_c2"], dict["L_1r_7_c1"], dict["L_1r_7_c0"],
                   dict["L_1r_8_c2"], dict["L_1r_8_c1"], dict["L_1r_8_c0"],
                   dict["L_1r_9_c2"], dict["L_1r_9_c1"], dict["L_1r_9_c0"],
                   dict["L_1r_10_c2"], dict["L_1r_10_c1"], dict["L_1r_10_c0"],
                   dict["L_1r_11_c2"], dict["L_1r_11_c1"], dict["L_1r_11_c0"],
                   dict["L_1r_12_c2"], dict["L_1r_12_c1"], dict["L_1r_12_c0"],
                   dict["L_1r_13_c2"], dict["L_1r_13_c1"], dict["L_1r_13_c0"],
                   dict["L_1r_14_c2"], dict["L_1r_14_c1"], dict["L_1r_14_c0"],
                   dict["L_1r_15_c2"], dict["L_1r_15_c1"], dict["L_1r_15_c0"],
                   dict["L_1r_16_c2"], dict["L_1r_16_c1"], dict["L_1r_16_c0"],
                   dict["L_1r_17_c2"], dict["L_1r_17_c1"], dict["L_1r_17_c0"],
                   dict["L_1r_18_c2"], dict["L_1r_18_c1"], dict["L_1r_18_c0"],
                   dict["L_1r_19_c2"], dict["L_1r_19_c1"], dict["L_1r_19_c0"],
                   dict["L_1r_20_c2"], dict["L_1r_20_c1"], dict["L_1r_20_c0"],
                   dict["L_1r_21_c2"], dict["L_1r_21_c1"], dict["L_1r_21_c0"],
                   dict["L_1r_22_c2"], dict["L_1r_22_c1"], dict["L_1r_22_c0"],
                   dict["L_1r_23_c2"], dict["L_1r_23_c1"], dict["L_1r_23_c0"],
                   dict["L_1r_24_c2"], dict["L_1r_24_c1"], dict["L_1r_24_c0"],
                   dict["L_1r_25_c2"], dict["L_1r_25_c1"], dict["L_1r_25_c0"],
                   dict["L_1r_26_c2"], dict["L_1r_26_c1"], dict["L_1r_26_c0"],
                   dict["L_1r_27_c2"], dict["L_1r_27_c1"], dict["L_1r_27_c0"],
                   dict["L_1r_28_c2"], dict["L_1r_28_c1"], dict["L_1r_28_c0"],
                   dict["L_1r_29_c2"], dict["L_1r_29_c1"], dict["L_1r_29_c0"],
                   dict["L_1r_30_c2"], dict["L_1r_30_c1"], dict["L_1r_30_c0"],
                   dict["L_1r_31_c2"], dict["L_1r_31_c1"], dict["L_1r_31_c0"],
                   dict["L_1r_32_c2"], dict["L_1r_32_c1"], dict["L_1r_32_c0"],
                   dict["L_1r_33_c2"], dict["L_1r_33_c1"], dict["L_1r_33_c0"],
                   dict["L_1r_34_c2"], dict["L_1r_34_c1"], dict["L_1r_34_c0"],
                   dict["L_1r_35_c2"], dict["L_1r_35_c1"], dict["L_1r_35_c0"],
                   dict["L_1r_36_c2"], dict["L_1r_36_c1"], dict["L_1r_36_c0"],
                   dict["L_1r_37_c2"], dict["L_1r_37_c1"], dict["L_1r_37_c0"],
                   dict["L_1r_38_c2"], dict["L_1r_38_c1"], dict["L_1r_38_c0"],
                   dict["L_1r_39_c2"], dict["L_1r_39_c1"], dict["L_1r_39_c0"],
                   dict["L_1r_40_c2"], dict["L_1r_40_c1"], dict["L_1r_40_c0"],
                   dict["L_1r_41_c2"], dict["L_1r_41_c1"], dict["L_1r_41_c0"],
                   dict["L_1r_42_c2"], dict["L_1r_42_c1"], dict["L_1r_42_c0"],
                   dict["L_1r_43_c2"], dict["L_1r_43_c1"], dict["L_1r_43_c0"],
                   dict["L_1r_44_c2"], dict["L_1r_44_c1"], dict["L_1r_44_c0"],
                   dict["L_1r_45_c2"], dict["L_1r_45_c1"], dict["L_1r_45_c0"],
                   dict["L_1r_46_c2"], dict["L_1r_46_c1"], dict["L_1r_46_c0"],
                   dict["L_1r_47_c2"], dict["L_1r_47_c1"], dict["L_1r_47_c0"],
                   dict["L_1r_48_c2"], dict["L_1r_48_c1"], dict["L_1r_48_c0"],
                   dict["L_1r_49_c2"], dict["L_1r_49_c1"], dict["L_1r_49_c0"],
                   dict["L_1r_50_c2"], dict["L_1r_50_c1"], dict["L_1r_50_c0"],
                   dict["L_1r_51_c2"], dict["L_1r_51_c1"], dict["L_1r_51_c0"],
                   dict["L_1r_52_c2"], dict["L_1r_52_c1"], dict["L_1r_52_c0"],
                   dict["L_1r_53_c2"], dict["L_1r_53_c1"], dict["L_1r_53_c0"],
                   dict["L_1r_54_c2"], dict["L_1r_54_c1"], dict["L_1r_54_c0"],
                   dict["L_1r_55_c2"], dict["L_1r_55_c1"], dict["L_1r_55_c0"],
                   dict["L_1r_56_c2"], dict["L_1r_56_c1"], dict["L_1r_56_c0"],
                   dict["L_1r_57_c2"], dict["L_1r_57_c1"], dict["L_1r_57_c0"],
                   dict["L_1r_58_c2"], dict["L_1r_58_c1"], dict["L_1r_58_c0"],
                   dict["L_1r_59_c2"], dict["L_1r_59_c1"], dict["L_1r_59_c0"],
                   dict["L_1r_60_c2"], dict["L_1r_60_c1"], dict["L_1r_60_c0"],
                   dict["L_1r_61_c2"], dict["L_1r_61_c1"], dict["L_1r_61_c0"],
                   dict["L_1r_62_c2"], dict["L_1r_62_c1"], dict["L_1r_62_c0"],
                   dict["L_1r_63_c2"], dict["L_1r_63_c1"], dict["L_1r_63_c0"]])


#约束1，求和c^k_2>=1,k in [0,127],也就是L64+R64
for i in range(0, 64):
    constraint = []
    constraint.append(dict["L_1r_" + str(i) + "_c2"])
    constraint.append(dict["R_1r_" + str(i) + "_c2"])
solver.add_clause(constraint)
#约束2，求和c^k_1>=1,k in [0,127],也就是L64+R64
for i in range(0, 64):
    constraint = []
    constraint.append(dict["L_1r_" + str(i) + "_c1"])
    constraint.append(dict["R_1r_" + str(i) + "_c1"])
solver.add_clause(constraint)
#约束3，求和c^k_0>=1,k in [0,127],也就是L64+R64
for i in range(0, 64):
    constraint = []
    constraint.append(dict["L_1r_" + str(i) + "_c0"])
    constraint.append(dict["R_1r_" + str(i) + "_c0"])
solver.add_clause(constraint)
#约束4，求和e^k_2>=1,k in [0,127],也就是L64+R64
for i in range(0, 64):
    constraint = []
    constraint.append(dict["L_1r_" + str(i) + "_e2"])
    constraint.append(dict["R_1r_" + str(i) + "_e2"])
solver.add_clause(constraint)
#约束5，求和e^k_1>=1,k in [0,127],也就是L64+R64
for i in range(0, 64):
    constraint = []
    constraint.append(dict["L_1r_" + str(i) + "_e1"])
    constraint.append(dict["R_1r_" + str(i) + "_e1"])
solver.add_clause(constraint)
#约束6，求和e^k_0>=1,k in [0,127],也就是L64+R64
for i in range(0, 64):
    constraint = []
    constraint.append(dict["L_1r_" + str(i) + "_e0"])
    constraint.append(dict["R_1r_" + str(i) + "_e0"])
solver.add_clause(constraint)



##################################################################################
##################################################################################
sat, solution = solver.solve()
count = 0

if sat == False:
    print("不存在差分路径")
else:
    for i in range(1, 33):
        for j in range(0, 64):
            print("L_" + str(i) + "r_" + str(j) + "_c2" +":  %s"%solution[dict["L_" + str(i) + "r_" + str(j) + "_c2"]] +"  "
                  "L_" + str(i) + "r_" + str(j) + "_c1" +":  %s"%solution[dict["L_" + str(i) + "r_" + str(j) + "_c1"]] +"  "
                  "L_" + str(i) + "r_" + str(j) + "_c0" +":  %s"%solution[dict["L_" + str(i) + "r_" + str(j) + "_c0"]])
            print("R_" + str(i) + "r_" + str(j) + "_c2" +":  %s"%solution[dict["R_" + str(i) + "r_" + str(j) + "_c2"]] +"  "
                  "R_" + str(i) + "r_" + str(j) + "_c1" +":  %s"%solution[dict["R_" + str(i) + "r_" + str(j) + "_c1"]] +"  "
                  "R_" + str(i) + "r_" + str(j) + "_c0" +":  %s"%solution[dict["R_" + str(i) + "r_" + str(j) + "_c0"]])
            print("######################    AND运算   ########################")
            print("SR1_" + str(i) + "r_" + str(j) + "_c2" +":  %s"%solution[dict["SR1_" + str(i) + "r_" + str(j) + "_c2"]] +"  "
                  "SR1_" + str(i) + "r_" + str(j) + "_c1" +":  %s"%solution[dict["SR1_" + str(i) + "r_" + str(j) + "_c1"]] +"  "
                  "SR1_" + str(i) + "r_" + str(j) + "_c0" +":  %s"%solution[dict["SR1_" + str(i) + "r_" + str(j) + "_c0"]])
            print("SR8_" + str(i) + "r_" + str(j) + "_c2" +":  %s"%solution[dict["SR8_" + str(i) + "r_" + str(j) + "_c2"]] +"  "
                  "SR8_" + str(i) + "r_" + str(j) + "_c1" +":  %s"%solution[dict["SR8_" + str(i) + "r_" + str(j) + "_c1"]] +"  "
                  "SR8_" + str(i) + "r_" + str(j) + "_c0" +":  %s"%solution[dict["SR8_" + str(i) + "r_" + str(j) + "_c0"]])
            print("aftAnd_" + str(i) + "r_" + str(j) + "_c2" +":  %s"%solution[dict["aftAnd_" + str(i) + "r_" + str(j) + "_c2"]] +"  "
                  "aftAnd_" + str(i) + "r_" + str(j) + "_c1" +":  %s"%solution[dict["aftAnd_" + str(i) + "r_" + str(j) + "_c1"]] +"  "
                  "aftAnd_" + str(i) + "r_" + str(j) + "_c0" +":  %s"%solution[dict["aftAnd_" + str(i) + "r_" + str(j) + "_c0"]])
            print("ProaftAnd_" + str(i) + "r_" + str(j) + "_ph" +":  %s"%solution[dict["ProaftAnd_" + str(i) + "r_" + str(j) + "_ph"]] +"  "
                  "ProaftAnd_" + str(i) + "r_" + str(j) + "_pl" +":  %s"%solution[dict["ProaftAnd_" + str(i) + "r_" + str(j) + "_pl"]])
            if (solution[dict["ProaftAnd_" + str(i) + "r_" + str(j) + "_ph"]] == True):
                count = count + 2
            elif (solution[dict["ProaftAnd_" + str(i) + "r_" + str(j) + "_pl"]] == True):
                count = count + 1
            print("###########################################################")
            print("#####################   XOR运算   #########################")
            print("aftAnd_" + str(i) + "r_" + str(j) + "_c2" +":  %s"%solution[dict["aftAnd_" + str(i) + "r_" + str(j) + "_c2"]] +"  "
                  "aftAnd_" + str(i) + "r_" + str(j) + "_c1" +":  %s"%solution[dict["aftAnd_" + str(i) + "r_" + str(j) + "_c1"]] +"  "
                  "aftAnd_" + str(i) + "r_" + str(j) + "_c0" +":  %s"%solution[dict["aftAnd_" + str(i) + "r_" + str(j) + "_c0"]])
            print("R_" + str(i) + "r_" + str(j) + "_c2" +":  %s"%solution[dict["R_" + str(i) + "r_" + str(j) + "_c2"]] +"  "
                  "R_" + str(i) + "r_" + str(j) + "_c1" +":  %s"%solution[dict["R_" + str(i) + "r_" + str(j) + "_c1"]] +"  "
                  "R_" + str(i) + "r_" + str(j) + "_c0" +":  %s"%solution[dict["R_" + str(i) + "r_" + str(j) + "_c0"]])
            print("aftXOR1_" + str(i) + "r_" + str(j) + "_c2" +":  %s"%solution[dict["aftXOR1_" + str(i) + "r_" + str(j) + "_c2"]] +"  "
                  "aftXOR1_" + str(i) + "r_" + str(j) + "_c1" +":  %s"%solution[dict["aftXOR1_" + str(i) + "r_" + str(j) + "_c1"]] +"  "
                  "aftXOR1_" + str(i) + "r_" + str(j) + "_c0" +":  %s"%solution[dict["aftXOR1_" + str(i) + "r_" + str(j) + "_c0"]])
            print("###########################################################")
    for k in range(0, 64):
        print("L_33r_" + str(k) + "_c2" +":  %s"%solution[dict["L_33r_" + str(k) + "_c2"]] +"  "
              "L_33r_" + str(k) + "_c1" +":  %s"%solution[dict["L_33r_" + str(k) + "_c1"]] +"  "
              "L_33r_" + str(k) + "_c0" +":  %s"%solution[dict["L_33r_" + str(k) + "_c0"]])
    print(count)

#获取程序结束时间
end_time = process_time()
runTime = end_time - start_time
print("程序运行时间：", runTime, "秒")