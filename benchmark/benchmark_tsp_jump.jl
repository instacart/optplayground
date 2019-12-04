using JuMP, CPLEX, Cbc;

at = time()
m = Model(solver=CplexSolver(CPX_PARAM_SCRIND=0, CPX_PARAM_TILIM=10));
# m = Model(solver=CbcSolver(logLevel=1))

# Parameter Initializationsd;kfjalkjdslfad
node = parse(ARGS[1]);
xcoord = rand(node);
ycoord = rand(node);

# Create the distance matrix and calculate the distance
dist = zeros(Float64, node, node);
for i in 1:node
    for j in 1:node
        dist[i,j] = sqrt((xcoord[i]-xcoord[j])^2 + (ycoord[i]-ycoord[j])^2);
    end
end

st = time()
# Variables :: x_{ij}
@variable(m, x[1:node,1:node], Bin);
@variable(m, u[1:node], Int);

# Objective :: minimize total travel distance
@objective(m, Min, sum(dist[i,j]*x[i,j] for i=1:node for j=1:node)/1000);

# # Constraints :: Touring inflow out-flow balance
for i in 1:node @constraint(m, sum(x[i,j] for j=1:node)==1) end
for j in 1:node @constraint(m, sum(x[i,j] for i=1:node)==1) end

# Constraints :: Subtour Elimination with Aux Variables
@constraint(m, u[1]==1);
for i in 2:node @constraint(m,  2 <= u[i]) end
for i in 2:node @constraint(m, u[i]<=node) end
for i in 2:node
    for j in 2:node @constraint(m, u[i]-u[j] + 1 <= node*(1-x[i,j])) end
end

rt = time()
solve(m, suppress_warnings=true)

print("$(m.numCols),$(length(m.linconstr)),$(time()-rt),$(time()-st),$(time()-at)\n")
