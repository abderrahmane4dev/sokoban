from sokoPuzzle import SokoPuzzle
from node import Node
from collections import deque
import itertools
from copy import deepcopy
import numpy as np

class Search:

    """ Uninformed/Blind Search """
    @staticmethod
    def breadthFirst(initial_node):
        
        # Check if the start element is the goal
        if initial_node.state.isGoal(Node.wall_space_obstacle):
            return initial_node, 0

        # Create the OPEN FIFO queue and the CLOSED list
        open = deque([initial_node]) # A FIFO queue
        closed = list()
       
        step = 0
        while True:

            print (f'*** Step {step} ***')
            step +=1
            
            # Check if the OPEN queue is empty => goal not found 
            if len(open) == 0:
                return None, -1
            
            # Get the first element of the OPEN queue
            current = open.popleft()
            
            # Put the current node in the CLOSED list
            closed.append(current)

            # Generate the successors of the current node
            succ = current.succ()
            while len(succ) != 0:
                child = succ.popleft()

                # Check if the child is not in the OPEN queue and the CLOSED list
                if (child.state.robot_block not in [n.state.robot_block for n in closed] and \
                    child.state.robot_block not in [n.state.robot_block for n in open]):

                    # Put the child in the OPEN queue 
                    open.append(child)    

                    # Check if the child is the goal
                    if child.state.isGoal(Node.wall_space_obstacle):
                        print (f'*** Step {step} ***')
                        print ("Goal reached")
                        return child, step      

""" ***************************************************** Main function **************************************************** """

board1 = [['O', 'O', 'O', 'O', 'O', 'O'],
        ['O', 'S', ' ', 'B', ' ', 'O'],
        ['O', ' ', 'O', 'R', ' ', 'O'],
        ['O', ' ', ' ', ' ', ' ', 'O'],
        ['O', ' ', ' ', ' ', ' ', 'O'],
        ['O', 'O', 'O', 'O', 'O', 'O']]

board2 = [['O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O'],
        ['O', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'O'],
        ['O', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'O'],
        ['O', ' ', ' ', 'O', 'O', 'O', ' ', ' ', 'O'],
        ['O', ' ', ' ', ' ', ' ', 'O', '.', ' ', 'O'],
        ['O', ' ', ' ', ' ', ' ', ' ', 'O', ' ', 'O'],
        ['O', ' ', ' ', 'B', ' ', ' ', 'O', ' ', 'O'],
        ['O', ' ', ' ', ' ', ' ', ' ', 'O', ' ', 'O'],
        ['O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O']]

board3 = [['O', 'O', 'O', 'O', 'O', 'O', 'O', 'O'],
        ['O', ' ', ' ', ' ', 'O', ' ', ' ', 'O'],
        ['O', ' ', ' ', 'B', 'R', ' ', ' ', 'O'],
        ['O', ' ', ' ', ' ', 'O', 'B', ' ', 'O'],
        ['O', 'O', 'O', 'O', 'O', ' ', 'S', 'O'],
        ['O', 'O', 'O', 'O', 'O', ' ', 'S', 'O'],
        ['O', 'O', 'O', 'O', 'O', 'O', 'O', 'O']]

board4 = [['O', 'O', 'O', 'O', 'O', 'O', 'O'],
        ['O', 'O', ' ', ' ', 'O', 'O', 'O'],
        ['O', 'O', ' ', ' ', 'O', 'O', 'O'],
        ['O', 'O', ' ', '*', ' ', ' ', 'O'],
        ['O', 'O', 'B', 'O', 'B', ' ', 'O'],
        ['O', ' ', 'S', 'R', 'S', ' ', 'O'],
        ['O', ' ', ' ', ' ', ' ', 'O', 'O'],
        ['O', 'O', 'O', ' ', ' ', 'O', 'O'],
        ['O', 'O', 'O', 'O', 'O', 'O', 'O']]

board5 = [['O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O'],
        ['O', 'O', 'O', 'S', 'O', ' ', ' ', 'O', 'O'],
        ['O', ' ', ' ', ' ', ' ', 'B', ' ', 'O', 'O'],
        ['O', ' ', 'B', ' ', 'R', ' ', ' ', 'S', 'O'],
        ['O', 'O', 'O', ' ', 'O', ' ', 'O', 'O', 'O'],
        ['O', 'O', 'O', 'B', 'O', ' ', 'O', 'O', 'O'],
        ['O', 'O', 'O', ' ', ' ', 'S', 'O', 'O', 'O'],
        ['O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O']]

""" This function will create from a board (a level): a static board (wall_space_obstacle) and a dynamic board (robot_block) 
    The static board will be the same in the whole search process (we will use it just for comparison), 
    so it's better to declare it as a static variable in the class Node 
    This function will also create the initial node"""

def create_initial_node(board=None):        
        
        height = len(board)
        width = len(board[0])
                
        # Separate walls, spaces and obstacles board from robot and boxes board
        robot_block = [['']*width for _ in range(height)]
        wall_space_obstacle = [['']*width for _ in range(height)]
        
        for i, j in itertools.product(range(height), range(width)):
            if board[i][j] == 'R':
                robot_position = (i, j) 
                robot_block[i][j] = 'R'
                wall_space_obstacle[i][j] = ' '
            elif board[i][j] == 'B':
                robot_block[i][j] = 'B'
                wall_space_obstacle[i][j] = ' '
            elif board[i][j] == 'S' or board[i][j] == 'O' or board[i][j] == ' ':
                robot_block[i][j] = ' '   
                wall_space_obstacle[i][j] = board[i][j]         
            elif board[i][j] == '*':
                robot_block[i][j] = 'B'
                wall_space_obstacle[i][j] = 'S'
            else: # self.board[i][j] == '.'
                robot_position = (i, j) 
                robot_block[i][j] = 'R'
                wall_space_obstacle[i][j] = 'S'

        Node.wall_space_obstacle = wall_space_obstacle        
        initial_node = Node(SokoPuzzle(robot_block, robot_position))

        return initial_node

initial_node = create_initial_node(board=board3)
goalNode, num_steps = Search.breadthFirst(initial_node)
if goalNode:
    print (f"Optimal Solution found after {num_steps} steps")
    solution = goalNode.getSolution()   
       
else:
    print ("Optimal solution not found")   

