# 참고자료 : https://towardsdatascience.com/streamlit-101-an-in-depth-introduction-fc8aad9492f2
# 참고자료 : https://github.com/shaildeliwala/experiments/blob/master/streamlit.py

import pandas as pd
import streamlit as st
import plotly.express as px
import pydeck as pdk
import numpy as np

@st.cache
def get_data():
    return pd.read_csv("files/listings.csv")

# The st.cache decorator indicates that Streamlit will perform
# internal magic so that the data will be downloaded only once
# and cached for future use.

df = get_data()

st.title("Streamlit 101: An in-depth introduction")
st.markdown("Welcome to this in-depth introduction to \
            [Streamlit](www.streamlit.io)! For this exercise, \
            we'll use an Airbnb [dataset](http://data.insideairbnb.com/united-states/ny/new-york-city/2019-09-12/visualisations/listings.csv) containing NYC listings.")
st.header("Customary quote")
st.markdown("> I just love to go home, no matter where I am,\
            the most luxurious hotel suite in the world, I love\
             to go home.\n\n—Michael Caine")
st.header("Airbnb NYC listings: data at a glance")
st.markdown("The first five records of the Airbnb data we \
            downloaded.")

st.dataframe(df)
st.header('Chaching our data')
st.markdown("Streamlit has a handy decorator['st.chace']\
        (https://streamlit.io/docs/api.html#optimize-performance) to enable data caching.")

st.code("""
@st.cache
def get_data():
    url = "http://data.insideairbnb.com/united-states/ny/new-york-city/2019-09-12/visualisations/listings.csv"
    return pd.read_csv(url)
""", language="python")

st.markdown("_To display a code block, pass in the string to display as code to [`st.code`](https://streamlit.io/docs/api.html#streamlit.code)_.")
with st.echo():
    st.markdown("Alternatively, use [`st.echo`](https://streamlit.io/docs/api.html#streamlit.echo).")

st.header("Where are the most expensive properties located?")
st.subheader("On a map")
st.markdown("The following map shows the top 1% most expensive Airbnbs priced at $800 and above.")
st.map(df.query("price>=800")[["latitude", "longitude"]].dropna(how="any"))

# 또다른 지도 라이브러리
# https://docs.streamlit.io/api.html#streamlit.map

df = pd.DataFrame(np.random.randn(1000, 2) / [50, 50] + [37.76, -122.4],
                  columns=['lat', 'lon'])

st.pydeck_chart(pdk.Deck(map_style='mapbox://styles/mapbox/light-v9',
                initial_view_state=pdk.ViewState(latitude=37.76,
                longitude=-122.4, zoom=11, pitch=50,),
            layers=[ pdk.Layer('HexagonLayer', data=df,
                    get_position='[lon, lat]', radius=200,
                    elevation_scale=4, elevation_range=[0, 1000],
                    pickable=True, extruded=True, ),
            pdk.Layer('ScatterplotLayer', data=df,
                get_position='[lon, lat]',
                get_color='[200, 30, 0, 160]',
                get_radius=200,),
            ],
            ))

