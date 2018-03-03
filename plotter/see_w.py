import matplotlib as mpl
import matplotlib.pyplot as plt
#from mpl_toolkits.mplot3d import Axes3D
import numpy as np

plt.close('all')
SHOW_1 = True; SHOW_2 = True;

# Internal state values
Hvector = np.fromfile("internal_state.log", np.float32)
H = Hvector.reshape(len(Hvector)/2,2)

# Motivation values
Mvector = np.fromfile("motivation.log",np.float32)
M = Mvector.reshape(len(Mvector)/2,2)

# Qmax values
Qmaxvector = np.fromfile("qmax.log",np.float32)
Qmax = Qmaxvector.reshape(len(Qmaxvector)/2,2)

t_range = range(0,H.shape[0]-1)

fig,ax = plt.subplots()

##############################
ax1 = plt.subplot(2,1,1)

plt.plot(H[:,0],'r',linewidth=0.3,alpha=0.7); 

plt.plot(H[:,1],'b',linewidth=0.3,alpha=0.7); 

H_smooth = np.convolve(H[:,0], np.ones(1000)/1000)
plt.plot(H_smooth,'r',linewidth=1.3);

H_smooth = np.convolve(H[:,1], np.ones(1000)/1000)
plt.plot(H_smooth,'b',linewidth=1.3);

plt.title('Internal state (with running average)')
plt.legend(['food','water','food(avg)','water(avg)'])
plt.grid()

###############################
plt.subplot(2,1,2,sharex = ax1)

plt.plot(M[:,0],'r'); 
plt.plot(M[:,1],'b'); 

plt.title('Motivation')
plt.legend(['food','water'])
plt.grid()

# ###############################
# plt.subplot(4,1,3,sharex = ax1)

# if SHOW_1:
#     plt.plot(Qmax[:,0],'r'); 
# if SHOW_2:
#      plt.plot(Qmax[:,1],'b'); 

# plt.title('Q_max')
# plt.legend(['food','water'])
# plt.grid()

# ###############################
# plt.subplot(4,1,4,sharex = ax1)

# if SHOW_1:
#     plt.plot(Qmax[:,0] * M[:,0],'r'); 
# if SHOW_2:
#      plt.plot(Qmax[:,1] * M[:,1],'b'); 

# plt.title('W')
# plt.legend(['food','water'])
# plt.grid()


plt.show()
