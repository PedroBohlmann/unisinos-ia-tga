# COMO USAR python simple_cvrp.py --file "CVRP/test.txt"

import random,sys,copy
from optparse import OptionParser

class cvrp:
    def __init__(self, filename):
        self.filename = filename
        self.nodes = []
        self.nodesCount = 0
        self.capacity = 0
        self.deposit = None
        self.init_data(self.filename)
        self.cost = self.calc_cost()

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

    def printStatus(self):
        print("\n")
        print("======")
        print("STATUS")
        print("======")
        print("Quantidade Depositos = ", self.nodesCount)
        print("Capacidade = ", self.capacity)
        print("Deposito = ", self.deposit)
        print("Nós:")
        for i in self.nodes:
            print(i)

    def hill_climbing():
        return 0

    def calc_cost(self):
        return 0

if __name__ == "__main__":

    parser = OptionParser()
    parser.add_option("--file", dest="filename", help="Path of file", default="CVRP/eil33.vrp.txt",
                     type="string")

    (options, args) = parser.parse_args()

    CVRP = cvrp(options.filename)
    CVRP.printStatus()
    print("OK")
