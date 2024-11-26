import streamlit as st
import get_openweather_data as weather
import pandas as pd
import plotly.express as px

st.title("Robot Dreams Python - Weather Map & Data Vizualization App")

entered_city = st.text_input("Enter city name", "Pécs")

current_weather = weather.get_data(city=entered_city, method="weather")

if current_weather:
    st.header(f"Current weather in {entered_city}")
    kpi1, kpi2, kpi3 = st.columns(3)
    #KPI
    with kpi1:
        st.metric(
            label = "Temperature (°C)", 
            value = f"{weather.get_teperature(city=entered_city):.2f}°C") #f"${df['Close'].iloc[-1]:.2f}"
    with kpi2:
        st.metric(
            label = "Humidity (%)", 
            value = f"{weather.get_humidity(city=entered_city)}%") #f"{df['Volume'].iloc[-1]:,.2f}"
    with kpi3:
        st.metric(
            label = "Wind Speed (m/s)", 
            value = f"{weather.get_wind_speed(city=entered_city):.2f} m/s") #f"${df['High'][-30:].max():.2f}"

st.subheader("Weather Map")
st.map(weather.get_coordinates(city=entered_city))

st.subheader("Temperature Trends (Next 5 Days)")

fw_data = weather.get_data(city=entered_city,method="forecast")
fw_dt_temp = []
for day in fw_data['list']:
    fw_dt_temp.append({
        "datetime": day["dt_txt"],
        "temperature": day["main"]["temp"]
    })
fw_df = pd.DataFrame(fw_dt_temp)
fw_df.set_index("datetime", inplace=True)

forecast_weather = px.line(fw_df, x=fw_df.index, y="temperature")
st.plotly_chart(forecast_weather)
