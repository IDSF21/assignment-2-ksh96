import streamlit as st
import pandas as pd
import numpy as np
# import matplotlib.pyplot as plt
# import seaborn as sns
import pydeck as pdk
import plotly.express as px

# from geopy.geocoders import Nominatim

# st.set_page_config(layout="wide")

# filename = '/Users/ksheerajaraghavan/CMU/2nd Sem/Interactive Data Science/HW2/HW2_Data_Science/cleaned.csv'

url='https://drive.google.com/file/d/1d71oTtuquCXbSqeSLzhnUhBSbOzpBllP/view?usp=sharing'
path = 'https://drive.google.com/uc?export=download&id='+url.split('/')[-2]
df = pd.read_csv(path)

# convert states
states = {'Alabama': 'AL', 'Alaska': 'AK', 'Arizona': 'AZ', 'Arkansas': 'AR', 'California': 'CA',
          'Colorado': 'CO', 'Connecticut': 'CT', 'Delaware': 'DE', 'Florida': 'FL', 'Georgia': 'GA',
          'Hawaii': 'HI', 'Idaho': 'ID', 'Illinois': 'IL', 'Indiana': 'IN', 'Iowa': 'IA', 'Kansas': 'KS',
          'Kentucky': 'KY', 'Louisiana': 'LA', 'Maine': 'ME', 'Maryland': 'MD', 'Massachusetts': 'MA',
          'Michigan': 'MI', 'Minnesota': 'MN', 'Mississippi': 'MS', 'Missouri': 'MO', 'Montana': 'MT',
          'Nebraska': 'NE', 'Nevada': 'NV', 'New Hampshire': 'NH', 'New Jersey': 'NJ', 'New Mexico': 'NM',
          'New York': 'NY', 'North Carolina': 'NC', 'North Dakota': 'ND', 'Ohio': 'OH', 'Oklahoma': 'OK',
          'Oregon': 'OR', 'Pennsylvania': 'PA', 'Rhode Island': 'RI', 'South Carolina': 'SC',
          'South Dakota': 'SD', 'Tennessee': 'TN', 'Texas': 'TX', 'Utah': 'UT', 'Vermont': 'VT',
          'Virginia': 'VA', 'Washington': 'WA', 'West Virginia': 'WV', 'Wisconsin': 'WI', 'Wyoming': 'WY'}


# geolocator = Nominatim(user_agent='application')

@st.cache
def load_data(f):
    df = pd.read_csv(f)
    return df


def maps_AQI(data):
    df = data[data['State'] != 'Country Of Mexico']  # deleting Mexico
    df = df[df['State'] != 'District Of Columbia']  # deleting Columbia
    df['sr'] = df.State.apply(lambda x: states[x])
    # st.write(df.head())
    b = df.drop(['NO2 Mean', 'SO2 Mean', 'O3 Mean', 'CO Mean', 'NO2 1st Max Value', 'SO2 1st Max Value', 'O3 1st Max Value', 'CO 1st Max Value','NO2 1st Max Hour', 'SO2 1st Max Hour', 'O3 1st Max Hour', 'CO 1st Max Hour'], axis=1)
    # st.write(b.head())
    #b = b.set_index('Date Local')
    b['Date Local'] = pd.to_datetime(b['Date Local'])
    pollutant_list = ['NO2 AQI', 'SO2 AQI', 'O3 AQI', 'CO AQI']
    pollutant1 = st.selectbox('What pollutant do you want to see', pollutant_list)
    # b = b.set_index('Date Local')
    a = b.groupby('sr').resample('Y',on='Date Local').mean()
    a.reset_index(inplace=True)
    # st.write('A is ')
    # st.write(a)
    a['Year'] = a['Date Local'].dt.year
    # Sorting values by Date Local (for animated choropleth presented below)
    a.sort_values(by = 'Date Local', inplace = True)
    # Plotly choropleth showing AQI for Nitrogen Dioxide changes from 2000 to 2016
    fig_NO2 = px.choropleth(a,
                  locations = 'sr',
                  animation_frame="Year", # showing changes through the years
                  color=pollutant1,
                  # Creating fixed scale (the same as defined by EPA)
                  color_continuous_scale = [(0.00, "green"),   (0.1, "green"),
                                            (0.1, "yellow"), (0.2, "yellow"),
                                            (0.2, "orange"),  (0.3, "orange"),
                                            (0.3, "red"),  (0.6, "red"),
                                            (0.6, "maroon"),  (1.00, "maroon"),
                                            ],
                  range_color = (0, 500),
                  locationmode='USA-states',
                  scope="usa",
                  title='Mean values of Air Quality Index (AQI) per year for ' + pollutant1,
                  height=600,
                 )

    # Modifying legend 
    fig_NO2.update_layout(coloraxis_colorbar=dict(
        title="Air Quality Index (AQI)",
        ticks="outside", 
        dtick=50
    ))
    st.plotly_chart(fig_NO2)
    # resample('Y').mean(4)


def onestate(data):
    st.subheader('Choose all the pollutants for one state')
    state_list = data.State.unique()
    values = st.selectbox(label='select multiple states', options=state_list)
    pollutant_list = ['NO2 Mean', 'SO2 Mean', 'O3 Mean', 'CO Mean', 'NO2 AQI', 'SO2 AQI', 'O3 AQI', 'CO AQI']
    pollutant1 = st.multiselect('What pollutant do you want to see', pollutant_list)
    # st.write(data.head(10000))
    time_list = ['Year', 'Month']
    time1 = st.selectbox('Choose time: ', time_list)
    b = data[data['State'] == values]
    pollutant1 = pollutant1 + ['Date Local', 'State']
    b = b.filter(pollutant1)
    b = b.set_index('Date Local')
    b.index = pd.to_datetime(b.index)
    b = b.resample(time1[0]).mean()
    st.line_chart(b)


def statewise(data):
    st.subheader('One Pollutant for One state')
    state_list = data.State.unique()
    state = st.selectbox('Choose state: ', state_list)
    st.write('You have selected: ' + state)
    pollutant_list = ['NO2 Mean', 'SO2 Mean', 'O3 Mean', 'CO Mean', 'NO2 AQI', 'SO2 AQI', 'O3 AQI', 'CO AQI']
    pollutant = st.selectbox('Choose pollutant: ', pollutant_list)
    st.write('You have selected: ' + pollutant)
    time_list = ['Month', 'Year']
    time2 = st.selectbox('Choose time: ', time_list)
    st.write('You have selected: ' + time2)
    column = data.columns
    # filter for histogram
    hist_data = data[data['State'] == state]
    a = hist_data.copy()
    a = a.set_index('Date Local')

    a.index = pd.to_datetime(a.index)
    b = a.resample(time2[0]).mean()
    b = b.filter([pollutant])
    st.subheader('Graph of ' + state + ' with pollutant ' + pollutant + ' for ' + time2 + 'ly view')
    st.line_chart(b)


def year(data):
    import time
    state_list = data.State.unique()
    st.text('Let us be more specific. Think of your home state...')
    values = st.selectbox(label='Select State', options=state_list)
    year_list = np.arange(2000, 2017)
    # st.write(year_list)
    year = st.selectbox('What year do you want to see?', year_list)
    # st.write(data.head(10000))

    b = data[data['State'] == values]
    # st.write(b)
    b['Date Local'] = pd.to_datetime(b['Date Local'])
    mask = b['Date Local'].dt.year == int(year)
    b = b[mask]
    b = b.drop(['NO2 1st Max Value', 'NO2 1st Max Hour', 'O3 1st Max Value', 'O3 1st Max Hour','SO2 1st Max Value', 'SO2 1st Max Hour', 'CO 1st Max Value', 'CO 1st Max Hour' ],axis=1)
    # st.write(b)

    for i in range(4, 20):
        fig = px.scatter(b, x='Date Local', y=b.columns[i])
        st.plotly_chart(fig)
        

    st.plotly_chart(fig)
    # st.line_chart(b)


if __name__ == '__main__':
    data = load_data(path)
    st.title('Have we destroyed our planet Earth?')
    st.header('Let us look at US Air Quality.....')
    st.text('Let us look at the raw data...')
    st.write(data.head(100))
    st.text('Hmm... I think I need to be an Environmental Engineer to understand this...')

    st.subheader('Lets make it simpler.')
    st.text('We can look at trends over time')
    year(data)
    st.subheader('Select Check Box for State Wise Plots')
    if st.checkbox('State Plots'):
        statewise(data)

    # maps_daily(data)
    # if st.checkbox('')
    maps_AQI(data)
    onestate(data)
    
