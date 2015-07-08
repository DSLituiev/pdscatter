#import sys
#sys.path.append("../pdscatter") 
#from scatter_clr_df import *
#from scatter_clr_df import *
import pdscatter as pdsc

import numpy as np
import pandas as pd
import datetime as dt

numdays = 80
base = dt.datetime.today().replace(minute = 0, second = 0, microsecond=0)
date_list = [base - dt.timedelta(days=x) for x in range(0, numdays)]

df = pd.DataFrame(np.random.randn(numdays, 5),
      columns=['usd', 'chf', 'eur', 'rur', 'cny'],
      index = pd.Index(date_list) )

df['chf'] = (df['usd'] - 0.1* df['eur']) * df['rur']

print(df)


pdsc.correlate_df(df, 'usd', 'chf')

pdsc.scatter_clr_df(df, 'usd', 'chf', 'rur')


out = pdsc.scatter_df_plotly(df, 'usd', 'chf', 'rur')
