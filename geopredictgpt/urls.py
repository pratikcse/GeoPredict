from django.urls import path
from . import views

urlpatterns = [
    path('weather/', views.home, name="home"),
    path('', views.main, name="main"),
    path('gemini-api/', views.gemini_api, name='gemini_api'),
    path('gemini-api2/', views.gemini_api2, name='gemini_api2'),
    path('gemini-api3/', views.gemini_api3, name='gemini_api3'),
    path('earth/', views.earth, name="earth"),
    path('rehab/', views.rehab, name="rehab"),
]
