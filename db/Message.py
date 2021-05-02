import datetime as dt


class Message(object):


    def __init__ (self, message, origin, instructions, time, id=None) :
        self.message = message
        self.origin = origin
        self.instructions = instructions
        self.time = time
        if id != None :
            self.id = id

    
    @staticmethod
    def from_dict(source) :
        if 'id' in source :
            return Message(source['message'], source['origin'], source['instructions'], source['time'], source['id'])
        else :
            return Message(source['message'], source['origin'], source['instructions'], source['time'])


    def to_dict(self) :
        result =  {
            'message' : self.message,
            'origin' : self.origin,
            'instructions' : self.instructions,
            'time' : self.time,
        }
        if hasattr(self, 'id') :
            result.update({'id' : self.id})
        return result
        

    def __repr__(self) :
        return self.to_dict()