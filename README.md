# GeoPredict

GeoPredict is a disaster prediction system designed to forecast and monitor earthquakes and heavy rainfall (storms) using real-time data collection and machine learning models. The project is built using Django and integrates various APIs to provide accurate predictions and alerts.

## Features

### 1. Real-Time Data Collection
GeoPredict fetches live earthquake and weather data using publicly available APIs such as:
- **USGS Earthquake API** - Provides real-time earthquake activity worldwide.
- **Meteo API** - Supplies weather data, including rainfall predictions and storm tracking.

### 2. Predictive Modeling
The system leverages:
- **ARIMA (AutoRegressive Integrated Moving Average)** - A time-series forecasting model used for predicting future disaster trends based on historical data.
- **Machine Learning Techniques** - Used to refine predictions and improve accuracy over time.

### 3. Forecasting Features
GeoPredict uses advanced forecasting techniques to enhance disaster prediction accuracy:
- **Temperature Forecasting**: Uses ARIMA models to predict future temperature changes based on historical data.
- **Rainfall Prediction**: Forecasts precipitation levels to assess potential flooding or storm severity.
- **Seismic Activity Prediction**: Analyzes past earthquake data to determine future probabilities of seismic activity in specific regions.
- **Storm Trend Analysis**: Detects patterns in wind speeds, cloud cover, and precipitation to forecast storms effectively.

### 4. Interactive Dashboard
- **Live Map View**: Displays earthquake and storm events on an interactive map.
- **Statistical Charts**: Graphs and visualizations help analyze trends over time.
- **Alert System**: Sends notifications for severe weather or earthquake warnings.

### 5. Historical Data Analysis
GeoPredict stores past disaster data to help researchers and authorities analyze trends and improve disaster preparedness.

### 6. Rehabilitation Management System Features
The rehabilitation system within GeoPredict includes the following capabilities:
- **Victim Search System**: Allows users to search for victims by name or ID, displaying their current location, rescued location, and status.
- **Donation System**: Users can donate funds for disaster relief, view recent donations, and contribute towards recovery efforts.
- **Emergency Contacts & Precautionary Measures**: Provides an AI-generated list of emergency numbers and essential safety precautions before, during, and after a storm.
- **Nearest Hospital Locator**: Displays nearby hospitals using geolocation and OpenStreetMap integration, allowing users to locate medical assistance quickly.

### 7. User-Friendly Interface
- **Web-based UI** built with Django templates and Bootstrap for responsiveness.
- **Easy-to-use navigation** for users to access forecasts and historical data.

## Installation Guide

### Prerequisites
Ensure you have the following installed:
- **Python 3.x** - Required for running Django and dependencies.
- **Django Framework** - The backbone of the web application.
- **Pip (Python Package Installer)** - Required for installing dependencies.
- **Virtualenv (Optional but Recommended)** - Helps manage project dependencies.

### Steps to Install

#### 1. Clone the Repository
```bash
git clone https://github.com/pratikcse/GeoPredict.git
cd GeoPredict
```

#### 2. Create a Virtual Environment (Optional but Recommended)
```bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

#### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

#### 4. Set Up Database
```bash
python manage.py makemigrations
python manage.py migrate
```

#### 5. Configure Gemini API Key
- Obtain a **Gemini API key** from [Google AI](https://ai.google.com/)
- Open the `views.py` file and update the key:
```python
GOOGLE_API_KEY = "your_gemini_api_key_here"
```

#### 6. Run the Server
```bash
python manage.py runserver
```
- Access the Web Application: Open your browser and go to **http://127.0.0.1:8000/**

## Project Structure
```
GeoPredict/
│-- geopredict/  # Main Django app
│   ├── models.py    # Database models
│   ├── views.py     # API & web views
│   ├── urls.py      # URL routing
│   ├── templates/   # HTML templates
│   ├── static/      # CSS, JavaScript, and media files
│-- manage.py    # Django management tool
│-- requirements.txt  # Dependencies
```

## Usage
- Monitor real-time earthquake and storm data.
- Analyze past disasters using the interactive dashboard.
- Receive predictive insights using the **ARIMA model**.
- Enable alerts for severe weather and seismic activity.
- Utilize the **rehabilitation management system** for victim tracking, donations, and medical assistance.

## API Integration
GeoPredict integrates the following APIs:
- **USGS Earthquake API**: Fetches global seismic activity.
- **Meteo API**: Provides weather forecasts and storm predictions.
- **Overpass API**: Retrieves real-time hospital locations for medical assistance.

## Setting Up Models
To use GeoPredict's machine learning models, follow these steps:
1. Ensure that **ARIMA** is installed (`pip install statsmodels`).
2. The models are configured inside `views.py` and trained using historical data.
3. Modify `views.py` if additional data sources or models are needed.

## Contributors
- **Pratik Rane** - Developer & Maintainer
- **Kartik Sambre** - Developer
- **Tanuj Jain** - Developer
- **Anvay Naik** - Developer

## License
This project is licensed under the **MIT License**.

## Acknowledgments
- **Django Community** - For providing an excellent web framework.
- **Meteo API** - For real-time weather data.
- **USGS Earthquake API** - For live earthquake updates.
- **OpenStreetMap & Overpass API** - For hospital location data.

For any issues or contributions, feel free to submit a **pull request** or open an **issue** in the repository!
