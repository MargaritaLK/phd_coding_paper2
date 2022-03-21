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


#--------------------------------------------------------------------------------
## GET DATA FROM DB
#------------------------------------------------------------------------------------------------------------
def get_link_data(variant_name, user_in, result_in, iteration_in, postgreSQLConnection):
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


#------------------------------------------------------------------------------------------------------------

def get_link_ioflow(variant_name, user_in, result_in, iteration_in, postgreSQLConnection):
    sql = f"\
        SELECT a.geom, b.* \
        FROM {variant_name}.link5_1data3 as b, public.links_geom AS a \
        WHERE b.linknr = a.linknr \
        AND b.result = {result_in}\
        AND b.user = {user_in}\
        AND b.iteration = {iteration_in}"
    
    link_io_flow = gpd.GeoDataFrame.from_postgis(sql, postgreSQLConnection, geom_col='geom' )
     
     #create unique links every dir
    link_io_flow["linknr_dir"] = link_io_flow["linknr"].astype(str) + "_" + link_io_flow["direction"].astype(str)
    return link_io_flow


#------------------------------------------------------------------------------------------------------------

def get_linknrs_connectors(variant_name, alchemyEngine):
    sql = f'SELECT * FROM {variant_name}.link2_1data1 as a \
        WHERE a.typenr = 1 \
        AND a.direction = 1'
    linknr_connectors_out = pd.read_sql_query(sql, alchemyEngine).linknr.values
    return linknr_connectors_out




## DERIVE SOME BASICS
#------------------------------------------------------------------------------------------------------------

def get_list_uniquelinks(link_df):
    links_nr = link_df['linknr'].unique()
    print(len(links_nrdr))
    return links_nrdr



#--------------------------------------------------------

def get_timesteps_plot(link_df):
    link_df.time.unique()
    first_timestep = link_df.time.min()
    last_timestep = link_df.time.max()
    time_period = last_timestep - first_timestep
    
    print(f'first timestep: {first_timestep}')
    print(f'last timestep: {last_timestep}')
    print(f'simulation period: {time_period} minutes')
    print(f'simulation period: {(time_period)/60} hrs')
  
    timesteps_plot = link_df.time.unique() - first_timestep
    return timesteps_plot




#--------------------------------------------------------------------------------
### COMPOUTE CLEARANCE TIME 
#---------------------------------------------------------------------

def compute_departures(link_io_flow_df, linknr_connectors):
    departures = link_io_flow_df.loc[(link_io_flow_df["linknr"].isin(linknr_connectors)) & (link_io_flow_df.direction == 1 )]
    cum_departures = departures.groupby("time").sum().linkcumulativeinflow

    cum_departures_final = cum_departures.values.max()
    print(f'total departures: {cum_departures_final}')
    return cum_departures

#----------------------------------------------------------------------------------------------------


def compute_in_network_and_arrivals(cum_departures, link_io_flow_df, supersafe_zone_nr, supersafe_linknr, supersafe_direction, total_nr_hh):
    
    #calculate ARRIVALS
    arrivals_safe = link_io_flow_df.loc[(link_io_flow_df.linknr == supersafe_linknr) & (link_io_flow_df.direction == supersafe_direction)]
    total_arrivals = np.round(arrivals_safe.linkcumulativeoutflow.max())
    
    ## calcualate number of people in network
    in_network = cum_departures.values -  arrivals_safe.linkcumulativeoutflow.values
    
    ## clearance time
    clearance_time_timestep = arrivals_safe[arrivals_safe.linkcumulativeoutflow > total_arrivals-0.3].time.min()
    clearance_time = clearance_time_timestep - link_io_flow_df.time[0]
    percentage_cleared = np.round((total_arrivals/total_nr_hh)*100)

    return in_network, arrivals_safe, total_arrivals, clearance_time, percentage_cleared



#----------------------------------------------------------------------------------------------------

def plot_in_network_and_safe(in_network, arrivals_safe, timesteps_plot):
    fig = plt.figure(figsize=(5, 5))

    plt.plot(timesteps_plot, in_network[:len(timesteps_plot)], label = 'in network', c= '#ef476f', linewidth = 2)
    plt.plot(timesteps_plot, arrivals_safe.linkcumulativeoutflow[:len(timesteps_plot)], label = 'in safe zone', c= '#06d6a0', linewidth = 2)
    plt.legend()


    
#---------------------------------------------------------------------------------------------  
def plot_clearance_time(timesteps_plot, cum_departures, in_network, arrivals_safe, total_arrivals, clearance_time, percentage_cleared, total_nr_hh, simulation_description, figures_path):
    
    #make plot
    fig = plt.figure(figsize=(10, 5))
    ax1 = fig.add_subplot(1, 1, 1)

    #total nr hh
    ax1.fill_between(timesteps_plot, 0, total_nr_hh , color= '#fcbf49', alpha = 0.4)
    ax1.hlines(total_nr_hh, 0,timesteps_plot.max(), color = '#fcbf49' )
    # ax1.text(len(timesteps_plot)/3, total_nr_hh/1.4, 'AT HOME', color = '#f8961e')

    ## total demand
    # ax1.hlines(sum_departures_total, 0,timesteps_plot.max(), color = 'grey' , linestyles='--')


    #departures
    ax1.plot(timesteps_plot, cum_departures, c = '#d00000', markersize = 3)
    ax1.fill_between(timesteps_plot, arrivals_safe['linkcumulativeinflow'], cum_departures, color='#d00000', alpha = 0.5)
    # ax1.text(len(timesteps_plot)/3, total_nr_hh/2, 'IN NETWORK', color = '#d00000')

    ##safe arrivals
    ax1.plot(timesteps_plot, arrivals_safe['linkcumulativeinflow'], c = '#52b788', linewidth = 2)
    ax1.fill_between(timesteps_plot, 0, arrivals_safe['linkcumulativeinflow'] , color= '#52b788', alpha = 0.5)

    #clearance time
    ax1.vlines(clearance_time, 0, total_nr_hh*1.0, color= '#2d6a4f', linestyles='--', linewidth = 2)
    ax1.text(clearance_time*1.02, total_arrivals*1.06, 
             f'clearance: {percentage_cleared }% in {np.round(clearance_time/60,2)} hrs', color= '#2d6a4f' )
    # ax1.text(clearance_time/1.5, total_nr_hh/3, 'SAFE', color = '#2d6a4f')

    ax1.set_title(f'{simulation_description} households')

    print(f'total hh in area {total_nr_hh}')
    print(f'total hh INFLOW safezone:  {total_arrivals}')
    print(f'percentage binnen {percentage_cleared } %')
    print(f'{percentage_cleared}% binnen na {np.round(clearance_time/60,2)} uur')

    plt.savefig(f'{figures_path}/clearance_time_{simulation_description}.png', dpi=300)  
    
    
    
    
    
    
    
    
    
    


#--------------------------------------------------------------------------------
## GENERAL PLOT FUNCTIONS
##---------------------------------------------------------------------

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
    
    
        
def plot_density_all_links(link_df, color, simulation_description, figures_path ):
    fig = plt.figure(figsize=(20, 5),facecolor='#e9ecef')
    ax = fig.add_subplot(1, 1, 1)
    ax.set_facecolor('#e9ecef')
    
    links_nrdr = link_df.linknr_dir.unique()
    for i in links_nrdr:
        link_data = link_df[link_df["linknr_dir"] == i]
        ax.plot(link_data['time'],link_data['density'], linewidth = 1.5, c = color, alpha = 0.3)

    ax.set_title(f'density_{simulation_description}') 
    plt.savefig(f'{figures_path}/density_{simulation_description}.png', dpi=300)   



    
    
#--------------------------------------------------------------------------------
## CLEARANCE TIME
##---------------------------------------------------------------------













