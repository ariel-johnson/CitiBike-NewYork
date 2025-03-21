################################################ NEW YORK CITIBIKES DASHABOARD #####################################################

import streamlit as st
import pandas as pd 
import numpy as np
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import matplotlib.pyplot as plt
from streamlit_keplergl import keplergl_static 
from keplergl import KeplerGl
from datetime import datetime as dt


########################### Initial settings for the dashboard ##################################################################


st.set_page_config(page_title = 'New York CitiBikes Strategy Dashboard', layout='wide')
st.title("New York CitiBikes Strategy Dashboard")
st.markdown("The dashboard will help with the expansion problems CitiBike currently faces")
st.markdown("Right now, CitiBike bikes runs into a situation where customers complain about bikes not being avaibale at certain times. This analysis aims to look at the potential reasons behind this.")

########################## Import data ###########################################################################################

df = pd.read_csv('dataset_wrangledsample.csv', index_col = 0, low_memory=False)
top20 = pd.read_csv('top20.csv', index_col = 0)

########################################### DEFINE THE CHARTS #####################################################################

## Bar Chart

fig = go.Figure(go.Bar(x = top20['start_station_name'], y = top20['value'], marker={'color': top20['value'],'colorscale': 'Purples'}))
fig.update_layout(
    title='Top 20 most popular bike stations in New York',
    xaxis_title='Start stations',
    yaxis_title='Sum of trips',
    width=900, height=600,
    plot_bgcolor='rgba(0,0,0,0)', 
    paper_bgcolor='rgba(255, 255, 255, 0.8)',
)
st.plotly_chart(fig, use_container_width=True)


## Line Chart

def setup_plot():
    fig_2 = make_subplots(specs=[[{"secondary_y": True}]])
    return fig_2

def add_bike_rides_trace(fig_2, df):
    fig_2.add_trace(
        go.Scatter(
            x=df['date'], 
            y=df['bike_rides_daily'], 
            name='Daily bike rides',
            line=dict(color='blue')  
        ),
        secondary_y=False
    )

def add_temperature_trace(fig_2, df):
    fig_2.add_trace(
        go.Scatter(
            x=df['date'], 
            y=df['avgTemp'], 
            name='Daily temperature',
            line=dict(color='red')  
        ),
        secondary_y=True
    )

def finalize_plot(fig_2):
    fig_2.update_layout(
        title='Daily Bike Rides and Temperature',
        xaxis_title='Date',
        yaxis_title='Bike Rides',
        yaxis2_title='Temperature',
        width=900,
        height=600
    )
    return fig_2  

def main(df):
    fig_2 = setup_plot()  
    add_bike_rides_trace(fig_2, df) 
    add_temperature_trace(fig_2, df)  
    return finalize_plot(fig_2)  

fig_2 = main(df)
st.plotly_chart(fig_2, use_container_width=True)


### Add the map ###

path_to_html = "NewYorkCitiBikeTripData (1).html" 

# Read file and keep in variable
with open(path_to_html,'r') as f: 
    html_data = f.read()

## Show in webpage
st.header("Aggregated Bike Trips in New York")
st.components.v1.html(html_data,height=1000)
