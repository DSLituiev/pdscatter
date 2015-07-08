# -*- coding: utf-8 -*-
"""
Created on Tue Jul  7 12:18:37 2015

@author: dima
"""
from .correlate_df import correlate_df
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from .rescale_marker import rescale_marker

def scatter_clr_df(df_samples, x, y, z, horizontal = 0):
    crlator = correlate_df(df_samples, x, y)
    ccf, valid = crlator(True)
    cm = plt.cm.get_cmap('RdYlBu')
           
    fig = plt.figure()
    ax = fig.add_subplot(111)
    gain = 5
    offset = 2
    df_samples.sort(z, ascending = False, inplace = True)
    sc = ax.scatter( list(df_samples[x][valid]), 
                list(df_samples[y][valid]) , 
                s = rescale_marker(df_samples[z][valid], square = True),
                c = df_samples[z][valid] ,
                vmax = df_samples[z][valid].max(), 
                vmin = df_samples[z][valid].min(), 
                edgecolors = None)
    
    sc.set_edgecolor('none')
    plt.title(crlator.__repr__().expandtabs() + '\n' + \
        'colour map: %s\n' % z, horizontalalignment = 'right')
    start, end = ax.get_ylim()
    ax.yaxis.set_ticks(np.arange(start, end, 1), minor=True)
    ax.yaxis.grid(True)
    plt.xlabel(x)
    plt.ylabel(y)
    if horizontal is not None:
        xlims = ax.get_xlim()
        ax.plot(xlims, [horizontal, horizontal], color = np.array([1,1,1])*0.3, zorder = 0 )
        ax.set_xlim(xlims)
    "colour bar"
    plt.colorbar(sc).set_label(z)
    plt.show()
    return fig, ax  

__all__ = ["scatter_clr_df"]
