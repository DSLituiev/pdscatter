# -*- coding: utf-8 -*-
"""
Created on Tue Jul  7 12:18:37 2015

@author: dima
"""
import plotly.plotly as py # interactive graphing
from plotly.graph_objs import Bar, Scatter, Marker, Layout , Data, Figure
import plotly.tools as tls
from .rescale_marker import rescale_marker

def _smart_format_(x, n = 4):
    xt = type(x)
    if xt is float:
        return '%s' %round(x, n)
    elif xt is int:
        return '%u' % x
    else:
        return '%s' % x

def hover_all(df, *args, **kwargs):
    out = '%s ' % df.name
    for n in df.index:
        out += '<br>%s:&nbsp;&nbsp;&nbsp;&nbsp;%s ' % (n, _smart_format_(df[n]) )
    return out

def hover_selected(df, x,y,z):
    out = '%s ' % df.name
    for n in (x,y,z):
        out += '<br>%s:&nbsp;&nbsp;&nbsp;&nbsp;%s ' % (n, _smart_format_(df[n]) )
    return out


def scatter_df_plotly(df, x, y, z, text_fnct = hover_all, 
                      interactive = True, filename= None):
    """
    a wrapper function for `plotlyi.graph_objs.Scatter` on `pandas.Dataframe`

    usage:
    =====
    d

    """
    SC = Scatter(x=df[x], y = df[y],
                    mode='markers',
                    marker = Marker(size = rescale_marker(df[z], square = True),
                                 color = df[z],
                                 colorscale = 'Jet',
                                 sizeref = 1,
                                 sizemode = 'area')
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
        df.apply(lambda ds: text_fnct(ds, x=x, y=y,z=z), axis = 1).tolist()  )

    if interactive:
        return py.plot(FIG, filename = filename)
    else:
        return py.iplot(FIG)


