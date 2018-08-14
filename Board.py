from random import shuffle,randint
from copy import deepcopy


class Board:

    def __init__(self,N=8):
        #self.state = list(range(N))
        #shuffle(self.state)
        self.board_size = N
        self.max_FF = N*(N-1)/2
        self.state = [randint(0,self.board_size-1) for _ in range(self.board_size)]

    def printState(self):
        board = ''
        for i in range(self.board_size):
            blank = ['0 ']*self.board_size
            blank[self.state[i]] = '█ '
            blank = ''.join(blank)+'\n'
            board += blank

        print(board)

    def solFound(self):
        if self.fitnessFunction()==0:
            return(True)
        else:
            return(False)


    def mutate(self):
        row = randint(0,self.board_size-1)
        col = randint(0,self.board_size-1)
        self.state[row] = col

    def fitnessFunction(self):
        pairs = 0
        for i in range(self.board_size):
            for j in range(i+1,self.board_size):
                if self.state[j]==self.state[i]:
                    pairs += 1
                if abs((self.state[j]-self.state[i]))==(j-i):
                    pairs += 1

        return(pairs)




#
