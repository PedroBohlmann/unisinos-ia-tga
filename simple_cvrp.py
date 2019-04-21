# COMO USAR python simple_cvrp.py --file "CVRP/test.txt"

import random, sys, copy, math
from optparse import OptionParser
from random import randint

solution = []

class cvrp:
    def __init__(self, filename, truck_count):
        self.filename = filename
        self.nodes = []
        self.nodes_count = 0
        self.capacity = 0
        self.deposit = None
        self.init_data(self.filename)
        self.truck_count = truck_count
        self.trucks = []
        self.init_trucks()
        self.solution = self.init_solution()
        self.total_distance = self.calc_total_distance()

        self.printStatus()
        self.solution = self.hill_climbing()
        print("Depois do hillclimbing")
        self.total_distance = self.calc_total_distance()
        self.printStatus()

    def init_data(self,filename):
        node_coord = False
        node_demand = False
        nodes_count = 0
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
                        nodes_count = nodes_count + 1
                        (deposit, x, y) = line.split()
                        self.nodes.append([deposit, int(x), int(y), 0])
                        # print(self.nodes)
                    elif node_demand == True:
                        self.nodes_count = nodes_count
                        (deposit, quantity) = line.split()
                        self.nodes[int(deposit)-1] = [self.nodes[int(deposit)-1][0], self.nodes[int(deposit)-1][1], self.nodes[int(deposit)-1][2], int(quantity)]
                        continue
                    continue
        self.deposit = self.nodes[0]
        self.nodes.pop(0)

    def retrieve_data(self,index):
        return self.nodes[int(index)][1],self.nodes[int(index)][2]

    def printStatus(self):
        print("STATUS")
        print("======")
        print("Capacidade = ", self.capacity)
        print("Deposito = ", self.deposit)
        print("Distancia total = ", self.total_distance)
        print("Trucks = ", self.trucks)
        # print("Nós:")
        total = 0
        for i in range(len(self.nodes)):
            if len(self.nodes[i]) == 5:
                total += 1
        print("Quantidade Depositos = ", len(self.nodes))
        print("Nós percorridos =", total)

    def init_trucks(self):
        for i in range(self.truck_count):
            self.trucks.append(int(self.capacity))

    def get_first_not_flagged_node(self):
        pos = 0
        for node in self.nodes:
            if len(node) != 5:
                return pos
            pos = pos + 1

    def count_available_nodes(self):
        count = 0
        for node in self.nodes:
            if len(node) != 5:
                count += 1
        return count

    def find_random_node(self, truck):
        node = None
        has_node = self.count_available_nodes() > 0
        smallest_node = self.get_lowest_available_node()
        while node is None and has_node and truck >= smallest_node[3]:
            pos = randint(0, len(self.nodes)-1)
            if len(self.nodes[pos]) != 5 and truck-self.nodes[pos][3] >= 0:
                self.nodes[pos].append(False)
                return pos
        return None

    def get_lowest_available_node(self):
        smallest_pos = self.get_first_not_flagged_node()
        if smallest_pos is None:
            return None

        smallest_node = self.nodes[smallest_pos]
        pos = 0
        for node in self.nodes:
            if node[3] < smallest_node[3] and len(node) != 5:
                smallest_node = node
                smallest_pos = pos
            pos += 1

        return smallest_node

    def init_solution(self):
        all_solutions = []
        for i in range(len(self.trucks)):
            current_solution = []
            truck = self.trucks[i]
            has_nodes = True
            while has_nodes:
                node = self.find_random_node(truck)
                if node is None:
                    has_nodes = False # has no more close nodes with enough capacity to supply
                else:
                    current_solution.append(node)
                    truck = truck - int(self.get_cost(node)) # update truck capacity
            self.trucks[i] = truck # update truck capacity
            all_solutions.append(current_solution)
        return all_solutions

    def hill_climbing(self):
        all_solutions = self.solution
        for solution_pos in range(len(all_solutions)):
            solution = all_solutions[solution_pos]

            for i in range(len(solution)):
                best_change_total = None
                best_change_pos = None
                for j in range(i+1, len(solution)):
                    distance_a_before = self.calc_distance_around_node_in_solution(solution[i], solution, i)
                    distance_b_before = self.calc_distance_around_node_in_solution(solution[j], solution, j)
                    total_before = distance_a_before + distance_b_before

                    # do change
                    aux = solution[i]
                    solution[i] = solution[j]
                    solution[j] = aux

                    # calc the same distance
                    distance_a_after = self.calc_distance_around_node_in_solution(solution[i], solution, i)
                    distance_b_after = self.calc_distance_around_node_in_solution(solution[j], solution, j)
                    total_after = distance_a_after + distance_b_after

                    # print('total before', total_before)
                    # print('total after', total_after)

                    # change back because original order was ok
                    aux = solution[i]
                    solution[i] = solution[j]
                    solution[j] = aux

                    if total_after < total_before:
                        if best_change_total is None:
                            best_change_pos = j
                            best_change_total = total_after
                        elif best_change_total > total_after:
                            best_change_pos = j
                            best_change_total = total_after
                if best_change_total is not None:
                    aux = solution[i]
                    solution[i] = solution[best_change_pos]
                    solution[best_change_pos] = aux
        # changes between trucks
        for solution_pos in range(len(all_solutions)):
            solution = all_solutions[solution_pos]

            best_change_total = None
            best_change_pos_current_solution = None
            best_change_pos_next_solution = None
            best_change_solution = None
            
            for next_solution_pos in range(solution_pos+1, len(all_solutions)):
                next_solution = all_solutions[next_solution_pos]

                best_change_total = None
                best_change_pos_current_solution = None
                best_change_pos_next_solution = None
                best_change_solution = None

                for i in range(len(solution)):
                    for j in range(len(next_solution)):
                        if (self.trucks[solution_pos] + self.get_cost(solution[i])) - self.get_cost(next_solution[j]) >= 0 and (self.trucks[next_solution_pos] + self.get_cost(next_solution[j]) - self.get_cost(solution[i])) >= 0: # check if truck has enough capacity
                            distance_a_before = self.calc_distance_around_node_in_solution(next_solution[j], solution, i)
                            distance_b_before = self.calc_distance_around_node_in_solution(solution[i], next_solution, j)
                            total_before = distance_a_before + distance_b_before

                            aux = solution[i]
                            solution[i] = next_solution[j]
                            next_solution[j] = aux

                            distance_a_after = self.calc_distance_around_node_in_solution(next_solution[j], solution, i)
                            distance_b_after = self.calc_distance_around_node_in_solution(solution[i], next_solution, j)
                            total_after = distance_a_after + distance_b_after

                            aux = solution[i]
                            solution[i] = next_solution[j]
                            next_solution[j] = aux
                            if total_after < total_before: # check if is better with change
                                if best_change_total is None:
                                    best_change_pos_current_solution = i
                                    best_change_pos_next_solution = j
                                    best_change_total = total_after
                                    best_change_solution = next_solution_pos
                                elif best_change_total > total_after:
                                    best_change_pos_current_solution = i
                                    best_change_pos_next_solution = j
                                    best_change_total = total_after
                                    best_change_solution = next_solution_pos
            if best_change_total is not None:
                # update truck capacity
                self.trucks[solution_pos] += self.get_cost(solution[best_change_pos_current_solution]) - self.get_cost(all_solutions[best_change_solution][best_change_pos_next_solution])
                self.trucks[best_change_solution] += self.get_cost(all_solutions[best_change_solution][best_change_pos_next_solution]) - self.get_cost(solution[best_change_pos_current_solution])
                # change
                aux = solution[best_change_pos_current_solution]
                solution[best_change_pos_current_solution] = all_solutions[best_change_solution][best_change_pos_next_solution]
                next_solution[best_change_pos_next_solution] = aux             

        return all_solutions

    def calc_cost_route(self, nodes):
        total = 0
        index = 0
        selected_nodes = []

        for i in nodes:
            selected_nodes.append(self.nodes[i])

        # print('self nodes',self.nodes)
        # print('nodes',selected_nodes)
        for node in selected_nodes:
            if index == 0:
                total += self.calc_cost(self.deposit[1], node[1], self.deposit[2], node[2])
            if index+1 < len(nodes):
                total += self.calc_cost(node[1], self.nodes[index+1][1], node[2], self.nodes[index+1][2])
            elif index == len(nodes)-1:
                total += self.calc_cost(node[1], self.deposit[1], node[2], self.deposit[2])
            else:
                total += self.calc_cost(node[1], self.nodes[index+1][1], node[2], self.nodes[index+1][2])
            index += 1
        return total

    def calc_total_distance(self):
        total = 0
        for solution in self.solution:
            total += self.calc_cost_route(solution)
        return total

    def calc_distance_around_node_in_solution(self, node_pos, solution, solution_pos):
        total_distance = 0
        if solution_pos == 0:
            total_distance += self.calc_distance(self.nodes[node_pos], self.deposit)
        else:
            total_distance += self.calc_distance(self.nodes[node_pos], self.nodes[solution[solution_pos - 1]])

        if solution_pos == len(solution)-1:
            total_distance += self.calc_distance(self.nodes[node_pos], self.deposit)
        else:
            total_distance += self.calc_distance(self.nodes[node_pos], self.nodes[solution[solution_pos + 1]])
        return total_distance


    def calc_distance(self, node_a, node_b):
        return self.calc_cost(node_a[1], node_b[1], node_a[2], node_b[2])

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
