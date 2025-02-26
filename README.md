# GeoPredict

GeoPredict is a disaster prediction system designed to forecast and monitor earthquakes and heavy rainfall (storms) using real-time data collection and machine learning models. The project is built using Django and integrates various APIs to provide accurate predictions and alerts.

## Features

### 1. Real-Time Data Collection
GeoPredict fetches live earthquake and weather data using publicly available APIs such as:
- **USGS Earthquake API** - Provides real-time earthquake activity worldwide.
- **OpenWeather API** - Supplies weather data, including rainfall predictions and storm tracking.

### 2. Predictive Modeling
The system leverages:
- **ARIMA (AutoRegressive Integrated Moving Average)** - A time-series forecasting model used for predicting future disaster trends based on historical data.
- **Machine Learning Techniques** - Used to refine predictions and improve accuracy over time.

### 3. Interactive Dashboard
- **Live Map View:** Displays earthquake and storm events on an interactive map.
- **Statistical Charts:** Graphs and visualizations help analyze trends over time.
- **Alert System:** Sends notifications for severe weather or earthquake warnings.

### 4. Historical Data Analysis
GeoPredict stores past disaster data to help researchers and authorities analyze trends and improve disaster preparedness.

### 5. User-Friendly Interface
- Web-based UI built with Django templates and Bootstrap for responsiveness.
- Easy-to-use navigation for users to access forecasts and historical data.

## Installation Guide

### Prerequisites
Ensure you have the following installed:
- **Python 3.x** - Required for running Django and dependencies.
- **Django Framework** - The backbone of the web application.
- **Pip (Python Package Installer)** - Required for installing dependencies.
- **Virtualenv (Optional but Recommended)** - Helps manage project dependencies.
- **PostgreSQL or SQLite** - Database to store historical data.

### Steps to Install

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/pratikcse/GeoPredict.git
   cd GeoPredict
   ```

2. **Create a Virtual Environment (Optional but Recommended):**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   ```

3. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set Up Database:**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Run the Server:**
   ```bash
   python manage.py runserver
   ```

6. **Access the Web Application:**
   Open your browser and go to `http://127.0.0.1:8000/`

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
- **Monitor real-time earthquake and storm data.**
- **Analyze past disasters using the interactive dashboard.**
- **Receive predictive insights using the ARIMA model.**
- **Enable alerts for severe weather and seismic activity.**

## API Integration
GeoPredict integrates the following APIs:
- **USGS Earthquake API:** Fetches global seismic activity.
- **OpenWeather API:** Provides weather forecasts and storm predictions.
- **Google Maps API (Optional):** Used for mapping disaster locations.

## Contributors
- **Pratik CSE** - Developer & Maintainer

## License
This project is licensed under the **MIT License**.

## Acknowledgments
- **Django Community** - For providing an excellent web framework.
- **OpenWeather API** - For real-time weather data.
- **USGS Earthquake API** - For live earthquake updates.

For any issues or contributions, feel free to submit a pull request or open an issue in the repository!

