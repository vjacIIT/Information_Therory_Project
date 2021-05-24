# import numpy
import numpy as np

# for map operator
from operator import add

# import only system from os
from os import system
  
# import sleep to show output for some time period
from time import sleep

# queue
from collections import deque

# for plotting purposes
import matplotlib.pyplot as plt

# some colors for printing purposes
WHITE = "\033[1;37;40m"
GREEN = "\033[1;32;40m"
RED = "\033[1;31;40m"
BLUE = "\033[1;34;40m"
BOLD = "\033[1;37:40m"
YELLOW = "\033[1;33;40m"

BG_BLACK = "\033[0;37;48m"
BG_RED = "\033[0;37;41m"
BG_GREEN = "\033[0;37;42m"
BG_YELLOW = "\033[0;37;43m"
BG_BLUE = "\033[0;37;44m"
BG_PINK = "\033[0;37;45m"

class search:
    def __init__(self, n, start, end, p):
        self.q = deque()
        self.p = p
        self.start = start
        self.end = end
        self.action= {0: [0, -1], 1: [0, 1], 2: [-1, 0], 3: [1, 0]}
        self.n = n
        self.grid = [['.' for i in range(self.n)] for j in range(self.n)]       # . for empty
        self.grid[start[0]][start[1]] = 'S'                                     # S for starting
        self.grid[end[0]][end[1]] = 'E'                                         # E for ending
        # stores the distance of each cell from the starting node
        # stores parent to go back
        self.parent = np.full(shape=(self.n, self.n, 2), fill_value=-1, dtype=np.int64)
        self.done = False                                                       # Tells whether the algorithm has ended or not
        self.nsteps = 0                                                         # stores the number of steps taken by algorithm to complete

    def initialize(self, start, end):
        self.q.clear()
        self.q = deque()
        self.grid = [['.' for i in range(self.n)] for j in range(self.n)]
        self.parent = np.full(shape=(self.n, self.n, 2), fill_value=-1, dtype=np.int64)
        self.start = start
        self.end = end
        self.grid[start[0]][start[1]] = 'S'                                     # S for starting
        self.grid[end[0]][end[1]] = 'E'                                         # E for ending
        self.done = False


    # dfs algorithm
    def dfs(self, curr_pos):
        if curr_pos==self.end or self.done:
            self.done = True
            return
        self.grid[curr_pos[0]][curr_pos[1]]='*'                         # for visited
        for cnt in range(4):
            act = self.action[cnt]
            new_pos = list( map(add, curr_pos, act) )
            if self.check_valid(new_pos):
                system('cls')
                self.printGrid()
                sleep(0.01)
                curr_pos = new_pos
                #self.grid[curr_pos[0]][curr_pos[1]]='O'
                self.dfs(curr_pos)
                if self.done:
                    return

    def printShortestPath(self, curr_pos, start_pos, to_show):
        self.grid = [['.' for i in range(self.n)] for j in range(self.n)]
        while not self.compare_pos(curr_pos, start_pos):
            #print(curr_pos)
            self.grid[curr_pos[0]][curr_pos[1]]=' '
            curr_pos = self.parent[curr_pos[0]][curr_pos[1]]
        self.grid[curr_pos[0]][curr_pos[1]]=' '
        #system('cls')
        if to_show:
            print("\n\n")
            print("Current Shortest Path to HOME")
            self.printGrid()
            #sleep(0.5)
        return

    def bfs(self, end_pos, to_show):
        #sleep(1)
        if self.done:
            return
        curr_pos = self.q.popleft()
        self.grid[curr_pos[0]][curr_pos[1]]='*'             # for visited
        if self.compare_pos(curr_pos,end_pos):
            self.printShortestPath(curr_pos, self.end, to_show)
            self.done = True
            return
        for cnt in range(4):
            act = self.action[cnt]
            new_pos = list( map(add, curr_pos, act) )
            if self.check_valid(new_pos):
                #system('cls')
                #self.printGrid()
                #sleep(0.01)
                self.q.append(new_pos)
                self.grid[new_pos[0]][new_pos[1]]='*'             # for visited
                self.parent[new_pos[0]][new_pos[1]] = curr_pos
        
        if self.done:
            return
        else:
            self.bfs(end_pos, to_show)

    def algorithm(self, to_show):
        curr_pos = self.start
        while not self.compare_pos(curr_pos, self.end):
            self.grid[curr_pos[0]][curr_pos[1]]='S'
            if to_show:
                system('cls')
                print("\n\nProbability of choosing shortest path ",self.p)
                print("\n\nCURRENT GRID")
                self.printGrid()
                #sleep(2)
            # append starting position to queue
            self.q.append(self.end)
            self.bfs(curr_pos, to_show)
            mchoice = int(np.random.choice(a=[-1,1], size=1, p=[1-self.p, self.p]))
            if mchoice==1:                                              # do bfs
                if to_show:
                    print("\n CHOOSES SHORTEST PATH")
                    sleep(0.5)
                curr_pos = self.parent[curr_pos[0]][curr_pos[1]]
            else:                                                       # choose random direction
                mchoice = int(np.random.choice(a=[0, 1, 2, 3], size=1))
                act = self.action[mchoice]
                new_pos = list( map(add, curr_pos, act) )
                while not self.check_valid(new_pos):
                    mchoice = int(np.random.choice(a=[0, 1, 2, 3], size=1))
                    act = self.action[mchoice]
                    new_pos = list( map(add, curr_pos, act) )
                if to_show:
                    print("\n CHOOSES RANDOM PATH", BLUE, self.printDirection(mchoice))
                    sleep(0.5)
                curr_pos = new_pos
            self.nsteps = self.nsteps+1
            self.initialize(curr_pos, self.end)
            #self.dfs(curr_pos)
        #print("Number of steps taken this time ", self.nsteps)
        return self.nsteps

    def check_valid(self, curr_pos):
        i = curr_pos[0]
        j = curr_pos[1]
        if (i<0 or j<0 or i>=self.n or j>=self.n):              # cell out of bounds
            return False
        elif self.grid[i][j]=='*':                              # cell already visited
            return False
        else:
            return True

    def printGrid(self):
        for i in range(self.n):
            for j in range(self.n):
                mcolor = self.find_color(i, j)
                print(mcolor, self.grid[i][j], end="")
                print(mcolor, BG_BLACK, "  ", end="")
            print("")

    def find_color(self, i, j):
        if self.grid[i][j]=='.':
            return WHITE
        elif self.grid[i][j]=='S':
            return YELLOW
        elif self.grid[i][j]=='E':
            return RED
        elif self.grid[i][j]==' ':
            return BG_BLUE
        else:
            return BLUE

    def compare_pos(self, a, b):
        for i in range(len(a)):
            if a[i]!=b[i]:
                return False
        return True
    
    def printDirection(self, mchoice):
        if mchoice==0:
            return "LEFT"
        elif mchoice==1:
            return "RIGHT"
        elif mchoice==2:
            return "UP"
        elif mchoice==3:
            return "DOWN"
        else:
            "SOMETHING IS WRONG"


# size of grid
n = 15
start = [7, 4]
end = [10, 10]

xpoints = []
ypoints = []

for i in range(2,10,2):
    # probability with which our man will choose to do bfs
    p = i/10                                            # p ranges from 0.2 to 1.0 with interval 0.2
    niterations = 1001                                  # number of times to run to get exptected value
    nsteps = 0
    for i in range(niterations):
        if i%100 ==0:
            print(i,"'th iteration")
        obj = search(n, start, end, p)
        if i==0:                                            # First time we need to show all the steps
            nsteps += obj.algorithm(True)                         
        else:                                               # No need to show, compute the exptected value
            nsteps += obj.algorithm(False)
        del obj
    expSteps = nsteps/niterations                           # expected number of steps
    print("\n\nExpected number of steps after",niterations, "steps with p", p,"is",expSteps)
    sleep(1)
    xpoints.append(p)
    ypoints.append(expSteps)

plt.plot(xpoints, ypoints)
plt.show()

print("\n",ypoints)

# Exptected number of steps with:
#       p = 0.2 -> 94.02497502497502
#       p = 0.4 -> 33.93306693306693
#       p = 0.6 -> 18.436563436563436 
#       p = 0.8 -> 12.090909090909092