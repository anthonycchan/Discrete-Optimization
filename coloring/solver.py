#!/usr/bin/python
# -*- coding: utf-8 -*-

from collections import Counter
from collections import namedtuple
Item = namedtuple("Item", ['nodeIndx', 'connections'])

def solve_it(input_data):
    # Modify this code to run your optimization algorithm

    # parse the input
    lines = input_data.split('\n')

    first_line = lines[0].split()
    node_count = int(first_line[0])
    edge_count = int(first_line[1])

    edges = []
    for i in range(1, edge_count + 1):
        line = lines[i]
        parts = line.split()
        edges.append((int(parts[0]), int(parts[1])))

    # build a trivial solution
    # every node has its own color
    #solution = range(0, node_count)
    color = [-1] * node_count    
    invalids = []    
    for i in range(node_count): # create a list with nested lists
        invalids.append([])

    maxColor = 0
    
    problemSize = node_count * len(edges)
    
    ##
    ## Best first algorithm
    ##
    if True:
        all_colors = node_count
        
        # Node index, # of connections to node
        node_byNumConnections = []
        # Node index, connected node indices
        node_connections = [0] * node_count
        
        for nodeIndx in range(node_count):
            connections = getConnections(nodeIndx, edges)
            node_byNumConnections.append(Item(nodeIndx, len(connections)))
            node_connections[nodeIndx] = connections
        
        # Sort nodes by number of connections
        node_byNumConnections.sort(key=lambda elem: elem[1], reverse=True)
        
        #for item in node_byNumConnections:
        #    print(item.nodeIndx, end="")
        #    print(" %s" %item.connections)
        
        for nodeItem in node_byNumConnections:
            connections = node_connections[nodeItem.nodeIndx]
            
            if problemSize > 20000:
                constrainedColors = getConstrainedColors(connections, invalids, all_colors)
                for colorIndx in constrainedColors:
                    if colorIndx not in invalids[nodeItem.nodeIndx]:
                        color[nodeItem.nodeIndx] = colorIndx
                        if colorIndx > maxColor:
                            maxColor = colorIndx
                        break
                    
            if color[nodeItem.nodeIndx] == -1:
                for colorIndx in range(all_colors):
                    if colorIndx not in invalids[nodeItem.nodeIndx]:
                        color[nodeItem.nodeIndx] = colorIndx
                        if colorIndx > maxColor:
                            maxColor = colorIndx
                        break
                        
            for connectedNode in connections:
                invalids[connectedNode].append(colorIndx)
            
        maxColor += 1
        
    ##    
    ## Greedy algorithm
    ##
    if False :
        for nodeIndx in range(node_count):
            for colorIndx in range(node_count):
                if colorIndx not in invalids[nodeIndx]:
                    color[nodeIndx] = colorIndx
                    if colorIndx > maxColor:
                        maxColor = colorIndx
                    #print(nodeIndx, end="")
                    #print(colorIndx)
                    #print("Connected nodes")
                    
                    # Mark this color as taken on the connected nodes
                    connections = getConnections(nodeIndx, edges)
                    for connectedNode in connections:
                        invalids[connectedNode].append(colorIndx)
                        #print("\tnode %s", connectedNode, end="")
                        #print(" : %s", colorIndx)
                        
                    break
                    
        maxColor += 1

    sequence = color
    

    
    # prepare the solution in the specified output format
    output_data = str(maxColor) + ' ' + str(0) + '\n'
    #output_data += ' '.join(map(str, solution))
    output_data +=' '.join(map(str, sequence))
    return output_data

    
def getConnections(nodeIndx, edges):
    connections = []
    for edge in edges:
        if nodeIndx == edge[0]:
            connections.append(edge[1])
        if nodeIndx == edge[1]:
            connections.append(edge[0])

    return connections
    
def getConstrainedColors(connections, invalids, all_colors):
    #items = [0,0,2,2,2,3,3,3,4,4,4,4,4]
    #frequency = Counter(items)    
    #for item in frequency:
    #    print ("%s: " %item, end="")
    #    print (frequency[item])
    allInvalidColors = []
    for connectionIndx in connections:
        invalidColors = invalids[connectionIndx]
        for color in invalidColors:
            allInvalidColors.append(color)
    
    frequency = Counter(allInvalidColors).most_common(all_colors)
    
    maxConstrainedColor = []
    for item in frequency:
        maxConstrainedColor.append(item[0])
        
    return maxConstrainedColor
    
    
import sys

if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        file_location = sys.argv[1].strip()
        with open(file_location, 'r') as input_data_file:
            input_data = input_data_file.read()
        print(solve_it(input_data))
    else:
        print('This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/gc_4_1)')

