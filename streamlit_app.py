import pandas as pd
import streamlit as st
import pydeck as pdk
from PIL import Image




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
data_load_state = st.text('Data is load!')

where_to_go = pd.merge(where_to_go,airports, left_on ='DESTINATION_AIRPORT',right_on='IATA_CODE')
st.write(where_to_go.head())

start_airport =  st.select_slider ('Выберите аэропорт отправления:', options = flights['ORIGIN_AIRPORT'].unique())
st.write('Аэропорт отправления: '+ start_airport)

where_to_go_from_start_airport = flights[flights.ORIGIN_AIRPORT==start_airport]['DESTINATION_AIRPORT'].unique()
where_to_go_from_start_airport = pd.DataFrame(where_to_go_from_start_airport)
where_to_go_from_start_airport.columns = ['DESTINATION_AIRPORT']

top3 = where_to_go_from_start_airport \
        .merge(where_to_go, on='DESTINATION_AIRPORT', how='inner') \
        .sort_values(by=['RMSE', 'MEAN_ARRIVAL_DELAY_PREDICT'], ascending=[True, True]) \
        .head(3)

top3 = pd.DataFrame(top3)
st.write('Подбираем аэропорт прибытия с минимальной вероятностью задержки : ')

#where_to_go['LATITUDE2'] = where_to_go[where_to_go.IATA_CODE==start_airport].apply(lambda row: row ['LATITUDE'] , axis=1)
#where_to_go['LONGITUDE2'] = where_to_go[where_to_go.IATA_CODE==start_airport].apply(lambda row: row ['LONGITUDE'] , axis=1)

def sourse_lat():
    lat = where_to_go[where_to_go.IATA_CODE==start_airport]['LATITUDE']
    return  lat
def sourse_lng():
    lng = where_to_go[where_to_go.IATA_CODE==start_airport]['LONGITUDE']
    return  lng

sourse_position = where_to_go[where_to_go.IATA_CODE==start_airport]
start_airport_position = top3.append(sourse_position)
start_airport_position.fillna(0, inplace = True)
top3['lat']=top3.apply(lambda row: sourse_lat(), axis=1)
top3['lng']=top3.apply(lambda row: sourse_lng(), axis=1)
st.write(top3)

st.pydeck_chart(pdk.Deck(
     map_style='mapbox://styles/mapbox/light-v9',
     initial_view_state=pdk.ViewState(
         latitude=40.3,
         longitude=-105,
         zoom=12,
         pitch=50,
     ),
     tooltip={
        "text": "RMSE: {RMSE}",
        'style': {
            'color': 'white'}},

     layers=[
         pdk.Layer(
            'ScatterplotLayer',
            data=start_airport_position,
            pickable=True,
            opacity=0.8,
            stroked=True,
            filled=True,
            radius_scale=6,
            get_position='[LONGITUDE, LATITUDE]',
            get_fill_color=[255, 140, 0],
            get_line_color=[0, 0, 0],
            get_radius=8000,
         ),
         pdk.Layer(
            "TextLayer",
            data=start_airport_position,
            get_position='[LONGITUDE, LATITUDE]',
            get_text="AIRPORT",
            get_color=[0, 0, 0],
            get_size=18,
            get_alignment_baseline="'bottom'",
         ),
         pdk.Layer(
            "GreatCircleLayer",
            top3,
            pickable=True,
            get_stroke_width=12,
            get_source_position='[lng, lat]',
            get_target_position='[LONGITUDE, LATITUDE]',
            get_source_color=[64, 255, 0],
            get_target_color=[0, 128, 200],
            auto_highlight=True,
            width_scale=0.0005,
            get_tilt=15,
            get_width="S000 * 2",
            width_min_pixels=7,
            width_max_pixels=30,
            ),
            ],
     ))

