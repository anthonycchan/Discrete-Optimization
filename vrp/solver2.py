#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import print_function
from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp

import math
from collections import namedtuple

Customer = namedtuple("Customer", ['index', 'demand', 'x', 'y'])

def length(customer1, customer2):
    return math.sqrt((customer1.x - customer2.x)**2 + (customer1.y - customer2.y)**2)

def solve_it(input_data):
    # Modify this code to run your optimization algorithm

    # parse the input
    lines = input_data.split('\n')

    parts = lines[0].split()
    customer_count = int(parts[0])
    vehicle_count = int(parts[1])
    vehicle_capacity = int(parts[2])
    
    customers = []
    for i in range(1, customer_count+1):
        line = lines[i]
        parts = line.split()
        customers.append(Customer(i-1, int(parts[0]), float(parts[1]), float(parts[2])))

    #the depot is always the first customer in the input
    depot = customers[0] 
    
    useGoogleVRPSolver = True
    if useGoogleVRPSolver == True:
    print (customer_count)
        # Create the routing index manager.
        manager = pywrapcp.RoutingIndexManager(
            len(customers), vehicle_count, depot.index)

        # Create Routing Model.
        routing = pywrapcp.RoutingModel(manager)


        # Create and register a transit callback.
        def distance_callback(from_index, to_index):
            """Returns the distance between the two nodes."""
            # Convert from routing variable Index to distance matrix NodeIndex.
            from_node = manager.IndexToNode(from_index)
            to_node = manager.IndexToNode(to_index)
            absLength = int(length(customers[from_node], customers[to_node])*100)
            #print("from: %s to %s = " %(from_node, to_node), end="")
            #print(absLength)
            return absLength

        transit_callback_index = routing.RegisterTransitCallback(distance_callback)

        # Define cost of each arc.
        routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)
    
        # Add Capacity constraint.
        def demand_callback(from_index):
            """Returns the demand of the node."""
            # Convert from routing variable Index to demands NodeIndex.
            from_node = manager.IndexToNode(from_index)
            #return data['demands'][from_node]
            #print("customer %s = " %from_node, end="")
            #print(customers[from_node].demand)
            return customers[from_node].demand

        vehicleCap=[vehicle_capacity for i in range(vehicle_count)]
        #print(vehicleCap)
        demand_callback_index = routing.RegisterUnaryTransitCallback(
            demand_callback)
        routing.AddDimensionWithVehicleCapacity(
            demand_callback_index,
            0,  # null capacity slack
            vehicleCap,  # vehicle maximum capacities
            True,  # start cumul to zero
            'Capacity')

        # Setting first solution heuristic.
        search_parameters = pywrapcp.DefaultRoutingSearchParameters()
        search_parameters.first_solution_strategy = (
            routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC)
        #search_parameters.local_search_metaheuristic = (
        #    routing_enums_pb2.LocalSearchMetaheuristic.AUTOMATIC)
        #search_parameters.time_limit.seconds = 900
        search_parameters.solution_limit = 1
        #search_parameters.log_search = True
        
        # Solve the problem.
        assignment = routing.SolveWithParameters(search_parameters)
        print("finish")
        
        #if assignment:
        #    print_solution(manager, routing, assignment, vehicle_count, customers)
        
    # build a trivial solution
    # assign customers to vehicles starting by the largest customer demands
    vehicle_tours = []
    for v in range(0, vehicle_count):
        vehicle_tours.append([])
        #vehicle_tours[v].append(v)
        #print(vehicle_tours)
        
    if True:
        remaining_customers = set(customers)
        remaining_customers.remove(depot)
        
        for v in range(0, vehicle_count):
            # print "Start Vehicle: ",v
            vehicle_tours.append([])
            capacity_remaining = vehicle_capacity
            #print("Vehicle %s " %v, end="")

            while sum([capacity_remaining >= customer.demand for customer in remaining_customers]) > 0:
                used = set()
                order = sorted(remaining_customers, key=lambda customer: -customer.demand)
                for customer in order:
                    if capacity_remaining >= customer.demand:
                        capacity_remaining -= customer.demand
                        vehicle_tours[v].append(customer)
                        # print '   add', ci, capacity_remaining
                        used.add(customer)
                remaining_customers -= used

    # checks that the number of customers served is correct
    assert sum([len(v) for v in vehicle_tours]) == len(customers) - 1

    # calculate the cost of the solution; for each vehicle the length of the route
    obj = 0
    for v in range(0, vehicle_count):
        vehicle_tour = vehicle_tours[v]
        #print("Vehicle %s - " %v, end="")
        #print(vehicle_tour)
        if len(vehicle_tour) > 0:
            obj += length(depot,vehicle_tour[0])
            for i in range(0, len(vehicle_tour)-1):
                obj += length(vehicle_tour[i],vehicle_tour[i+1])
            obj += length(vehicle_tour[-1],depot)

    # prepare the solution in the specified output format
    outputData = '%.2f' % obj + ' ' + str(0) + '\n'
    for v in range(0, vehicle_count):
        outputData += str(depot.index) + ' ' + ' '.join([str(customer.index) for customer in vehicle_tours[v]]) + ' ' + str(depot.index) + '\n'

    return outputData

def print_solution(manager, routing, assignment, vehicle_count, customers):
    print("print_solution")
    
    """Prints assignment on console."""
    total_distance = 0
    total_load = 0
    for vehicle_id in range(vehicle_count):
        index = routing.Start(vehicle_id)
        plan_output = 'Route for vehicle {}:\n'.format(vehicle_id)
        route_distance = 0
        route_load = 0
        while not routing.IsEnd(index):
            node_index = manager.IndexToNode(index)
            #route_load += data['demands'][node_index]
            route_load += customers[node_index].demand
            plan_output += ' {0} Load({1}) -> '.format(node_index, route_load)
            previous_index = index
            index = assignment.Value(routing.NextVar(index))
            route_distance += routing.GetArcCostForVehicle(
                previous_index, index, vehicle_id)
        plan_output += ' {0} Load({1})\n'.format(
            manager.IndexToNode(index), route_load)
        plan_output += 'Distance of the route: {}m\n'.format(route_distance)
        plan_output += 'Load of the route: {}\n'.format(route_load)
        print(plan_output)
        total_distance += route_distance
        total_load += route_load
    print('Total distance of all routes: {}m'.format(total_distance))
    print('Total load of all routes: {}'.format(total_load))


import sys

if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        file_location = sys.argv[1].strip()
        with open(file_location, 'r') as input_data_file:
            input_data = input_data_file.read()
        print(solve_it(input_data))
    else:

        print('This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/vrp_5_4_1)')

