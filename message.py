board=[['0','0','0','0','0','0','0','0'],
       ['0','0','0',' ',' ',' ','0','0'],
       ['0','.',' ','B',' ',' ','0','0'],
       ['0','0','0',' ','B','S','0','0'],
       ['0','S','0','0','B',' ','0','0'],
       ['0',' ','0',' ','S',' ','0','0'],
       ['0','B',' ','*','B','B','S','0'],
       ['0',' ',' ',' ','S',' ',' ','0'],
       ['0','0','0','0','0','0','0','0']]

#SokoPuzzle
#itertools -> python library to do the mult of two matrixes and so on .... 
class sokoban:
    def __init__(self, board): 
        self.height = len(board)
        self.width = len(board[0])
        self.board_stat = []
        self.board_dyn = []

        for i in range(self.height):
            line=[]
            for j in range(self.width):
                line.append(' ')

            self.board_stat.append(line)       
            self.board_dyn.append(line)  

#for i,j in itertools.product(range(height), range(width))

        for i in range(self.height):
            for j in range(self.width):
                if board[i][j] == 'R':
                    self.robot_pos=(i,j)
                    self.board_dyn[i][j]='R'
                elif board[i][j] == 'B':
                    self.board_dyn[i][j]= 'B'    
                elif board[i][j] == 'S':
                    self.board_stat[i][j]= 'S' 
                elif board[i][j] == 'O':
                    self.board_stat[i][j]= 'O' 
                elif board[i][j] == '.':
                    self.board_stat[i][j]= 'S' 
                    self.board_dyn[i][j]= 'R'
                    self.robot_pos=(i,j) 
                elif board[i][j] == '*':
                    self.board_stat[i][j]= 'S'    
                    self.board_dyn[i][j]= 'B'
        self.moves=['U','D','L','R']      

    def isGoal(self):
        for i in range(self.height):
            for j in range(self.width):
                if self.board_stat[i][j]=='S':
                    if self.board_dyn[i][j]!='B':
                        return False
        return True

    def do_Move(self,m):
        if m=='U':
            return (self.up()) #return true or false
        elif m=='D':
            return (self.down())
        elif m=='L':
            return (self.left())
        else:
            return (self.right())

    def up(self):
        r_x,r_y=self.robot_pos
        r_x -=1
        # its a robot
        if self.board_dyn[r_x][r_y] !='B':
            if self.board_stat[r_x][r_y]!='0':
                self.robot_pos=(r_x,r_y)
                self.board_dyn[r_x+1] [r_y]=' '
                self.board_dyn[r_x][r_y]='R'
                return True
        # its a block        
        elif self.board_dyn[r_x][r_y]=='B' & self.board_dyn[r_x-1][r_y]!='B' & self.board_stat[r_x-1][r_y]!= '0':
            self.robot_pos=(r_x,r_y)
            self.board_dyn[r_x][r_y]='R'
            self.board_dyn[r_x+1][r_y]=' '
            self.board_dyn[r_x-1][r_y]='B'
            return True

        return False 
    
    
    def down(self):
        r_x,r_y=self.robot_pos
        r_x +=1
        # its a robot
        if self.board_dyn[r_x][r_y] !='B':
            if self.board_stat[r_x][r_y]!='0':
                self.robot_pos=(r_x,r_y)
                self.board_dyn[r_x-1] [r_y]=' '
                self.board_dyn[r_x][r_y]='R'
                return True
        # its a block        
        elif self.board_dyn[r_x][r_y]=='B' & self.board_dyn[r_x+1][r_y]!='B' & self.board_stat[r_x+1][r_y]!= '0':
            self.robot_pos=(r_x,r_y)
            self.board_dyn[r_x][r_y]='R'
            self.board_dyn[r_x-1][r_y]=' '
            self.board_dyn[r_x+1][r_y]='B'
            return True

        return False 
    
    
    def right(self):
        r_x,r_y=self.robot_pos
        r_y +=1
        # its a robot
        if self.board_dyn[r_x][r_y] !='B':
            if self.board_stat[r_x][r_y]!='0':
                self.robot_pos=(r_x,r_y)
                self.board_dyn[r_x] [r_y-1]=' '
                self.board_dyn[r_x][r_y]='R'
                return True
        # its a block        
        elif self.board_dyn[r_x][r_y]=='B' & self.board_dyn[r_x][r_y+1]!='B' & self.board_stat[r_x][r_y+1]!= '0':
            self.robot_pos=(r_x,r_y)
            self.board_dyn[r_x][r_y]='R'
            self.board_dyn[r_x][r_y-1]=' '
            self.board_dyn[r_x][r_y+1]='B'
            return True

        return False 
    
    
    def left(self):
        r_x,r_y=self.robot_pos
        r_y -=1
        # its a robot
        if self.board_dyn[r_x][r_y] !='B':
            if self.board_stat[r_x][r_y]!='0':
                self.robot_pos=(r_x,r_y)
                self.board_dyn[r_x] [r_y+1]=' '
                self.board_dyn[r_x][r_y]='R'
                return True
        # its a block        
        elif self.board_dyn[r_x][r_y]=='B' & self.board_dyn[r_x][r_y+1]!='B' & self.board_stat[r_x][r_y+1]!= '0':
            self.robot_pos=(r_x,r_y)
            self.board_dyn[r_x][r_y]='R'
            self.board_dyn[r_x][r_y+1]=' '
            self.board_dyn[r_x][r_y-1]='B'
            return True

        return False 

    def printdyn(self):
        print("----------the dynamique board-------------")
        print('\n')
        for row in self.board_dyn:
            print(row)
        print('\n')
        print("------------------------------")
    
    def printstat(self):
        print("----------the static board-------------")
        print('\n')
        for row in self.board_stat:
            print(row)
        print('\n')
        print("------------------------------")

sokoban_board = sokoban(board) 
sokoban_board.printdyn()
sokoban_board.printstat() 
from collections import deque 
from copy import deepcopy
from sys import setprofile
#function deepcopy permet de faire une copy du pere
#using pygame
class node:
    #m-> c le mouvement courant
    def __init__(self,sokoPuzzle, parent=None, m=""):
        self.state=sokoPuzzle
        self.parent=parent
        if self.parent!=None:
            self.moves=self.parent.moves+m
        else:
            self.moves=m

            
    #idkkkkkkkkkkkkkkkkkkkk


    def succ(self):
        succ=deque()
        for m in self.state.moves:
            child=deepcopy(self.state)
            if child.do_Move(m):
                succ.append(node(child,self,m))
                #m dans le jeu on va pas l'utiliser c just epour l'affichage
        return succ

class search:
    @staticmethod
#Creer un noeud initial
# init_node=node(sokoban(board),m)
    def largeur_dabord(init_node):
        if init_node.state.isGoal():
            return init_node,0
        
        OPEN=deque([init_node])
        CLOSED=list()
        #OPEN.append(init_node)
        while True:
            if len(OPEN)==0:
                return None,-1
            current=OPEN.popleft()
            CLOSED.append(current)
            succs=current.succ()
            while len(succs)!=0:
                child=succs.popleft()
 #list_comprehension 
 #list=[float(e)  for e in l1] 
                if child.state.board_dyn not in [ n.state.board_dyn for n in OPEN ] & child.state.board_dyn  not in [n.state.board_dyn for n in CLOSED] :
                    OPEN.append(child)
                    if child.state.isGoal():
                        return child,step


    def Get_solution(self):
        n=self
        solution=[]
        while n:
            solution.append(n)
            n=n.parent

        solution=reversed(solution)
        #Solution[::-1]
        return solution