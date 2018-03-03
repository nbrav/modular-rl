import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.cm as cm
#from mpl_toolkits.mplot3d import Axes3D
import numpy as np

plt.close('all')
#fig = plt.figure(1,figsize=(10,10))

# Internal state values
Hvector = np.fromfile("internal_state.log", np.float32)
H = Hvector.reshape(len(Hvector)/2, 2)

t_range = H.shape[0]-1

plt.xlim(-1,10);
plt.ylim(-1,10);
plt.grid()

animated_plot = plt.plot(H[0,0], H[0,1], 'ro')[0]
plt.plot(8,5,'*')
plt.xlabel('H1')
plt.ylabel('H2')

step = 1;
for t in range(90000,t_range/step):
    animated_plot.set_xdata(H[t*step,0])
    animated_plot.set_ydata(H[t*step,1])
    plt.title('Time:'+str(t*step))
    plt.draw()
