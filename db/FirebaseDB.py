import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import random
import datetime as dt
from db.Message import Message
from db.SensorReading import SensorReading
from db.Error import Error

__db__ = None

__MESSAGES_COLLECTION__ = u'messages'
__READINGS_COLLECTION__ = u'readings'
__ERRORS_COLLECTION__ = u'errors'

class FirebaseDB :

    def __init__(self, certificate):
        firebase_admin.initialize_app(certificate)
        self.client = firestore.client()

    def is_initiated(self) :
        return self.client != None

    def store_message(self, message) :
        if self.is_initiated() :
            if isinstance(message, Message) :
                self.client.collection(__MESSAGES_COLLECTION__).add(message.to_dict())
        else:
            raise Exception('Firebase DB not initiated')
        
    def retrieve_messages(self, filter_by=None, filter_value="", limit=10) :
        if self.is_initiated() :
            query = None
            messages_ref = self.client.collection(__MESSAGES_COLLECTION__)
            if filter_by != None :
                if filter_by in ['origin'] :
                    query = messages_ref.where(filter_by, u'==', filter_value).order_by(u'time', direction=firestore.Query.DESCENDING).limit(limit)
            if query == None :
                query = messages_ref.order_by(u'time', direction=firestore.Query.DESCENDING).limit(limit)
            result = []
            query_results = query.stream()
            for message_res in query_results:
                result.append(Message.from_dict(message_res.to_dict()))
            return result
        else:
            raise Exception('Firebase DB not initiated')

    def store_reading(self, sensor_reading) :
        if self.is_initiated() :
            if isinstance(sensor_reading, SensorReading) :
                self.client.collection(__READINGS_COLLECTION__).add(sensor_reading.to_dict())
        else:
            raise Exception('Firebase DB not initiated')
        
    def retrieve_reading(self, filter_by=None, filter_value="", limit=10) :
        if self.is_initiated() :
            query = None
            readings_ref = self.client.collection(__READINGS_COLLECTION__)
            if filter_by != None :
                if filter_by in ['origin','sensor_type'] :
                    query = readings_ref.where(filter_by, u'==', filter_value).order_by(u'time', direction=firestore.Query.DESCENDING).limit(limit)
            if query == None :
                query = readings_ref.order_by(u'time', direction=firestore.Query.DESCENDING).limit(limit)
            result = []
            query_results = query.stream()
            for reading_res in query_results:
                result.append(SensorReading.from_dict(reading_res.to_dict()))
            return result
        else:
            raise Exception('Firebase DB not initiated')

    def store_error(self, error) :
        if self.is_initiated() :
            if isinstance(error, Error) :
                self.client.collection(__ERRORS_COLLECTION__).add(error.to_dict())
        else:
            raise Exception('Firebase DB not initiated')
        
    def retrieve_error(self, filter_by=None, filter_value="", limit=10) :
        if self.is_initiated() :
            query = None
            errors_ref = self.client.collection(__ERRORS_COLLECTION__)
            if filter_by != None :
                if filter_by in ['origin'] :
                    query = errors_ref.where(filter_by, u'==', filter_value).order_by(u'time', direction=firestore.Query.DESCENDING).limit(limit)
            if query == None :
                query = errors_ref.order_by(u'time', direction=firestore.Query.DESCENDING).limit(limit)
            result = []
            query_results = query.stream()
            for error_res in query_results:
                result.append(Error.from_dict(error_res.to_dict()))
            return result
        else:
            raise Exception('Firebase DB not initiated')

if __name__ == '__main__' :
    cred = credentials.Certificate('../conf/certificates/sensorina-ee77d-634877ba7bb5.json')
    db = FirebaseDB(cred)
    m_data = {
        'instructions' : 'Nope',
        'message' : 'Message by python {}'.format(random.randrange(0,1000)),
        'origin' : 'Python',
        'time' : dt.datetime.now(dt.timezone(offset=-dt.timedelta(hours=2)))
    }
    message = Message.from_dict(m_data)
    db.store_message(message)
    rel = db.retrieve_messages(filter_by='origin', filter_value='Python', limit=3)
    for m in rel :
        print(m.to_dict())

    r_data = {
        'sensor_type' : 'Temperature',
        'value' : random.randrange(-10,40),
        'origin' : 'Python',
        'time' : dt.datetime.now(dt.timezone(offset=-dt.timedelta(hours=2)))
    }
    reading = SensorReading.from_dict(r_data)
    db.store_reading(reading)
    rel = db.retrieve_reading(filter_by='sensor_type', filter_value='Temperature', limit=4)
    for r in rel :
        print(r.to_dict())

    e_data = {
        'error' : 'Test error {}'.format(random.randrange(0,520)),
        'origin' : 'Python',
        'time' : dt.datetime.now(dt.timezone(offset=-dt.timedelta(hours=2)))
    }
    error = Error.from_dict(e_data)
    db.store_error(error)
    rel = db.retrieve_error(filter_by='origin', filter_value='Python', limit=4)
    for e in rel :
        print(e.to_dict())

        






