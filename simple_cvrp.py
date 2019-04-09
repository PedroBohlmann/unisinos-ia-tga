# COMO USAR python simple_cvrp.py --file "CVRP/test.txt"

import random,sys,copy,math
from optparse import OptionParser

#          truck,node1,node2,node3,node4
solution = [[1,1,2,3,4,5,6,7,8,9,10]]

class cvrp:
    def __init__(self, filename):
        self.filename = filename
        self.nodes = []
        self.nodesCount = 0
        self.capacity = 0
        self.deposit = None
        self.init_data(self.filename)

        # test one cost
        (xa, ya) = self.retrieve_data(2)
        (xb, yb) = self.retrieve_data(1)
        self.cost = self.calc_cost(int(xa), int(xb), int(ya), int(yb))

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

    def hill_climbing():
        return 0

    def calc_cost(self, xa, xb, ya, yb):
        return math.sqrt(((xa-xb) * (xa-xb))+((ya-yb) * (ya-yb)))

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

    (options, args) = parser.parse_args()

    CVRP = cvrp(options.filename)
    CVRP.printStatus()
    print("OK")
