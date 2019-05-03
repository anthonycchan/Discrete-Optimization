#!/usr/bin/python
# -*- coding: utf-8 -*-

from collections import namedtuple
Item = namedtuple("Item", ['index', 'value', 'weight'])

def solve_it(input_data):
    # Modify this code to run your optimization algorithm

    # parse the input
    lines = input_data.split('\n')

    firstLine = lines[0].split()
    item_count = int(firstLine[0])
    capacity = int(firstLine[1])

    items = []

    for i in range(1, item_count+1):
        line = lines[i]
        parts = line.split()
        items.append(Item(i-1, int(parts[0]), int(parts[1])))

    w, h = item_count, capacity;
    Opt_cache = [[-2 for x in range(w+1)] for y in range(h)]
    
    # Opt_cache[0][0] to Opt_cache[10][4]
    #for y in range(h):
    #    for x in range(w+1):
    #        print(Opt_cache[y][x], end="")
    #    print ()

    print ("k: %s \t" %(capacity), end="")
    print ("j: %s" %(item_count-1))
        
    Opt_cache[capacity-1][item_count] = Opt(capacity, item_count-1, items, Opt_cache)
    
    print (Opt(capacity-3, 0, items, Opt_cache))
    print (Opt(capacity-3, 1, items, Opt_cache))
    print (Opt(capacity-3, 2, items, Opt_cache))
    print (Opt(capacity-3, 3, items, Opt_cache))
    print (Opt(capacity, 0, items, Opt_cache))
    print (Opt(capacity, 1, items, Opt_cache))
    print (Opt(capacity, 2, items, Opt_cache))
    print (Opt(capacity, 3, items, Opt_cache))
    for y in range(h):
        for x in range(w+1):
            print("%s \t" %Opt_cache[y][x], end="")
        print ()


    value = Opt_cache[capacity-1][item_count]

    # a trivial greedy algorithm for filling the knapsack
    # it takes items in-order until the knapsack is full
    #value = 0
    weight = 0
    taken = [0]*len(items)

    for item in items:
        if weight + item.weight <= capacity:
            taken[item.index] = 1
    #        value += item.value
            weight += item.weight
    
    # prepare the solution in the specified output format
    output_data = str(value) + ' ' + str(0) + '\n'
    output_data += ' '.join(map(str, taken))
    return output_data

    
# Recursive Dynamic Programming
def Opt(k, j, items, Opt_cache):
    #print("capacity %s" %k)
    #print("item %s" %j)
    #print(items[j].value)
    #print(items[j].weight)
    
    #if Opt_cache[k-1][j+1] != -2:
    #    return Opt_cache[k-1][j+1]
    
    if j == -1:
        Opt_cache[k-1][0] = 0
        return 0
    elif items[j].weight <= k:      
        prev = Opt(k, j-1, items, Opt_cache)
        #print ("k: %s \t" %(k), end="")
        #print ("j: %s" %(j-1))
        #print ("prev %s" %prev)
        
        curr = items[j].value + Opt(k-items[j].weight, j-1, items, Opt_cache)                  
        #print ("k: %s \t" %(k-items[j].weight), end="")
        #print ("j: %s" %(j-1))
        #print ("curr %s" %curr)
        
        Opt_cache[k-1][j+1] = max(prev, curr)
        return Opt_cache[k-1][j+1]
    else:
        Opt_cache[k-1][j+1] = Opt(k, j-1, items, Opt_cache)
        return Opt_cache[k-1][j+1]
        
if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        file_location = sys.argv[1].strip()
        with open(file_location, 'r') as input_data_file:
            input_data = input_data_file.read()
        print(solve_it(input_data))
    else:
        print('This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/ks_4_0)')

