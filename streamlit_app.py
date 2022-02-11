import pandas as pd
import streamlit as st
import pydeck as pdk
from PIL import Image
import numpy as np

image = Image.open('1590132426_3.jpg')
st.image(image, caption='Airlines of USA')
st.title('FLIGHT DELAYS')

# Настройка боковой панели
st.sidebar.title("About")
st.sidebar.info(
    """
    This app is Open Source dashboard.
    """
)
st.sidebar.info("Feel free to collaborate and comment on the work. The github link can be found "
                "[here](https://github.com/sv-zeynalova/Flight-delays-project).")
data_load_state = st.text('Loading data...')

@st.cache
def load_data():
    flights = pd.read_csv('Flights3.csv')
    return flights
flights = load_data()

@st.cache
def load_data():
    where_to_go = pd.read_csv('where_to_go.csv')
    return where_to_go
where_to_go = load_data()

@st.cache
def load_data():
    airports = pd.read_csv('airports1.csv')
    return airports
airports = load_data()


where_to_go = pd.merge(where_to_go,airports, left_on ='DESTINATION_AIRPORT',right_on='IATA_CODE')
where_to_go.drop(['IATA_CODE','Unnamed: 0'], axis = 1, inplace=True)
st.write(where_to_go.head())

ad =  st.select_slider ('Выберите эропорт отправления:', options = flights['ORIGIN_AIRPORT'].unique())

#start_airport = np.random.choice(flights['ORIGIN_AIRPORT'].unique())
st.write('Аэропорт отправления: '+ ad)
where_to_go_from_start_airport = flights[flights.ORIGIN_AIRPORT==ad]['DESTINATION_AIRPORT'].unique()
where_to_go_from_start_airport = pd.DataFrame(where_to_go_from_start_airport)
where_to_go_from_start_airport.columns = ['DESTINATION_AIRPORT']

top3 = where_to_go_from_start_airport \
        .merge(where_to_go, on='DESTINATION_AIRPORT', how='inner') \
        .sort_values(by=['RMSE', 'MEAN_ARRIVAL_DELAY_PREDICT'], ascending=[True, True]) \
        .head(3)
st.write('Подбираем аэропорт с минимальной вероятностью задержки прибытия: ')
st.write(top3)

st.pydeck_chart(pdk.Deck(
     map_style='mapbox://styles/mapbox/light-v9',
     initial_view_state=pdk.ViewState(
         latitude=40.3,
         longitude=-105,
         zoom=11,
         pitch=50,
     ),
     tooltip={"text": "{from_name} to {to_name}"},

    layers=[
         pdk.Layer(
            'ScatterplotLayer',
            data=top3,
            pickable=True,
            opacity=0.8,
            stroked=True,
            filled=True,
            radius_scale=6,
            get_position='[LONGITUDE, LATITUDE]',
            get_fill_color=[255, 140, 0],
            get_line_color=[0, 0, 0],
            get_radius=10000,
         ),
         pdk.Layer(
            "TextLayer",
            data=top3,
            get_position='[LONGITUDE, LATITUDE]',
            get_text="AIRPORT",
            get_color=[0, 0, 0],
            get_size=18,
            get_alignment_baseline="'bottom'",
         ),
         #pdk.Layer(
            #"GreatCircleLayer",
            #start_airport_position,
            #pickable=True,
            #get_stroke_width=12,
            #get_source_position='[LONGITUDE2, LATITUDE2]',
            #get_target_position='[LONGITUDE, LATITUDE]',
            #get_source_color=[64, 255, 0],
            #get_target_color=[0, 128, 200],
            #auto_highlight=True,
            #),
            ],
     ))




