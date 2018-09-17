import pulp, re, sys, time
import pandas as pd
import numpy as np

at = time.time()
node = int(sys.argv[1]);
xcoord = np.random.rand(node);
ycoord = np.random.rand(node);

edge = node * node
dist = np.zeros((node, node), dtype=np.float64)
for i in range(node):
  for j in range(node):
    dist[i,j] = np.sqrt((xcoord[i]-xcoord[j])**2 + (ycoord[i]-ycoord[j])**2);

st = time.time()
m = pulp.LpProblem("tsp", pulp.LpMinimize)

x = pulp.LpVariable.dicts('x', [(i, j) for i in range(node) for j in range(node)], 0, 1, pulp.LpBinary)
u = pulp.LpVariable.dicts('u', [i for i in range(node)], lowBound=0, upBound=None, cat=pulp.LpInteger)

m += pulp.lpSum(dist[i,j] * x[(i,j)] / 1000.0 for i in range(node) for j in range(node))

for i in range(node):
  m += pulp.lpSum(x[(i,j)] for j in range(node)) == 1
for j in range(node):
  m += pulp.lpSum(x[(i,j)] for i in range(node)) == 1

m += u[0] == 1
for i in range(1, node):
  u[i] >= 2
for i in range(1, node):
  u[i] <= node
for i in range(1, node):
  for j in range(1, node):
    m += u[i] - u[j] + 1 <= node * (1-x[(i,j)])

rt = time.time()
m.solve(pulp.solvers.CPLEX_CMD(msg=0, timelimit=10))
print "%s,%s,%s,%s,%s" % (len(x)+len(u), node*2+1+(node-1)*2+(node-1)**2, time.time()-rt, time.time()-st, time.time()-at)
