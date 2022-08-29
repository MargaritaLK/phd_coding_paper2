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
from datetime import timedelta, datetime, tzinfo, timezone,  time
import matplotlib.dates as mdates




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
    print(f'variant name: {variant_name}')
    print(f'result in: {result_in}')
    
    print(f'first timestep: {link_df.time.min()}')
    print(f'last timestep: {link_df.time.max()}')
    
    
    #create unique links every dir
    link_df["linknr_dir"] = link_df["linknr"].astype(str) + "_" + link_df["direction"].astype(str)
    return  link_df

# def save_link_data(link_df, output_path, directory_code):
#     link_df.to_json(f'{output_path}/{directory_code}test.json')

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


# def save_link_ioflow_data(link_io_flow, output_path, directory_code):
#     link_io_flow.to_json(f'{output_path}/{directory_code}/link_io_flow_{directory_code}.json')

#------------------------------------------------------------------------------------------------------------

def get_linknrs_connectors(variant_name, alchemyEngine):
    sql = f'SELECT * FROM {variant_name}.link2_1data1 as a \
        WHERE a.typenr = 1 \
        AND a.direction = 1'
    linknr_connectors_out = pd.read_sql_query(sql, alchemyEngine).linknr.values
    return linknr_connectors_out




def get_centroid_data(variant_name, user_in, result_in, iteration_in, alchemyEngine):
    sql = f"SELECT * FROM {variant_name}.centroid5_2data1 as b \
        WHERE   b.result = {result_in}\
        AND b.user = {user_in}\
        AND b.iteration = {iteration_in}"
    centroid_data = pd.read_sql_query(sql, alchemyEngine)
    return centroid_data


## DERIVE SOME BASICS
#------------------------------------------------------------------------------------------------------------

def get_list_uniquelinks(link_df):
    links_nr = link_df['linknr'].unique()
    print(len(links_nrdr))
    return links_nrdr



def get_timesteps_sim(link_df):
    return link_df.time.unique()

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


def get_datetimes_plot(timesteps_plot):
    datetimes_plot = []
    for i in timesteps_plot:
        delta = timedelta(minutes=int(i))
        datetime1 = datetime(2000, 1, 1, tzinfo=timezone.utc) + delta
        datetimes_plot.append(datetime1)
    return datetimes_plot


def get_time_dimensions(link_df):
    link_df.time.unique()
    first_timestep = link_df.time.min()
    last_timestep = link_df.time.max()
    time_period = last_timestep - first_timestep
    
    print(f'first timestep: {first_timestep}')
    print(f'last timestep: {last_timestep}')
    print(f'simulation period: {time_period} minutes')
    print(f'simulation period: {(time_period)/60} hrs')
  
    return first_timestep, last_timestep, time_period






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


def compute_in_network_and_arrivals(cum_departures, link_io_flow_df, supersafe_zone_nr, supersafe_linknrs, supersafe_direction, total_nr_hh):
    
    #calculate ARRIVALS
    arrivals_safe_temp = link_io_flow_df.loc[(link_io_flow_df['linknr'].isin(supersafe_linknrs) & (link_io_flow_df.direction == supersafe_direction))]
    arrivals_safe = arrivals_safe_temp.groupby('time',  as_index=False).sum()
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
    ax1.fill_between(timesteps_plot, 0, total_nr_hh , color= '#fcbf49', alpha = 1)
    ax1.hlines(total_nr_hh, 0,timesteps_plot.max(), color = '#343a40' )
    # ax1.text(len(timesteps_plot)/3, total_nr_hh/1.4, 'AT HOME', color = '#f8961e')

    ## total demand
    # ax1.hlines(sum_departures_total, 0,timesteps_plot.max(), color = 'grey' , linestyles='--')


    #departures
    ax1.plot(timesteps_plot, cum_departures, c = '#ef476f', markersize = 3)
    ax1.fill_between(timesteps_plot, arrivals_safe['linkcumulativeinflow'], cum_departures, color='#ef476f', alpha = 1)
    # ax1.text(len(timesteps_plot)/3, total_nr_hh/2, 'IN NETWORK', color = '#d00000')

    ##safe arrivals
    ax1.plot(timesteps_plot, arrivals_safe['linkcumulativeinflow'], c = '#343a40', linewidth = 1)
    ax1.fill_between(timesteps_plot, 0, arrivals_safe['linkcumulativeinflow'] , color= '#06d6a0', alpha = 1)

    #clearance time
    ax1.vlines(clearance_time, 0, total_nr_hh*1.0, color= '#2d6a4f', linestyles='--', linewidth = 2)
    ax1.text(clearance_time*1.02, total_arrivals*1.06, 
             f'clearance: {percentage_cleared }% in {np.round(clearance_time/60,2)} hrs', color= '#ffd166' )
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
    

    
    
def plot_density_all_links(link_df, datetimes_plot, color, simulation_description, figures_path ):
    fig = plt.figure(figsize=(20, 5),facecolor='#e9ecef')
    ax = fig.add_subplot(1, 1, 1)
    ax.set_facecolor('#e9ecef')
    
    links_nrdr = link_df.linknr_dir.unique()
    for i in links_nrdr:
        link_data = link_df[link_df["linknr_dir"] == i]
        ax.plot(datetimes_plot,link_data['density'], linewidth = 1.5, c = color, alpha = 0.3)

    #timestamps
    hours = mdates.HourLocator(interval = 2)
    ax.xaxis.set_major_locator(hours)
    h_fmt = mdates.DateFormatter('%H')
    ax.xaxis.set_major_formatter(h_fmt)
   
    ax.set_title(f'density_{simulation_description}') 
    plt.grid()
    plt.savefig(f'{figures_path}/density_{simulation_description}.png', dpi=300)
    plt.xlim(datetimes_plot[0], datetimes_plot[int(23*(60/5))])


    

def plot_load_all_links(link_df, datetimes_plot, color, simulation_description, figures_path ):
    fig = plt.figure(figsize=(20, 5),facecolor='#e9ecef')
    ax = fig.add_subplot(1, 1, 1)
    ax.set_facecolor('#e9ecef')
    
    links_nrdr = link_df.linknr_dir.unique()
    for i in links_nrdr:
        link_data = link_df[link_df["linknr_dir"] == i]
        ax.plot(datetimes_plot,link_data['load'], linewidth = 1.5, c = color, alpha = 0.3)
    
    #timestamps
    hours = mdates.HourLocator(interval = 2)
    ax.xaxis.set_major_locator(hours)
    h_fmt = mdates.DateFormatter('%H')
    ax.xaxis.set_major_formatter(h_fmt)
    plt.xlim(datetimes_plot[0], datetimes_plot[int(23*(60/5))])
    
    plt.grid()
    ax.set_title(f'loads_{simulation_description}') 
    plt.savefig(f'{figures_path}/laods_{simulation_description}.png', dpi=300)   

    
    
#--------------------------------------------------------------------------------
## visualization traffic flow
##-----------------------------------------------------------------------------

def get_links_geom(postgreSQLConnection):
    geom_sql = 'SELECT * FROM public.links_geom AS a'
    geom_df = gpd.GeoDataFrame.from_postgis(geom_sql, postgreSQLConnection, geom_col='geom' )
#     geom_df.plot(column='roadtypeab')
    
    return geom_df


def get_links_geom_noconnectors(postgreSQLConnection, variant_name, alchemyEngine):
    geom_sql = 'SELECT * FROM public.links_geom AS a'
    geom_df = gpd.GeoDataFrame.from_postgis(geom_sql, postgreSQLConnection, geom_col='geom' )
    
    linknrs_connectors = get_linknrs_connectors(variant_name, alchemyEngine)
    geom_df_noconnectors = geom_df[~geom_df["linknr"].isin(linknrs_connectors)] #is not in, due to the ~
    
    return geom_df_noconnectors





def get_centroids_geom(postgreSQLConnection):
    centroids_geom_sql = 'SELECT * FROM public.centroids_geom AS a'
    centroids_geom_df = gpd.GeoDataFrame.from_postgis(centroids_geom_sql, postgreSQLConnection, geom_col='geom' )
#     centroids_geom_df.plot()
    
    return centroids_geom_df




def export_linkdata_geojson(link_df, timestep, output_path, simulation_description, hr):
    timeslice = link_df.loc[link_df.time == timestep]
    print(type(timeslice))
    timeslice.to_file(f'{output_path}/linkdata_time/{simulation_description}_t_{timestep}_{hr}hr.geojson', drive="GeoJSON")
    
    
    
##----------------------------------------------------------------------------------



def plot_traffic_load(geom_df, df, timestep):
    fig = plt.figure(figsize=(10, 10))
    ax = fig.add_subplot(1, 1, 1)
    ax.set_facecolor('#93a8ac')
    
    timeslice = df[df["time"] == timestep]
    geom_df.plot(ax=ax, color= '#d9d9d9' )
    timeslice.plot(ax=ax,column='load', cmap="viridis", linewidth=2)
    return timestep




# start_breach_time_obj = datetime.strptime(start_breach_time, '%Y-%m-%dT%H:%M:%S')

def get_minutes_from_start_flood(start_breach_time_obj, timestep_str):
    if len(timestep_str) == 19: #is lengte van goede timstamp format
        datetime_obj = datetime.strptime(timestep_str, '%Y-%m-%d %H:%M:%S')
        delta_from_start = datetime_obj - start_breach_time_obj
        minutes_from_start =  int(delta_from_start.total_seconds() / 60)
        return minutes_from_start
    else:
        print('a timestamp skipped due to error in notation')


        
        
        
###---------STUCK ZONES-----------------------


def get_departing_zones(centroidgeom_connectordata, directory_code, zonal_path, output_path):
    
    #get shapefile zones
    buurten_all = gpd.read_file(f'{zonal_path}/cbs_buurten.shp')
    buurten_all_filterfields = buurten_all[['BU_CODE', 'BU_NAAM', 'geometry', 'AANT_INW', 'AANTAL_HH']]

    #create df with linknrs and centroidnames
    centroidgeom_linknr = centroidgeom_connectordata[['centroidnr', 'name', 'linknr']].copy().drop_duplicates()

    # merge with shapefile
    departure_zones = buurten_all_filterfields.merge(centroidgeom_linknr, left_on='BU_NAAM', right_on='name')
    
    departure_zones.to_file(f'{output_path}/{directory_code}/buurten_departured.geojson', drive="GeoJSON")
    
    return buurten_all, departure_zones




def get_outflow_zone_percentage_at_time(connector_nr, centroidgeom_connectordata, time):
    connector_nr_dir = f'{connector_nr}_1'
    in_outflow_one_connector = centroidgeom_connectordata.loc[centroidgeom_connectordata.linknr_dir == connector_nr_dir ]
    
    linkcumulativeoutflow_over_time = in_outflow_one_connector.linkcumulativeoutflow
    linkcumulativeoutflow_at_t = in_outflow_one_connector[in_outflow_one_connector.time == time].linkcumulativeoutflow
    total_hh = linkcumulativeoutflow_over_time.max()
    centroidnr = in_outflow_one_connector.centroidnr.unique()

    percentage_in_zone_at_t = ((total_hh - linkcumulativeoutflow_at_t ) / total_hh) * 100
    
    return round(percentage_in_zone_at_t.values[0], 1), centroidnr[0]




def create_df_percentages_at_time_all_zones(departure_zones, link_ids_connectors,centroidgeom_connectordata, hr):
    df_percentages_at_time_all_zones  = departure_zones.copy()
    timestep = (hr*60) + 100
    
    for linknr in link_ids_connectors: 
        percentage, centroidnr = get_outflow_zone_percentage_at_time(linknr, centroidgeom_connectordata, timestep)
        df_percentages_at_time_all_zones.loc[df_percentages_at_time_all_zones.linknr == linknr, 'percentage'] = percentage
        df_percentages_at_time_all_zones.loc[df_percentages_at_time_all_zones.linknr == linknr, 'time_hr'] = hr    
    
    return df_percentages_at_time_all_zones




def plot_zones_with_inhabitants_left(hr, departure_zones, link_ids_connectors, centroidgeom_connectordata, buurten_all, simulation_code, figures_path, directory_code, output_path):

    df_percentages_at_time_all_zones = create_df_percentages_at_time_all_zones(departure_zones, link_ids_connectors, centroidgeom_connectordata, hr)
    zones_left = df_percentages_at_time_all_zones[df_percentages_at_time_all_zones.percentage > 0]

    fig = plt.figure(figsize=(4, 4))
    ax = fig.add_subplot(1, 1, 1)
    buurten_all.plot(ax=ax, color= '#9eb3c2')

    buurten_all.plot(ax=ax, color= '#9eb3c2')
    zones_left.plot(ax=ax, color= '#ffd166')
    buurten_all.boundary.plot(ax=ax , color = '#212529', linewidth = 0.1)

    plt.title(f'{simulation_code}  || {hr} hr')
    ax.set_xlim(108000,122000)
    ax.set_ylim(535079,554000)
    ax.set_axis_off()
    
    plt.savefig(f'{figures_path}/{directory_code}/zones_with_inhabitants_left_after_{hr}hr_{directory_code}.png', dpi=300)
    zones_left.to_file(f'{output_path}/{directory_code}/zones_with_inhabitants_left_after_{hr}hr_{directory_code}.geojson', drive="GeoJSON")
    zones_left.to_csv(f'{output_path}/{directory_code}/zones_left_{hr}.csv', sep=';', decimal= ',')
    
    return zones_left


