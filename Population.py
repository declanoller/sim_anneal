import matplotlib.pyplot as plt
from time import sleep
from random import randint,random
from copy import deepcopy
from datetime import datetime
from math import exp

'''
The object must have the following functions or attributes:
-fitnessFunction()
-mutate()
-isSame()
-mate()
-state (maybe change to getState()?)
'''

class Population:

    def __init__(self,individ_class,**kwargs):


        self.T = 100

        self.kwargs_str = '__'.join(['{}={}'.format(x[0],x[1]) for x in kwargs.items()])
        print(self.kwargs_str)

        self.individ_class = individ_class
        self.class_name = individ_class.__name__
        print('using',self.class_name,'class')

        self.state = self.individ_class(**kwargs)

        self.FF = []
        self.FF.append(self.state.fitnessFunction())


    def step(self):

        new_state = deepcopy(self.state)

        new_state.mutate()

        cur_FF = self.state.fitnessFunction()
        new_FF = new_state.fitnessFunction()

        if new_FF < cur_FF:
            self.state = new_state
        else:
            if exp(-(new_FF - cur_FF)/self.T) > random():
                self.state = new_state

        self.FF.append(self.state.fitnessFunction())


    def plotEvolve(self,generations = 550,state_plot_obj = None):

        if state_plot_obj is None:
            fig = plt.figure()
            axis = plt.gca()
            print('no subplot')
        else:
            fig, axes = plt.subplots(2,1,figsize=(8,10))
            axis = axes[0]

        fig.show()

        found = False
        gen = []

        for i in range(generations):

            gen.append(i)

            '''if cur_best==0 and not found:
                print('found solution in generation {}!\n'.format(i))
                self.sorted_population[0][0].printState()
                found = True'''

            axis.clear()
            axis.set_xlabel('# generations')
            axis.set_ylabel('fitness function')
            axis.plot(gen,self.FF,label='FF')
            axis.legend()

            #axis.text(.6*i,.8*max(best),'best: {:.3f}\nmean: {:.3f}'.format(cur_best,cur_mean))

            if state_plot_obj is not None:
                state_plot_obj.copyState(self.sorted_population[0][0])
                state_plot_obj.plotState(plot_axis=axes[1])


            fig.canvas.draw()

            self.step()


        date_string = datetime.now().strftime("%H-%M-%S")
        plt.savefig('SA_' + self.class_name + '__gen=' + str(generations) + '__' + self.kwargs_str + '__' + date_string + '.png')

        print('\n\nending pop:\n')
        #[print(tuple[1],tuple[0].state) for tuple in self.sorted_population]

        #return(self.sorted_population[0][0])


    def evolve(self,generations = 550):



        #generations = 550

        gen = []
        best = []
        mean = []

        found = False

        cur_best,cur_mean = 0,0

        for i in range(generations):
            self.sortIndivids()
            cur_best,cur_mean = self.getBestAndMean()

            gen.append(i)
            best.append(cur_best)
            mean.append(cur_mean)

            if cur_best==0 and not found:
                print('found solution in generation {}!\n'.format(i))
                self.sorted_population[0][0].printState()
                found = True


            self.mateGrid()


        date_string = datetime.now().strftime("%H-%M-%S")

        print('\n\nending pop:\n')
        [print(tuple[1],tuple[0].state) for tuple in self.sorted_population]

        print('\nending mean:',cur_mean)
#

#scrap

'''





'''
