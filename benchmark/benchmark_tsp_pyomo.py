import re, sys, time

at = time.time()

import numpy as np
import pyomo.environ as pe
from pyomo.opt import SolverFactory

node = int(sys.argv[1]);
edge = node * node
xcoord = np.random.rand(node)
ycoord = np.random.rand(node)
dist = {}
for i in range(node):
    for j in range(node):
        dist[i,j] = np.sqrt((xcoord[i]-xcoord[j])**2 + (ycoord[i]-ycoord[j])**2);

st = time.time()

m = pe.ConcreteModel()
m.N = pe.Set(initialize=range(node))
m.d = pe.Param(m.N, m.N, initialize=dist)
m.x = pe.Var(m.N, m.N, within=pe.Binary)
m.u = pe.Var(m.N, within=pe.Integers)
m.node = pe.Param(initialize=node)

def obj_total_distance(model):
    return sum(model.d[i,j] * model.x[i,j] for i in model.N for j in model.N)

def constr_outflow_balance(model, i):
    return sum(model.x[i,j] for j in model.N) == 1

def constr_inflow_balance(model, j):
    return sum(model.x[i,j] for i in model.N) == 1

def constr_u_start_regulate(model):
    return m.u[0] == 0

def constr_u_lb_regulate(model, i):
    if i > 0:
        return m.u[i] >= 2
    else:
        return pe.Constraint.Skip

def constr_u_ub_regulate(model, i):
    if i > 0:
        return m.u[i] <= node
    else:
        return pe.Constraint.Skip

def constr_subtour_elimination(model, i, j):
    if i > 0 and j > 0:
        return m.u[i] - m.u[j] + 1 <= m.node * (1-m.x[i,j])
    else:
        return pe.Constraint.Skip

m.obj = pe.Objective(rule=obj_total_distance, sense=pe.minimize)
m.con_outflow = pe.Constraint(m.N, rule=constr_outflow_balance)
m.con_inflow = pe.Constraint(m.N, rule=constr_inflow_balance)
m.con_ustart = pe.Constraint(rule=constr_u_start_regulate)
m.con_u_lb = pe.Constraint(m.N, rule=constr_u_lb_regulate)
m.con_u_ub = pe.Constraint(m.N, rule=constr_u_ub_regulate)
m.con_subtour = pe.Constraint(m.N, m.N, rule=constr_subtour_elimination)

rt = time.time()

opt = SolverFactory('gurobi_cl', logfile='check.log')
opt.options['timelimit'] = 10
opt.options['presolve'] = 0
# opt.options['preprocessing presolve'] = 0
result = opt.solve(m)

print "%s,%s,%s,%s,%s" % (node+node**2, node*2+1+(node-1)*2+(node-1)**2, time.time()-rt, time.time()-st, time.time()-at)
