import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import os

plt.close('all')

_ITER_PER_REWARD = 1;
_num_rewards = 3;
_num_pellets = [1,10,1];

##############################

# Parse parameters from file
_PARAMETER_FILE = 'grid_paramfile.par';
#colormap = plt.cm.rainbow
colormap = ['#edb91fff','#40a4dfff','#FFA500']

plt.figure(1,figsize=(21,7))
FONTSIZE = 25;

Hiters = np.zeros((_ITER_PER_REWARD,100000,_num_rewards))
Miters = np.zeros((_ITER_PER_REWARD,100000,_num_rewards))

for _iter in range(_ITER_PER_REWARD):

    f = open(_PARAMETER_FILE,'r+')
    
    M, N = [int(x) for x in f.readline().split()] 
    _grid_size = (M,N);
    _grid_original = np.zeros(_grid_size) - 2;

    num_place_cells = int(f.readline())
    place_field_radius = int(f.readline())

    _num_agents = int(f.readline())
    _state = [int(x) for x in f.readline().split()]

    f.write(str(_num_rewards)+'\n')

    for reward_idx in range(0,_num_rewards):
        f.write(str(_num_pellets[reward_idx])+'\n')
        
        print "\nO",reward_idx,
        for pellet_idx in range(0,_num_pellets[reward_idx]):

            if reward_idx == 0:
                temp = [1,8];
            if reward_idx == 2:
                temp = [6,2];
            if reward_idx == 1:
                temp = [np.random.randint(M), np.random.randint(N)] # or the other way?
            print temp,
            _grid_original[temp[0],temp[1]] = reward_idx;
            f.write(' '.join(str(x) for x in temp))
            f.write('\n')

    _num_walls = 0
    f.write(str(_num_walls)+'\n')
    for i in range(_num_walls):
        temp = [int(x) for x in f.readline().split()]; # get rid of temp variable
        print temp
        for j in range(temp[0],temp[2]+1):
            for k in range(temp[1],temp[3]+1):
                _grid_original[j,k] = -1

    f.close()

    ##############################
    
    #os.system('./main.o')

    print 'n=', _num_rewards, 'iter=', _iter

    Hvector = np.fromfile("internal_state.log", np.float32)
    H = Hvector.reshape(len(Hvector)/_num_rewards, _num_rewards)
    del Hvector

    Mvector = np.fromfile("motivation.log",np.float32)
    M = Mvector.reshape(len(Mvector)/2,2)
    del Mvector

    for _reward_idx in range(_num_rewards):            
        # H(t)
        #plt.plot(H[:,_reward_idx],colormap[_reward_idx],linewidth=0.3,alpha=0.7); 
            
        # <H(t)>
        H_smooth = np.convolve(H[:,_reward_idx], np.ones(1000)/1000)
        Hiters[_iter,:,_reward_idx] = H_smooth[:H.shape[0]]
        
        #M_smooth = np.convolve(M[:,_reward_idx], np.ones(1000)/1000)
        #Miters[_iter,:,_reward_idx] = M_smooth[:M.shape[0]]
        

##############################

norm=mpl.colors.Normalize(vmin=0,vmax=_num_rewards-1)

for _reward_idx in range(_num_rewards):
    # H*
    Hstar = np.ones(H.size) * 5
    #if _reward_idx + 1 is _num_rewards:
    #    Hstar = np.ones(H.size) * 10        
    plt.plot(Hstar,'--',color=colormap[_reward_idx],linewidth=2.5); 

#plt.plot(Hstar,colormap[_reward_idx],linewidth=2.5);

Hiters_mean = np.mean(Hiters,axis=0)
Hiters_std = np.std(Hiters,axis=0)

#Miters_mean = np.mean(Miters,axis=0)
#Miters_std = np.std(Miters,axis=0)

iters_mean = Hiters_mean
iters_std = Hiters_std

plot_lines = [];

for _reward_idx in range(_num_rewards):
    linemean, = plt.plot(range(iters_mean.shape[0]), iters_mean[:,_reward_idx], color=colormap[_reward_idx], linewidth=1.8, label='lmean');
    fillstd = plt.fill_between( range(iters_mean.shape[0]), iters_mean[:,_reward_idx]-iters_std[:,_reward_idx], iters_mean[:,_reward_idx]+iters_std[:,_reward_idx], facecolor=colormap[_reward_idx], alpha=0.3);
    
    plot_lines.append([linemean,fillstd])

plt.xlim(0,H.shape[0]-1)
plt.ylim(0,15)

plt.tick_params(axis='both', which='major', labelsize=20)
plt.ticklabel_format(style='sci', axis='x', scilimits=(0,0))
plt.tick_params(axis='both', which='minor', labelsize=20)

plt.xlabel('t (time)', fontsize=FONTSIZE)
plt.ylabel(r'$ \mathrm{H}_{i}(t) $', fontsize=FONTSIZE+5)

legend1 = plt.legend(plot_lines[0],[r'$\mu$',r'$\mu \pm \sigma$'], loc=1,fontsize=FONTSIZE)
ax = plt.gca().add_artist(legend1)

#legend2 = plt.legend([l[0] for l in plot_lines],[str(x) for x in range(_num_rewards)], loc='upper left',fontsize=FONTSIZE)
#legend2.set_title('Objective $i$',prop={'size':FONTSIZE})
#norm = mpl.colors.BoundaryNorm(np.arange(0,_num_rewards,1), colormap)
#plt.colorbar(ticks=np.linspace(0,_num_rewards,1))

plt.show()

file_name = 'exp63_obj_conc' + str(_num_rewards) + '.png'
#plt.savefig(file_name, bbox_inches='tight')
