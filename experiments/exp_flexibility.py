import numpy as np
import matplotlib.pyplot as plt 
from matplotlib import gridspec

FONTSIZE = 20;

plt.close('all')

plt.figure(figsize=(24, 8))
plt.subplot(2,1,1,gridspec_kw = {'width_ratios':[3, 1]} )

execfile('exp_flexibility_hm.py')

plt.subplot(2,1,1,gridspec_kw = {'width_ratios':[3, 1]} )
execfile('exp_flexibility_perf.py')

plt.show()
