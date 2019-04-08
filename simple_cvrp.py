# COMO USAR python simple_cvrp.py --file "CVRP/test.txt"

import random,sys,copy
from optparse import OptionParser

class cvrp:
    def __init__(self, filename):
        self.filename = filename
        self.deposits = []
        self.depositCount = 0
        self.capacity = 0
        self.init_data(self.filename)
        self.cost = self.calc_cost()

    def init_data(self,filename):
        node_coord = False
        node_demand = False
        depositCount = 0
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
                    self.capacity = line[9:]
                    continue
                else:
                    if node_coord == True:
                        depositCount = depositCount + 1
                        (deposit, x, y) = line.split()
                        self.deposits.append([deposit,x,y,0])
                        # print(self.deposits)
                    elif node_demand == True:
                        self.depositCount = depositCount
                        (deposit, quantity) = line.split()
                        self.deposits[int(deposit)-1] = [self.deposits[int(deposit)-1][0],self.deposits[int(deposit)-1][1],self.deposits[int(deposit)-1][2],quantity]
                        continue
                    continue

    def printStatus(self):
        print("\n")
        print("======")
        print("STATUS")
        print("======")
        print("Quantidade Depositos = ", self.depositCount)
        print("Capacidade = ", self.capacity)
        print("Depositos:")
        for i in self.deposits:
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
