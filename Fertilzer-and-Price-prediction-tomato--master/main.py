import streamlit as st
import pandas as pd
from joblib import load
from sklearn.preprocessing import LabelEncoder
import datetime as dt
import requests 

# Load the saved model
loaded_model = load('model (2).joblib')
# Load the CSV file with additional information
info_df = pd.read_csv('tomato_suplliments.csv')  

#write funciton to convert kelvin to celsius
def kelvin_to_celsius(kelvin):
    celsius = kelvin - 273.15
    return celsius

#write a function to collect whether data from the api
def collect_weather_data(city):
    try:
        BASE_URL = "http://api.openweathermap.org/data/2.5/weather?"
        API_KEY = open('apikey.txt','r').read()
        url = BASE_URL + "appid=" + API_KEY + "&q=" + city
        response = requests.get(url)
        if response.status_code == 200:
            print(response)
            return response.json()
        else:
            return None
    except Exception as e:
        st.error(f"An error occured while fetching weather data {e}")
        return None


# Streamlit app
st.title("Fertilizer Prediction App for Tomato")

# Open live weather app
proceed = 0
# while city is None:
#     city = st.text_input("Enter City:",key="city_input")
#     if city:
#         weather_data = collect_weather_data(city)
#         if weather_data is None:
#             st.warning("Invalid City Name. Please enter the city name again!!")
#             city = None
#         else:
#             proceed = 1

#different method
city = st.text_input("enter your city:")
weather_data = collect_weather_data(city)
if weather_data is None: 
    st.warning("invalid city name. Please enter the correct city name")
else:
    proceed = 1

#fetch weather data
if proceed == 1:
    temp_kelvin = weather_data['main']['temp']
    temp = kelvin_to_celsius(temp_kelvin)
    temparature = int(temp)
    humidity = weather_data['main']['humidity']

    # User inputc
    # temparature = st.slider("Temperature", min_value=0, max_value=100, value=25)
    # humidity = st.slider("Humidity", min_value=0, max_value=100, value=50)
    moisture = st.slider("Moisture", min_value=0, max_value=100, value=30)
    soil_type = st.selectbox("Soil Type", ["Clay", "Sandy", "Loam"])
    # crop_type = st.selectbox("Crop Type", ["Wheat", "Rice", "Maize"])
    crop_type = "Maize"
    nitrogen = st.slider("Nitrogen", min_value=0, max_value=100, value=50)
    potassium = st.slider("Potassium", min_value=0, max_value=100, value=50)
    phosphorous = st.slider("Phosphorous", min_value=0, max_value=100, value=50)

# Apply label encoding to 'soil type' and 'crop type' on the fly
    le_soil = LabelEncoder()
    le_soil.fit(['Clay', 'Sandy', 'Loam'])
    soil_type_encoded = le_soil.transform([soil_type])[0]

    le_crop_type = LabelEncoder()
    le_crop_type.fit(['Wheat', 'Rice', 'Maize'])
    crop_type_encoded = le_crop_type.transform([crop_type])[0]


    # Make prediction
    input_data = pd.DataFrame({
        'temparature': [temparature],
        'humidity': [humidity],
        'moisture': [moisture],
        'soil type': [soil_type_encoded],
        'crop type': [crop_type_encoded],
        'nitrogen': [nitrogen],
        'potassium': [potassium],
        'phosphorous': [phosphorous],
    })
    #Display city and local area information

    st.write(f"City: {city}")

    # Display prediction
    if st.button("Predict Fertilizer"):
        prediction = loaded_model.predict(input_data)
        st.success(f"The Predicted Fertilizer for your tomato farm is: {prediction[0]}")




