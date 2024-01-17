import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import pprint
import numpy as np
import math

datafile = "data/gadm41_NLD_1.json"
def plot_netherlands(datafile):
    """
    Create plot of country to plot train lines on.
    Args:
    - json file with geopandas data
    Returns:
    - country_plot(axes object): object containing country plot
    """
    # load data from file
    mapdf = gpd.read_file(datafile)

    # remove irrelevant columns
    dropnames = ['GID_1', 'GID_0', 'ISO_1', 'COUNTRY', 'VARNAME_1', 'NL_NAME_1', 'TYPE_1', 'ENGTYPE_1', 'CC_1',
        'HASC_1',]
    mapdf = mapdf.drop(dropnames, axis = 1)

    # plot country
    country_plot = mapdf.plot()
    
    return country_plot


plot_netherlands(datafile)
plt.show()