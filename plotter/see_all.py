import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import time
from matplotlib import animation

PLOT_QVALUE = True;

plt.close('all')

# Qvalues
Qvector = np.fromfile("qvalue.log", np.float32)
Q = Qvector.reshape(len(Qvector)/1000,2,10,10,5)

# Internal state values
Hvector = np.fromfile("internal_state.log",np.float32)
H = Hvector.reshape(len(Hvector)/2,2)

# Motivation values
motivationvector = np.fromfile("motivation.log",np.float32)
motivation = motivationvector.reshape(len(motivationvector)/2,2)

del Qvector, Hvector, motivationvector

_PARAMETER_FILE = 'grid_paramfile.par';
_REFRESH_RATE = 0.05; #(sec)
_REPLAY_REWARD_ALONE = False

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

    _num_walls = int(next(f))
    for i in range(_num_walls):
        temp = [int(x) for x in next(f).split()]; # get rid of temp variable
        _grid_original[temp[0],temp[1]] = -1

cmap = mpl.colors.ListedColormap(['black','green','brown','yellow'])
bounds = [-3.5,-2.5,-1.5,-0.5,10.5]
norm = mpl.colors.BoundaryNorm(bounds, cmap.N)

grid = _grid_original

if PLOT_QVALUE:
    plt.figure(1, figsize=(8,12))
    print_screen = plt.suptitle('Initialising...')

    im1 = plt.subplot(3,2,1)
    im1 = plt.imshow(grid.T,interpolation='nearest',cmap = cmap,norm=norm)
    plt.xticks(())
    plt.yticks(())

    im2 = plt.subplot(3,2,2)
    im2 = plt.imshow(Q[0,0,:,:,0],interpolation="none",cmap=plt.cm.autumn)
    plt.clim(np.min(Q),np.max(Q))
    plt.xticks(())
    plt.yticks(())

    im3 = plt.subplot(3,2,3)
    im3 = plt.imshow(Q[0,0,:,:,0],interpolation="none",cmap=plt.cm.autumn)
    plt.clim(np.min(Q),np.max(Q))
    plt.xticks(())
    plt.yticks(())

    im4 = plt.subplot(3,2,4)
    im4 = plt.imshow(Q[0,1,:,:,0],interpolation="none",cmap=plt.cm.autumn)
    plt.clim(np.min(Q),np.max(Q))
    plt.xticks(())
    plt.yticks(())

    ax1 = plt.subplot(3,2,5)
    ax2 = plt.subplot(3,2,6)
    
    ax1.set_xlim(0,10); ax1.set_ylim(0,10);
    ax2.set_xlim(0,10); ax2.set_ylim(0,10);
    ax1.set_xticks(()); ax1.set_yticks(());
    ax2.set_xticks(()); ax2.set_yticks(());

    patches = create_patches(Q);        

    _updstep = 1;
    state_file = open('state_data.dat');

    for state_i in state_file:
        t,bot_x,bot_y,action,reward = [int(x) for x in state_i.split()]             
        
        if t>10000 :            
            arena = np.copy(_grid_original);
            arena[bot_x,bot_y] = -3;                           

            im1.set_data(arena.T)            
            plt.draw()

            im2.set_data(Q[t*_updstep,0,:,:,3]+motivation[t*_updstep,0]+Q[t*_updstep,1,:,:,3]+motivation[t*_updstep,1])
            plt.draw()

            im3.set_data(Q[t*_updstep,0,:,:,3]) #+motivation[t*_updstep,0])
            plt.draw()
            
            im4.set_data(Q[t*_updstep,1,:,:,3]) #+motivation[t*_updstep,1])
            plt.draw()

            Qtemp = Q[t,0,:,:,:];
            Qtemp = np.reshape(Qtemp,(500))
            colors = Qtemp 
            p = PatchCollection(patches, cmap=mpl.cm.autumn, alpha=1)
            p.set_array(np.array(colors))            
            ax1.add_collection(p)
            plt.draw()

            Qtemp = Q[t,1,:,:,:];
            Qtemp = np.reshape(Qtemp,(500))
            colors = Qtemp 
            p = PatchCollection(patches, cmap=mpl.cm.autumn, alpha=1)
            p.set_array(np.array(colors))
            ax2.add_collection(p)
            plt.draw()

            print_screen.set_text('TIME:'+str(t)+'\nM1:'+str(motivation[t][0])+' M2:'+str(motivation[t][1])+'\nH1:'+str(H[t][0])+' H2:'+str(H[t][1]))

            #time.sleep(_REFRESH_RATE)             
