#!/usr/bin/python3
# -*- coding:utf-8 -*-

import sys
import os
import logging
import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image
from waveshare_epd import epd2in13b_V3

def read_data_table( file_name):
    table = pd.read_csv( file_name, index_col=0, parse_dates=True)
    # limit data
    window_hours = 8
    dt = 60
    num_lines = window_hours * dt    
    table = table.tail(num_lines)

    # outlier removal
    table2 = table
    Q1 = table2.quantile(0.05)
    Q3 = table2.quantile(0.95)
    IQR = Q3 - Q1
    table2 = table2[~((table2 < (Q1 - 1.5 * IQR)) |(table2 > (Q3 + 1.5 * IQR))).any(axis=1)]

    # create copy of table and modify
    table3 = table2.copy()    
    # convert datetime index to elapsed hours
    table3.index = ( table3.index - table3.index[-1] ) / pd.Timedelta(hours=1)
    # time window and rolling mean
    table3 = table3[-window_hours:0].rolling( 3).mean()    
    return table3


def creat_table_plot( table, w, h, dpi):
    # plot settings
    plt.rcParams['text.antialiased'] = False
    plt.rcParams['lines.antialiased'] = False
    plt.rcParams['font.family'] = 'DejaVu Sans'
    plt.rcParams['font.size'] = 9
    plt.rcParams['xtick.labelsize'] = 6
    plt.rcParams['ytick.labelsize'] = 6
    plt.rcParams['font.weight'] = 'bold'
    plt.rcParams['lines.linewidth'] = .5
    plt.rcParams["legend.frameon"] = False
    plt.rcParams["legend.handlelength"] = 0.5
    plt.rcParams['grid.linestyle'] = ':'
    plt.rcParams['grid.linewidth'] = 0.5

    # create figure and axis layout
    fig, axs=plt.subplots( figsize=( w/dpi, h/dpi), dpi=dpi, 
        nrows=3, sharex=True, gridspec_kw={'hspace': 0, 'wspace': 0})
    fig.subplots_adjust(top=1, bottom=0.15, left=0.18, right=0.93)
    
    # plot table data
    table.plot( ax=axs, subplots=True, style='r-')
    plt.tick_params(
        axis='x',          # changes apply to the x-axis
        which='both',      # both major and minor ticks are affected
        bottom=False,      # ticks along the bottom edge are off
        top=False,         # ticks along the top edge are off
        labelbottom=False) # labels along the bottom edge are off
    plt.xlabel('')
    for ax in fig.get_axes():
        ax.label_outer()
        ax.autoscale(enable=True, axis='both', tight=True)
        ax.grid(True, 'both', 'both')        
        #ax.set_frame_on(False)
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)

    # current data at bottom    
    last = table.tail(1)
    temp = last['Temp/°C'].values[0] 
    humi = last['Feucht/%'].values[0]
    co2  = last['CO2/ppm'].values[0]
    current_data = "%0.1f°C  %0.1f%%  %0.0fppm" % ( temp, humi, co2)
    plt.text( 0.01, 0.01, current_data, transform=plt.gcf().transFigure, color='r')
    return co2    


def fig2img(plt):
    """Convert a Matplotlib figure to a PIL Image and return it"""
    import io
    buf = io.BytesIO()
    plt.savefig( buf)
    buf.seek(0)
    img = Image.open(buf)
    return img


try:
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger()
    #logger.disabled = True

    logging.info("starting e-paper data logger")
    
    # get epaper handle
    epd = epd2in13b_V3.EPD()

    # data file name
    file_name = 'data_log_last_500.csv'

    # read data
    table = read_data_table( file_name)

    # plot table data
    w, h = (epd.height, epd.width)
    dpi = 111
    last_co2 = creat_table_plot( table, w, h, dpi)
    #plt.savefig("data_plot.png")

    # save last value for ampel.py
    file_co2 = 'data_last_co2.txt'
    with open( file_co2, 'w') as f:
        f.write('%d\n' % last_co2)
    
    # convert plot to image
    img = fig2img(plt)
    img = img.convert('RGB', dither=0 )

    # split into black and red pixels
    imgB = Image.new('1', img.size, 255)  
    imgR = Image.new('1', img.size, 255)  
    redData = []
    blackData = []
    for color in img.getdata():
        r, g, b = color    
        if r>b and r>g:
            redData.append( 0)      
        else:
            redData.append( 255)      
                
        if r<200 and b<200 and g<200:
            blackData.append( 0)  
        else:
            blackData.append( 255)  
    imgB.putdata(blackData)
    imgR.putdata(redData)

    # save images
    img.save("data_plot.png")
    #imgB.save("data_plotB.png")
    #imgR.save("data_plotR.png")

    # display images on e-paper
    logging.info("init and clear display " + str(epd.height) + "x" + str(epd.width) )
    epd.init()
    logging.info("Drawing") 
    epd.display(epd.getbuffer(imgB), epd.getbuffer(imgR))   
    logging.info("Goto Sleep...")
    epd.sleep()
    epd.Dev_exit()
        
except IOError as e:
    logging.info(e)
    
except KeyboardInterrupt:    
    logging.info("ctrl + c:")
    epd2in13b_V3.epdconfig.module_exit()
    exit()    