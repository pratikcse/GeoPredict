from django.http import JsonResponse
from django.shortcuts import render
import google.generativeai as genai
import openmeteo_requests
import requests_cache
import pandas as pd
import numpy as np
from statsmodels.tsa.arima.model import ARIMA
from retry_requests import retry
from datetime import datetime 
import requests
from geopy.geocoders import Nominatim
from geopy.distance import geodesic
import json
from django.shortcuts import render
from googleapiclient.discovery import build
from google.oauth2 import service_account
from django.conf import settings
import os
from requests.adapters import HTTPAdapter, Retry
from .models import Patient, Donation
from .forms import DonationForm
from django.db.models import Q
from django.shortcuts import redirect



#LOCATION AND COORDINATES

def get_ip():
    response = requests.get('https://api.ipify.org?format=json')
    ip_address = response.json()['ip']
    return ip_address

ip_address = get_ip()

def get_location(ip_address):
    response = requests.get(f'http://ip-api.com/json/{ip_address}')
    data = response.json()
    return data['lat'], data['lon']

lat, lon = get_location(ip_address)

lat = 25.26
lon = 82.99

def reverse_geocode(lat, lon):
    geolocator = Nominatim(user_agent="GeoPredictApp") 
    try:
        location = geolocator.reverse((lat, lon), exactly_one=True)
        return location.address if location else "Location not found"
    except Exception as e:
        return f"Error: {str(e)}"

address = reverse_geocode(lat, lon)

#GEMINI AI

def get_gemini_response(prompt):
    try:
        response = model.generate_content(prompt)
        
        if response and hasattr(response, 'text'):
            return response.text
        else:
            return "Error: Empty response from Gemini API"
    except Exception as e:
        print(f"Gemini API Error: {e}")
        return f"Error: {str(e)}"


PROMPT_1 = "Provide a list of emergency contact numbers and government helplines for disaster response in {address}. Only list the numbers and relevant agencies—no explanations, no additional details."
PROMPT_2 = "List essential safety precautions to follow before, during, and after a storm. Keep it brief and structured—no explanations, just key actionable points."
PROMPT_3 = "Given the coordinates {lat}, {lon}, list at least 5 nearby cities or districts within a 200 km radius that are known to be prone to storms. Return the output as a numbered list with each city/district on a new line. Do not include detailed descriptions, only the city or district names."


def gemini_api(request):
    prompt = PROMPT_1.format(address=address)
    response = get_gemini_response(prompt)
    return JsonResponse({'response': response})

def gemini_api2(request):
    response = get_gemini_response(PROMPT_2)
    return JsonResponse({'response': response})

def gemini_api3(request):
    prompt = PROMPT_3.format(lat=lat, lon=lon)
    response = get_gemini_response(prompt)
    return JsonResponse({'response': response})


GOOGLE_API_KEY = "AIzaSyDjwsK1OMbi52uXGINe6ZY33stzXz29IdA"
genai.configure(api_key=GOOGLE_API_KEY)

model = genai.GenerativeModel('gemini-1.5-pro-latest')

#EARTHQUAKE DATA

def fetch_earthquake_data():
    url = "https://earthquake.usgs.gov/fdsnws/event/1/query"
    params = {
        "format": "geojson",
        "starttime": "2020-01-01",
        "endtime": "2025-12-31",
        "minlatitude": lat,
        "maxlatitude": lat+2,
        "minlongitude": lon,
        "maxlongitude": lon+2
    }
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        return response.json()["features"] 
    return []

#MAP DATA/ HOSPITALS

def get_nearest_hospitals(lat, lon):
    query = f"""
    [out:json];
    node["amenity"="hospital"](around:10000,{lat},{lon});
    out;
    """
    url = "https://overpass-api.de/api/interpreter"
    headers = {"User-Agent": "GeoPredict/1.0"}

    try:
        response = requests.get(url, params={"data": query}, headers=headers, timeout=15)
        response.raise_for_status()
        data = response.json()
    except requests.exceptions.RequestException as e:
        print("Overpass API Request Failed:", e)
        return []
    except json.JSONDecodeError:
        print("Error: Overpass API returned invalid JSON")
        return []

    hospitals = []
    for element in data.get("elements", []):
        hospital_name = element.get("tags", {}).get("name", "Unknown Hospital")

        if any(keyword in hospital_name.lower() for keyword in ["general", "specialty","Hospital", "multispeciality"]):
            hospital_lat = element["lat"]
            hospital_lon = element["lon"]

            distance = geodesic((lat, lon), (hospital_lat, hospital_lon)).km

            hospitals.append({
                "latitude": hospital_lat,
                "longitude": hospital_lon,
                "name": hospital_name,
                "distance_km": distance
            })

    hospitals = sorted(hospitals, key=lambda x: x["distance_km"])[:5]

    return hospitals


def retry(session, retries=3, backoff_factor=0.3, status_forcelist=(500, 502, 504)):
    retry = Retry(
        total=retries,
        read=retries,
        connect=retries,
        backoff_factor=backoff_factor,
        status_forcelist=status_forcelist,
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    return session

def home(request):

    cache_session = requests_cache.CachedSession('.cache', expire_after=3600)
    retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
    openmeteo = openmeteo_requests.Client(session=retry_session)

    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": lat,
        "longitude": lon,
        "current": ["temperature_2m", "precipitation", "weather_code", "cloud_cover", "wind_speed_10m"],
        "daily": ["weather_code", "temperature_2m_max", "precipitation_sum", "rain_sum", "showers_sum", "snowfall_sum", "precipitation_probability_max"],
        "timezone": "Asia/Tokyo",
        "past_days": 30,
        "forecast_days": 0,
        "models": "best_match"
    }
    responses = openmeteo.weather_api(url, params=params)

    response = responses[0]
    current = response.Current()
    weather_info = {
        "Current Time": current.Time(),
        "Temperature (°C)": round(current.Variables(0).Value(), 5),
        "Precipitation (mm)": round(current.Variables(1).Value(), 5),
        "Weather Code": round(current.Variables(2).Value(), 5),
        "Cloud Cover (%)": round(current.Variables(3).Value(), 5),
        "Wind Speed (m/s)": round(current.Variables(4).Value(), 5),
    }

    daily = response.Daily()
    daily_data = {
        "date": pd.date_range(
            start=pd.to_datetime(daily.Time(), unit="s", utc=True),
            periods=len(daily.Variables(0).ValuesAsNumpy()),
            freq="D"
        ),
        "weather_code": daily.Variables(0).ValuesAsNumpy(),
        "temperature_2m_max": daily.Variables(1).ValuesAsNumpy(),
        "precipitation_sum": daily.Variables(2).ValuesAsNumpy(),
        "rain_sum": daily.Variables(3).ValuesAsNumpy(),
        "showers_sum": daily.Variables(4).ValuesAsNumpy(),
        "snowfall_sum": daily.Variables(5).ValuesAsNumpy(),
        "precipitation_probability_max": daily.Variables(6).ValuesAsNumpy(),
    }

    daily_dataframe = pd.DataFrame(data=daily_data)
    daily_dataframe.set_index("date", inplace=True) 

    columns_to_forecast = ["temperature_2m_max", "precipitation_sum", "rain_sum", "showers_sum", "snowfall_sum", "precipitation_probability_max"]
    forecast_results = {}

    for col in columns_to_forecast:
        model = ARIMA(daily_dataframe[col], order=(5, 1, 0)) 
        model_fit = model.fit()
        forecast = model_fit.forecast(steps=2) 
        forecast_results[col] = forecast.values

    today = pd.Timestamp.now().normalize()
    future_dates = [today, today + pd.Timedelta(days=1)] 

    forecast_info = {
        "Today": {
            "Date": future_dates[0].strftime("%Y-%m-%d"),
            "Temperature (°C)": round(forecast_results["temperature_2m_max"][0], 5),
            "Precipitation (mm)": round(forecast_results["precipitation_sum"][0], 5),
            "Rain (mm)": round(forecast_results["rain_sum"][0], 5),
            "Showers (mm)": round(forecast_results["showers_sum"][0], 5),
            "Snowfall (mm)": round(forecast_results["snowfall_sum"][0], 5),
            "Precipitation Probability (%)": round(forecast_results["precipitation_probability_max"][0], 5),
        },
        "Tomorrow": {
            "Date": future_dates[1].strftime("%Y-%m-%d"),
            "Temperature (°C)": round(forecast_results["temperature_2m_max"][1], 5),
            "Precipitation (mm)": round(forecast_results["precipitation_sum"][1], 5),
            "Rain (mm)": round(forecast_results["rain_sum"][1], 5),
            "Showers (mm)": round(forecast_results["showers_sum"][1], 5),
            "Snowfall (mm)": round(forecast_results["snowfall_sum"][1], 5),
            "Precipitation Probability (%)": round(forecast_results["precipitation_probability_max"][1], 5),
        },
    }

    return render(request, 'weather.html', {
        'forecast_info': forecast_info,
        'weather_info': weather_info,
        'add': address,
    })



def earth(request):
    earthquakes = fetch_earthquake_data()
    
    earthquake_list = []
    for earthquake in earthquakes:
        properties = earthquake["properties"]
        geometry = earthquake["geometry"]
     
        timestamp_seconds = properties["time"] / 1000

        datetime_obj = datetime.fromtimestamp(timestamp_seconds)
        earthquake_list.append({
            "magnitude": properties["mag"],
            "place": properties["place"],
            "time": datetime_obj, 
            "coordinates": geometry["coordinates"] 
        })
    
    return render(request, 'index.html', {'earthquakes': earthquake_list})


def rehab(request):

    hospitals = get_nearest_hospitals(lat, lon)
    query = request.GET.get('q', '')  # Default to an empty string if 'q' is None
    if query:
        patients = Patient.objects.filter(
            Q(name__icontains=query) | Q(patient_id__icontains=query)
        )
    else:
        patients = Patient.objects.all()

    
    donations = Donation.objects.all().order_by('-date')  # Fetch all donations
    form = DonationForm()

    if request.method == "POST":
        form = DonationForm(request.POST)
        if form.is_valid():
            form.save()  # Save donation to the database
            return redirect('rehab')  # Redirect to clear the form

    return render(request, "rehab.html", {
        "lat": lat,
        "lon": lon,
        "hospitals": json.dumps(hospitals),
        'patients': patients,
        'query': query,'form': form, 'donations': donations
    })


def main(request):
    return render(request, "home.html", {})
