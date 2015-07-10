#import sys
#sys.path.append("/home/dima/data/repos/pdscatter/pdscatter/") 
#from correlate_df import *
# from scatter_df import *

import pdscatter as pdsc
import numpy as np
import pandas as pd
import datetime as dt

def sample_frame():
    numdays = 80
    base = dt.datetime.today().replace(minute = 0, second = 0, microsecond=0)
    date_list = [base - dt.timedelta(days=x) for x in range(0, numdays)]
    
    df = pd.DataFrame(np.random.randn(numdays, 5),
          columns=['usd', 'chf', 'eur', 'rur', 'cny'],
          index = pd.Index(date_list) )
    
    df['chf'] = (df['usd'] - 0.1* df['eur']) * df['rur']
    return df

df = sample_frame()

print(df)
"check correlations"
pdsc.correlate_df(df, 'usd', 'chf')

#"attach the method"
import types
#def attach_method(df, meth, mname = 'scatter'):
#    df.__dict__[mname] = types.MethodType( meth, df )
#    
#attach_method(df, pdsc.scatter_df, 'scatter')

#fig,ax = df.scatter('usd', 'chf', 'rur')
#
#
#"or use it as a classical function"
#pdsc.scatter_df(df, 'usd', 'chf', 'rur')
#
#pdsc.scatter_df(df, 'chf', 'rur')
#
#"plotly"
#link_ = pdsc.scatter_df_plotly(df, 'usd', 'chf', 'rur')
#"attached version"
df.scatter = types.MethodType( pdsc.scatter_df_plotly, df )
link_ = df.scatter('usd', 'chf', 'rur', streaming = True)
