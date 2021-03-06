#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import print_function
from ortools.linear_solver import pywraplp
from collections import namedtuple
from ortools.linear_solver import linear_solver_pb2
import math

Point = namedtuple("Point", ['x', 'y'])
Facility = namedtuple("Facility", ['index', 'setup_cost', 'capacity', 'location'])
Customer = namedtuple("Customer", ['index', 'demand', 'location'])

def length(point1, point2):
    return math.sqrt((point1.x - point2.x)**2 + (point1.y - point2.y)**2)

def solve_it(input_data):
    # Modify this code to run your optimization algorithm

    # parse the input
    lines = input_data.split('\n')

    parts = lines[0].split()
    facility_count = int(parts[0])
    customer_count = int(parts[1])
    
    facilities = []
    for i in range(1, facility_count+1):
        parts = lines[i].split()
        facilities.append(Facility(i-1, float(parts[0]), int(parts[1]), Point(float(parts[2]), float(parts[3])) ))

    customers = []
    for i in range(facility_count+1, facility_count+1+customer_count):
        parts = lines[i].split()
        customers.append(Customer(i-1-facility_count, int(parts[0]), Point(float(parts[1]), float(parts[2]))))

    print("variables: %s" %((facility_count*customer_count)+facility_count))
    
    # Create the mip solver with the CBC backend.
    solver = pywraplp.Solver('simple_mip_program',
                             pywraplp.Solver.CBC_MIXED_INTEGER_PROGRAMMING)
    
    infinity = solver.infinity()
    
    # Define the variables and set the objective
    objective = solver.Objective()
    facilitiesVar = [[]] * len(facilities)
    #print(facilities)
    #print(facilitiesVar)
    for i in range(0, facility_count):
        facilitiesVar[i] = solver.IntVar(0.0, 1.0, str(i))
        objective.SetCoefficient(facilitiesVar[i], facilities[i].setup_cost)
    
    customersVar = [[-1 for x in range(facility_count)] for y in range(customer_count)]
    for i in range(0, customer_count):
        for j in range(0, facility_count):
            customersVar[i][j] = solver.IntVar(0.0, 1.0, str(i) + "-" + str(j))
            #print(str(i) + "-" + str(j) + " ", end="")
            #print(customers[i].location, end="")
            #print(facilities[j].location, end="")
            #print(" =%s" %length(customers[i].location, facilities[j].location))
            objective.SetCoefficient(customersVar[i][j], length(customers[i].location, facilities[j].location))
            
            #print(customers[i].index, end="")
            #print(" %s" %facilities[j].index) 
        
    print('Number of variables =', solver.NumVariables())
        
    objective.SetMinimization()
        
    # Define the constraints
    # Facility activation constraint
    FAconstraints = [0] * facility_count
    #print(FAconstraints)
    #for i in range(0, facility_count):
    #    FAconstraints[i] = solver.Constraint(0, solver.infinity())
    #    FAconstraints[i].SetCoefficient(facilitiesVar[i], facility_count)
        #print(facility_count)
    #    for j in range(0, customer_count):
    #        FAconstraints[i].SetCoefficient(customersVar[j][i], -1)
    for i in range(0, facility_count):
        for j in range(0, customer_count):
            FAconstraints[i] = solver.Constraint(0, solver.infinity())
            FAconstraints[i].SetCoefficient(facilitiesVar[i], 1)
            FAconstraints[i].SetCoefficient(customersVar[j][i], -1)
            
    # Customer connection constraint
    CCConstraint = [0] * customer_count 
    for i in range(0, customer_count):
        CCConstraint[i] = solver.Constraint(1, 1)
        for j in range(0, facility_count):
            CCConstraint[i].SetCoefficient(customersVar[i][j], 1)

    # Facility capacity constraint
    FCConstraint = [0] * facility_count
    for i in range(0, facility_count):
        FCConstraint[i] = solver.Constraint(0, solver.infinity())
        print(facilitiesVar[i])
        print(facilities[i].capacity)
        print(facilitiesVar[i]*facilities[i].capacity)
        FCConstraint[i].SetCoefficient(facilitiesVar[i], facilitiesVar[i]*facilities[i].capacity)
        for j in range(0, customer_count):
            FCConstraint[i].SetCoefficient(customersVar[j][i], -customers[j].demand)
        
        
    print('Number of constraints =', solver.NumConstraints())
    
    if solver.NumVariables() >= 4002000:
        solver.SetTimeLimit(3600000)
    else:
        solver.SetTimeLimit(1800000)
    
    result_status = solver.Solve()
   
    if result_status == solver.OPTIMAL:
        print('Optimal Objective value =', solver.Objective().Value())
    else:  # No optimal solution was found.
        if result_status == solver.FEASIBLE:
          print('A potentially suboptimal solution was found.')
          print('Suboptimal Objective value =', solver.Objective().Value())
        else:
          print('The solver could not solve the problem.')
      
    #for i in range(0, facility_count):
    #    print("%s =" %i, end="")
    #    print(facilitiesVar[i].solution_value())
    #for i in range(0, customer_count):
    #    for j in range(0, facility_count):
    #        print("%s =" %(str(i) + "-" + str(j)), end="")
    #        print(customersVar[i][j].solution_value())
    
    solution = [-1]*len(customers)
    for i in range(0, customer_count):
        for j in range(0, facility_count):
            if customersVar[i][j].solution_value() == 1.0:
                solution[i] = j
                
    #capacity_remaining = [f.capacity for f in facilities]
    #facility_index = 0
    #for customer in customers:
    #    if capacity_remaining[facility_index] >= customer.demand:
    #       solution[customer.index] = facility_index
    #        capacity_remaining[facility_index] -= customer.demand
    #    else:
    #        facility_index += 1
    #        assert capacity_remaining[facility_index] >= customer.demand
    #        solution[customer.index] = facility_index
    #        capacity_remaining[facility_index] -= customer.demand

            
    used = [0]*len(facilities)
    for facility_index in solution:
        used[facility_index] = 1

    # calculate the cost of the solution
    obj = sum([f.setup_cost*used[f.index] for f in facilities])
    for customer in customers:
        obj += length(customer.location, facilities[solution[customer.index]].location)

    # prepare the solution in the specified output format
    output_data = '%.2f' % obj + ' ' + str(0) + '\n'
    output_data += ' '.join(map(str, solution))

    return output_data


import sys

if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        file_location = sys.argv[1].strip()
        with open(file_location, 'r') as input_data_file:
            input_data = input_data_file.read()
        print(solve_it(input_data))
    else:
        print('This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/fl_16_2)')

