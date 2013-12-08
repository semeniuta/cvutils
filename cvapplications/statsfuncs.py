# -*- coding: utf-8 -*-
from scipy import stats

def round_dataframe_col(col, ndigits):
   return col.apply(round, args=[ndigits])
    
def round_dataframe(df, ndigits):  
    return df.apply(round_dataframe_col, args=[ndigits])
    
def calc_mode(data):
    return stats.mode(data)[0][0] 