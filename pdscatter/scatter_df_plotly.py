# -*- coding: utf-8 -*-
"""
Created on Tue Jul  7 12:18:37 2015

@author: dima
"""
import plotly.plotly as py # streaming graphing
from plotly.graph_objs import Bar, Scatter, Marker, Layout , Data, Figure, XAxis, YAxis, Font
import plotly.tools as tls
from .rescale_marker import rescale_marker

def smart_format(x, n = 4):
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
        out += '<br>%s:&nbsp;&nbsp;&nbsp;&nbsp;%s ' % (n, smart_format(df[n]) )
    return out

def hover_selected(df, x,y,z):
    out = '%s ' % df.name
    for n in (x,y,z):
        out += '<br>%s:&nbsp;&nbsp;&nbsp;&nbsp;%s ' % (n, smart_format(df[n]) )
    return out


def scatter_df_plotly(df, x, y, z, text_fnct = hover_all, 
                      streaming = True, filename= None):
    """
    a wrapper function for `plotlyi.graph_objs.Scatter` on `pandas.Dataframe`

    usage:
    =====
    d

    """
    layout = Layout(
        title='colour map: %s' % z,
        hovermode='closest',  # (!) hover -> closest data pt
        showlegend=False,     # remove legend (info in hover)
        autosize=False,       # turn off autosize
        width=650,            # plot width
        height=500,           # plot height
        xaxis=XAxis(
            title= x,
            titlefont=Font(
                family='Courier New, monospace',
                size=14,
                color='#7f7f7f'
            )
        ),
        yaxis=YAxis(
            title= y,
            titlefont=Font(
                family='Courier New, monospace',
                size=14,
                color='#7f7f7f'
            )
        )
    )
#    print('marker sizes:')
#    print(rescale_marker(df[z], square = True))
    SC = Scatter(x=df[x], y = df[y],
                    mode='markers',
                    marker = Marker(size = rescale_marker(df[z], square = True),
                                 color = df[z],
                                 colorscale = 'Jet',
                                 sizeref = 1,
                                 sizemode = 'area')
                )

    FIG = Figure(data = Data([SC]) , layout=layout )   
    #FIG['layout'].update( )
    
    if text_fnct is not None:
        FIG['data'][0].update(text = \
        df.apply(lambda ds: text_fnct(ds, x=x, y=y,z=z), axis = 1).tolist()  )

    if not streaming:
        if filename is not None:
            return py.plot(FIG, filename = filename)
        else:
            return py.plot(FIG)
    else:
        return py.iplot(FIG)


