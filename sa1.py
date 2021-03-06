import sys
sys.path.append('../IndividualClasses')

from SimAnneal import SimAnneal
from Board import Board
from Brachistochrone import Brachistochrone
from Skyscraper import Skyscraper





easy_SS = [[2,1,3,2],[2,2,1,3],[2,3,1,3],[3,1,2,2]]

pop1 = Population(Skyscraper,N=4,see_list=easy_SS)
ending_state = pop1.plotEvolve(generations = 10000,reset_marker = 2000)



exit(0)

Npts = 25
height = 1.3

sa1 = SimAnneal(Brachistochrone, N=Npts, height=height, init_T_factor=0.00001, mutate_strength_height_frac=0.015)
ending_state = sa1.plotEvolve(N_gen = 6000, make_gif=True)

#,reset_marker = 2000



'''s = Skyscraper(4,see_list=[[2,1,3,4],[2,1,3,4],[2,1,3,4],[2,1,3,4]])
#s = Skyscraper(4,see_list=[[2,1,3,4],[2,9,7,4],[8,99,3,4],[897,678,55,4]])
s.printState()'''

#print(s.fitnessFunction())

easy_SS = [[2,1,3,2],[2,2,1,3],[2,3,1,3],[3,1,2,2]]

#pop1 = Population(Skyscraper,N=4,see_list=easy_SS)

med_88_SS = [[2,3,2,4,4,2,3,1],[1,3,5,3,2,3,2,4],[2,3,2,2,4,6,3,1],[1,2,3,4,3,2,2,4]]

med_88_constlist = [([0,1],1),([1,3],1),([2,1],3),([3,2],3),([4,2],6),([4,3],3),([4,5],5),([5,0],4),([5,4],6),([6,1],2),([6,4],1),([7,4],5)]

pop1 = Population(Skyscraper,N=8,see_list=med_88_SS,const_list=med_88_constlist)
ending_state = pop1.plotEvolve(generations = 10000,reset_marker = 2000)
#s.countOccurrences()



pop = Population(Board,N=30)


pop.plotEvolve(generations=20000,reset_marker=1000)
