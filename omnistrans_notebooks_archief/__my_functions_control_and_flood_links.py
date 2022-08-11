import psycopg2
from sqlalchemy import create_engine
import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import time
import random
import math
import plotly.express as px


from __my_functions import get_link_data
from __my_functions import get_link_ioflow
from __my_functions import get_linknrs_connectors
from __my_functions import compute_departures
from __my_functions import compute_in_network_and_arrivals
from __my_functions import get_timesteps_sim
from __my_functions import get_timesteps_plot
from __my_functions import get_time_dimensions
from __my_functions import plot_in_network_and_safe
from __my_functions import plot_clearance_time




def create_df_with_linknr_flooded(links_omni_arrival):
    
    ## df with only linknr and minutes
    linknrs_arrival_df = links_omni_arrival[['linknr', 'minutes']]
    linknrs_arrival_df = linknrs_arrival_df.dropna()
    linknrs_arrival_df = linknrs_arrival_df.astype({"linknr": int})
    linknrs_arrival_df = linknrs_arrival_df.astype({"minutes": int})
    
    #group based on first arrival at link
    linknrs_first_arrival_df = linknrs_arrival_df.groupby(['linknr']).min()
    
    return linknrs_first_arrival_df
   
    
    
def create_link_df_with_accessibility(link_df, links_omni_arrival, variant_name, alchemyEngine, output_path):
    
    first_timestep, last_timestep, time_period = get_time_dimensions(link_df)
    timesteps_plot = get_timesteps_plot(link_df)
    timesteps_sim = get_timesteps_sim(link_df)

    # compute for every link the first arrival 
    linknrs_first_arrival_df = create_df_with_linknr_flooded(links_omni_arrival)


    # filter out the connectors
    linknrs_connectors = get_linknrs_connectors(variant_name, alchemyEngine)
    link_df_noconnectors = link_df[~link_df["linknr"].isin(linknrs_connectors)] #is not in, due to the '~'


    # create db of link_df _including road accesibility 
    links_accessibility = link_df_noconnectors.copy()
    links_accessibility["inaccessible"] = math.nan

    #if flood arrival time in minutes is between t1 en t1, set inaccessible to 1
    for index, row in links_accessibility.iterrows():
        linknr = row.linknr
        timestep = row.time
        absolute_time = timestep - first_timestep

        if linknr in linknrs_first_arrival_df.index:
            arrivaltime = linknrs_first_arrival_df.loc[linknr].minutes
            if absolute_time > arrivaltime:
                links_accessibility.at[index, 'inaccessible'] = 1


    links_accessibility.to_file(f'{output_path}/links_accessibility.json' )
    
    return links_accessibility