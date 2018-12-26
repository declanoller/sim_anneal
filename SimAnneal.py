import matplotlib.pyplot as plt
from time import sleep
from random import randint,random
from copy import deepcopy
from datetime import datetime
from math import exp
import FileSystemTools as fst
import subprocess
import numpy as np

'''
The object must have the following functions or attributes:
-fitnessFunction()
-mutate()
-isSame()
-mate()
-state (maybe change to getState()?)
'''

class SimAnneal:

    def __init__(self, individ_class, **kwargs):



        self.kwargs_str = '__'.join(['{}={}'.format(x[0],x[1]) for x in kwargs.items()])
        print(self.kwargs_str)

        self.individ_class = individ_class
        self.class_name = individ_class.__name__
        print('using',self.class_name,'class')

        self.init_T_factor = kwargs.get('init_T_factor', 0.015)
        self.state = self.individ_class(**kwargs)
        self.init_T = .015*self.state.max_FF
        self.T = self.init_T
        self.T_decrease_rate = 0.995

        self.FF = []
        self.best_FF = []
        self.FF.append(self.state.fitnessFunction())
        self.best_FF.append(self.state.fitnessFunction())


    def step(self):

        new_state = deepcopy(self.state)

        new_state.mutate()
        #new_state.mutateSingle()

        cur_FF = self.state.fitnessFunction()
        new_FF = new_state.fitnessFunction()

        if new_FF < cur_FF:
            self.state = new_state
        else:
            if exp(-(new_FF - cur_FF)/self.T) > random():
                self.state = new_state

        new_FF = self.state.fitnessFunction()
        self.FF.append(new_FF)

        if new_FF < min(self.best_FF):
            self.best_FF.append(new_FF)
        else:
            self.best_FF.append(self.best_FF[-1])

        self.T = self.T_decrease_rate*self.T
        #print('T = {:.3f}, FF = {:.3f}'.format(self.T, new_FF))


    def resetTemp(self):
        print('reset temp!')
        self.T = self.init_T


    def plotFF(self, ax, best_FF, current_FF):

        ax.clear()
        ax.set_xlabel('# generations')
        ax.set_ylabel('fitness function')
        ax.plot(best_FF, label='best', color='dodgerblue')
        ax.plot(current_FF, label='current', color='tomato')
        ax.legend()
        ax.text(0.15*len(best_FF), min(current_FF) + 0.2*(max(current_FF) - min(current_FF)), 'best: {:.3f}\ncurrent: {:.3f}'.format(best_FF[-1], current_FF[-1]))


    def matchDecayRateToNgen(self, N_gen):
        # This makes the decay rate for T go to about 0 at the end of N_gen.
        self.T_decrease_rate = (10**-8)**(1.0/(N_gen/2.0))


    def plotEvolve(self,  **kwargs):

        N_gen = kwargs.get('N_gen', 550)
        reset_period = kwargs.get('reset_period', N_gen)
        show_plot = kwargs.get('show_plot', True)
        plot_state = kwargs.get('plot_state', True)
        make_gif = kwargs.get('make_gif', False)
        save_FF = kwargs.get('save_FF', True)
        match_decay_rate = kwargs.get('match_decay_rate', True)

        if match_decay_rate:
            self.matchDecayRateToNgen(N_gen)

        date_string = fst.getDateString()
        base_name = f'SimAnneal_{self.class_name}__gen={N_gen}__{self.kwargs_str}__{date_string}'


        if make_gif:
            N_gif_frames = 100
            gif_dir = fst.combineDirAndFile('gifs', base_name)
            print(gif_dir)
            subprocess.check_call(['mkdir', gif_dir])

        if plot_state:
            fig, axes = plt.subplots(2,1,figsize=(8,10))
            ax_FF = axes[0]
            ax_state = axes[1]
        else:
            fig, ax_FF = plt.subplots(1,1,figsize=(8,8))

        if show_plot:
            plt.show(block=False)

        sol_found = False

        method_list = [func for func in dir(self.individ_class) if callable(getattr(self.individ_class, func))]

        for i in range(N_gen):

            if i%max(1, int(N_gen/20.0))==0:
                print('Generation {}, T = {:.6f}, FF = {:.3f}'.format(i, self.T, self.best_FF[-1]))

            if 'solFound' in method_list:
                if self.state.solFound():
                    print(f'found solution in generation {i}!\n')
                    if 'printState' in method_list:
                        self.state.printState()
                    break

            # Plot the current best and mean.
            self.plotFF(ax_FF, self.best_FF, self.FF)

            # If we're plotting the state of the population, call their plotState() functions.
            # You can plot either the best member, or the whole pop.
            if plot_state:
                ax_state.clear()
                self.state.plotState(ax_state, color='black', plot_sol=True, plot_label=True)

            if show_plot:
                fig.canvas.draw()

            if make_gif:
                if i==0 or (i%max(1, int(N_gen/N_gif_frames))==0):
                    plt.savefig(f'{gif_dir}/{i+1}.png')

            if (i != 0) and (i%reset_period==0):
                self.resetTemp()

            self.step()


        # Finished


        plt.savefig(f'misc_runs/{base_name}.png')

        if save_FF:
            np.savetxt(f'misc_runs/bestFF_{base_name}.txt', self.best_FF)

        if make_gif:
            gif_name = fst.gifFromImages(gif_dir, base_name, ext='.png', delay=20)
            gif_basename = fst.fnameFromFullPath(gif_name)
            subprocess.check_call(['mv', gif_name, fst.combineDirAndFile('misc_runs', gif_basename)])
            subprocess.check_call(['rm', '-rf', gif_dir])


        return(self.state)



#scrap

'''





'''
