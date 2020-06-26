import os
from pathlib import Path

import plotly.express as px
import streamlit as st
import pandas as pd
import seaborn as sns
from scipy import stats
from matplotlib import pyplot as plt

def resumetable(df):
    print(f"Dataset Shape: {df.shape}")
    summary = pd.DataFrame(df.dtypes, columns=['dtypes'])
    summary = summary.reset_index()
    summary['Name'] = summary['index']
    summary = summary[['Name', 'dtypes']]
    summary['Fehlend'] = df.isnull().sum().values
    summary['Eindeutig'] = df.nunique().values
    summary['Erster Wert'] = df.loc[0].values
    summary['Letzter Wert'] = df.loc[(len(df.index) - 1)].values

    #    for name in summary['Name'].value_counts().index:
    #        summary.loc[summary['Name'] == name, 'Entropie'] = round(
    #            stats.entropy(df[name].value_counts(normalize=True), base=2), 2)

    return summary


# path = str(Path(os.getcwd()).parent) + '/acled_api.csv'
path = str(Path(os.getcwd())) + '/acled_api.csv'
if os.path.exists(path):
    filepath = path
#    print('Using local ACLED')
else:
    print('Downloading ACLED')
    filepath = 'https://api.acleddata.com/acled/read.csv?terms=accept&limit=0'

@st.cache
def read_addmonth_cache(file):

    cf = pd.read_csv(file)
    cf['event_date'] = cf['event_date'].astype('datetime64[ns]')
    cf.insert(6, 'month', cf.event_date.dt.month, allow_duplicates=True)
    print(type(cf))
    return cf


# Reuse this data across runs!
read_and_cache_csv = st.cache(pd.read_csv, allow_output_mutation=True)
data = read_addmonth_cache(filepath)

# Add Month column
#data= data['event_date'] = data['event_date'].astype('datetime64[ns]')
#data.insert(6, 'month', data.event_date.dt.month, allow_duplicates=True)
st.sidebar.subheader('Navigation')

radio_navigation = st.sidebar.radio('Select Page:', ['Welcome', 'Data Exploration', 'Filter Data', 'Scatter Map', 'Fatality Globe'])

if radio_navigation == 'Welcome':
    st.write('This is my first streamlit app!')
    button_loadacled = st.button('Load newest ACLED-Dataset')
    if button_loadacled:
        data = read_and_cache_csv('https://api.acleddata.com/acled/read.csv?terms=accept&limit=0')
        st.write('new ACLED loaded!')

    st.write(resumetable(data))

if radio_navigation == 'Data Exploration':
    plt.figure(figsize=(11, 10))
    plt.xticks(rotation=0)

    sns.countplot(x='year', data=data)

    plt.title('Data distribution by years')
    st.pyplot()
    st.write('test')

elif radio_navigation == 'Filter Data':

    st.sidebar.subheader('Filter')
    selectbox_country = st.sidebar.multiselect('Filter to country:', data.country.unique())
    # st.write(selectbox_iso3)
    selectbox_event_type = st.sidebar.multiselect(
        'Filter to event_type:', data[data.country.isin(selectbox_country)].event_type.unique())
    # st.write(selectbox_event_type)

    x = st.sidebar.multiselect('Filter to year:', data[data.country.isin(selectbox_country)].year.unique(),)

    checkbox_fatalities = st.sidebar.checkbox("Show only events involving fatalities")

    # x = st.sidebar.slider('x', min_value=int(data[data.country.isin(selectbox_country)].year.min()),
    #                      max_value=int(data[data.country.isin(selectbox_country)].year.max()))
    if checkbox_fatalities:
        #    (data.fatalities >= 1)
        st.write(data[data.year.isin(x)
                      & (data.country.isin(selectbox_country))
                      & (data.event_type.isin(selectbox_event_type))
                      & (data.fatalities[data.fatalities >= 1])
                      ].head(10000))

        st.subheader('Map of all pickups')

        st.map(data[data.year.isin(x)
                    & (data.country.isin(selectbox_country))
                    & (data.event_type.isin(selectbox_event_type))
                    & (data.fatalities >= 1)
                    ])
    else:
        st.write(data[data.year.isin(x)
                      & (data.country.isin(selectbox_country))
                      & (data.event_type.isin(selectbox_event_type))
                      ].head(10000))

        st.subheader('Map of all pickups')

        st.map(data[data.year.isin(x)
                    & (data.country.isin(selectbox_country))
                    & (data.event_type.isin(selectbox_event_type))
                    ])


elif radio_navigation == 'Scatter Map':

    x = st.slider("Select year", int(data.year.min()), int(data.year.max()) , 2019)
    slider_zoom = st.sidebar.slider("Select Zoomlevel", 0, 8, 2)
    fig = px.scatter_mapbox(data[data.year == x],
                            lat="latitude", lon="longitude", color="fatalities", size="fatalities",
                            hover_data=['actor1', 'actor2', 'event_type'],
                            color_continuous_scale=px.colors.cyclical.IceFire, size_max=15, zoom=slider_zoom,
                            width=1000, height=800, animation_frame="month")
    fig.update_layout(mapbox_style="open-street-map")
    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})

    st.plotly_chart(fig)

elif radio_navigation == 'Fatality Globe':
    data_map = data[['iso3', 'year', 'country', 'fatalities']].groupby(
        ['year', 'country', 'iso3'], as_index=False).count().reset_index()

    st.write(data_map)

    fig = px.choropleth(
        data_map,
        locations="iso3",
        locationmode="ISO-3",
        hover_name="country",
        animation_frame="year",
        color='fatalities',
        width=800, height=1000,
        projection="orthographic")
    st.plotly_chart(fig)

mapstyle_dict = {"streets": "streets-v11",
                 "light": "light-v10",
                 "dark": "dark-v10",
                 "satellite": "satellite-v9"}

mapstyle = st.sidebar.selectbox('Map style', list(mapstyle_dict), 1)
