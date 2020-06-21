import streamlit as st
import pandas as pd

st.write('This is my first streamlit app!')

x = st.slider('x', min_value=2000, max_value=2020)
st.write('Year chosen:', x)

# Reuse this data across runs!
read_and_cache_csv = st.cache(pd.read_csv)

BUCKET = "https://streamlit-self-driving.s3-us-west-2.amazonaws.com/"
data = read_and_cache_csv('https://nx9055.your-storageshare.de/s/mperqsyoN8o3NB6/download')
selectbox_country = st.multiselect('Filter to country:', data.country.unique())
# st.write(selectbox_iso3)
selectbox_event_type = st.multiselect('Filter to event_type:', data.event_type.unique())
# st.write(selectbox_event_type)


st.write(data[(data.year == x)
              & (data.country.isin(selectbox_country))
              & (data.event_type.isin(selectbox_event_type))
              ].head(1000))
