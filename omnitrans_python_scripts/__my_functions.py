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



## config functions

def get_link5_data(variant_name, user_in, result_in, iteration_in, postgreSQLConnection):
    sql = f"\
        SELECT a.geom, b.* \
        FROM {variant_name}.link5_2data1 as b, public.links_geom AS a \
        WHERE b.linknr = a.linknr \
        AND b.result = {result_in}\
        AND b.user = {user_in}\
        AND b.iteration = {iteration_in}\
        "
    link_df = gpd.GeoDataFrame.from_postgis(sql, postgreSQLConnection, geom_col='geom' )
    print(f'first timestep: {link_df.time.min()}')
    print(f'last timestep: {link_df.time.max()}')
    
    #create unique links every dir
    link_df["linknr_dir"] = link_df["linknr"].astype(str) + "_" + link_df["direction"].astype(str)

    return  link_df



def get_list_uniquelinks(link_df):
    links_nr = link_df['linknr'].unique()
    print(len(links_nrdr))
    return links_nrdr







## plot functions

def plot_load_one_link(link_df, linknr_plot, link_name, simulation_description, figures_path ):
    
    fig = plt.figure(figsize=(20, 5),facecolor='#e9ecef')
    ax = fig.add_subplot(1, 1, 1)
    ax.set_facecolor('#e9ecef')
    
    link_data = link_df[link_df["linknr_dir"] == linknr_plot]
    ax.plot(link_data['time'],link_data['load'], linewidth = 2, c='#52b788')
    ax.set_title(f'{link_name}_{linknr_plot}_{simulation_description}') 
    
    plt.savefig(f'{figures_path}/load_{link_name}_{linknr_plot}_{simulation_description}.png', dpi=300)  
    max_load = link_data['load'].max()
    sum_load = link_data['load'].sum()
    plt.grid()
    print(f'{linknr_plot}')
    print(f'max load: {max_load}')
    print(f'sum load: {sum_load}')
    print('----')
    


    
def plot_density_all_links(link_df, simulation_description, figures_path ):
    
  
    fig = plt.figure(figsize=(20, 5),facecolor='#e9ecef')
    ax = fig.add_subplot(1, 1, 1)
    ax.set_facecolor('#e9ecef')
    
    links_nrdr = link_df.linknr_dir.unique()

    for i in links_nrdr:
        link_data = link_df[link_df["linknr_dir"] == i]
        ax.plot(link_data['time'],link_data['density'], linewidth = 1.5, c = '#fb8500', alpha = 0.3)

    ax.set_title(f'density_{simulation_description}') 
    plt.savefig(f'{figures_path}/density_{simulation_description}.png', dpi=300)   


