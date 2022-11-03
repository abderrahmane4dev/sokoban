from collections import deque
from copy import deepcopy
import numpy as np
from math import inf
import itertools

class Node:

    wall_space_obstacle = [] # The wall_space_obstacle is a static variable of the class Node
        
    def __init__(self, sokoPuzzle, parent=None, move=""):
        self.state = sokoPuzzle
        self.parent = parent
        self.Fline_i_lock=[]
        self.Fline_j_lock=[]
        self.coin=[]
        if self.parent == None:
            self.moves = move
            # The function g represents the cost from the initial node to the current node. For the initial node, g=0
            self.g = 0             
        else :
            self.moves = self.parent.moves + move
            """ The function g represents the cost from the initial node to the current node. 
            For a node which is different from the initial node, 
            g = self.parent.g (which is the cost from the initial node to the parent node) 
                + 1 (which is the cost from the parent node to the current node = the cost of one move) """
            self.g = self.parent.g + 1         
    
    # functon generate list of coins 
    

    def dedlock(self,static_board)  :
       
        height = len(static_board)
        width = len(static_board[0])
      
        line_i_lock=[]
        line_j_lock=[]
       

        for i , j in itertools.product(range(height),range(width)) :
        # dedlock coin 
       
            lock=False
        
            if static_board[i][j]==' ':
                if (static_board[i-1][j-1]=='O') and (static_board[i-1][j]=='O') and (static_board[i][j-1]=='O'):  
                    lock=True
                   
                elif (static_board[i-1][j]=='O') and (static_board[i-1][j+1]=='O') and (static_board[i][j+1]=='O') :
                    lock = True  
                elif (static_board[i][j+1]=='O') and (static_board[i+1][j+1]=='O') and (static_board[i+1][j]=='O') :     
                    lock = True
                elif (static_board[i+1][j]=='O') and (static_board[i+1][j-1]=='O') and (static_board[i][j-1]=='O') :     
                    lock = True   
                       
            if lock : 
            
                self.coin.append((i,j)) 
        i = 0               
        while i < len(self.coin) :
            j=i+1
            coin_i,coin_j=self.coin[i]
            while j<len(self.coin):
                 coin2_i,coin2_j=self.coin[j]
                 if coin_i==coin2_i  :       
                    line_i_lock.append(coin_i)
                 if coin_j==coin2_j :
                    line_j_lock.append(coin_j) 
                 j+=1     
        #dedlock line
            i+=1
      
    
    
        for i in line_i_lock:
            murUp=True 
            murDown=True
            for j in range(width):   
                if static_board[i-1][j] != 'O' : 
                   murDown=False
                if static_board[i+1][j] != 'O' : 
                   murUp=False   
            if murDown or murUp :
               self.Fline_i_lock.append(i)

        for i in line_j_lock:
            murLeft=True
            murRight=True
            for j in range(height):
                
                if static_board[j][i+1]!='O':
                   murRight=False
                if static_board[j][i-1]!='O':
                    murLeft=False 
            if murLeft or murRight : 
                self.Fline_j_lock.append(i)           
             

         

    

    def verifie_dedlock(self):
        self.dedlock(Node.wall_space_obstacle)
        coin_lock = False
        line_i_lock = False
        line_j_lock = False
        print("besmelah")
        print(self.state.robot_block)
        S_indices_x, S_indices_y = np.where(np.array(self.state.robot_block) == 'B') 
        i=0
        j=0
        while i<len(S_indices_x) : 
              if (S_indices_x[i],S_indices_y[j]) in self.coin :
                coin_lock = True 
                print("zebbyyyyyyyyyy")
              if (S_indices_x[i]) in self.Fline_i_lock : 
                line_i_lock = True      
              if (S_indices_y[j]) in self.Fline_j_lock : 
                line_j_lock = True   
              i+=1
              j+=1  
                    
        return coin_lock or line_i_lock or line_j_lock



    













    
    # Generate the successors
    def succ(self):
        succs = deque()
       
        for m in self.state.moves:
            succState = deepcopy(self.state)
            if succState.executeMove(m, Node.wall_space_obstacle) and  self.verifie_dedlock()==False : 
                    
                print('appendit')
                print(self.verifie_dedlock())
                succs.append(Node(succState, self, m))
            else : 
                print("reni ma appenditch")    
        return succs

    # Return the search solution
    def getSolution(self):
        node = self
        solution = []
        while node:
            height = len(node.state.robot_block)
            width = len(node.state.robot_block[0])
            state = deepcopy(Node.wall_space_obstacle)
            for i, j in itertools.product(range(height), range(width)):
                if node.state.robot_block[i][j] == 'R':
                    if state[i][j] == ' ':
                        state[i][j] = 'R'
                    else:
                        state[i][j] = '.'
                elif node.state.robot_block[i][j] == 'B':
                    if state[i][j] == ' ':
                        state[i][j] = 'B'
                    else:
                        state[i][j] = '*'                
            solution.append(state)
            node = node.parent
        solution = solution[::-1]
        return solution

    # The estimation of the evaluation function f
    def F_Evaluation(self, heuristic=1):
        # The function h represents an estimation of the cost from the current node to the goal node using a heuristic.
        heuristics = {1: self.heuristic1(),
                    2: self.heuristic2(),
                    3: self.heuristic3()}        
        self.h = heuristics[heuristic]

        # The function f is the total cost, i.e., the sum of g and h. 
        self.f = self.g + self.h 
    
    """ First heuristic: Number of left storages """
    def heuristic1(self):

        # Retrieve all the storages
        wall_space_obstacle = np.array(Node.wall_space_obstacle)
        S_indices_x, S_indices_y = np.where(wall_space_obstacle == 'S')
        
        # Count the number of the left storages
        left_storage = len(S_indices_x)
        for ind_x, ind_y in zip(S_indices_x, S_indices_y):
            if self.state.robot_block[ind_x][ind_y] == 'B':
                left_storage -= 1

        return left_storage

    """ Second heuristic: 2 * Number of left storages + Min Manhattan Distance between the blocks and the storages """
    def heuristic2(self):

        # Retrieve all the storages
        wall_space_obstacle = np.array(Node.wall_space_obstacle)
        S_indices_x, S_indices_y = np.where(wall_space_obstacle == 'S')

        # Retrieve all the blocks
        robot_block = np.array(self.state.robot_block)
        B_indices_x, B_indices_y = np.where(robot_block == 'B')

        # Get the distance between each block and the nearest storage, and meanwhile, count the number of left storages
        sum_distance = 0
        storage_left = len(S_indices_x)        
        for b_ind_x, b_ind_y in zip(B_indices_x, B_indices_y):            
            min_distance = +inf
            for s_ind_x, s_ind_y in zip(S_indices_x, S_indices_y):
                distance = abs(b_ind_x-s_ind_x) +  abs(b_ind_y-s_ind_y) # Manhattan distance between a storage and a block
                # if the distance between a block and a storage is 0 => the block is in the storage => we decrease the number of left storages
                if distance == 0: storage_left -= 1
                # Check if the current storage is the nearest to the current block
                if distance < min_distance:
                    min_distance = distance
            # Get the sum of the distances between each block and the nearest storage 
            sum_distance += min_distance
        
        return sum_distance + 2*storage_left

    """ Third heuristic: 2 * Number of left storages + Min Manhattan Distance between the blocks and the storages 
                        + Min Manhattan Distance between the robot and the blocks """
    def heuristic3(self):

        # Retrieve all the storages
        wall_space_obstacle = np.array(Node.wall_space_obstacle)
        S_indices_x, S_indices_y = np.where(wall_space_obstacle == 'S')

        # Retrieve all the blocks
        robot_block = np.array(self.state.robot_block)
        B_indices_x, B_indices_y = np.where(robot_block == 'B')

        # Get the distance between each block and the nearest storage and 
        # the distance between the robot and the nearest block, and meanwhile, count the number of the left storages
        sum_distance = 0
        storage_left = len(S_indices_x)
        min_distance_br = +inf
        for b_ind_x, b_ind_y in zip(B_indices_x, B_indices_y):

            # Get the distance between the robot and the nearest block
            # Manhattan distance between the robot and a block
            distance_br = abs(b_ind_x-self.state.robot_position[0]) + abs(b_ind_y-self.state.robot_position[1]) 
            # Check if the current block is the nearest to the robot
            if distance_br < min_distance_br:
                min_distance_br = distance_br

            # Get the distance between each block and the nearest storage
            min_distance = +inf
            for s_ind_x, s_ind_y in zip(S_indices_x, S_indices_y):
                distance = abs(b_ind_x-s_ind_x) +  abs(b_ind_y-s_ind_y) # Manhattan distance between a storage and a block
                # if the distance between a block and a storage is 0 => the block is in the storage => we decrease the number of left storages
                if distance == 0: storage_left -= 1 
                # Check if the current storage is the nearest to the current block
                if distance < min_distance:
                    min_distance = distance
            # Get the sum of the distances between each block and the nearest storage 
            sum_distance += min_distance
                        
        return sum_distance + min_distance_br + 2*storage_left