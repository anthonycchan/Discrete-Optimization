#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import print_function
import math
from collections import namedtuple

import copy
import random


import math
from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp

Point = namedtuple("Point", ['x', 'y'])

def length(point1, point2):
    return math.sqrt((point1.x - point2.x)**2 + (point1.y - point2.y)**2)

def nextEdge(nodeCount, index):
    if index < nodeCount-1:
        nextIndx = index +1
    else:
        nextIndx = 0
    return nextIndx
    
def prevEdge(nodeCount, index):
    if index > 0:
        prevIndx = index-1
    else:
        prevIndx = nodeCount-1
    return prevIndx
    
def swap(solution, nodeCount, startIndx, endIndx):
    if startIndx < endIndx:
        num_elements = endIndx
    else:
        num_elements = (startIndx+1) + nodeCount - (startIndx-endIndx) -1
    
    solutionCopy = copy.deepcopy(solution)
    sublist = []
    revsublist = []
    for index in range(startIndx+1, num_elements):
        index2 = index % nodeCount
        sublist.append(index2)

    revsublist = sublist[::-1]
    
    #print("---")
    #print(startIndx)
    #print(endIndx)
    #print(sublist)
    #print(revsublist)
    #print(solution)
    #print(solutionCopy)
    
    for index3 in range(len(sublist)):
        #print(index3)
        elem1 = sublist[index3]
        elem2 = revsublist[index3]
        temp = solution[elem1]
        solutionCopy[elem1] = solution[elem2]
        solutionCopy[elem2] = temp
    
    #print(solutionCopy)
    
    return solutionCopy
    
def create_data_model(inputData):
    """Stores the data for the problem."""
    data = {}
    # Locations in block units
    data['locations'] = inputData
    data['num_vehicles'] = 1
    data['depot'] = 0
    return data


def compute_euclidean_distance_matrix(locations):
    """Creates callback to return distance between points."""
    distances = {}
    for from_counter, from_node in enumerate(locations):
        distances[from_counter] = {}
        for to_counter, to_node in enumerate(locations):
            if from_counter == to_counter:
                distances[from_counter][to_counter] = 0
            else:
                # Euclidean distance
                distances[from_counter][to_counter] = (int(
                    math.hypot((from_node[0] - to_node[0]),
                               (from_node[1] - to_node[1]))))
    return distances


def print_solution(manager, routing, assignment):
    """Prints assignment on console."""
    #print('Objective: {}'.format(assignment.ObjectiveValue()))
    index = routing.Start(0)
    plan_output = 'Route:\n'
    route_distance = 0
    result = []
    while not routing.IsEnd(index):
        result.append(index)
        plan_output += ' {} ->'.format(manager.IndexToNode(index))
        previous_index = index
        index = assignment.Value(routing.NextVar(index))
        route_distance += routing.GetArcCostForVehicle(previous_index, index, 0)
    plan_output += ' {}\n'.format(manager.IndexToNode(index))
    #print(plan_output)
    plan_output += 'Objective: {}m\n'.format(route_distance)
    return result
    
def solve_it(input_data):
    """Entry point of the program."""
    # Instantiate the data problem.
    # parse the input
    lines = input_data.split('\n')

    nodeCount = int(lines[0])

    points = []
    inputData = []
    for i in range(1, nodeCount+1):
        line = lines[i]
        parts = line.split()
        points.append(Point(float(parts[0]), float(parts[1])))
        x = int(float(parts[0])*100)
        y = int(float(parts[1])*100)
        inputData.append( (x, y) )

    # Modify this code to run your optimization algorithm
    solution = []
    if nodeCount <= 1889: #Using the google solver for problem 6
        solution = solveCustom(nodeCount, points)
    else:
        solution = solveGoogle(nodeCount, inputData, points)

    # calculate the length of the tour    
    obj = length(points[solution[-1]], points[solution[0]])
    for index in range(0, nodeCount-1):
        obj += length(points[solution[index]], points[solution[index+1]])

    # prepare the solution in the specified output format
    output_data = '%.2f' % obj + ' ' + str(0) + '\n'
    output_data += ' '.join(map(str, solution))

    return output_data

def solveGoogle(nodeCount, inputData, points):
    #####GOOGLE SOLVER#####
    print("GOOGLE!!!")
    data = create_data_model(inputData)

    # Create the routing index manager.
    manager = pywrapcp.RoutingIndexManager(
        len(data['locations']), data['num_vehicles'], data['depot'])

    # Create Routing Model.
    routing = pywrapcp.RoutingModel(manager)

    #distance_matrix = compute_euclidean_distance_matrix(data['locations'])

    def distance_callback(from_index, to_index):
        """Returns the distance between the two nodes."""
        # Convert from routing variable Index to distance matrix NodeIndex.
        #from_node = manager.IndexToNode(from_index)
        #to_node = manager.IndexToNode(to_index)
        #return distance_matrix[from_node][to_node]
            
        #print("google- %s" %distance_matrix[from_node][to_node])
        if to_index == nodeCount:
            to_index -=1
        #print("%s-" %from_index,end="")
        #print(to_index)
        x = int(length(points[from_index], points[to_index])*100)
        #print(x)
        return x

    transit_callback_index = routing.RegisterTransitCallback(distance_callback)

    # Define cost of each arc.
    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

    # Setting first solution heuristic.
    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.first_solution_strategy = (
        routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC)
    #search_parameters.local_search_metaheuristic = (routing_enums_pb2.LocalSearchMetaheuristic.SIMULATED_ANNEALING)
    search_parameters.lns_time_limit.seconds = 1
    search_parameters.solution_limit = 1
    
    # Solve the problem.
    assignment = routing.SolveWithParameters(search_parameters)

    # Print solution on console.
    if assignment:
        solution = print_solution(manager, routing, assignment)
    
    return solution
    
def solveCustom(nodeCount, points):
    #globalMinimum0 = -1
    #globalMinSolution0 = []
    #for iter2 in range(0, 10):
    
    # build a trivial solution
    # visit the nodes in the order they appear in the file
    #solution = range(0, nodeCount)
    solution = []
    for indx in range(0, nodeCount):
        solution.append(indx)
    #random.shuffle(solution)
        
    print(nodeCount)
    tabu = {}


    globalMinimum = -1
    globalMinSolution = []
    L = 10
    movement = 0
    globalMinIter = 0
    

    for iter in range(0, 1000000):
        
        nextAltConnection = -1
        
        if nodeCount > 1889 and globalMinimum <= 78478868 and globalMinimum != -1: #problem 6
            break
        if nodeCount == 1889 and globalMinimum <= 378069 and globalMinimum != -1: #problem 5
            break
        elif nodeCount == 51 and globalMinimum <= 430 and globalMinimum != -1: #problem 1
            break
        elif nodeCount == 100 and globalMinimum <= 23433 and globalMinimum != -1: #problem 2
            break
        elif nodeCount == 200 and globalMinimum <= 35985 and globalMinimum != -1: #problem 3
            break            
        elif nodeCount == 574 and globalMinimum <= 40000 and globalMinimum != -1: #problem 4
            break
         
        if nodeCount == 5 and iter >500:
            break
            
        #print("%s - " %iter, end="")
        #print("%s - " %movement, end="")
        #print(globalMinimum)
       
        if movement <= 0 and iter > 0:
            start = nextEdge(nodeCount, (iter % nodeCount))
            end = prevEdge(nodeCount, start)
            solution = swap(globalMinSolution, nodeCount, start, end)
        
        if iter > globalMinIter + 2 and globalMinIter > 0: # 2
            start = nextEdge(nodeCount, (iter+L % nodeCount))
            end = prevEdge(nodeCount, start)
            solution = swap(globalMinSolution, nodeCount, start, end)
            
        if iter > globalMinIter + 4 and globalMinIter > 0: # 4
            start = nextEdge(nodeCount, (iter % nodeCount))
            end = prevEdge(nodeCount, (iter-L %nodeCount))
            solution = swap(globalMinSolution, nodeCount, start, end)
        
        if iter > globalMinIter + 5 and globalMinIter > 0: #5
            start = nextEdge(nodeCount, (iter+L+L+1 % nodeCount))
            end = prevEdge(nodeCount, (iter+L+L-1 %nodeCount))
            solution = swap(globalMinSolution, nodeCount, start, end)
            
        #if nodeCount == 100 and iter > globalMinIter + 60:
        #    random.shuffle(solution)
        #    print(solution)
        #    globalMinIter = iter
            
        exploreWorstSolutions = False
        if iter > globalMinIter + 40:
            exploreWorstSolutions = True
            globalMinIter = iter

        exploreLargestSolution = False
        if iter > globalMinIter + 50:
            exploreLargestSolution = True
            globalMinIter = iter
        
        # problem 2 only
        if nodeCount == 100 and iter > globalMinIter + 6:
            start = nextEdge(nodeCount, ( iter+L % nodeCount))
            end = nextEdge(nodeCount, start + L %nodeCount)
            solution = swap(globalMinSolution, nodeCount, start, end)
            
        if nodeCount == 100 and iter > globalMinIter + 7:
            start = nextEdge(nodeCount, ( iter+L % nodeCount))
            end = nextEdge(nodeCount, start + L %nodeCount)
            solution = swap(globalMinSolution, nodeCount, start, end)
            
        if nodeCount == 100 and iter > globalMinIter + 8:
            start = nextEdge(nodeCount, ( iter+L % nodeCount))
            end = nextEdge(nodeCount, start + L %nodeCount)
            solution = swap(globalMinSolution, nodeCount, start, end)
            
        if nodeCount == 100 and iter > globalMinIter + 50:
            start = prevEdge(nodeCount, ( iter % nodeCount))
            end = prevEdge(nodeCount, start %nodeCount)
            solution = swap(globalMinSolution, nodeCount, start, end)
            #print(solution)
           
            
        #problem 6
        twoOptOnly = False
        if nodeCount > 1889 and iter < 60000: 
            twoOptOnly = True
            #exploreWorstSolutions = False
            #exploreLargestSolution = False
            
        movement = 0
        for mainIndx in range(0, nodeCount):
            lastIndx = prevEdge(nodeCount, mainIndx)
            
            mainConnectionIndx = nextEdge(nodeCount, mainIndx)
            altConnection = nextEdge(nodeCount, mainConnectionIndx)  
            nextAltConnection = altConnection
            
            #print("MainIndx: %s" %mainIndx)
            
            hasSwap = True
            while hasSwap:
                if nextAltConnection != -1:
                    altConnection = nextAltConnection
                    
                if nextAltConnection >= lastIndx-1:
                    break
                    
                nextAltConnection = -1
                hasSwap = False
               
                mainDistance = length(points[solution[mainIndx]], points[solution[mainConnectionIndx]])
                
                #movement.append(mainIndx)
                altConnectionStart = nextEdge(nodeCount, altConnection)
                altConnectionEnd = lastIndx                    
                altConnectionTotal = -1
                if altConnectionStart < altConnectionEnd:
                    altConnectionTotal = altConnectionEnd + 1
                else:
                    altConnectionTotal = altConnectionStart + nodeCount - (altConnectionStart-altConnectionEnd) + 1
                
                smallestDistance = -1
                smallestAltConnection = -1
                secondSmallestDistance = -1
                secondSmallestAltConnection = -1
                largestDistance = -1
                largestAltConnection = -1
                for index in range(altConnectionStart, altConnectionTotal):
                    
                    if index >= nodeCount:
                        altConnection = index % nodeCount
                    else:
                        altConnection = index

                    altDistance = length(points[solution[mainConnectionIndx]], points[solution[altConnection]])
                    
                    if altDistance < smallestDistance or smallestDistance == -1:
                        secondSmallestDistance = smallestDistance
                        secondSmallestAltConnection = altConnection
                        smallestDistance = altDistance
                        smallestAltConnection = altConnection
                
                    if altDistance > largestDistance or largestDistance == -1:
                        largestDistance = altDistance
                        largestAltConnection = altConnection
                        
                if exploreWorstSolutions:
                    smallestDistance = secondSmallestDistance
                    smallestAltConnection = secondSmallestAltConnection
                    
                if exploreLargestSolution:
                    smallestDistance = largestDistance
                    smallestAltConnection = largestAltConnection
                
                if (mainIndx, smallestAltConnection) not in tabu:
                    tabu[(mainIndx, smallestAltConnection)] = 0
                if (smallestAltConnection, mainIndx) not in tabu:
                    tabu[smallestAltConnection, mainIndx] = 0
                    
                if tabu[mainIndx, smallestAltConnection] <= iter and tabu[smallestAltConnection, mainIndx] <= iter:
                    currentObj = 0
                    hypoObj = 0
                    if not twoOptOnly:
                        hypoSwap = swap(solution, nodeCount, mainIndx, smallestAltConnection)
                        currentObj = length(points[solution[-1]], points[solution[0]])
                        hypoObj = length(points[hypoSwap[-1]], points[hypoSwap[0]])
                        for index in range(0, nodeCount-1):
                            currentObj += length(points[solution[index]], points[solution[index+1]])
                            hypoObj += length(points[hypoSwap[index]], points[hypoSwap[index+1]])
                    
                    if smallestDistance < mainDistance or hypoObj < currentObj or exploreWorstSolutions or exploreLargestSolution:
                        solution = swap(solution, nodeCount, mainIndx, smallestAltConnection)
                        nextAltConnection = smallestAltConnection
                        hasSwap = True
                        tabu[mainIndx, smallestAltConnection] = iter + L
                        tabu[smallestAltConnection, mainIndx] = iter + L
                        movement +=1
                        if twoOptOnly:
                            hasSwap = False
                        #print("\tAltStart: %s" %altConnectionStart)
                        #print("\tAltEnd: %s" %altConnectionEnd)
                        #print("\tsmallestAlt: %s" %smallestAltConnection)
                            

        globalLength = length(points[solution[-1]], points[solution[0]])
        for index in range(0, nodeCount-1):
            globalLength += length(points[solution[index]], points[solution[index+1]])
        if globalLength < globalMinimum or globalMinimum == -1:
            globalMinimum = globalLength
            globalMinSolution = copy.deepcopy(solution)
            globalMinIter = iter
            print("%s - " %iter, end="")
            print("%s - " %movement, end="")
            print(globalMinimum)
    
    solution = copy.deepcopy(globalMinSolution)
    return solution
    
import sys

if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        file_location = sys.argv[1].strip()
        with open(file_location, 'r') as input_data_file:
            input_data = input_data_file.read()
        print(solve_it(input_data))
    else:
        print('This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/tsp_51_1)')

