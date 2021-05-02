from web.weather import openweathermap
from sensors.AbstractSensor import AbstractSensor
from db.Error import Error
import db.SensorReading as sr
import datetime as dt

class WeatherSensor(AbstractSensor) :

    def __init__(self, api_key, lat, lon) :
        self.db = None
        self.lat = lat
        self.lon = lon
        # Every 5 Minutes
        self.delay = 5*60
        openweathermap.init_api_key(api_key)

    def setup(self, db) :
        self.db = db

    def shutdown(self) :
        pass

    def get_reading(self) :
        print('Reading Web Weather data')
        weather_data = openweathermap.get_weather_data(self.lat, self.lon)
        #'dt','sunrise','sunset','temp','pressure','humidity','uvi','clouds','wind_speed','weather'
        time = dt.datetime.fromtimestamp(weather_data['dt'])
        reading_temp = sr.SensorReading(sensor_type = sr.TEMPERATURE, value = weather_data['temp'], origin = 'OpenWeatherMap', time = time) 
        reading_pressure = sr.SensorReading(sensor_type = sr.PRESSURE, value = weather_data['pressure'], origin = 'OpenWeatherMap', time = time) 
        reading_humidity = sr.SensorReading(sensor_type = sr.HUMIDITY, value = weather_data['humidity'], origin = 'OpenWeatherMap', time = time) 
        self.db.store_reading(reading_temp)
        self.db.store_reading(reading_pressure)
        self.db.store_reading(reading_humidity)

    def min_call_delay(self):
        return self.delay
