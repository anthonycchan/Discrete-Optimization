#!/usr/bin/python
# -*- coding: utf-8 -*-
import copy
from collections import namedtuple
Item = namedtuple("Item", ['index', 'value', 'weight'])

class BBMax:
    def __init__(self, size):
        self.maxValue = 0
        self.sequence = [0]*size
        self.bestSequence = [0]*size
        self.size = size
        self.returned = False
        
class Node:

    def __init__(self, value, capacity, estimate, rightEval):

        self.left = None
        self.right = None
        self.value = value
        self.capacity = capacity
        self.estimate = estimate
        self.rightEval = rightEval
        
# Insert Node
    def insert(self, value, weight):

        #Insert to the left
        if self.left is None:
            leftValue =self.value + value
            leftCapacity = self.capacity - weight
            leftEstimate = self.estimate
            if leftCapacity >= 0:
                self.left = Node(leftValue, leftCapacity, leftEstimate, self.rightEval)
        else:
            self.left.insert(value, weight)

        #Insert to the right
        if self.rightEval > 0:
            if self.right is None:
                rightValue = self.value
                rightCapacity = self.capacity
                rightEstimate = self.estimate - value
                self.rightEval -= 1
                self.right = Node(rightValue, rightCapacity, rightEstimate, self.rightEval)
            else:
                self.right.insert(value, weight)
            
# Print the Tree
    def PrintTree(self, level, MaxVal, selected):
        level += 1
        
        if selected == True:
            MaxVal.sequence[level-2] = 1
            #print (MaxVal.sequence)
           
            
        if( self.value > MaxVal.maxValue ):
            MaxVal.maxValue = self.value
            MaxVal.bestSequence = [0] * MaxVal.size
            MaxVal.bestSequence = copy.deepcopy(MaxVal.sequence)
            print("best0: %s" %MaxVal.bestSequence)
            #MaxVal.sequence = [0] * MaxVal.size
        
        if self.left:
            MaxVal = self.left.PrintTree(level, MaxVal, True)

        #print( "level: %s " %level, end = "" )
        #print( "value: %s " %self.value, end = "")
        #print( "capacity: %s " %self.capacity, end = "")
        #print( "estimate: %s " %self.estimate)

        if( self.value > MaxVal.maxValue ):
            MaxVal.maxValue = self.value
            MaxVal.bestSequence = [0] * MaxVal.size
            MaxVal.bestSequence = copy.deepcopy(MaxVal.sequence)
            #print("best1: %s" %MaxVal.bestSequence)
            #MaxVal.sequence = [0] * MaxVal.size

        if MaxVal.returned == True:
            #print ("end Level: %s" %level)
            MaxVal.sequence[level-2] = 0
            
        if self.right:
            MaxVal = self.right.PrintTree(level, MaxVal, False)
        
        MaxVal.returned = True
        #print ("Returning: %s" %MaxVal.bestSequence)
        return MaxVal

# Inorder traversal
# Left -> Root -> Right
    def inorderTraversal(self, root):
        res = []
        if root:
            res = self.inorderTraversal(root.left)
            res.append(root.value)
            res = res + self.inorderTraversal(root.right)
        return res
        
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
    
    #print ("k: %s \t" %(capacity), end="")
    #print ("j: %s" %(item_count))
    #print ("total: %s" %(capacity * item_count) )
    #print ("weight: %s" %(items[item_count-1].weight))

    
    
    #Opt_cache[capacity-4][0] = Opt(capacity-3, 0, items, Opt_cache)
    #print (Opt(capacity-3, 1, items, Opt_cache))
    #print (Opt(capacity-3, 2, items, Opt_cache))
    #print (Opt(capacity-3, 3, items, Opt_cache))
    
    #print (Opt(capacity, 0, items, Opt_cache))
    #print (Opt(capacity, 1, items, Opt_cache))
    #print (Opt(capacity, 2, items, Opt_cache))
    #print (Opt(capacity-4, 3, items, Opt_cache))
    
    #for y in range(0, h):
    #    for x in range(0, w):
    #        print("%s \t" %Opt_cache[y][x], end="")
    #    print ()
    #print()
    
    lastZeroK = 0
    lastZeroJ = 0
    
    #for y in range(0, h):
    #    for x in range(1, w+1):
    #        print("%s \t" %Opt(y+1, x-1, items, Opt_cache, lastZeroK, lastZeroJ), end="")
    #    print ()
        
    #value = Opt_cache[capacity-1][item_count-1]
    #print ("value: %s" %value)
    
    # a trivial greedy algorithm for filling the knapsack
    # it takes items in-order until the knapsack is full
    value = 0
    weight = 0
    taken = [0]*len(items)
    
    if (capacity * item_count) < 1:
        print ("DP")
        
        w, h = item_count, capacity;
        Opt_cache = [[-2 for x in range(w)] for y in range(h)]
        
        currCapacity = capacity
        for x in range(item_count-1, -1, -1):
            currentVal = Opt(currCapacity, x, items, Opt_cache, lastZeroK, lastZeroJ)
            previousVal = Opt(currCapacity, x-1, items, Opt_cache, lastZeroK, lastZeroJ)
            
            if ( x>=0 and currentVal != previousVal ) :
                taken[x] = 1
                value += items[x].value
                currCapacity = currCapacity - items[x].weight
                
        Opt_cache.clear()
    
    else:
        print ("BnB")
        
        estimate = 0
        for item in items:
            estimate += item.value
        
        value = 0
        #print ("value: %s " %value)
        #print ("capacity: %s " %capacity)
        #print ("estimate: %s " %estimate)

        root = Node(value, capacity, estimate, 3)
        for item in items:
            root.insert(item.value, item.weight)
        #root.insert(8,4)
        #root.insert(10,5)
        #root.insert(15,8)
        #root.insert(4,3)
        
        MaxVal = BBMax(item_count)
        MaxVal = root.PrintTree(0, MaxVal, False)
        
        if MaxVal.returned == True:
            #print ("end Level: %s" %level)
            MaxVal.bestSequence[0] = 0
            
        #print(root.inorderTraversal(root))
        
        value = MaxVal.maxValue
        
        taken = copy.deepcopy(MaxVal.bestSequence)
        #print(value)
        for x in range(0, item_count, 1):
            if MaxVal.bestSequence[x] == 1:
                print (x, end="")
                print ( " ", end="" )
        print()
        #Traverse the tree to 
        
        #root.insert(items[2], -1, -1)
        #for item in items:
        #    root.insert(item)
        #print(root.inorderTraversal(root))    
        
        #items_sorted = items
        #items_sorted.sort(key=lambda elem: elem[2])
        #####
        #root = Node(27)
        #root.insert(14)
        #root.insert(35)
        #root.PrintTree()
        #print(root.inorderTraversal(root))
        #####
    
        #for item in items:
        #    if weight + item.weight <= capacity:
        #        taken[item.index] = 1
        #        value += item.value
        #        weight += item.weight
    
    
    # prepare the solution in the specified output format
    output_data = str(value) + ' ' + str(0) + '\n'
    output_data += ' '.join(map(str, taken))
    return output_data
    
# Recursive Dynamic Programming
def Opt(k, j, items, Opt_cache, lastZeroK, lastZeroJ):
    	
    if k <= lastZeroK and j <= lastZeroJ:
        return 0
        
    if items[j].value == 0:
        lastZeroK = k
        lastZeroJ = j
      
    if j == -1:
        return 0
    elif k <= 0:
        return 0
    elif Opt_cache[k-1][j] != -2:
        return Opt_cache[k-1][j]
    elif items[j].weight <= k:      
        prev = Opt(k, j-1, items, Opt_cache, lastZeroK, lastZeroJ)        
        curr = items[j].value + Opt(k-items[j].weight, j-1, items, Opt_cache, lastZeroK, lastZeroJ)                  
        Opt_cache[k-1][j] = max(prev, curr)
        return Opt_cache[k-1][j]
    else:
        Opt_cache[k-1][j] = Opt(k, j-1, items, Opt_cache, lastZeroK, lastZeroJ)
        return Opt_cache[k-1][j]
        
if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        file_location = sys.argv[1].strip()
        with open(file_location, 'r') as input_data_file:
            input_data = input_data_file.read()
        print(solve_it(input_data))
    else:
        print('This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/ks_4_0)')