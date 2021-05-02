import requests
import json
from dotenv import dotenv_values

API_KEY = None

# Some selected locations for towns, as looked up on https://latitudelongitude.org/
LOCATIONS = {
    'Biella'          : {'lat' : 45.56630, 'lon' : 8.05499},
    'Frankfurt'       : {'lat' : 50.11552, 'lon' : 8.68417},
    'Mainz'           : {'lat' : 49.98419, 'lon' : 8.27910},
    'Ruesselsheim'     : {'lat' : 49.98955, 'lon' : 8.42251},
    }

# The key to actually select from the response
weather_rel_keys = ['dt','sunrise','sunset','temp','pressure','humidity','uvi','clouds','wind_speed','weather']


# -----------------------------------------------------------------

def init_api_key(api_key) :
    """Set the API key for calls to the OpenWeatherMap API

    The function sets the API key to be used for all subsequent
    calls in functions. In this way it is not necessary to provide
    the key everytime a function is called.
    
    Keyword Arguments:
    api_key -- the API key to use for future API calls
    """
    global API_KEY
    API_KEY = api_key


# -------------------------------------------------------------------

def flatten(d, prefix = '', rel_keys = None) :
    """ Flatten a nested dict

    Internal function which is used to flatten, e.g. the weather part
    of an API response.
    
    Keyword Arguments:
    d -- the dict to flatten
    prefix -- prefix to add to all keys (default '')
    rel_keys -- filter list of keys to preserve, if None all keys are
        preserved (default None)
    
    Returns:
    flattened dict
    """
    result = {}
    for key in d:
        if rel_keys == None or key in rel_keys:
            # Nested dictionary in JSON comes as list
            if type(d[key]) is list :
                # Iterate elements of the list
                for element in d[key] :
                    # Recurse and merge result
                    result.update(flatten(element,prefix = key+'_'))
            else:
                result[prefix+key] = d[key]
    return result



# -------------------------------------------------------------------

def get_weather_data(lat, lon):
    """ Get the current weather data for a location

    Retrieves and converts the weather data for a given lat-lon
    position. The result is flattened and converted into a Pandas
    dataframe.
    
    Keyword Arguments:
    [lat,lon] -- two element list with latitude and longitude
    
    Returns
    Pandas dataframe with information on the weather
    """
    if API_KEY == None :
        # API key has not been set -- raise Exception
        raise Exception('OpenWeatherMap module not initialised! Need to set the API key using init_api_key()')

    url = "https://api.openweathermap.org/data/2.5/onecall?lat={}&lon={}&appid={}&expclude=minutely,hourly,daily,alerts&units=metric".format(lat, lon, API_KEY)
    response = requests.get(url)
    if response.status_code == 200 :
        # result looks ok, so convert to JSON
        data = json.loads(response.text)
        # obtain lat and lon which is actually reported
        result = {
            'lat' : data['lat'],
            'lon' : data['lon'],
            'source' : 'api.openweathermap.org'
        }
        # Flatten the relevant part of the JSON response
        d = flatten(data['current'], rel_keys=weather_rel_keys)
        # Merge all info and build dataframe
        result.update(d)
        #df_result = pd.DataFrame(result, index = [1])
        return result
    else :
        # Something caused an error in the RECT call - pass on
        raise Exception('OpenWeatherMap API replied with error {}'.format(response.status_code))

if __name__ == '__main__' :
    config = dotenv_values('api_key.env')
    print('Using API Key: {}'.format(config['OPENWEATHERMAP_API_KEY']))
    init_api_key(config['OPENWEATHERMAP_API_KEY'])
    print(get_weather_data(LOCATIONS['Ruesselsheim']['lat'], LOCATIONS['Ruesselsheim']['lon']))


