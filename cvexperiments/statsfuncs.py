# -*- coding: utf-8 -*-

def round_dataframe_col(col, ndigits):
   return col.apply(round, args=[ndigits])
    
def round_dataframe(df, ndigits):  
    return df.apply(round_dataframe_col, args=[ndigits])