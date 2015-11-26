# -*- coding: utf-8 -*-
"""
Created on Tue Jul  7 12:18:37 2015

@author: dima
"""
from .correlate_df import correlate_df, valid_indices
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import sys

from .rescale_marker import rescale_marker

def scatter_df(df_samples, x, y, z, horizontal = 0, clim = (None, None),
        fig = None, ax = None, correlate = True, colorbar = True,
        x_str = None, y_str = None, z_str = None, 
         size_min = 2, size_max = 5, alphamin = 0.1, alphamax = 1):

    if correlate:
        crlator = correlate_df(df_samples, x, y)
    # _, valid = crlator(True)
    valid = valid_indices(df_samples, x, y, z)
    # cm = plt.cm.get_cmap('RdYlBu')
    if not valid.all():
        print( 'discarding 2f %% of items' %  (100 *(1 - sum(valid)/ len(valid)) ), file = sys.stderr )
    if fig is None:
        fig = plt.figure()
    if ax is None:
        ax = fig.add_subplot(111)
    # df_samples.sort(z, ascending = False, inplace = True)
    df_samples = df_samples.sort_values(by = z, axis = 0 , ascending = False )
    
    vmin = df_samples[z][valid].min() if clim[0] is None else clim[0]
    vmax = df_samples[z][valid].max() if clim[1] is None else clim[1]
    
    from matplotlib import colors
    import matplotlib.cm as cm
    norm = colors.Normalize(vmin=vmin, vmax=vmax)
    colorvalues = cm.ScalarMappable(norm=norm, cmap=cm.jet).to_rgba(df_samples[z][valid])


    def calc_alpha(ds, vmin, vmax, alphamin = 0.1):
        tmp = ((ds - vmin).map(lambda x : max(x,0)) / (vmax-vmin)).map( lambda x: min(x,1) )
        tmp =  ( 1- (1-tmp)**2 )
        tmp = (alphamax - alphamin)* tmp + alphamin
        return tmp
    
    if not alphamin == 1:
        if not (alphamax==alphamin):
            alphavalues = calc_alpha(df_samples[z][valid], vmin, vmax, alphamin = alphamin ).tolist()
        else:
            alphavalues = [alphamax]*len(colorvalues)
        colorvalues = list(map(lambda z: z[0][:3] + [z[-1],],  zip(colorvalues.tolist(), alphavalues) ) )

    sc = ax.scatter( list(df_samples[x][valid]), 
                list(df_samples[y][valid]) , 
                s = rescale_marker(df_samples[z][valid], square = True,
                    vmin = vmin, vmax = vmax,
                    size_min = size_min, size_max = size_max),
                 c = colorvalues,
#                c = df_samples[z][valid] ,
#                vmax = vmax,
#                vmin = vmin, 
                edgecolors = None)
    
    sc.set_edgecolor('none')
    
    fmt = lambda z : z if type(z) is str else  ', '.join(z)
    z_str = fmt(z) if z_str is None else z_str
    y_str = fmt(y) if y_str is None else y_str
    x_str = fmt(x) if x_str is None else x_str

    if correlate:
        plt.title(crlator.__repr__().expandtabs() + '\n' + \
            'colour map: %s\n' % z_str, horizontalalignment = 'right')
    else:
        plt.title('colour map: %s\n' % z_str)
 
    start, end = ax.get_ylim()
    # ax.yaxis.set_ticks(np.arange(start, end, 1), minor=True)
    ax.yaxis.grid(True)
    ax.xaxis.grid(True)

    plt.xlabel(x_str)
    plt.ylabel(y_str)
    if horizontal is not None:
        xlims = ax.get_xlim()
        ax.plot(xlims, [horizontal, horizontal], color = np.array([1,1,1])*0.3, zorder = 0 )
        ax.set_xlim(xlims)
    "colour bar"
    if colorbar:
        plt.colorbar(sc).set_label(z_str)
    #plt.show()
    return fig, ax, sc 

__all__ = ["scatter_clr_df"]
