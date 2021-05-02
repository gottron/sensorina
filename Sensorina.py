import datetime as dt
from db.FirebaseDB import FirebaseDB
from dotenv import dotenv_values
from firebase_admin import credentials
from sensors.WeatherSensor import WeatherSensor
from web.weather import openweathermap
import time


__refresh__ = 1.0
__db__ = None
__sensors__ = []
__shutdown__ = False


def setup(conf_file) :
    settings = dotenv_values('conf/sensorina.env')
    global __refresh__, __db__, __sensors__
    __refresh__ = float(settings['REFRESH'])
    # Setup DB connection
    certificate = credentials.Certificate(settings['FIREBASE_CERT'])
    __db__ = FirebaseDB(certificate)

    # Init OpenWeatherMap sensor
    weather_sensor = {
        'sensor'    : WeatherSensor(settings['OPENWEATHERMAP_API_KEY'] ,openweathermap.LOCATIONS['Ruesselsheim']['lat'], openweathermap.LOCATIONS['Ruesselsheim']['lon']),
    }
    __sensors__.append(weather_sensor)

    # Now setup all sensors
    for s in __sensors__ :
        s['sensor'].setup(__db__)
        s['next_call'] = dt.datetime.now()

def loop():
    __shutdown__ = False
    while not __shutdown__ :
        t = dt.datetime.now()
        for s in __sensors__:
            if t > s['next_call'] :
                s['sensor'].get_reading()
                s['next_call'] = s['next_call'] + dt.timedelta(seconds = s['sensor'].min_call_delay())
        time.sleep(__refresh__)

def shutdown() :
    for s in __sensors__:
        s['sensor'].shutdown()


if __name__ == "__main__":
    print('Initiating...')
    setup('conf/sensorina.env')
    try :
        print('Starting...')
        loop()
    except KeyboardInterrupt:
        print('Shutting down...')
        shutdown()
    print('Done!')
