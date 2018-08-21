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



        self.kwargs_str = '__'.join(['{}={}'.format(x[0],x[1]) for x in kwargs.items()])
        print(self.kwargs_str)

        self.individ_class = individ_class
        self.class_name = individ_class.__name__
        print('using',self.class_name,'class')

        self.state = self.individ_class(**kwargs)
        self.init_T = .015*self.state.max_FF
        self.T = self.init_T
        self.T_decrease_rate = 0.995

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

        new_FF = self.state.fitnessFunction()
        self.FF.append(new_FF)
        self.T = self.T_decrease_rate*self.T
        print('T = {:.3f}, FF = {:.3f}'.format(self.T,new_FF))


    def resetTemp(self):
        print('reset temp!')
        self.T = self.init_T

    def plotEvolve(self,generations = 550,state_plot_obj = None,reset_marker = 1000000):

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

        method_list = [func for func in dir(self.individ_class) if callable(getattr(self.individ_class, func))]

        for i in range(generations):

            gen.append(i)

            axis.clear()
            axis.set_xlabel('# generations')
            axis.set_ylabel('fitness function')
            axis.plot(gen,self.FF,label='FF')
            axis.legend()

            #axis.text(.6*i,.8*max(best),'best: {:.3f}\nmean: {:.3f}'.format(cur_best,cur_mean))

            if state_plot_obj is not None:
                axes[1].clear()
                state_plot_obj.copyState(self.state)
                state_plot_obj.plotState(plot_axis=axes[1])


            fig.canvas.draw()

            if 'solFound' in method_list:
                if self.state.solFound():
                    print('found solution in generation {}!\n'.format(i))
                    if 'printState' in method_list:
                        self.state.printState()
                    break


            if i%reset_marker==0:
                self.resetTemp()

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
