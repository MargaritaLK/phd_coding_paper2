import matplotlib
import matplotlib.pyplot as plt

import matplotlib.dates as mdates
import numpy as np
from datetime import datetime
import pandas as pd
from matplotlib.animation import FuncAnimation
import geopandas as gpd
import threedigrid
from threedigrid.admin.gridresultadmin import GridH5ResultAdmin
from threedigrid.admin.gridadmin import GridH5Admin

import uuid



def get_time_dimensions_flood(gr, start_breach_time):
    tijdstappen = gr.nodes.timestamps
    laatste_tijdstap = tijdstappen[-1]
    aantal_tijdstappen = tijdstappen.shape
    interval = tijdstappen[5] -  tijdstappen[4]

    print('rekentijd:',laatste_tijdstap/3600, 'uur')
    print('aantal tijdstappen:',aantal_tijdstappen[0])
    print(f'interval: {round(interval,2)}, secondes = {round(interval/60,2)} min')
    
    node_for_time = gr.nodes.filter(id__eq = 1)
    timestamps = node_for_time.timestamps
    last_timestamp=  timestamps[-1]

    epoch = np.datetime64(start_breach_time)
    timestamps_dtnotation = epoch + timestamps.astype(np.timedelta64(1, 's'))
    time_humanized = timestamps_dtnotation.astype(datetime)
    print(f' breach start time at: {time_humanized[0]}')
    
    return time_humanized, last_timestamp
   
    
    
    
    
    
def create_df_flooddepth_houses(scenario_name, samplesize, sample_uuid, houses_df, gr, time_humanized, last_timestamp, output_path):
    
    flooddepth_time_houses_df= pd.DataFrame( index = time_humanized)

    for index, row in houses_df.iterrows():
        cell_id = int(row["cell_id"])
        house_id = f'id_{str(row["huis_id"])}'
        maaiveld = row["h_maaiveld"]

        restult_node = gr.nodes.filter(id__eq = cell_id).timeseries(start_time=0, end_time=last_timestamp)
        waterstand =  restult_node.s1
        
        if waterstand.max() > maaiveld :
            waterdiepte =  waterstand - maaiveld
            waterdiepte[waterdiepte < 0] = 0
            flooddepth_time_houses_df[house_id] = waterdiepte
     
    flooddepth_time_houses_df.to_json(f'{output_path}/fdepth_houses_df_{scenario_name}_sz{samplesize}_sampleuuid_{sample_uuid}.json')
    
    return flooddepth_time_houses_df
    
    
    
    
    
    
    
    
 
