import numpy as np
import itertools
""" Representations:
O => Obstacle
S => Storage
B => Block
R => Robot
* => Block on a storage
. => Robot on a storage """

class SokoPuzzle:

    def __init__(self, robot_block, robot_position):        
        
        # Initialize the SokoPuzzle Board
        self.robot_block = robot_block
        self.robot_position = robot_position 
        self.count = 0 
        self.Fline_i_lock=[]
        self.Fline_j_lock=[]
        self.coin=[]        
        # List of the robot's moves
        self.moves = ["U", "D", "L", "R"]        


    """"

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
             

    def verifie_dedlock(self,wall_space_obstacle):
        self.dedlock(wall_space_obstacle)
        coin_lock = False
        line_i_lock = False
        line_j_lock = False
       
        
        S_indices_x, S_indices_y = np.where(np.array(self.robot_block) == 'B') 
        i=0
        j=0
        while i<len(S_indices_x) : 
              if (S_indices_x[i],S_indices_y[j]) in self.coin :
                coin_lock = True 
             
              if (S_indices_x[i]) in self.Fline_i_lock : 
                line_i_lock = True      
              if (S_indices_y[j]) in self.Fline_j_lock : 
                line_j_lock = True   
              i+=1
              j+=1  
        if (coin_lock or line_i_lock or line_j_lock ) == True : 
            print('hnaya kyn dedlock lhadj')
            print(self.robot_block)     
            self.count = self.count+1    
            print(self.count)   
        return coin_lock or line_i_lock or line_j_lock



        
"""
   



    def isGoal(self, wall_space_obstacle):

        # Retrieve all the storage cells
        S_indices_x, S_indices_y = np.where(np.array(wall_space_obstacle) == 'S')
        
        # Check if the storage cells contain blocks
        for ind_x, ind_y in zip(S_indices_x, S_indices_y):
            if self.robot_block[ind_x][ind_y] != 'B':
                return False
        return True

    def executeMove(self, action, wall_space_obstacle):
        if action == "U":
            return (self.up(wall_space_obstacle))  
        if action == "D":
            return (self.down(wall_space_obstacle))
        if action == "L":
            return (self.left(wall_space_obstacle))
        if action == "R":
            return (self.right(wall_space_obstacle))

    def up(self, wall_space_obstacle):

        # Get the robot position
        robot_x, robot_y = self.robot_position

        # Move the robot up: U => [-1, 0]
        robot_x = robot_x-1
        
        # Check if the robot is moving towards a block
        if self.robot_block[robot_x][robot_y] == 'B':
            # Moving the box
            box_x, box_y = robot_x-1, robot_y
            # If the robot is not pushing another box and is moving the box towards an empty space or storage
            if self.robot_block[box_x][box_y] != 'B' and (wall_space_obstacle[box_x][box_y] == ' ' or wall_space_obstacle[box_x][box_y] == 'S'):
                self.robot_position = (robot_x, robot_y)
                self.robot_block[robot_x+1][robot_y] = ' ' 
                self.robot_block[robot_x][robot_y] = 'R'
                self.robot_block[box_x][box_y] = 'B'
                return True            

        else: # The robot is moving towards an empty space, a storage or a wall
            if wall_space_obstacle[robot_x][robot_y] == ' ' or wall_space_obstacle[robot_x][robot_y] == 'S':
                self.robot_position = (robot_x, robot_y)
                self.robot_block[robot_x+1][robot_y] = ' ' 
                self.robot_block[robot_x][robot_y] = 'R'                
                return True

        return False

    def down(self, wall_space_obstacle):

        # Get the robot position
        robot_x, robot_y = self.robot_position

        # Move the robot down: D => [1, 0]
        robot_x = robot_x+1

        # Check if the robot is moving towards a block
        if self.robot_block[robot_x][robot_y] == 'B':
            # Moving the box
            box_x, box_y = robot_x+1, robot_y
            # If the robot is not pushing another box and is moving the box towards an empty space or storage
            if self.robot_block[box_x][box_y] != 'B' and (wall_space_obstacle[box_x][box_y] == ' ' or wall_space_obstacle[box_x][box_y] == 'S'):
                self.robot_position = (robot_x, robot_y)
                self.robot_block[robot_x-1][robot_y] = ' ' 
                self.robot_block[robot_x][robot_y] = 'R'
                self.robot_block[box_x][box_y] = 'B'
                return True
            
        else: # The robot is moving towards an empty space, a storage or a wall
            if wall_space_obstacle[robot_x][robot_y] == ' ' or wall_space_obstacle[robot_x][robot_y] == 'S':
                self.robot_position = (robot_x, robot_y)
                self.robot_block[robot_x-1][robot_y] = ' '
                self.robot_block[robot_x][robot_y] = 'R'                
                return True

        return False
            
    def left(self, wall_space_obstacle):

        # Get the robot position
        robot_x, robot_y = self.robot_position

        # Move the robot left: L => [0, -1]
        robot_y = robot_y-1

        # Check if the robot is moving towards a block
        if self.robot_block[robot_x][robot_y] == 'B':
            # Moving the box
            box_x, box_y = robot_x, robot_y-1
            # If the robot is not pushing another box and is moving the box towards an empty space or storage
            if self.robot_block[box_x][box_y] != 'B' and (wall_space_obstacle[box_x][box_y] == ' ' or wall_space_obstacle[box_x][box_y] == 'S'):
                self.robot_position = (robot_x, robot_y)
                self.robot_block[robot_x][robot_y+1] = ' ' 
                self.robot_block[robot_x][robot_y] = 'R'
                self.robot_block[box_x][box_y] = 'B'
                return True
            
        else: # The robot is moving towards a space, a storage or a wall
            if wall_space_obstacle[robot_x][robot_y] == ' ' or wall_space_obstacle[robot_x][robot_y] == 'S':
                self.robot_position = (robot_x, robot_y)
                self.robot_block[robot_x][robot_y+1] = ' ' 
                self.robot_block[robot_x][robot_y] = 'R'                
                return True

        return False

    def right(self, wall_space_obstacle):

        # Get the robot position
        robot_x, robot_y = self.robot_position

        # Move the robot right: R => [0, 1]
        robot_y = robot_y+1

        # Check if the robot is moving towards a block
        if self.robot_block[robot_x][robot_y] == 'B':
            # Moving the box
            box_x, box_y = robot_x, robot_y+1
            # If the robot is not pushing another box and is moving the box towards an empty space or storage
            if self.robot_block[box_x][box_y] != 'B' and (wall_space_obstacle[box_x][box_y] == ' ' or wall_space_obstacle[box_x][box_y] == 'S'):
                self.robot_position = (robot_x, robot_y)
                self.robot_block[robot_x][robot_y-1] = ' ' 
                self.robot_block[robot_x][robot_y] = 'R'
                self.robot_block[box_x][box_y] = 'B'
                return True
        
        else: # The robot is moving towards an empty space, a storage or a wall
            if wall_space_obstacle[robot_x][robot_y] == ' ' or wall_space_obstacle[robot_x][robot_y] == 'S':
                self.robot_position = (robot_x, robot_y)
                self.robot_block[robot_x][robot_y-1] = ' ' 
                self.robot_block[robot_x][robot_y] = 'R'                
                return True

        return False 

    
