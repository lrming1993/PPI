from gurobipy import *

num_node = 5
# num_edge = 5
# weight = [1, 2, 3, 4, 5]
"""
g1 = [0, 1, 2]
g2 = [3, 4]
edges = []
for i in g1:
    for j in g2:
        edges.append((i, j))
        edges.append((j, i))
"""

# edges = [(0, 1), (1, 5), (5, 4), (4, 3), (3, 0), (3, 2), (2, 1)]

edges = [(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3), (3, 4), (1, 4)]

num_edge = len(edges)

###################
model_1 = Model("test1")
variables_x_dict = {}
variables_y_dict = {}
node_list = []

for i in edges:
    y1 = i[0]
    y2 = i[1]
    variables_x_dict["{}_{}".format(y1, y2)] = model_1.addVar(vtype=GRB.CONTINUOUS, lb=0, ub=1, name="x{}_{}".format(y1, y2))
    # variables_y.append(model_1.addVar(vtype=GRB.INTEGER, name='w{}'.format(i), lb=0, ub=num_node - 1))
    if y1 not in node_list:
        node_list.append(y1)
        variables_y_dict["{}".format(y1)] = model_1.addVar(vtype=GRB.CONTINUOUS, lb=0, ub=1, name="y{}".format(y1))
    if y2 not in node_list:
        node_list.append(y2)
        variables_y_dict["{}".format(y2)] = model_1.addVar(vtype=GRB.CONTINUOUS, lb=0, ub=1, name="y{}".format(y2))

variables_x_list = list(variables_x_dict[i] for i in variables_x_dict)
variables_y_list = list(variables_y_dict[i] for i in variables_y_dict)
model_1.setObjective(quicksum(variables_x_list), GRB.MAXIMIZE)

model_1.addConstr(quicksum(variables_y_list) <= 1)
for n, i in enumerate(edges):
    model_1.addConstr(variables_x_dict["{}_{}".format(i[0], i[1])] <= variables_y_dict["{}".format(i[0])], "c{}_{}".format(n, 0))
    model_1.addConstr(variables_x_dict["{}_{}".format(i[0], i[1])] <= variables_y_dict["{}".format(i[1])], "c{}_{}".format(n, 1))
model_1.optimize()

for v in model_1.getVars():
    if v.varName[0] == "y":
        print("{}, {}".format(v.varName, v.x))

for v in model_1.getVars():
    if v.varName[0] == "x":
        print("{}, {}".format(v.varName, v.x))
###################
'''
model_1 = Model("test1")
variables_x = []
variables_w = []
for i in range(num_node):
    variables_x.append(model_1.addVar(vtype=GRB.BINARY, name="x{}".format(i)))
    variables_w.append(model_1.addVar(vtype=GRB.INTEGER, name='w{}'.format(i), lb=0, ub=num_node - 1))

model_1.setObjective(quicksum(variables_x), GRB.MINIMIZE)
for n, i in enumerate(edges):
    model_1.addConstr(variables_w[i[0]] - variables_w[i[1]] + num_node * variables_x[i[0]] >= 1, "c{}".format(i))
model_1.optimize()
for v in model_1.getVars():
    if v.varName[0] == "x":
        print('{}, {}'.format(v.varName, v.x))
for v in model_1.getVars():
    if v.varName[0] == "w":
        print('{}, {}'.format(v.varName, v.x))
print('Obj: {}'.format(model_1.objVal))

'''