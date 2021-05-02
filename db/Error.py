import datetime as dt


class Error(object):


    def __init__ (self, error, origin, time=dt.datetime.now(), id=None) :
        self.error = error
        self.origin = origin
        self.time = time
        if id != None :
            self.id = id

    
    @staticmethod
    def from_dict(source) :
        if 'id' in source :
            return Error(source['error'], source['origin'], source['time'], source['id'])
        else :
            return Error(source['error'], source['origin'], source['time'])


    def to_dict(self) :
        result =  {
            'error' : self.error,
            'origin' : self.origin,
            'time' : self.time,
        }
        if hasattr(self, 'id') :
            result.update({'id' : self.id})
        return result
        

    def __repr__(self) :
        return self.to_dict()