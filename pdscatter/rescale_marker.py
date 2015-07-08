# -*- coding: utf-8 -*-
"""
Created on Tue Jul  7 12:18:37 2015

@author: dima
"""
import numpy as np

def rescale_marker(xl, gain = 5, offset = 2, square = True):
    maxl = max(xl)
    minl = min(xl)
    range_ = maxl - minl
    k = gain / range_
    x_out = [ (offset + (x - minl) *k) for x in xl]
    if square:
        return [np.pi*x**2 for x in x_out]
    else:
        return x_out

