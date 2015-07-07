# -*- coding: utf-8 -*-
"""
Created on Tue Jul  7 12:18:37 2015

@author: dima
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def scatter_df_plotly(df_samples, x, y, z, text_fnct = None,
                      interactive = True, filename= None):
    
    import plotly.plotly as py # interactive graphing
    from plotly.graph_objs import Bar, Scatter, Marker, Layout , Data
    import plotly.tools as tls
    
    SC = Scatter(x=df_samples[x], y = df_samples[y],
                  mode='markers',
                 marker = Marker(size = df_samples[z], 
                                 color = df_samples[z],
                                 colorscale = 'Jet',
                                 sizeref = 0.5,
                                 sizemode = 'diameter')
                )
    FIG = Figure(data = Data([SC]) )
    
    FIG['layout'].update(
        hovermode='closest',  # (!) hover -> closest data pt
        showlegend=False,     # remove legend (info in hover)
        autosize=False,       # turn off autosize
        width=650,            # plot width
        height=500,           # plot height
    )
    
    if text_fnct is not None:
        FIG['data'][0].update(text = \
        df_samples.apply(make_text, axis = 1).tolist()  )
    if interactive:
        return py.plot(FIG, filename = filename)
    else:
        return py.iplot(FIG)


def scatter_clr_df(df_samples, x, y, z, horizontal = 0):
    crlator = correlate_df(df_samples, 'log2_gene_exp_ratio', 'log10_control_gene_coverage')
    ccf, valid = crlator(True)
    cm = plt.cm.get_cmap('RdYlBu')
    
    def rescale_marker(x_in, gain = 5, offset = 2):
        xl = [x**2 for x in x_in]
        maxl = max(xl)
        minl = min(xl)
        range_ = maxl - minl
        k = gain / range_
        return [ np.pi*(offset + (x - minl) *k)**2 for x in xl]
        
    fig = plt.figure()
    ax = fig.add_subplot(111)
    gain = 5
    offset = 2
    df_samples.sort(z, ascending = False, inplace = True)
    sc = ax.scatter( list(df_samples[x][valid]), 
                list(df_samples[y][valid]) , 
                s = rescale_marker(df_samples[z][valid]),
                c = df_samples[z][valid] , vmax = max(s_in), 
                vmin = min(s_in), edgecolors = None)
    
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