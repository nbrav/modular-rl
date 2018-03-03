import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from pylab import *
import time
from matplotlib import animation

plt.close('all')
#plt.ion()
plt.figure(1,figsize=(10,10))
#plt.axis('off')
plt.show()

Num_Resets = np.ones((9)) #[[1,],[2,],[3,],[4,],[5,],[6,],[7,]];
Sigma_R = np.ones((9,2)) #[[1,],[2,],[3,],[4,],[5,],[6,],[7,]];
flexibility = np.ones((9)) #[[1,],[2,],[3,],[4,],[5,],[6,],[7,]];

#N1
Sigma_R[1,:] =  [3, 9877]
Num_Resets[1] = 9880

#N2
Sigma_R[2,:]=[ 3, 9886]
Num_Resets[2]=9889

#N3
Sigma_R[3,:]=[ 4 ,9865]
Num_Resets[3]=9869

#N4
Sigma_R[4,:]=[ 3, 9880]
Num_Resets[4]=9883

#N5
Sigma_R[5,:]=[ 10738, 218]
Num_Resets[5]=10956

#N6
Sigma_R[6,:]=[ 12140, 169]
Num_Resets[6]=12309

#N7
Sigma_R[7:]=[ 13901, 152]
Num_Resets[7]=14053

#N8
Sigma_R[8,:]=[ 16222, 154]
Num_Resets[8]=16376

FONTSIZE=25;
#plt.semilogy()
plt.plot(range(1,9),Sigma_R[1:,0]/Num_Resets[1:],'yo-',linewidth=4.0)
plt.plot(range(1,9),Sigma_R[1:,1]/Num_Resets[1:],'bo-',linewidth=4.0)
plt.tick_params(axis='both', which='major', labelsize=15)
plt.xlabel('x (arm position)', fontsize=FONTSIZE)
plt.ylabel('Probability of turn', fontsize=FONTSIZE)
#plt.legend(['Reward 1','Reward 2'], fontsize=FONTSIZE, loc='upper right')

savefig('exp_arms.png', bbox_inches='tight')

