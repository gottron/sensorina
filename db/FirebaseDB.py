import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import random
import datetime as dt
from Message import Message
from SensorReading import SensorReading
from Error import Error

__db__ = None

__MESSAGES_COLLECTION__ = u'messages'
__READINGS_COLLECTION__ = u'readings'
__ERRORS_COLLECTION__ = u'errors'

def init(certificate):
    global __db__
    firebase_admin.initialize_app(certificate)
    __db__ = firestore.client()

def is_initiated() :
    return __db__ != None

def store_message(message) :
    if is_initiated() :
        if isinstance(message, Message) :
            __db__.collection(__MESSAGES_COLLECTION__).add(message.to_dict())
    else:
        raise Exception('Firebase DB not initiated')
    
def retrieve_messages(filter_by=None, filter_value="", limit=10) :
    if is_initiated() :
        query = None
        messages_ref = __db__.collection(__MESSAGES_COLLECTION__)
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

def store_reading(sensor_reading) :
    print(str(sensor_reading.to_dict()))
    if is_initiated() :
        if isinstance(sensor_reading, SensorReading) :
            __db__.collection(__READINGS_COLLECTION__).add(sensor_reading.to_dict())
    else:
        raise Exception('Firebase DB not initiated')
    
def retrieve_reading(filter_by=None, filter_value="", limit=10) :
    if is_initiated() :
        query = None
        readings_ref = __db__.collection(__READINGS_COLLECTION__)
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

def store_error(error) :
    if is_initiated() :
        if isinstance(error, Error) :
            __db__.collection(__ERRORS_COLLECTION__).add(error.to_dict())
    else:
        raise Exception('Firebase DB not initiated')
    
def retrieve_error(filter_by=None, filter_value="", limit=10) :
    if is_initiated() :
        query = None
        errors_ref = __db__.collection(__ERRORS_COLLECTION__)
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
    init(cred)
    m_data = {
        'instructions' : 'Nope',
        'message' : 'Message by python {}'.format(random.randrange(0,1000)),
        'origin' : 'Python',
        'time' : dt.datetime.now(dt.timezone(offset=-dt.timedelta(hours=2)))
    }
    message = Message.from_dict(m_data)
    store_message(message)
    rel = retrieve_messages(filter_by='origin', filter_value='Python', limit=3)
    for m in rel :
        print(m.to_dict())

    r_data = {
        'sensor_type' : 'Temperature',
        'value' : random.randrange(-10,40),
        'origin' : 'Python',
        'time' : dt.datetime.now(dt.timezone(offset=-dt.timedelta(hours=2)))
    }
    reading = SensorReading.from_dict(r_data)
    store_reading(reading)
    rel = retrieve_reading(filter_by='sensor_type', filter_value='Temperature', limit=4)
    for r in rel :
        print(r.to_dict())

    e_data = {
        'error' : 'Test error {}'.format(random.randrange(0,520)),
        'origin' : 'Python',
        'time' : dt.datetime.now(dt.timezone(offset=-dt.timedelta(hours=2)))
    }
    error = Error.from_dict(e_data)
    store_error(error)
    rel = retrieve_error(filter_by='origin', filter_value='Python', limit=4)
    for e in rel :
        print(e.to_dict())

        






