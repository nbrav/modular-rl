import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import time
from matplotlib import animation
from matplotlib.patches import Polygon
from matplotlib.collections import PatchCollection

PLOT_QVALUE = 0;
PLOT_QVALUE_ALL = 1;
PLOT_QUIVER = False;
PLOT_ALL_ARROWS = False;

plt.close('all')

_REWARD_SIZE = 1;

# Q values 
Qvector = np.fromfile("qvalue.log", np.float32)
Q = Qvector.reshape(len(Qvector)/10/10/5/_REWARD_SIZE,_REWARD_SIZE,10,10,5)
del Qvector

# Internal state values
Hvector = np.fromfile("internal_state.log",np.float32)
H = Hvector.reshape(len(Hvector)/2,2)

# Motivation values
motivationvector = np.fromfile("motivation.log",np.float32)
motivation = motivationvector.reshape(len(motivationvector)/2,2)

if PLOT_QVALUE:
    plt.figure(1, figsize=(15,5))

    im1 = plt.subplot(1,2,1)
    im1 = plt.imshow(Q[0,0,:,:,1],interpolation="none",cmap=plt.cm.autumn)
    #plt.clim(np.min(Q),np.max(Q))
    plt.clim(np.min(Q),np.max(Q))
    plt.colorbar()

    im2 = plt.subplot(1,2,2)
    im2 = plt.imshow(Q[0,1,:,:,1],interpolation="none",cmap=plt.cm.autumn)
    plt.clim(np.min(Q),np.max(Q))
    plt.colorbar()

    _updstep = 1000;
    for t in range(0,Q.shape[0]/_updstep):
        im1.set_data(Q[t*_updstep,0,:,:,3])
        im2.set_data(Q[t*_updstep,1,:,:,3])
        
        #plt.title('H1:'+str(H[t*_updstep,0])+' H2:'+str(H[t*_updstep,0]))
        plt.title('TIME:'+str(t*_updstep)+'/'+str(Q.shape[0]))
        plt.draw()
        
def create_patches(Q):        
    patches = [];
    for y in range(Q.shape[2]):
        for x in range(Q.shape[3]):    
            # euclidean coordinate shift
            ex = x 
            ey = 9-y 
            
            # UP POLYGON
            polygon = Polygon([[ex,ey+1],[ex+1.0/3,ey+2.0/3],[ex+2.0/3,ey+2.0/3],[ex+1,ey+1]], True) 
            patches.append(polygon)    

            # LEFT POLYGON
            polygon = Polygon([[ex,ey],[ex+1.0/3,ey+1.0/3],[ex+1.0/3,ey+2.0/3],[ex,ey+1]], True)
            patches.append(polygon)    

            # DOWN POLYGON
            polygon = Polygon([[ex,ey],[ex+1.0/3,ey+1.0/3],[ex+2.0/3,ey+1.0/3],[ex+1,ey]], True)
            patches.append(polygon)    

            # RIGHT POLYGON
            polygon = Polygon([[ex+1,ey],[ex+2.0/3,ey+1.0/3],[ex+2.0/3,ey+2.0/3],[ex+1,ey+1]], True)
            patches.append(polygon)    
            
            # STAY POLYGON
            polygon = Polygon([[ex+1.0/3,ey+1.0/3],[ex+1.0/3,ey+2.0/3],[ex+2.0/3,ey+2.0/3],[ex+2.0/3,ey+1.0/3]], True)

            patches.append(polygon)                
    return patches

if PLOT_QVALUE_ALL:
    fig = plt.figure(1,figsize=(10,10))
    print_screen = plt.suptitle('Q-values')

    ax1 = plt.subplot(1,1,1)

    _updstep = 10000;
    state_file = open('state_data.dat');
    
    ax1.set_xlim(0,10); ax1.set_ylim(0,10);
    ax1.set_xticks(()); ax1.set_yticks(());

    patches = create_patches(Q);        
    
    COLORBAR = False;
    Qmax = np.max(Q); Qmin = np.min(Q);
            
    #fig.colorbar(cmap.mpl.Blues);

    for state_i in state_file:
        t,bot_x,bot_y,action,reward = [int(x) for x in state_i.split()]             

        if t%_updstep==0:            
            Qtemp = Q[t,0,:,:,:];
            Qtemp = np.reshape(Qtemp,(500))

            colors = Qtemp
            p = PatchCollection(patches, cmap=mpl.cm.coolwarm, alpha=1)
            p.set_array(np.array(colors))
            p.set_clim(Qmin,Qmax)

            ax1.set_title('Qmax:'+str(round(np.max(Q[:,0,:,:,:]),1))+' Qmin:'+str(round(np.min(Q[:,0,:,:,:]),2)))    
            ax1.add_collection(p)
            
            plt.draw()    
        
            #time.sleep(_REFRESH_RATE)             
            
if PLOT_QUIVER:
    # TODO: try animating over learning time
    SCALE = 15;

    WIDTH = 0.010;
    WIDTH_MAX = 0.010;
    WIDTH_MIN = 0.001;
    AS_WIDTH = True;

    Q_end = Q_end[-1,:,:,:]
    Q_MAX = np.max(Q)

    plt.figure(3, figsize=(10,10))

    for t in range(1):

        for i in range(0,10):
            for j in range(0,10):
                if PLOT_ALL_ARROWS and AS_WIDTH:
                    q_norm = Q_end[i,j,:] / Q_MAX
                    plt.quiver(j, 9-i, 0, Q_MAX/30, scale=Q_MAX, width=(q_norm[0]*(WIDTH_MAX-WIDTH_MIN) + WIDTH_MIN))
                    plt.quiver(j, 9-i, -Q_MAX/30, 0, scale=Q_MAX, width=(q_norm[1]*(WIDTH_MAX-WIDTH_MIN) + WIDTH_MIN))
                    plt.quiver(j, 9-i, 0, -Q_MAX/30, scale=Q_MAX, width=(q_norm[2]*(WIDTH_MAX-WIDTH_MIN) + WIDTH_MIN))
                    plt.quiver(j, 9-i, Q_MAX/30, 0, scale=Q_MAX, width=(q_norm[3]*(WIDTH_MAX-WIDTH_MIN) + WIDTH_MIN))
                elif PLOT_ALL_ARROWS:
                    q_norm = Q_end[i,j,:] / Q_MAX
                    plt.quiver(j, 9-i, 0, 1*(q_norm[0]), scale=Q_MAX, width=WIDTH)
                    plt.quiver(j, 9-i, -1*(q_norm[1]), 0, scale=Q_MAX, width=WIDTH)
                    plt.quiver(j, 9-i, 0, -1*(q_norm[2]), scale=Q_MAX, width=WIDTH)
                    plt.quiver(j, 9-i, 1*(q_norm[3]), 0, scale=Q_MAX, width=WIDTH)           
                else:
                    policy = np.argmax(Q_end[i,j,:])
                    plt.quiver(j, 9-i, 0, 1*(policy==0), scale=SCALE)
                    plt.quiver(j, 9-i, -1*(policy==1), 0, scale=SCALE)
                    plt.quiver(j, 9-i, 0, -1*(policy==2), scale=SCALE)
                    plt.quiver(j, 9-i, 1*(policy==3), 0, scale=SCALE)

                plt.xticks(())
                plt.yticks(())
                plt.grid()
                plt.show()
                plt.axis([-1,10,-1,10])


#del Q
del Hvector, H, motivationvector, motivation
