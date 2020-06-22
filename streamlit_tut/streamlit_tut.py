import os
from pathlib import Path

import streamlit as st
import pandas as pd

path = str(Path(os.getcwd()).parent) + '/acled_api.csv'
if os.path.exists(path):
    filepath = path
#    print('Using local ACLED')
else:
    print('Downloading ACLED')
    filepath = 'https://api.acleddata.com/acled/read.csv?terms=accept&limit=0'

st.write('This is my first streamlit app!')

# Reuse this data across runs!
read_and_cache_csv = st.cache(pd.read_csv)

st.sidebar.subheader('Navigation')

data = read_and_cache_csv(filepath)
st.sidebar.subheader('Filter')
selectbox_country = st.sidebar.multiselect('Filter to country:', data.country.unique(), )
# st.write(selectbox_iso3)
selectbox_event_type = st.sidebar.multiselect(
    'Filter to event_type:', data[data.country.isin(selectbox_country)].event_type.unique())
# st.write(selectbox_event_type)

x = st.sidebar.multiselect('Filter to year:', data[data.country.isin(selectbox_country)].year.unique())

# x = st.sidebar.slider('x', min_value=int(data[data.country.isin(selectbox_country)].year.min()),
#                      max_value=int(data[data.country.isin(selectbox_country)].year.max()))

st.write(data[data.year.isin(x)
              & (data.country.isin(selectbox_country))
              & (data.event_type.isin(selectbox_event_type))
              ].head(10000))

st.subheader('Map of all pickups')

st.map(data[data.year.isin(x)
            & (data.country.isin(selectbox_country))
            & (data.event_type.isin(selectbox_event_type))
            ])

mapstyle_dict = {"streets": "streets-v11",
                 "light": "light-v10",
                 "dark": "dark-v10",
                 "satellite": "satellite-v9"}

mapstyle = st.sidebar.selectbox('Map style', list(mapstyle_dict), 1)
