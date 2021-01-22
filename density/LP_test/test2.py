from gurobipy import *

class Node:
    def __init__(self):
        self.id = ""
        self.neighbor = []
        self.degree = 0
        self.weight = 0


path = "data/test1.txt"
node_index_dict = {}
all_nodes = []
all_nodes_pointer = 0
all_edges = []


def add_node(n):
    global all_nodes_pointer
    temp = Node()
    temp.id = n
    all_nodes.append(temp)
    node_index_dict[n] = all_nodes_pointer
    all_nodes_pointer += 1


def add_neighbor(n1, n2):
    all_nodes[node_index_dict[n1]].neighbor.append(n2)
    all_nodes[node_index_dict[n1]].degree += 1
    all_nodes[node_index_dict[n2]].neighbor.append(n1)
    all_nodes[node_index_dict[n2]].degree += 1


def add_neighbor_weighted(n1, n2, w):
    all_nodes[node_index_dict[n1]].neighbor.append(n2)
    all_nodes[node_index_dict[n1]].degree += 1
    all_nodes[node_index_dict[n1]].weight += w
    all_nodes[node_index_dict[n2]].neighbor.append(n1)
    all_nodes[node_index_dict[n2]].degree += 1
    all_nodes[node_index_dict[n2]].weight += w


with open(path) as f1:
    for n, i in enumerate(f1):
        if n == 0:
            continue
        i = i.split()
        n1 = i[0]
        n2 = i[1]
        w = i[2]
        all_edges.append((n1, n2))
        if n1 not in node_index_dict:
            add_node(n1)
        if n2 not in node_index_dict:
            add_node(n2)
        add_neighbor(n1, n2)

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
    variables_x_dict["{}_{}".format(y1, y2)] = model_1.addVar(vtype=GRB.CONTINUOUS, lb=0, ub=1,
                                                              name="x{}_{}".format(y1, y2))
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
    model_1.addConstr(variables_x_dict["{}_{}".format(i[0], i[1])] <= variables_y_dict["{}".format(i[0])],
                      "c{}_{}".format(n, 0))
    model_1.addConstr(variables_x_dict["{}_{}".format(i[0], i[1])] <= variables_y_dict["{}".format(i[1])],
                      "c{}_{}".format(n, 1))
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
