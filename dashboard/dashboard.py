import pandas as pd
import streamlit as st
from chart import *

data = pd.read_csv("dashboard/clean_data.csv")

list_pol = list(data.columns[2:8])
list_pol.sort()

list_station = list(data["station"].unique())
list_station.sort()

data["date"] = pd.to_datetime(data["date"], errors='coerce')
list_year = list(data["date"].dt.year.unique())
list_year.sort()


# Set Streamlit page configuration
st.set_page_config(
    page_title="Customized Streamlit App",
    layout="wide",  # Makes the app layout wider
    initial_sidebar_state="expanded"
)

# Streamlit content
st.title("Air Quality In China")

container1 = st.container(border=True)
summary, mapPos = container1.columns([4, 2])

with summary:
    st.text(f"Last Update Of Air Pollutant : {list(data["date"].unique())[-1]}")
    station_list = list(data["station"].unique())
    tabs = st.tabs(station_list)

    for tab, station in zip(tabs, station_list):
        with tab:
            row1= tab.container()
            row2= tab.container()

            col11, col12, col13 = row1.columns(3)
            col21, col22, col23 = row2.columns(3)

            col11.markdown("**PM2.5**", unsafe_allow_html=True)
            col11.altair_chart(donut_chart(data, station, "PM2.5"))
            
            col12.markdown("**PM10**", unsafe_allow_html=True)
            col12.altair_chart(donut_chart(data, station, "PM10"))

            col13.markdown("**SO2**", unsafe_allow_html=True)
            col13.altair_chart(donut_chart(data, station, "SO2"))
            
            col21.markdown("**NO2**", unsafe_allow_html=True)
            col21.altair_chart(donut_chart(data, station, "NO2"))

            col22.markdown("**CO**", unsafe_allow_html=True)
            col22.altair_chart(donut_chart(data, station, "CO"))

            col23.markdown("**O3**", unsafe_allow_html=True)
            col23.altair_chart(donut_chart(data, station, "O3"))

with mapPos:
    radio_pollutant1 = st.popover("Choose pollutant")
    pollutant = radio_pollutant1.radio("", list_pol) 


    st.markdown(f"**Pollutant : {pollutant}**", unsafe_allow_html=True)

    date_max = data["date"].max()
    new_data = data[data["date"] == date_max]
    st.bar_chart(new_data, x="station", y=pollutant, horizontal=True)

    radio_station1 = st.popover("Choose station")
    station = radio_station1.radio("", list_station) 

    station_data = data[data["station"] == station]
    class_counts = station_data[f"class_{pollutant}"].value_counts()

    st.markdown(f"**Station : {station}**", unsafe_allow_html=True)
    st.bar_chart(class_counts)

container2 = st.container(border=True)   
col_pol, col_loc, col_year = container2.columns(3)
radio_pollutant2 = col_pol.popover("Choose pollutant")
radio_station2 = col_loc.popover("Choose Station")
radio_year = col_year.popover("Choose Year")

pollutant2 = radio_pollutant2.radio("", list_pol + [""])
station2 = radio_station2.radio("", list_station + [""])
year = radio_year.radio("", list_year)

container2.subheader(f"{pollutant2} Condition in {station2} during {year}")

data_used = data[(data["station"] == station2) & (data["date"].dt.year == year)]
col_line, col_bar, col_line2  = container2.columns(3)

col_line.markdown("**Daily pollution condition**", unsafe_allow_html=True)
col_line.line_chart(data_used, x="date", y=pollutant2)

data_used["month"] = data_used["date"].dt.month
monthly_means = data_used.groupby('month')[pollutant2].mean().reset_index()
col_bar.markdown("**Monthly average pollution condition each day**", unsafe_allow_html=True)
col_bar.bar_chart(monthly_means, x="month", y=pollutant, horizontal=True)

data_used["hour"] = data_used["date"].dt.hour
hourly_means = data_used.groupby('hour')[pollutant2].mean().reset_index()
col_line2.markdown("**Hourly average pollution condition each day**", unsafe_allow_html=True)
col_line2.line_chart(hourly_means, x="hour", y=pollutant2)
