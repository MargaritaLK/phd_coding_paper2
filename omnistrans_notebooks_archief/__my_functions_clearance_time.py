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
from __my_functions import get_timesteps_plot
from __my_functions import plot_in_network_and_safe
from __my_functions import plot_clearance_time




def create_df_centroidgeom_connectordata(link_io_flow_df, centroid_data, centroids_geom, variant_name, alchemyEngine):
    
    ## STEP 1
    linknr_connectors = get_linknrs_connectors( variant_name, alchemyEngine)
    
    # departures over time
    departures_over_time = link_io_flow_df.loc[(link_io_flow_df["linknr"].isin(linknr_connectors)) & (link_io_flow_df.direction == 1 )]
    total_departures = compute_departures(link_io_flow_df, linknr_connectors)
    
    #drop connector geoms
    departures_nogeom = departures_over_time.drop(labels = 'geom', axis = 1)
    
    
    ## STEP 2 join van geom centroids en centroid data -> zodat geomcentroids ook linknr heeft
    #get geom of centroid only of the departing ones
    relevant_centroids = centroid_data.centroidnr.unique()
    rel_centroid_geoms = centroids_geom[centroids_geom["centroidnr"].isin(relevant_centroids)]

    # get table of centroidsnr and linknr
    centroid_links = centroid_data.loc[centroid_data.time == link_io_flow_df.time[0]][['centroidnr', 'linknr' ]]

    # join these two, to get geom of relevant centroids, incl linknr
    centroids_geom_linknr = rel_centroid_geoms.merge(centroid_links, left_on='centroidnr', right_on='centroidnr')

    ## cleanup_onused columns
    centroids_geom_linknr = centroids_geom_linknr.drop(labels = {'centroidab', 'centroab_2', 'centroab_3'}, axis = 1)

    
    ## join restult 1 en result 2
    departures_centroid_geom = departures_nogeom.merge(centroids_geom_linknr, left_on='linknr', right_on='linknr')
    departures_centroid_geom = departures_centroid_geom.drop(labels = {'linkinflow', 'linkoutflow'}, axis = 1)

    return departures_centroid_geom



def timeslice_centroidgeom_connectordata(timestep, centroidgeom_connectordata):
    timeslice = centroidgeom_connectordata[centroidgeom_connectordata["time"] == timestep]
    print(f'total outflow: {timeslice.linkcumulativeinflow.max()}')
    return timeslice


def get_data_for_clearancetime(variant_name, user_in, result_in, iteration_in, postgreSQLConnection, alchemyEngine):
    
    link_df = get_link_data(
        variant_name = variant_name,
        user_in = user_in,
        result_in = result_in,
        iteration_in = iteration_in, 
        postgreSQLConnection= postgreSQLConnection)

    link_io_flow_df = get_link_ioflow(variant_name = variant_name, 
                 user_in = user_in, 
                 result_in =  result_in, 
                 iteration_in = iteration_in, 
                 postgreSQLConnection = postgreSQLConnection)

    linknr_connectors = get_linknrs_connectors( variant_name, alchemyEngine)
    
    return link_df, link_io_flow_df, linknr_connectors





def compute_clearance_time(link_df, link_io_flow_df, linknr_connectors, total_nr_hh, simulation_description, figures_path):
    
    cum_departures = compute_departures(link_io_flow_df, linknr_connectors)

    in_network, arrivals_safe, total_arrivals, clearance_time, percentage_cleared = compute_in_network_and_arrivals(
                cum_departures= cum_departures,
                link_io_flow_df = link_io_flow_df, 
                supersafe_zone_nr = 80, 
                supersafe_linknr = 3311, 
                supersafe_direction = 2, 
                total_nr_hh = 99999)

    timesteps_plot = get_timesteps_plot(link_df)

    plot_clearance_time(timesteps_plot, 
                    cum_departures,
                    in_network, 
                    arrivals_safe, 
                    total_arrivals, 
                    clearance_time, 
                    percentage_cleared, 
                    total_nr_hh,
                    simulation_description, 
                    figures_path)