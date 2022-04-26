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


def create_sample_houses_withinZone(samplesize, houses_all, selected_zone ):
    sample_uuid = uuid.uuid1()
    
    zone_name = selected_zone.BU_NAAM
    
    #calculate_houses_in_zones
    houses_within_zone = houses_all[houses_all.geometry.within(selected_zone.geometry)]
    

    #create sample
    print(f'nr houses in {selected_zone.BU_NAAM}: {len(houses_within_zone)}')
    if len(houses_within_zone) > samplesize:
        print(f'too many, therefor sample of {samplesize} houses taken')
        houses_df = houses_within_zone.sample(samplesize)
    else:
        print(f'all houses in zones taken' )
        houses_df = houses_within_zone

    #plot
    fig = plt.figure(figsize=(2, 2))
    ax = fig.add_subplot(1, 1, 1)
    plt.title(f'{selected_zone.BU_NAAM}')
    gpd.GeoSeries(selected_zone.geometry).plot(ax=ax, color="#dee2e6")
    houses_within_zone.plot(ax=ax, markersize=2)
    houses_df.plot(ax=ax, markersize=4)
    ax.set_axis_off()
    
    return zone_name, houses_df





## FLOOD TIME DIMENSION
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
   
    
    
## CALCULATE FLOOD DEPTH OVER TIME FOR HOUSES   
def create_df_flooddepth_houses(scenario_name, samplesize, zone_name, houses_df, gr, time_humanized, last_timestamp, output_path):
    
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
     
    flooddepth_time_houses_df.to_json(f'{output_path}/fdepth_houses_df_{scenario_name}_zone{zone_name}.json')
    
    return flooddepth_time_houses_df
    
    
    
    
### COMPUTE first arrival and max depth for zone
def calculate_first_qth_arrival_and_maxdepth(flooddepth_time_houses_df):
    arrival_times = []
    max_depths = []
    quantile_value = 0.1
    
    #loop over all (sample) houses within zone
    for house, floodepths in flooddepth_time_houses_df.items():
        max_depth = flooddepths.max()
        max_depths.append(max_depth)

        for i in range(len(content)):
            if content[i] > 0.01:
                arrival_time = flooddepth_time_houses_df.index[i]
                arrival_timestamp = datetime.timestamp(arrival_time)
                arrival_times.append(arrival_timestamp)
                break
                

                
    #derive arrival for zone
    first_qth_arrival = np.quantile(arrival_times, quantile_value)
    first_qth_arrival_dt = datetime.fromtimestamp(first_qth_arrival)
    
    
    #derive max depth for zone
    max_depth = max(max_depths)
    
    return first_qth_arrival_dt, max_depth 

    
    
def plot_flooddepth_houses_in_zone(zone_name, flooddepth_time_houses_df, first_qth_arrival, max_depth, time_humanized):
    fig = plt.figure(figsize=(4, 2))
    ax = fig.add_subplot(1, 1, 1)

    for label, content in flooddepth_time_houses_df.items():
        ax.plot(content, c = '#003566', alpha = 0.5)

#     ax.set_xlim(time_humanized[0],time_humanized[40])
    ax.axvline(x = first_qth_arrival, color = 'r', linestyle ='--')
    ax.axhline(max_depth, color= '#ffc300', linestyle ='--')
    plt.title(f'{zone_name}')
    
 
