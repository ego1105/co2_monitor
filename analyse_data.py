#!/usr/bin/python3
# -*- coding:utf-8 -*-

import sys
import os
import pandas as pd
import matplotlib.pyplot as plt

# for testing of outlier removal and data smoothing
# plotting on high resolution image

# data file name
file_name = 'data_log.csv'
table = pd.read_csv( file_name, index_col=0, parse_dates=True)
#table = table.tail(500)

print( table.tail(10) )
print( table.describe() )

fig, axs = plt.subplots( figsize=( 12, 8), dpi=100, 
    nrows=3, sharex=True, gridspec_kw={'hspace': 0, 'wspace': 0})

# outlier removal
table2 = table.sort_index()
Q1 = table2.quantile(0.03)
Q3 = table2.quantile(0.97)
IQR = Q3 - Q1
table2 = table2[~((table2 < (Q1 - 1.5 * IQR)) |(table2 > (Q3 + 1.5 * IQR))).any(axis=1)]
print( table2.tail(10) )
print( table2.describe() )

table2.plot( subplots=True, ax=axs)
for ax in fig.get_axes():
    ax.label_outer()
    ax.autoscale(enable=True, axis='both', tight=True)
    ax.grid(True, 'major', 'both')            

plt.savefig("analysis_plot.png")

table3 = table2
table3.index = ( table3.index - table3.index[-1] ) / pd.Timedelta(hours=1)
if len(table3.index) > 5:
    table3 = table3.rolling( 3).mean()
print( table3.tail(10) )
print( table3.describe() )


fig, axs = plt.subplots( figsize=( 12, 8), dpi=100, 
    nrows=3, sharex=True, gridspec_kw={'hspace': 0, 'wspace': 0})
for ax in fig.get_axes():
    ax.label_outer()
    ax.autoscale(enable=True, axis='both', tight=True)
    ax.grid(True, 'major', 'both')        

table2.plot( subplots=True, ax=axs)
table3.plot( subplots=True, ax=axs, style='k--')
plt.savefig("analysis_plot2.png")