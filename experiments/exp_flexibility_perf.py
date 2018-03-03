import matplotlib as mpl
import matplotlib.pyplot as plt
#from mpl_toolkits.mplot3d import Axes3D
import numpy as np

plt.close('all')
SHOW_1 = True; SHOW_2 = True;

# Internal state values
Hvector = np.fromfile("internal_state.log", np.float32)
H = Hvector.reshape(len(Hvector)/2, 2)

plt.figure(1,figsize=(20,10))

#colormap = plt.cm.rainbow
colormap = ['#edb91fff','#40a4dfff','#FFA500']

##############################

H1star = np.ones(H.size) * 5
H2star = np.ones(H.size) * 5

plt.plot(H1star,'--',color=colormap[0],linewidth=2.5); 
plt.plot(H2star,'--',color=colormap[1],linewidth=2.5); 

if SHOW_1:
    plt.plot(H[:,0],color=colormap[0],linewidth=0.3,alpha=0.7); 
if SHOW_2:
    plt.plot(H[:,1],color=colormap[1],linewidth=0.3,alpha=0.7); 

if SHOW_1:
    H_smooth = np.convolve(H[:,0], np.ones(1000)/1000)
    plt.plot(H_smooth,color=colormap[0],linewidth=1.8);
if SHOW_2:
    H_smooth = np.convolve(H[:,1], np.ones(1000)/1000)
    plt.plot(H_smooth,color=colormap[1],linewidth=1.8);

FONTSIZE = 25;

#plt.title('Homeostasis', fontsize=FONTSIZE)
plt.xlim(100000,H.shape[0]-1)
plt.ylim(0,10)

plt.tick_params(axis='both', which='major', labelsize=20)
plt.ticklabel_format(style='sci', axis='x', scilimits=(0,0))
plt.tick_params(axis='both', which='minor', labelsize=20)

plt.xlabel('t (time)', fontsize=FONTSIZE)
plt.ylabel(r'$ \mathrm{H}_{i}(t) $', fontsize=FONTSIZE+5)
plt.legend([r'$ \mathrm{H}_{1}^* $',r'$ \mathrm{H}_{2}^* $',r'$ \mathrm{H}_{1} $',r'$ \mathrm{H}_{2} $',r'$ \overline{\mathrm{H}}_{1} $',r'$ \overline{\mathrm{H}}_{2} $'],fontsize=FONTSIZE,loc='upper right');
#plt.grid()
plt.show()

savefig('exp_flexibility_perf_keramati.png', bbox_inches='tight')
