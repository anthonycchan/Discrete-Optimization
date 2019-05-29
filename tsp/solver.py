#!/usr/bin/python
# -*- coding: utf-8 -*-

import math
from collections import namedtuple
import copy
import random

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
    
def solve_it(input_data):
    # Modify this code to run your optimization algorithm

    # parse the input
    lines = input_data.split('\n')

    nodeCount = int(lines[0])

    points = []
    for i in range(1, nodeCount+1):
        line = lines[i]
        parts = line.split()
        points.append(Point(float(parts[0]), float(parts[1])))

    # build a trivial solution
    # visit the nodes in the order they appear in the file
    #solution = range(0, nodeCount)
    solution = []
    for indx in range(0, nodeCount):
        solution.append(indx)


    tabu = {}
    for i in range(0, nodeCount):
        for j in range(0, nodeCount):
            if i == j:
                continue
            tabu[(i,j)] = 1
            #print ("%s," %i, end="")
            #print ("%s " %j, end="")
            #print(tabu[i,j])

    ## Debug ##
    #for mainIndx in range(0, nodeCount): 
        #mainConnectionIndx = nextEdge(nodeCount, mainIndx)
        #print("%s-" %mainIndx, end="")
        #print("%s " %mainConnectionIndx, end="")
        #print(length(points[solution[mainIndx]], points[solution[mainConnectionIndx]]))
        
    #print("DEBUG END")

    globalMinimum = -1
    globalMinSolution = []
    L = 10
    for iter in range(0, 500):
        nextAltConnection = -1
        
        for mainIndx in range(0, nodeCount):
            lastIndx = prevEdge(nodeCount, mainIndx)
            
            #if nextAltConnection >= lastIndx:
            #    break
            
            mainConnectionIndx = nextEdge(nodeCount, mainIndx)
            
            #print("OuterLoop %s-" %mainIndx, end="")
            #print("%s " %mainConnectionIndx)
            
            altConnection = nextEdge(nodeCount, mainConnectionIndx)  
            nextAltConnection = altConnection
            
            hasSwap = True
            while hasSwap:
                if nextAltConnection != -1:
                    altConnection = nextAltConnection
                    
                if nextAltConnection >= lastIndx-1:
                    break
                    
                nextAltConnection = -1
                hasSwap = False
                
                #print (mainIndx, end="")
                #print ("-%s " %mainConnectionIndx, end="")

                mainDistance = length(points[solution[mainIndx]], points[solution[mainConnectionIndx]])
                #print(" mainDistance: %s" %mainDistance)
                
                altConnectionStart = nextEdge(nodeCount, altConnection)
                altConnectionEnd = lastIndx
                
                altConnectionTotal = -1
                if altConnectionStart < altConnectionEnd:
                    altConnectionTotal = altConnectionEnd + 1
                else:
                    altConnectionTotal = altConnectionStart + nodeCount - (altConnectionStart-altConnectionEnd) + 1

                #print("altConnectionStart %s" %altConnectionStart)
                #print("altConnectionEnd %s" %altConnectionEnd)
                #print("altConnectionTotal %s" %altConnectionTotal)
                
                smallestDistance = -1
                smallestAltConnection = -1
                #print("smallestDistance: %s" %smallestDistance)
                for index in range(altConnectionStart, altConnectionTotal):
                    #print(index)
                    
                    if index >= nodeCount:
                        altConnection = index % nodeCount
                    else:
                        altConnection = index

                    altDistance = length(points[solution[mainConnectionIndx]], points[solution[altConnection]])
                    
                    #print("\t%s - " %mainConnectionIndx, end="")
                    #print("%s distance: " %altConnection, end="")
                    #print(altDistance)
                        
                    if altDistance < smallestDistance or smallestDistance == -1:
                        smallestDistance = altDistance
                        smallestAltConnection = altConnection
                    
                #print("smallestAltConnection: %s" %smallestAltConnection)
                #print("smallestDistance: %s" %smallestDistance)
                #print("mainDistance: %s" %mainDistance)
                currentObj = 0
                hypoObj =0
                hypoSwap = swap(solution, nodeCount, mainIndx, smallestAltConnection)
                for index in range(0, nodeCount-1):
                    currentObj += length(points[solution[index]], points[solution[index+1]])
                    hypoObj += length(points[hypoSwap[index]], points[hypoSwap[index+1]])
                
                if tabu[mainIndx, smallestAltConnection] <= iter:
                    if smallestDistance < mainDistance or hypoObj < currentObj:
                        solution = swap(solution, nodeCount, mainIndx, smallestAltConnection)
                        nextAltConnection = smallestAltConnection
                        hasSwap = True
                        tabu[mainIndx, smallestAltConnection] = iter + L
                        tabu[smallestAltConnection, mainIndx] = iter + L
                        
        globalLength = -1
        for index in range(0, nodeCount-1):
            globalLength += length(points[solution[index]], points[solution[index+1]])
        if globalLength < globalMinimum or globalMinimum == -1:
            globalMinimum = globalLength
            globalMinSolution = copy.deepcopy(solution)
                
                #print("\n\tnewSolution: %s" %solution)    
                #print(nextAltConnection)
                #print("====================")
            #print("====================")
            #break
            

    solution = copy.deepcopy(globalMinSolution)
    # calculate the length of the tour    
    obj = length(points[solution[-1]], points[solution[0]])
    for index in range(0, nodeCount-1):
        obj += length(points[solution[index]], points[solution[index+1]])

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
        print('This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/tsp_51_1)')

