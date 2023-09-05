"""
Function: Model SIMON algorithm and find Mixture differential distinguishers   /////Supplementary experiments for SIMON32-64
Date: 2022/07/14
Author: Zehan Wu
Contact:
"""
import pycryptosat
from time import process_time

##############################################################################################
#定义SIMON算法模型中的变量，一共应该有7个状态，因此应该定义7个状态的bit的混合差分变量模式，还需要带上轮数
##############################################################################################
#每一轮的输入bit的混合差分模式,分为左侧输入和右侧输入
def genVars_Round(r):
    return ['L_'+str(r)+'r_'+str(i) for i in range(16)] + ['R_'+str(r)+'r_'+str(i) for i in range(16)]

#每一轮的左移1位的bit的混合差分模式
def genVars_SR1_Round(r):
    return ['SR1_'+str(r)+'r_'+str(i) for i in range(16)]

#每一轮的左移2位的bit的混合差分模式
def genVars_SR2_Round(r):
    return ['SR2_'+str(r)+'r_'+str(i) for i in range(16)]

#每一轮的左移8位的bit的混合差分模式
def genVars_SR8_Round(r):
    return ['SR8_'+str(r)+'r_'+str(i) for i in range(16)]

#每一轮的＆运算之后的bit的混合差分模式
def genVars_aftAnd_Round(r):
    return ['aftAnd_'+str(r)+'r_'+str(i) for i in range(16)]

#每一轮的第一次异或后的bit的混合差分模式
def genVars_aftXOR1_Round(r):
    return ['aftXOR1_'+str(r)+'r_'+str(i) for i in range(16)]

#每一轮的and操作后的混合差分概率变量
def genVars_ProaftAnd_Round(r):
    return ['ProaftAnd_'+str(r)+'r_'+str(i) for i in range(16)]

#生成每一轮需要的copy变量，copy变量在传递约束方面是很有用的
def genVars_Copy_Round(r, k):
    return ['Copy_'+str(k)+'_'+str(r)+'r_'+str(i) for i in range(16)]

#生成每一轮需要的概率变量ph的copy变量
def genVars_PCopy_Round():
    #用p_number来表示概率变量的下标
    global  p_number
    return ['PCopy_'+str(i) for i in range(p_number, p_number+16)]

####################################################################################
####################################################################################
#定义向SAT模型中添加clause（CNF约束）的函数
####################################################################################
dict = {}
def gen_AndCNF_Constraint(a, b, c, d):
    global number
    for i in range(0, 16):
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
    for i in range(0, 16):
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
    for i in range(0, 16):
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
    for i in range(0, 16):
        dict[b[i]] = number; number = number + 1
        solver.add_clause([dict[a[i] + str("_ph")], -dict[b[i]]])          #ph+ph_copy'
        solver.add_clause([-dict[a[i] + str("_ph")], dict[b[i]]])          #ph'+ph_copy


#定义概率变量pl的copy操作的CNF
def gen_PlCopyCNF_Constraint(a, b):
    global number
    for i in range(0, 16):
        dict[b[i]] = number; number = number + 1
        solver.add_clause([dict[a[i] + str("_pl")], -dict[b[i]]])          #pl+pl_copy'
        solver.add_clause([-dict[a[i] + str("_pl")], dict[b[i]]])          #pl'+pl_copy

# 定义一个函数，不向模型中添加新的变量，相同的变量，通过不同的名字进行调用
def copy(a, b):
    for i in range(0, 16):
        #要保证变量a已经在字典中已经定义了
        dict[b[i] + str("_c2")] = dict[a[i] + str("_c2")]
        dict[b[i] + str("_c1")] = dict[a[i] + str("_c1")]
        dict[b[i] + str("_c0")] = dict[a[i] + str("_c0")]


#定义bit的循环左移,将相应的bit的混合差分模式赋给循环左移后的bit,k表示循环左移位数，其实主要的功能是让不同的变量名在SAT中指向同一变量，这样约束就不会混乱
def shift_left(a, b, k):
    if k == 1:
        for i in range(0, 16):
            dict[b[(i - 1) % 16] + str("_c2")] = dict[a[i] + str("_c2")]
            dict[b[(i - 1) % 16] + str("_c1")] = dict[a[i] + str("_c1")]
            dict[b[(i - 1) % 16] + str("_c0")] = dict[a[i] + str("_c0")]
    elif k == 2:
        for i in range(0, 16):
            dict[b[(i - 2) % 16] + str("_c2")] = dict[a[i] + str("_c2")]
            dict[b[(i - 2) % 16] + str("_c1")] = dict[a[i] + str("_c1")]
            dict[b[(i - 2) % 16] + str("_c0")] = dict[a[i] + str("_c0")]
    else:
        for i in range(0, 16):
            dict[b[(i - 8) % 16] + str("_c2")] = dict[a[i] + str("_c2")]
            dict[b[(i - 8) % 16] + str("_c1")] = dict[a[i] + str("_c1")]
            dict[b[(i - 8) % 16] + str("_c0")] = dict[a[i] + str("_c0")]

#定义一个函数，用于在dict中添加相应的值，方便添加约束用
def insert_dict(a):
    global number
    for i in range(0, 16):
        dict[a[i] + str("_c2")] = number; number = number + 1
        dict[a[i] + str("_c1")] = number; number = number + 1
        dict[a[i] + str("_c0")] = number; number = number + 1


#生成目标函数的约束
def gen_objectfuntion_Constraint(r, w):
    #r为轮次数, w为目标函数上界
    global number
    n = r*16*3          #
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

def gen_objectfunction2_Constraint(r, c, vars_num):
    list = []  # 用于存放指定变量的模型中位置数字
    for i in range(1, r+1):
        for j in range(0, 16):
            list.append(dict['ProaftAnd_'+str(i)+'r_'+str(j) + str("_Pdep")])
    cnf = CardEnc.atleast(lits=list, bound=c, top_id=vars_num, encoding=1)
    solver.add_clauses(cnf.clauses)


#添加SIMON算法and运算的差分因为移位产生的约束（差分依赖性约束）
def gen_rotation_Constraint(a, c, d):
    global number
    for i in range(0, 16):
        # 我需要先在模型中给Pdep分配位置
        dict[d[i] + str("_Pdep")] = number; number = number + 1
    for i in range(0, 16):
        with open('dependent_withpro_Constraint.txt', 'r') as file:
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
                        constraint.append("dict[a[(i+7)%16] + str(\"_c2\")]")
                    if line_split[j] == "αy_c1":
                        constraint.append("dict[a[(i+7)%16] + str(\"_c1\")]")
                    if line_split[j] == "αy_c0":
                        constraint.append("dict[a[(i+7)%16] + str(\"_c0\")]")
                    if line_split[j] == "αy_c2'":
                        constraint.append("-dict[a[(i+7)%16] + str(\"_c2\")]")
                    if line_split[j] == "αy_c1'":
                        constraint.append("-dict[a[(i+7)%16] + str(\"_c1\")]")
                    if line_split[j] == "αy_c0'":
                        constraint.append("-dict[a[(i+7)%16] + str(\"_c0\")]")
                    # 添加az相关约束
                    if line_split[j] == "αz_c2":
                        constraint.append("dict[a[(i+9)%16] + str(\"_c2\")]")
                    if line_split[j] == "αz_c1":
                        constraint.append("dict[a[(i+9)%16] + str(\"_c1\")]")
                    if line_split[j] == "αz_c0":
                        constraint.append("dict[a[(i+9)%16] + str(\"_c0\")]")
                    if line_split[j] == "αz_c2'":
                        constraint.append("-dict[a[(i+9)%16] + str(\"_c2\")]")
                    if line_split[j] == "αz_c1'":
                        constraint.append("-dict[a[(i+9)%16] + str(\"_c1\")]")
                    if line_split[j] == "αz_c0'":
                        constraint.append("-dict[a[(i+9)%16] + str(\"_c0\")]")
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
                        constraint.append("dict[c[(i+9)%16] + str(\"_c2\")]")
                    if line_split[j] == "βxz_c1":
                        constraint.append("dict[c[(i+9)%16] + str(\"_c1\")]")
                    if line_split[j] == "βxz_c0":
                        constraint.append("dict[c[(i+9)%16] + str(\"_c0\")]")
                    if line_split[j] == "βxz_c2'":
                        constraint.append("-dict[c[(i+9)%16] + str(\"_c2\")]")
                    if line_split[j] == "βxz_c1'":
                        constraint.append("-dict[c[(i+9)%16] + str(\"_c1\")]")
                    if line_split[j] == "βxz_c0'":
                        constraint.append("-dict[c[(i+9)%16] + str(\"_c0\")]")
                    #添加dep相关约束,依赖特征导致的概率变量,这里对应的就是从0-31比特,每一位的输出比特的计算,所以i不用+25之类的
                    if line_split[j] == "Pdep":
                        constraint.append("dict[d[(i-1)%16] + str(\"_Pdep\")]")
                    if line_split[j] == "Pdep'":
                        constraint.append("-dict[d[(i-1)%16] + str(\"_Pdep\")]")
                constraint_real = []
                for k in range(0, len(constraint)):
                    constraint_real.append(eval(constraint[k]))
                solver.add_clause(constraint_real)


#定义一个简单的两个比特变量机型异或运算时候的函数(主要是用于约束输入混合差分模式的约束）
def gen_XORCNF_input(a, b):
    global number
    for i in range(0, 16):
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
for i in range(1, 6):
    Lin = genVars_Round(i)[0:16]
    Rin = genVars_Round(i)[16:32]
    SR1 = genVars_SR1_Round(i)
    SR2 = genVars_SR2_Round(i)
    SR8 = genVars_SR8_Round(i)
    aft_And = genVars_aftAnd_Round(i)
    Pro_aftAnd = genVars_ProaftAnd_Round(i)
    aft_XOR = genVars_aftXOR1_Round(i)

    PCopy1 = genVars_PCopy_Round()
    for k in range(1, 17):
        p_number = p_number + 1
    PCopy2 = genVars_PCopy_Round()
    for k in range(1, 17):
        p_number = p_number + 1
    PCopy3 = genVars_PCopy_Round()
    for k in range(1, 17):
        p_number = p_number + 1
    #在生成约束前，先在字典中给Lin,Rin分配相应的位置,分轮次，第一轮不需要，后续轮次的Lin和Rin由前一轮生成
    if i == 1:
        insert_dict(Lin)
        insert_dict(Rin)
    else:
        copy(genVars_Round(i - 1)[0:16], Rin)  # 这里实际上就是R(r)和Lin(r-1)实际上指向的是同一个变量，通过这样可以减少相应的变量数目

    #在进行And操作前，先进行移位操作
    shift_left(Lin, SR1, 1)
    shift_left(Lin, SR8, 8)
    shift_left(Lin, SR2, 2)
    #生成每一轮每一个bit对应的and约束
    gen_AndCNF_Constraint(SR1, SR8, aft_And, Pro_aftAnd)

    #添加每一个bit对应三元组的依赖混合差分的约束
    gen_rotation_Constraint(Lin,  aft_And, Pro_aftAnd)

    #生成概率变量ph的copy变量
    gen_PhCopyCNF_Constraint(Pro_aftAnd, PCopy1)
    gen_PhCopyCNF_Constraint(Pro_aftAnd, PCopy2)
    #生成概率变量pl的copy变量
    gen_PlCopyCNF_Constraint(Pro_aftAnd, PCopy3)
    #生成每一轮每一个bit对应的第一次XOR约束
    gen_XORCNF_Constraint(aft_And, Rin, aft_XOR)
    #生成每一轮每一个bit对应的第二次XOR约束,用下一轮的Lin来作为XOR操作的输出
    gen_XORCNF_Constraint(aft_XOR, SR2, genVars_Round(i+1)[0:16])

    # 添加输入混合差分模式的有关约束,先添加异或变量的有关约束，
    if i == 1:
        gen_XORCNF_input(Lin, Rin)

####################################################
##最终目标函数2Ph+Pl-Pdep≤w-c   变向实现有负数的基数约束
####################################################
gen_objectfuntion_Constraint(5, 16)
vars_num = solver.nb_vars()
gen_objectfunction2_Constraint(5, 0, vars_num)


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
                   dict["L_1r_15_c2"], dict["L_1r_15_c1"], dict["L_1r_15_c0"]])

#约束1，求和c^k_2>=1,k in [0,31],也就是L16+R16
for i in range(0, 16):
    constraint = []
    constraint.append(dict["L_1r_" + str(i) + "_c2"])
    constraint.append(dict["R_1r_" + str(i) + "_c2"])
solver.add_clause(constraint)
#约束2，求和c^k_1>=1,k in [0,31],也就是L16+R16
for i in range(0, 16):
    constraint = []
    constraint.append(dict["L_1r_" + str(i) + "_c1"])
    constraint.append(dict["R_1r_" + str(i) + "_c1"])
solver.add_clause(constraint)
#约束3，求和c^k_0>=1,k in [0,31],也就是L16+R16
for i in range(0, 16):
    constraint = []
    constraint.append(dict["L_1r_" + str(i) + "_c0"])
    constraint.append(dict["R_1r_" + str(i) + "_c0"])
solver.add_clause(constraint)
#约束4，求和e^k_2>=1,k in [0,31],也就是L16+R16
for i in range(0, 16):
    constraint = []
    constraint.append(dict["L_1r_" + str(i) + "_e2"])
    constraint.append(dict["R_1r_" + str(i) + "_e2"])
solver.add_clause(constraint)
#约束5，求和e^k_1>=1,k in [0,31],也就是L16+R16
for i in range(0, 16):
    constraint = []
    constraint.append(dict["L_1r_" + str(i) + "_e1"])
    constraint.append(dict["R_1r_" + str(i) + "_e1"])
solver.add_clause(constraint)
#约束6，求和e^k_0>=1,k in [0,31],也就是L16+R16
for i in range(0, 16):
    constraint = []
    constraint.append(dict["L_1r_" + str(i) + "_e0"])
    constraint.append(dict["R_1r_" + str(i) + "_e0"])
solver.add_clause(constraint)


######################################################################################
######################################################################################
Vars_number = solver.nb_vars()
print(Vars_number)

sat, solution = solver.solve()
count = 0

if sat == False:
    print("不存在差分路径")
else:
    for i in range(1, 6):
        for j in range(0, 16):
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
                  "ProaftAnd_" + str(i) + "r_" + str(j) + "_pl" +":  %s"%solution[dict["ProaftAnd_" + str(i) + "r_" + str(j) + "_pl"]] +"  "
                  "ProaftAnd_" + str(i) + "r_" + str(j) + "_Pdep" +":  %s"%solution[dict["ProaftAnd_" + str(i) + "r_" + str(j) + "_Pdep"]])
            if (solution[dict["ProaftAnd_" + str(i) + "r_" + str(j) + "_ph"]] == True):
                count = count + 2
            elif (solution[dict["ProaftAnd_" + str(i) + "r_" + str(j) + "_pl"]] == True):
                count = count + 1
            elif (solution[dict["ProaftAnd_" + str(i) + "r_" + str(j) + "_Pdep"]] == True):
                count = count - 1
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
    for k in range(0, 16):
        print("L_6r_" + str(k) + "_c2" +":  %s"%solution[dict["L_6r_" + str(k) + "_c2"]] +"  "
              "L_6r_" + str(k) + "_c1" +":  %s"%solution[dict["L_6r_" + str(k) + "_c1"]] +"  "
              "L_6r_" + str(k) + "_c0" +":  %s"%solution[dict["L_6r_" + str(k) + "_c0"]])
    print(count)


#获取程序结束时间
end_time = process_time()
runTime = end_time - start_time
print("程序运行时间：", runTime, "秒")