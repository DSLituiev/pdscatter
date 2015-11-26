# -*- coding: utf-8 -*-
"""
Created on Tue Jul  7 12:18:37 2015

@author: dima
"""
import numpy as np

def rescale_marker(xl, size_min = 2, size_max = 5, square = True, vmin = None, vmax = None):
    if type(xl) is not np.ndarray:
        xl = xl.values
    valid = ~np.isinf(xl)
    vmax = np.nanmax(xl[valid]) if vmax is None else vmax
    vmin = np.nanmin(xl[valid]) if vmin is None else vmin
    vrange = vmax - vmin

    if not vrange == 0:
        gain = (size_max - size_min) / vrange
    else:
        gain = (size_max - size_min)
    x_out = [ (size_min + (x - vmin) * gain ) for x in xl.tolist()]
    
    if square:
        return [np.pi*x**2 for x in x_out]
    else:
        return x_out

