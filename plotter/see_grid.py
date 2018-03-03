import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from pylab import *
import time
#import Displ
from matplotlib import animation

#TODO: get legend
#TODO: visualize PC

plt.close('all')
plt.ion()
plt.figure(1,figsize=(10,10))
plt.show()

_PARAMETER_FILE = 'grid_paramfile.par';
_REFRESH_RATE = 0.05; #(sec)
_REPLAY_REWARD_ALONE = False

# Get Internal state values
Hvector = np.fromfile("internal_state.log", np.float32)
H = Hvector.reshape(len(Hvector)/2, 2)

# Get Motivation values
motivationvector = np.fromfile("motivation.log",np.float32)
motivation = motivationvector.reshape(len(motivationvector)/2,2)

# COLOR CODING:
# R1,R2,... = 0,1,2,... 
# WALL = -1
# GROUND = -2
# AGENT = -3

# Parse parameters from file
with open(_PARAMETER_FILE) as f:
    M, N = [int(x) for x in next(f).split()] 
    _grid_size = (M,N);
    _grid_original = np.zeros(_grid_size) - 2;

    num_place_cells = int(next(f))
    place_field_radius = int(next(f))

    _num_agents = int(next(f))
    _state = [int(x) for x in next(f).split()]

    _num_rewards = int(next(f))

    for reward_idx in range(0,_num_rewards):
        _num_pellets = int(next(f))

        for pellet_idx in range(0,_num_pellets):
            temp = [int(x) for x in next(f).split()] # get rid of temp variable
            _grid_original[temp[0],temp[1]] = reward_idx;
            plt.text(temp[0],temp[1],reward_idx+1, va='center', ha='center',fontsize=25)

    _num_walls = int(next(f))
    for i in range(_num_walls):
        temp = [int(x) for x in next(f).split()]; # get rid of temp variable
        print temp
        for j in range(temp[0],temp[2]+1):
            for k in range(temp[1],temp[3]+1):
                _grid_original[j,k] = -1

# Coloring the gridworld
cmap = mpl.colors.ListedColormap(['black', '#01A611','#723730','#EDB91FFF','#40A4DFFF','#FFA500'])
bounds = [-3.5,-2.5,-1.5,-0.5,0.5,1.5,2.5]
norm = mpl.colors.BoundaryNorm(bounds, cmap.N)
grid = _grid_original

#plt.axis('off')

# Uncomment to see grid in the gridworld!
ax = plt.gca();
ax.set_xticks(np.arange(-0.5, 10.5, 1));
ax.xaxis.set_major_formatter(plt.NullFormatter())
ax.yaxis.set_major_formatter(plt.NullFormatter())
ax.set_yticks(np.arange(-0.5, 10.5, 1));
ax.grid(which='major', color='#F2F2F2', linestyle='-', linewidth=0.5)

img = plt.imshow(grid.T, interpolation='nearest', cmap = cmap, norm=norm)

# Save grid image for report
savefig('grid.png', bbox_inches='tight')

if _REPLAY_REWARD_ALONE == False:
    with open('state_data.dat') as f:
        for state_i in f:        
            current_time,bot_x,bot_y,action,reward = [int(x) for x in state_i.split()]             
            if current_time >= 0:
                arena = np.copy(_grid_original);
                arena[bot_x,bot_y] = -3;
                
                print_screen = 'TIME: '+str(current_time)
                #print_screen = print_screen+' M1:'+str(round(motivation[current_time][0],2))+' M2:'+str(round(motivation[current_time][1],2));
                print_screen = print_screen+' H1:'+str(round(H[current_time][0],2))+' H2:'+str(round(H[current_time][1],2));

                plt.title(print_screen)
                img.set_data(arena.T)
                plt.pause(_REFRESH_RATE)
else:
    window_before_reward = 10;
    start_seeing_grid_at = [];

    with open('reward_timing_data.dat') as reward_timing_array:
        for reward_time in reward_timing_array:
            temp = max(int(reward_time)-window_before_reward,0)+1
            start_seeing_grid_at.append(temp);
            
        print "Action starts at ",start_seeing_grid_at ,".."
            
    with open('state_data.dat') as f:
        for state_i in f:        
            current_time,bot_x,bot_y,action,reward = [int(x) for x in state_i.split()] 

            if current_time in start_seeing_grid_at:
                window_active = True;
                window_counter = 0

            if window_active == True:
                window_counter = window_counter + 1;

            if window_counter > window_before_reward:
                window_active = False;
            
            if window_active == True:
                #print current_time,bot_x,bot_y,reward
                
                arena = np.copy(arena_original);
                arena[bot_y,bot_x] = 1;
                
                #print_screen = 'TIME: '+str(current_time)+' R:'+str(reward);
                #print print_screen
                
                #plt.title(print_screen)
                plt.draw()
                time.sleep(refresh_time)             

      
plt.show()
