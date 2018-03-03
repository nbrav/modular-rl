import matplotlib as mpl
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

plt.close('all')
#fig = plt.figure(1,figsize=(10,10))

# Motivation values
motivationvector = np.fromfile("motivation.log",np.float32)
motivation = motivationvector.reshape(len(motivationvector)/2,2)

t_range = range(0,motivation.shape[0]-1)

fig = plt.figure()
ax = fig.gca(projection='3d')

z = t_range
x = motivation[t_range,0]
y = motivation[t_range,1]

ax.plot(x, y, z, label='parametric curve')
ax.legend()

plt.show()
