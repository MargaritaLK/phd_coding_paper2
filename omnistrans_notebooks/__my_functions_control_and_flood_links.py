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
   
    
    
def create_link_df_with_accessibility(links_omni_arrival,variant_name, alchemyEngine, output_path):

    # compute for every link the first arrival 
    linknrs_first_arrival_df = create_df_with_linknr_flooded(links_omni_arrival)


    # filter out the connectors
    linknrs_connectors = get_linknrs_connectors(variant_name, alchemyEngine)
    link_df_noconnectors = link_df[~link_df["linknr"].isin(linknrs_connectors)] #is not in, due to the '~'
    geom_df_noconnectors = geom_df[~geom_df["linknr"].isin(linknrs_connectors)] #is not in, due to the ~



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