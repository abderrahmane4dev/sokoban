from sokoPuzzle import SokoPuzzle
from node_1 import Node
from collections import deque
import itertools
from copy import deepcopy
import numpy as np
import time

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

            print (f'**** Step {step} ****')
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
            while len(succ) != 0  :
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

    """ Informed Search """                       
    """ @staticmethod
    def A(initial_node, heuristic=1):
        
        # Check if the start element is the goal
        if initial_node.state.isGoal(Node.wall_space_obstacle):
            return initial_node, 0

        # Evaluate the cost f for the initial node
        initial_node.F_Evaluation(heuristic)

        # Create the OPEN queue with the initial node as the first element
        open = deque([initial_node])

        # Create the CLOSED list
        closed = list()
        
        step = 0
        while True:

            step +=1
            print (f'*** Step {step} ***')            
            
            # Check if the OPEN queue is empty => goal not found 
            if len(open) == 0:
                return None, -1
            
            # Get the first element of the OPEN queue after sorting
            open = deque(sorted(list(open), key=lambda node: node.f))
            current = open.popleft()
            
            # Put the current node in the CLOSED list
            closed.append(current)
            
            # Check if the current state is a goal
            if current.state.isGoal(Node.wall_space_obstacle):
                print ("Goal reached") 
                return current, step 

            # Generate the successors of the current node
            succ = current.succ()
            while len(succ) != 0:
                # Pop a child node from the list of successors 
                child = succ.popleft()
                # Evaluate the cost f for this child node
                child.F_Evaluation(heuristic)
                
                # If the child is in the OPEN queue
                if child.state.robot_block in [n.state.robot_block for n in open]:
                    # Get the index of the child in the OPEN queue
                    index = [n.state.robot_block for n in open].index(child.state.robot_block)
                    # Replace the node in the OPEN queue by the new one if its cost f is less than the old one
                    if open[index].f > child.f:
                        # Remove the old node from the OPEN queue
                        open.remove(open[index])
                        # Put the new node with the minimal cost f in the OPEN queue 
                        open.append(child) 

                # If the child is not in the OPEN queue    
                else:
                    # If the child is not in the CLOSED list
                    if child.state.robot_block not in [n.state.robot_block for n in closed]:
                        # Put the child in the OPEN queue 
                        open.append(child)  

                    # If the child is in the CLOSED list
                    else:
                        # Get the index of the child in the CLOSED list
                        index = [n.state.robot_block for n in closed].index(child.state.robot_block)
                        # Remove the node from the CLOSED list and add the new one in the OPEN queue if its cost f is less than the old one
                        if closed[index].f > child.f:
                            # Remove the child from the CLOSED list
                            closed.remove(closed[index])
                            # Put the child in the OPEN queue 
                            open.append(child) """      

    @staticmethod
    def A(initial_node, heuristic=1):
        
        # Check if the initial node is the goal
        if initial_node.state.isGoal(Node.wall_space_obstacle):
            return initial_node, 0

        # Evaluate the cost f for the initial node
        initial_node.F_Evaluation(heuristic)

        # Create the OPEN list with the initial node as the first element
        open = [initial_node]

        # Create the CLOSED list
        closed = list()
        
        step = 0
        while True:

            step +=1
            print (f'*** Step {step} ***')            
            
            # Check if the OPEN list is empty => goal not found 
            if len(open) == 0:
                return None, -1
            
            # Get the index of the node with least f in the OPEN list 
            min_index, _ = min(enumerate(open), key=lambda element: element[1].f)            
            current = open[min_index]

            # Remove the current node (i.e. the node with least f) from the OPEN list
            open.remove(current)
            
            # Put the current node in the CLOSED list
            closed.append(current)
            
            # Check if the current state is a goal
            if current.state.isGoal(Node.wall_space_obstacle):
                print ("Goal reached") 
                return current, step 

            # Generate the successors of the current node
            succ = current.succ()
            while len(succ) != 0:
                # Pop a child node from the list of successors 
                child = succ.popleft()
                # Evaluate the cost f for this child node
                child.F_Evaluation(heuristic)
                
                # If the child is in the OPEN list
                if child.state.robot_block in [n.state.robot_block for n in open]:
                    # Get the index of the child in the OPEN list
                    index = [n.state.robot_block for n in open].index(child.state.robot_block)
                    # Replace the node in the OPEN list by the new one if its cost f is less than the old one
                    if open[index].f > child.f: 
                        # Remove the old node from the OPEN list
                        open.remove(open[index])
                        # Put the new node with the minimal cost f in the OPEN list 
                        open.append(child) 

                # If the child is not in the OPEN list    
                else:
                    # If the child is not in the CLOSED list
                    if child.state.robot_block not in [n.state.robot_block for n in closed]:
                        # Put the child in the OPEN list 
                        open.append(child)  

                    # If the child is in the CLOSED list
                    else:
                        # Get the index of the child in the CLOSED list
                        index = [n.state.robot_block for n in closed].index(child.state.robot_block)
                        # Remove the node from the CLOSED list and add the new one in the OPEN list if its cost f is less than the old one
                        if closed[index].f > child.f:
                            # Remove the child from the CLOSED list
                            closed.remove(closed[index])
                            # Put the child in the OPEN list 
                            open.append(child)

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
""""
# QUESTION 1 DEDLOCK
def dedlock(static_board)  :
    height = len(static_board)
    width = len(static_board[0])
    coin = []
    line_i_lock=[]
    line_j_lock=[]
    Fline_i_lock=[]
    Fline_j_lock=[]

    for i , j in itertools.product(range(height),range(width)) :
        # dedlock coin 
       
        lock=False
        
        if static_board[i][j]==' ':
           if (static_board[i-1][j-1]=='O') and (static_board[i-1][j]=='O') and (static_board[i][j-1]=='O'):  
                    lock=True
                    print("position is")
                    print(i)
           elif (static_board[i-1][j]=='O') and (static_board[i-1][j+1]=='O') and (static_board[i][j+1]=='O') :
                    lock = True  
           elif (static_board[i][j+1]=='O') and (static_board[i+1][j+1]=='O') and (static_board[i+1][j]=='O') :     
                    lock = True
           elif (static_board[i+1][j]=='O') and (static_board[i+1][j-1]=='O') and (static_board[i][j-1]=='O') :     
                    lock = True   
                       
        if lock : 
            
                coin.append((i,j)) 
    i = 0               
    while i < len(coin) :
        j=i+1
        coin_i,coin_j=coin[i]
        while j<len(coin):
              coin2_i,coin2_j=coin[j]
              if coin_i==coin2_i  :       
                 line_i_lock.append(coin_i)
              if coin_j==coin2_j :
                 line_j_lock.append(coin_j) 
              j+=1     
        #dedlock line
        i+=1
    print("test i ")
    print(line_i_lock)
    print(line_j_lock) 
    
    
    for i in line_i_lock:
        murUp=True 
        murDown=True
        for j in range(width):   
            if static_board[i-1][j] != 'O' : 
               murDown=False
            if static_board[i+1][j] != 'O' : 
               murUp=False   
        if murDown or murUp :
           Fline_i_lock.append(i)

    for i in line_j_lock:
        murLeft=True
        murRight=True
        for j in range(height):
                
            if static_board[j][i+1]!='O':
                murRight=False
            if static_board[j][i-1]!='O':
                murLeft=False 
        if murLeft or murRight : 
            Fline_j_lock.append(i)           
             

    return coin,Fline_i_lock,Fline_j_lock                        
# QUESTION 2 VERIFICATION DES DEDLOCK POUR UN ETAT ET RETOURNE DES BOOLEEN          
def verifie_dedlock(Node,coin,Fline_i_lock,Fline_j_lock):
    coin_lock = False
    line_i_lock = False
    line_j_lock = False
    S_indices_x, S_indices_y = np.where(np.array(Node.state.robot_block) == 'B') 
    i=0
    j=0
    while i<len(S_indices_x) : 
        if (S_indices_x[i],S_indices_y[j]) in coin :
            coin_lock = True 
        if (S_indices_x[i]) in Fline_i_lock : 
            line_i_lock = True      
        if (S_indices_y[j]) in Fline_j_lock : 
            line_j_lock = True   
        i+=1
        j+=1        
    return coin_lock,line_i_lock,line_j_lock
           

        
"""
level = board3
initial_node = create_initial_node(board=level)

goalNode, num_steps = Search.breadthFirst(initial_node)
if goalNode:
    print (f"Optimal Solution found after {num_steps} steps")
    solution = goalNode.getSolution()        
else:
    print("tnakeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeet")
    print ("Optimal solution not found")  

goalNode, num_steps = Search.A(initial_node, heuristic=3)
if goalNode:
    print (f"Optimal Solution found after {num_steps} steps")
    solution = goalNode.getSolution()    
      
else:
    print("nemyy")
    print ("Optimal solution not found")  
"""""
coins,Ieme,Jeme = dedlock(initial_node.wall_space_obstacle)
print(initial_node.wall_space_obstacle)
print('ikd')
print(coins)
print('linee is')
print(Ieme)
print('Collone is')
print(Jeme)

coinFinal,lineFinal,ColonneFinal =verifie_dedlock(initial_node,coins,Ieme,Jeme)
if coinFinal : 
    print("Dedlok en coin existe  ")
if lineFinal : 
    print("Dedlok line existe ")
if ColonneFinal : 
    print("Dedlok collone existe ")  
 

"""      

