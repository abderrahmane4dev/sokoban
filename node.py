from collections import deque
from copy import deepcopy
import numpy as np
from math import inf
import itertools

class Node:

    wall_space_obstacle = []
    deadlock_map = []

    def __init__(self, sokoPuzzle, parent=None, move="", cost=1):
        self.state = sokoPuzzle
        self.parent = parent
        if self.parent == None:
            self.depth = 0
            self.cost = 0
            self.moves = move
        else :
            self.depth = self.parent.depth + 1
            self.cost = self.parent.cost + cost
            self.moves = self.parent.moves + move

    # Generate the successors
    def succ(self):
        succs = deque()
        for m in self.state.moves:
            succState = deepcopy(self.state)
            if succState.executeMove(m, Node.wall_space_obstacle):
                succs.append(Node(succState, self, m))
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
    
    # Choose one of the available heuristics
    def costHeur(self, heuristic=1):
        heuristics = {1: self.heuristic1(),
                    2: self.heuristic2(),
                    3: self.heuristic3()}
        self.costH = self.cost + heuristics[heuristic]
        

    """ First heuristic: Number of left storages """
    def heuristic1(self):

        # Retrieve all the storage cells
        wall_space_obstacle = np.array(Node.wall_space_obstacle)
        S_indices_x, S_indices_y = np.where(wall_space_obstacle == 'S')
        
        left_storage = len(S_indices_x)
        # Count the number of the left storages
        for ind_x, ind_y in zip(S_indices_x, S_indices_y):
            if self.state.robot_block[ind_x][ind_y] == 'B':
                left_storage -= 1

        return left_storage

    """ Second heuristic: 2*Number of left storage cells + Min Manhattan Distance between blocks and storage goals """
    def heuristic2(self):

        # Retrieve all the storage cells
        wall_space_obstacle = np.array(Node.wall_space_obstacle)
        S_indices_x, S_indices_y = np.where(wall_space_obstacle == 'S')

        # Retrieve all the blocks
        robot_block = np.array(self.state.robot_block)
        B_indices_x, B_indices_y = np.where(robot_block == 'B')

        sum_distance = 0
        storage_left = len(S_indices_x)
        for b_ind_x, b_ind_y in zip(B_indices_x, B_indices_y):

            # Get the distance between each box and the nearest storage
            min_distance = +inf
            for s_ind_x, s_ind_y in zip(S_indices_x, S_indices_y):
                distance = abs(b_ind_x-s_ind_x) +  abs(b_ind_y-s_ind_y)
                if distance == 0: storage_left -= 1
                if distance < min_distance:
                    min_distance = distance
            sum_distance += min_distance
        
        return sum_distance + 2*storage_left

    """ Third heuristic: Min Manhattan Distance between blocks and storage goals + Min Manhattan Distance between the robot and the blocks 
                        + 2 * Number of left storage cells"""
    def heuristic3(self):

        # Retrieve all the storage cells
        wall_space_obstacle = np.array(Node.wall_space_obstacle)
        S_indices_x, S_indices_y = np.where(wall_space_obstacle == 'S')

        # Retrieve all the blocks
        robot_block = np.array(self.state.robot_block)
        B_indices_x, B_indices_y = np.where(robot_block == 'B')

        sum_distance = 0
        storage_left = len(S_indices_x)
        min_distance_br = +inf
        for b_ind_x, b_ind_y in zip(B_indices_x, B_indices_y):

            # Get the distance between each box and the robot
            distance_br = abs(b_ind_x-self.state.robot_position[0]) + abs(b_ind_y-self.state.robot_position[1])
            if distance_br < min_distance_br:
                min_distance_br = distance_br

            # Get the distance between each box and the nearest storage
            min_distance = +inf
            for s_ind_x, s_ind_y in zip(S_indices_x, S_indices_y):
                distance = abs(b_ind_x-s_ind_x) +  abs(b_ind_y-s_ind_y)
                if distance == 0: storage_left -= 1
                if distance < min_distance:
                    min_distance = distance
            sum_distance += min_distance
                        
        return sum_distance + min_distance_br + 2*storage_left

"""
board = [['O', 'O', 'O', 'O', 'O', 'O', 'O'],
        ['O', ' ', ' ', 'O', 'R', ' ', 'O'],
        ['O', ' ', ' ', ' ', 'B', ' ', 'O'],
        ['O', ' ', ' ', 'O', ' ', ' ', 'O'],
        ['O', 'O', 'O', 'O', 'B', 'S', 'O'],
        ['O', ' ', ' ', 'O', ' ', 'S', 'O'],
        ['O', 'O', 'O', 'O', 'O', 'O', 'O']]

state = SokoPuzzle(board)
node = Node(state)
print (node.goalState())
for succ in node.succ():
    print (succ.state.printSokoPuzzle(board_RB=True))
    print ('\n')
"""
