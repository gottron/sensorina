import datetime as dt

TEMPERATURE = 'Temperature'
HUMIDITY = 'Humidity'
PRESSURE = 'Pressure'
BRIGHTNESS = 'Brightness'
SOIL_HUMIDITY = 'SoilHumidity'

class SensorReading(object):


    def __init__ (self, sensor_type, value, origin, time, id=None) :
        self.sensor_type = sensor_type
        self.value = value
        self.origin = origin
        self.time = time
        if id != None :
            self.id = id

    
    @staticmethod
    def from_dict(source) :
        if 'id' in source :
            return SensorReading(source['sensor_type'], source['value'], source['origin'], source['time'], source['id'])
        else :
            return SensorReading(source['sensor_type'], source['value'], source['origin'], source['time'])


    def to_dict(self) :
        result =  {
            'sensor_type' : self.sensor_type,
            'value' : self.value,
            'origin' : self.origin,
            'time' : self.time,
        }
        if hasattr(self, 'id') :
            result.update({'id' : self.id})
        return result
        

    def __repr__(self) :
        return self.to_dict()