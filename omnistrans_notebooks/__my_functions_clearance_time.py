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

from __my_functions import get_link_data
from __my_functions import get_link_ioflow
from __my_functions import get_linknrs_connectors
from __my_functions import compute_departures
from __my_functions import compute_in_network_and_arrivals
from __my_functions import get_timesteps_plot
from __my_functions import plot_in_network_and_safe
from __my_functions import plot_clearance_time




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