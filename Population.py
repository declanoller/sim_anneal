import matplotlib.pyplot as plt
from time import sleep
from random import randint,random
from copy import deepcopy
from datetime import datetime
from math import exp,floor,ceil
from statistics import mean

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
        '''self.init_T = .015*self.state.max_FF
        self.T = self.init_T'''
        self.T_scale = .01*self.state.max_FF
        self.init_T = 1.0
        self.T = self.init_T
        self.T_decrease_rate = 0.99

        self.FF = []
        self.FF.append(self.state.fitnessFunction())
        self.mut_accepted = [1]

    def step(self):

        new_state = deepcopy(self.state)

        new_state.mutate()

        cur_FF = self.FF[-1]
        new_FF = new_state.fitnessFunction()
        next_FF = cur_FF

        accepted = 0

        if new_FF < cur_FF:
            self.state = new_state
            next_FF = new_FF
            accepted = 1
        else:
            if exp(-(new_FF - cur_FF)/(self.T*self.T_scale)) > random():
                self.state = new_state
                next_FF = new_FF
                accepted = 1

        self.mut_accepted.append(accepted)
        self.FF.append(next_FF)
        self.T = self.T_decrease_rate*self.T
        print('T = {:.3f}, FF = {:.3f}'.format(self.T,next_FF))


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


        axis_accepted = axis.twinx()
        fig.show()

        method_list = [func for func in dir(self.individ_class) if callable(getattr(self.individ_class, func))]

        found = False
        gen = []
        accepted_window = []
        Ts = []
        moving_window_percent = .10

        for i in range(generations):

            accepted_moving_window = max(1,floor(i*moving_window_percent))

            gen.append(i)
            accepted_window.append(mean(self.mut_accepted[-accepted_moving_window:]))
            Ts.append(self.T)

            axis.clear()
            axis_accepted.clear()
            axis.set_xlabel('# generations')
            axis.set_ylabel('fitness function')


            axis.plot(gen,self.FF,label='FF')

            axis_accepted.set_ylabel('% of last {:.2f} mut. accepted'.format(moving_window_percent))
            axis_accepted.plot(gen,accepted_window,label='accepted',color='darkred')
            axis_accepted.plot(gen,Ts,label='T',color='olivedrab')

            axis.set_title('T = {:.3E}, Last {} muts'.format(self.T,accepted_moving_window))
            '''axis.text(.6*i,.8*max(self.FF),'T = {}'.format(self.T))
            axis.text(.6*i,.9*max(self.FF),'Last {} muts'.format(accepted_moving_window))'''

            axis.legend()


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
