import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from pylab import *
import time
from matplotlib import animation

plt.close('all')
plt.figure(1,figsize=(20,20))

_PARAMETER_FILE = 'grid_paramfile.par';

# COLOR CODING:
# R1,R2,... = 0,1,2,... 
# WALL = -1
# GROUND = -2
# AGENT = -3

# Parse parameters from file
with open(_PARAMETER_FILE) as f:
    M, N = [int(x) for x in next(f).split()] 
    _grid_size = (M,N);
    _grid_original = np.zeros(_grid_size);

    num_place_cells = int(next(f))
    place_field_radius = int(next(f))

    _num_agents = int(next(f))
    _state = [int(x) for x in next(f).split()]

    _num_rewards = int(next(f))

    for reward_idx in range(0,_num_rewards):
        _num_pellets = int(next(f))

        for pellet_idx in range(0,_num_pellets):
            temp = [int(x) for x in next(f).split()] # get rid of temp variable
            _grid_original[temp[0],temp[1]] = 0;
            plt.text(temp[0],temp[1],reward_idx+1, va='center', ha='center',fontsize=25)

    _num_walls = int(next(f))
    for i in range(_num_walls):
        temp = [int(x) for x in next(f).split()]; # get rid of temp variable
        for j in range(temp[0],temp[2]+1):
            for k in range(temp[1],temp[3]+1):
                _grid_original[j,k] = 0

cmap = mpl.colors.ListedColormap(['black','green','brown','yellow','blue'])
bounds = [-3.5,-2.5,-1.5,-0.5,0.5,1.5]
norm = mpl.colors.BoundaryNorm(bounds, cmap.N)

grid = _grid_original

arena3d = np.zeros((M,N,20000));

with open('state_data.dat') as f:
    for state_i in f:        
        current_time,bot_x,bot_y,action,reward = [int(x) for x in state_i.split()]             

        if current_time > 100000:
            arena = np.copy(_grid_original);
            arena[bot_x,bot_y] = 100;
            arena3d[:,:,current_time-100000] = arena

arena_hm = np.average(arena3d,2)

plt.imshow(arena_hm.T,cmap='coolwarm',interpolation='none')
cb = plt.colorbar()
cb.ax.set_yticklabels(cb.ax.get_yticklabels(), fontsize=20)
plt.clim(0,2.5)
plt.axis('off')
plt.show()

savefig('exp_flexibility_hm_keramati.png', bbox_inches='tight')

