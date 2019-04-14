# COMO USAR python simple_cvrp.py --file "CVRP/test.txt"

import random,sys,copy,math
from optparse import OptionParser

#          truck,node1,node2,node3,node4
solution = [[1,1,2,3,4,5,6,7,8,9,10]]

class cvrp:
    def __init__(self, filename, truck_count):
        self.filename = filename
        self.nodes = []
        self.nodesCount = 0
        self.capacity = 0
        self.deposit = None
        self.init_data(self.filename)
        self.truck_count = truck_count
        self.trucks = []
        self.init_trucks()

        self.hill_climbing()

    def init_data(self,filename):
        node_coord = False
        node_demand = False
        nodesCount = 0
        with open (filename, 'rt') as file:
            for line in file:
                if "NODE_COORD_SECTION" in line:
                    node_demand = False
                    node_coord = True
                    # do something
                    continue
                elif "DEMAND_SECTION" in line:
                    node_demand = True
                    node_coord = False
                    # do something
                    continue
                elif "CAPACITY" in line:
                    self.capacity = line[9:-1] #-1 para remover o \n
                    continue
                else:
                    if node_coord == True:
                        nodesCount = nodesCount + 1
                        (deposit, x, y) = line.split()
                        self.nodes.append([deposit,x,y,0])
                        # print(self.nodes)
                    elif node_demand == True:
                        self.nodesCount = nodesCount
                        (deposit, quantity) = line.split()
                        self.nodes[int(deposit)-1] = [self.nodes[int(deposit)-1][0],self.nodes[int(deposit)-1][1],self.nodes[int(deposit)-1][2],quantity]
                        continue
                    continue
        self.deposit = self.nodes[0]
        self.nodes.pop(0)

    def retrieve_data(self,index):
        return self.nodes[int(index)][1],self.nodes[int(index)][2]

    def printStatus(self):
        print("\n")
        print("======")
        print("STATUS")
        print("======")
        print("Quantidade Depositos = ", self.nodesCount)
        print("Capacidade = ", self.capacity)
        print("Deposito = ", self.deposit)
        print("Custo = ", self.cost)
        # print("Nós:")
        # for i in self.nodes:
        #     print(i)

    def init_trucks(self):
        for i in range(self.truck_count):
            self.trucks.append(int(self.capacity))

    def get_first_not_flagged_node(self):
        pos = 0
        for node in self.nodes:
            if len(node) != 5:
                return pos
            pos = pos + 1

    def findClosestAfordableNode(self, truck, xTruck, yTruck):
        smallest_pos = self.get_first_not_flagged_node()
        if smallest_pos is None:
            return None

        (xSmall, ySmall) = self.retrieve_data(smallest_pos)

        smallest_cost = self.calc_cost(int(xSmall), int(xTruck), int(ySmall), int(yTruck))

        pos = 0
        for node in self.nodes:
            cost = self.calc_cost(int(node[1]), int(xTruck), int(node[2]), int(yTruck))
            if cost < smallest_cost and len(node) != 5 and (truck-int(node[3]) >= 0):
                smallest_cost = cost
                smallest_pos = pos
            pos = pos + 1
        if (truck-int(self.nodes[smallest_pos][3])) < 0:
            return None
        self.nodes[smallest_pos].append(False)
        return smallest_pos

    def hill_climbing(self):
        all_solutions = []
        for i in range(len(self.trucks)):
            current_solution= []
            truck = self.trucks[i]
            has_nodes = True
            while truck > 0 and has_nodes:
                if len(current_solution) == 0:
                    node = self.findClosestAfordableNode(truck, self.deposit[1], self.deposit[2])
                else:
                    (xTruck, yTruck) = self.retrieve_data(current_solution[-1])
                    node = self.findClosestAfordableNode(truck, xTruck, yTruck)
                if node is None:
                    has_nodes = False # has no more close nodes with enough capacity to supply
                else:
                    current_solution.append(node)
                    truck = truck - int(self.get_cost(node)) # update truck capacity
            self.trucks[i] = truck # update truck capacity
            all_solutions.append(current_solution)
        return all_solutions

    def calc_cost(self, xa, xb, ya, yb):
        return math.sqrt(((xa-xb) * (xa-xb))+((ya-yb) * (ya-yb)))

    def get_cost(self, pos):
        if not self.nodes:
            return None
        else:
            return self.nodes[pos][3]

    def check_quantity(self):
        qtyOk = 0
        count = 0
        truckQty = int(self.capacity)
        for trip in solution:
            node_length = len(trip)-1
            for node in range(0, node_length):
                print(int(self.nodes[int(node)][3]))
                truckQty = truckQty - int(self.nodes[int(node)][3])
                if truckQty < 0:
                    qtyOk = qtyOk -1
                print("current quantity", truckQty)
        if qtyOk == 0:
            qtyOk = qtyOk+1
        return qtyOk

if __name__ == "__main__":

    parser = OptionParser()
    parser.add_option("--file", dest="filename", help="Path of file", default="CVRP/eil33.vrp.txt",
                     type="string")
    parser.add_option("--trucks", dest="truck_count", help="Quantity of trucks", default="4",
                     type="int")

    (options, args) = parser.parse_args()

    CVRP = cvrp(options.filename, options.truck_count)
    CVRP.printStatus()
    print("OK")
