# -*- coding: utf-8 -*-
"""
Created on Tue Jul  7 12:18:37 2015

@author: dima
"""
from .correlate_df import correlate_df, valid_indices
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from .rescale_marker import rescale_marker

def scatter_df(df_samples, x, y, z, horizontal = 0, clim = (None, None), fig = None, ax = None, correlate = True):
    if correlate:
        crlator = correlate_df(df_samples, x, y)
    # _, valid = crlator(True)
    valid = valid_indices(df_samples, x, y, z)
    # cm = plt.cm.get_cmap('RdYlBu')

    if fig is None:
        fig = plt.figure()
    if ax is None:
        ax = fig.add_subplot(111)
    gain = 5
    offset = 2
    df_samples.sort(z, ascending = False, inplace = True)
    
    vmin = df_samples[z][valid].min() if clim[0] is None else clim[0]
    vmax = df_samples[z][valid].max() if clim[1] is None else clim[1]

    sc = ax.scatter( list(df_samples[x][valid]), 
                list(df_samples[y][valid]) , 
                s = rescale_marker(df_samples[z][valid], square = True),
                c = df_samples[z][valid] ,
                vmax = vmax,
                vmin = vmin, 
                edgecolors = None)
    
    sc.set_edgecolor('none')
    
    fmt = lambda z : z if type(z) is str else  ', '.join(z)
    z_str = fmt(z)
    y_str = fmt(y)
    x_str = fmt(x)

    if correlate:
        plt.title(crlator.__repr__().expandtabs() + '\n' + \
            'colour map: %s\n' % z_str, horizontalalignment = 'right')
    else:
        plt.title('colour map: %s\n' % z_str)
 
    start, end = ax.get_ylim()
    ax.yaxis.set_ticks(np.arange(start, end, 1), minor=True)
    ax.yaxis.grid(True)
    plt.xlabel(x_str)
    plt.ylabel(y_str)
    if horizontal is not None:
        xlims = ax.get_xlim()
        ax.plot(xlims, [horizontal, horizontal], color = np.array([1,1,1])*0.3, zorder = 0 )
        ax.set_xlim(xlims)
    "colour bar"
    plt.colorbar(sc).set_label(z_str)
    #plt.show()
    return fig, ax 

__all__ = ["scatter_clr_df"]
