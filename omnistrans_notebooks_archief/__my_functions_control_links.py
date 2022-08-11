import psycopg2
from sqlalchemy import create_engine
import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import time
import random
import plotly.express as px





def create_df_with_linknr_flooded(links_omni_arrival):
    
    ## df with only linknr and minutes
    linknrs_arrival_df = links_omni_arrival[['linknr', 'minutes']]
    linknrs_arrival_df = linknrs_arrival_df.dropna()
    linknrs_arrival_df = linknrs_arrival_df.astype({"linknr": int})
    linknrs_arrival_df = linknrs_arrival_df.astype({"minutes": int})
    
    #group based on first arrival at link
    linknrs_first_arrival_df = linknrs_arrival_df.groupby(['linknr']).min()
    
    return linknrs_first_arrival_df
    