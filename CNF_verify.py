"""
Function: Verify whether the CNF matches the feasible point set
Date: 2022/03/04
Arthor: Zehan Wu
Contact:
"""
#c2:1   c1:2   c0:3   d2:4  d1:5  d0:6   e2:7   e1:8  e0:9   ph:10   pl:11
import pycryptosat
from pycryptosat import Solver
#首先添加利用可行点集与logic Friday生成的初始的CNF
solver = pycryptosat.Solver()
solver.add_clause([1, 2, 3, 4, 5, 6, -11])  #c2+c1+c0+d2+d1+d0+pl'
solver.add_clause([1, 4, -7])   #c2+d2+e2'
solver.add_clause([2, 5, -8])   #c1+d1+e1'
solver.add_clause([3, 6, -9])   #c0+d0+e0'
solver.add_clause([-1, 2, -3, 7, -8, -9])   #c2'+c1+c0'+e2+e1'+e0'
solver.add_clause([-1, -2, 3, 7, -8, -9])   #c2'+c1'+c0+e2+e1'+e0'
solver.add_clause([-4, 5, -6, 7, -8, -9])   #d2'+d1+d0'+e2+e1'+e0'
solver.add_clause([-4, -5, 6, 7, -8, -9])   #d2'+d1'+d0+e2+e1'+e0'
solver.add_clause([4, -5, -6, -7, 8, -9])   #d2+d1'+d0'+e2'+e1+e0'
solver.add_clause([1, -2, -3, -7, 8, -9])   #c2+c1'+c0'+e2'+e1+e0'
solver.add_clause([-1, -2, 3, -7, 8, -9])   #c2'+c1'+c0+e2'+e1+e0'
solver.add_clause([-4, -5, 6, -7, 8, -9])   #d2'+d1'+d0+e2'+e1+e0'
solver.add_clause([4, -5, -6, -7, -8, 9])   #d2+d1'+d0'+e2'+e1'+e0
solver.add_clause([-4, 5, -6, -7, -8, 9])   #d2'+d1+d0'+e2'+e1'+e0
solver.add_clause([1, -2, -3, -7, -8, 9])   #c2+c1'+c0'+e2'+e1'+e0
solver.add_clause([-1, 2, -3, -7, -8, 9])   #c2'+c1+c0'+e2'+e1'+e0
solver.add_clause([1, 3, -4, 7, -9])   #c2+c0+d2'+e2+e0'
solver.add_clause([2, 3, -5, 8, -9])   #c1+c0+d1'+e1+e0'
solver.add_clause([-1, 4, 6, 7, -9])   #c2'+d2+d0+e2+e0'
solver.add_clause([-2, 5, 6, 8, -9])   #c1'+d1+d0+e1+e0'
solver.add_clause([1, 2, -4, 7, -8])   #c2+c1+d2'+e2+e1'
solver.add_clause([2, 3, -6, -8, 9])   #c1+c0+d0'+e1'+e0
solver.add_clause([-1, 4, 5, 7, -8])   #c2'+d2+d1+e2+e1'
solver.add_clause([-3, 5, 6, -8, 9])   #c0'+d1+d0+e1'+e0
solver.add_clause([1, 2, -5, -7, 8])   #c2+c1+d1'+e2'+e1
solver.add_clause([1, 3, -6, -7, 9])   #c2+c0+d0'+e2'+e0
solver.add_clause([-2, 4, 5, -7, 8])   #c1'+d2+d1+e2'+e1
solver.add_clause([-3, 4, 6, -7, 9])   #c0'+d2+d0+e2'+e0
solver.add_clause([-1, 2, -3, 4, -5, -6, 7, 8, 9])   #c2'+c1+c0'+d2+d1'+d0'+e2+e1+e0
solver.add_clause([-1, -2, 3, 4, -5, -6, 7, 8, 9])   #c2'+c1'+c0+d2+d1'+d0'+e2+e1+e0
solver.add_clause([1, -2, -3, -4, 5, -6, 7, 8, 9])   #c2+c1'+c0'+d2'+d1+d0'+e2+e1+e0
solver.add_clause([-1, -2, 3, -4, 5, -6, 7, 8, 9])   #c2'+c1'+c0+d2'+d1+d0'+e2+e1+e0
solver.add_clause([1, -2, -3, -4, -5, 6, 7, 8, 9])   #c2+c1'+c0'+d2'+d1'+d0+e2+e1+e0
solver.add_clause([-1, 2, -3, -4, -5, 6, 7, 8, 9])   #c2'+c1+c0'+d2'+d1'+d0+e2+e1+e0
solver.add_clause([-10, -11])   #ph'+pl'
solver.add_clause([-6, 10, 11])   #d0'+ph+pl
solver.add_clause([-5, 10, 11])   #d1'+ph+pl
solver.add_clause([-3, -5, 6, -11])   #c0'+d1'+d0+pl'
solver.add_clause([-2, 5, -6, -11])   #c1'+d1+d0'+pl'
solver.add_clause([-4, 10, 11])   #d2'+ph+pl
solver.add_clause([-1, 4, -5, -11])   #c2'+d2+d1'+pl'
solver.add_clause([4, 5, 6, -10])   #d2+d1+d0+ph'
solver.add_clause([-2, 3, -6, -11])   #c1'+c0+d0'+pl'
solver.add_clause([2, -3, -5, -11])   #c1+c0'+d1'+pl'
solver.add_clause([-3, -4, 6, -11])   #c0'+d2'+d0+pl'
solver.add_clause([1, 2, 3, -10])   #c2+c1+c0+ph'
solver.add_clause([1, -3, -4, -11])   #c2+c0'+d2'+pl'
solver.add_clause([-3, 10, 11])   #c0'+ph+pl
solver.add_clause([-2, -3, -5, -6, -8, 9])   #c1'+c0'+d1'+d0'+e1'+e0
solver.add_clause([-2, -3, -5, -6, 8, -9])   #c1'+c0'+d1'+d0'+e1+e0'
solver.add_clause([-1, -3, -4, -6, 7, -9])   #c2'+c0'+d2'+d0'+e2+e0'
solver.add_clause([-1, 3, -6, -11])   #c2'+c0+d0'+pl'
solver.add_clause([-1, -2, -4, -5, -7, 8])   #c2'+c1'+d2'+d1'+e2'+e1
solver.add_clause([-1, -3, -4, -6, -7, 9])   #c2'+c0'+d2'+d0'+e2'+e0
solver.add_clause([-1, -2, -4, -5, 7, -8])   #c2'+c1'+d2'+d1'+e2+e1'
solver.add_clause([-1, -2, -3, -4, -5, -6, 11])   #c2'+c1'+c0'+d2'+d1'+d0'+pl
solver.add_clause([-2, -4, 5, -11])   #c1'+d2'+d1+pl'
solver.add_clause([-2, 10, 11])   #c1'+ph+pl
solver.add_clause([-1, 4, -6, -11])   #c2'+d2+d0'+pl'
solver.add_clause([-1, 2, 3, 5, 6, 11])   #c2'+c1+c0+d1+d0+pl
solver.add_clause([-1, 2, -5, -11])   #c2'+c1+d1'+pl'
solver.add_clause([1, -2, -4, -11])   #c2+c1'+d2'+pl'
solver.add_clause([-1, -2, 3, -4, -5, 6, 11])   #c2'+c1'+c0+d2'+d1'+d0+pl
solver.add_clause([-1, 2, -3, -4, 5, -6, 11])   #c2'+c1+c0'+d2'+d1+d0'+pl
solver.add_clause([1, -2, -3, 4, -5, -6, 11])   #c2+c1'+c0'+d2+d1'+d0'+pl
solver.add_clause([1, 3, 4, 6, -10])   #c2+c0+d2+d0+ph'
solver.add_clause([1, 2, 4, 5, -10])   #c2+c1+d2+d1+ph'
solver.solve()
print(solver.solve())
#循环添加每一次求解出来的可行点对应的约束,重点是要循环几次
flag = 1
feasible_point_new = solver.solve()
count = 0   #统计可行点数量
while(flag == 1):
    if feasible_point_new[0] == False:  #循环终止条件
        flag = 0
        break
    clause_new = [0] * 11  # 11维的点，对应的新的约束也是11维的
    count = count + 1
    # print(feasible_point_new)
    for i in range(1, 12):
        if feasible_point_new[1][i] == False:
            clause_new[i-1] = i
        else:
            clause_new[i-1] = -i
    print(clause_new)
    solver.add_clause(clause_new)
    solver.solve()
    feasible_point_new = solver.solve()
    print(feasible_point_new)
print(count)
# solver.add_clause([1, 2, -3, 4, -5, 6, 7, 8, 9, -10, 11])   #去除求解出的第一个可行解
# solver.solve()
# print(solver.solve())




















































