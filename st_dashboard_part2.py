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
from PIL import Image
from numerize.numerize import numerize


########################### Initial settings for the dashboard ##################################################################


st.set_page_config(page_title = 'New York CitiBike Strategy Dashboard', layout='wide')
st.title("New York CitiBike Strategy Dashboard")

# Define side bar
st.sidebar.title("Aspect Selector")
page = st.sidebar.selectbox('Select an aspect of the analysis',
  ["Intro page","Weather component and bike usage",
   "User Type and Member Distribution", "Most popular stations",
    "Interactive map with aggregated bike trips", "Recommendations"])

########################## Import data ###########################################################################################

df = pd.read_csv('reduced_data_to_plot_7.csv')
top20 = pd.read_csv('top20.csv', index_col = 0)

######################################### DEFINE THE PAGES #####################################################################


### Intro page

# --- Function Definitions for Plotting ---

# Function to set up the plot
def setup_plot():
    fig_2 = make_subplots(specs=[[{"secondary_y": True}]])
    return fig_2

# Function to add bike rides trace
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

# Function to add temperature trace
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

# Function to finalize the plot layout
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

# Main function to create the chart
def main(df):
    fig_2 = setup_plot()  
    add_bike_rides_trace(fig_2, df) 
    add_temperature_trace(fig_2, df)  
    return finalize_plot(fig_2)

# --- Streamlit Page Code ---

if page == "Intro page":
    st.markdown("#### This dashboard aims at providing helpful insights on the expansion problems CitiBike currently faces.")
    st.markdown("Right now, CitiBike runs into a situation where customers complain about bikes not being available at certain times. This analysis will look at the potential reasons behind this. The dashboard is separated into 4 sections:")
    st.markdown("- User Type and Member Distribution")
    st.markdown("- Weather component and bike usage")
    st.markdown("- Most popular stations")
    st.markdown("- Interactive map with aggregated bike trips")
    st.markdown("- Recommendations")
    st.markdown("The dropdown menu on the left 'Aspect Selector' will take you to the different aspects of the analysis our team looked at.")

    myImage = Image.open("CitiBikes.jpg")  
    st.image(myImage)

# Page for 'Weather component and bike usage'
elif page == 'Weather component and bike usage':
    fig_2 = main(df)  
    st.plotly_chart(fig_2, use_container_width=True)
    st.markdown("There is an obvious correlation between the rise and drop of temperatures and their relationship with the frequency of bike trips taken daily. As temperatures plunge, so does bike usage. This insight indicates that the shortage problem may be prevalent merely in the warmer months, approximately from May to October.")

# Most popular stations page
elif page == 'Most popular stations':
    
    # Create the filter on the side bar
    with st.sidebar:
        season_filter = st.multiselect(label='Select the season', options=df['season'].unique(), default=df['season'].unique())

    df1 = df.query('season == @season_filter')
    
    # Define the total rides
    total_rides = float(df1['bike_rides_daily'].count())    
    st.metric(label='Total Bike Rides', value=numerize(total_rides))

    # Bar Chart for most popular stations
    df1['value'] = 1
    df_groupby_bar = df1.groupby('start_station_name', as_index=False).agg({'value': 'sum'})
    top20 = df_groupby_bar.nlargest(20, 'value')

    fig = go.Figure(go.Bar(
        x=top20['start_station_name'], 
        y=top20['value'], 
        marker={'color': top20['value'], 'colorscale': 'Purples'}
    ))

    fig.update_layout(
        title='Top 20 most popular bike stations in New York',
        xaxis_title='Start stations',
        yaxis_title='Sum of trips',
        width=900, height=600,
        plot_bgcolor='rgba(0,0,0,0)', 
        paper_bgcolor='rgba(255, 255, 255, 0.8)',
    )
    
    st.plotly_chart(fig, use_container_width=True)
    st.markdown("From the bar chart it is clear that overall, there are some start stations that are more popular than others - in the top 3 we can see W 21 St/6 Ave, West St/Chambers St as well as Broadway/W 58 St." )
    st.markdown("During Fall and Winter, W 21 St/6 Ave consistently have the most trips.")
    st.markdown("During Spring and Summer, West St/Chambers St becomes the most popular station.")

 # User type and member distribution bar and pie plots page
elif page == 'User Type and Member Distribution':
    st.header('User Type and Member Distribution')

    # Check if the columns exist
    if 'bike_type' in df.columns and 'membership_type' in df.columns:
        usertype_counts = df['bike_type'].value_counts()  
        member_counts = df['membership_type'].value_counts()     

        # Create a figure with two axes (subplots)
        fig_3, ax = plt.subplots(1, 2, figsize=(14, 6))

        # Plotting the bar chart for 'bike_type' on the first axis (ax[0])
        bar_colors = ['#9b4d96', '#5c1358'][:len(usertype_counts)]
        usertype_counts.plot(kind='bar', ax=ax[0], color=bar_colors, edgecolor='black')
        ax[0].set_title('Usertype Distribution')  
        ax[0].set_xlabel('User Type')  
        ax[0].set_ylabel('Count')  

        # Plotting the pie chart for 'membership_type' on the second axis (ax[1])
        pie_colors = ['#9b4d96', '#6a0e5e']
        ax[1].pie(member_counts, labels=member_counts.index, autopct='%1.1f%%', colors=pie_colors, startangle=90)
        ax[1].set_title('Member Distribution')  

        # Display the plot in Streamlit using st.pyplot()
        st.pyplot(fig_3)
        st.markdown("The bar chart illustrating user type distribution reveals that classic bikes are used significantly more frequently than electric bikes.")
        st.markdown("The pie chart provides a clear view of the member vs. casual user distribution for 2022. This demonstrates that the majority of CitiBike riders are frequent, repeat customers who likely have subscriptions, which indicates strong customer loyalty and suggests that the service is well-established among New York City's commuting population.")
    else:
        st.error("The 'bike_type' or 'membership_type' column is missing from the dataset.")

# Page for 'Interactive map with aggregated bike trips'
elif page == 'Interactive map with aggregated bike trips':
    # Add the map 
    st.write("Interactive map showing aggregated bike trips over New York")

    path_to_html = "NewYorkCitiBikeTripData.html" 

    # Read file and keep in variable
    with open(path_to_html, 'r') as f: 
        html_data = f.read()

    # Show in webpage
    st.header("Aggregated Bike Trips in New York")
    st.components.v1.html(html_data, height=1000)
    st.markdown("#### Using the filter on the left-hand side of the map, we can check whether the most popular start stations also appear in the most popular trips.")
    st.markdown("A high number of trips through central New York, and there is opportunity for expansion near waterfront areas, namely near Battery Park where West St/Chambers St is located and is a popular station during warmer months.")


else:
    st.header("Conclusions and recommendations")
    bikes = Image.open("successful_chart.jpg")  # Source : https://www.google.com/url?sa=i&url=https%3A%2F%2Fwww.vecteezy.com%2Ffree-photos%2Fsuccess-diagram&psig=AOvVaw1T08uqfku_0pb1XkmECwc5&ust=1742926573353000&source=images&cd=vfe&opi=89978449&ved=0CBQQjRxqFwoTCLDfstupo4wDFQAAAAAdAAAAABAE
    st.image(bikes)
    st.markdown("### Our analysis has shown that New York CitiBike should focus on the following objectives moving forward:")
    st.markdown("- Given the clear correlation between warmer temperatures and higher bike usage, CitiBike should consider scaling up its fleet during peak months (May-October). This would help address customer complaints about bike unavailability and ensure more bikes are available during high-demand periods.")
    st.markdown("- Stations such as W 21 St/6 Ave, West St/Chambers St, as well as Broadway/W 58 St show high levels of demand. CitiBike could explore expanding bike capacity at these locations and adding more stations in densely populated areas with frequent usage, and this includes the area surrounding Battery Park at the waterfront as well.")
    st.markdown("- Instead of a uniform scaling back of bikes during the winter, I recommend a dynamic allocation model where bikes are reduced at low-demand stations, but kept at high demand stations, such as W 21/6 Ave as well as Broadway/W 58 st.")
    st.markdown("- Since classic bikes are used more often than electric bikes, CitiBike should assess whether the electric bike fleet is large enough to meet the growing demand. Expanding electric bike availability could attract more users, particularly for longer trips.")
    st.markdown("- Consider creating an incentive program to reward loyal members, and entice casual users to become members. This could include offering reward points for members based on the amount of miles they have ridden. These points could then be redeemed for discounts, free rides, or special rewards. Another incentive recommendation is a referral bonus for new riders, where both the referrer and the new user gets reward points when a first-time rider joins CitiBike as a member using a referral code. These ideas can help grow the user base while rewarding loyal customers.")
