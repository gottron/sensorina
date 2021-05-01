import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import random
import datetime as dt


cred = credentials.Certificate('../conf/certificates/sensorina-ee77d-634877ba7bb5.json')
firebase_admin.initialize_app(cred)

db = firestore.client()


messages_ref = db.collection(u'Message')
ms = messages_ref.stream()

for m in ms:
    print(f'{m.id} => {m.to_dict()}')


nm = {
    'instructions' : 'Nope',
    'message' : 'Message by python {}'.format(random.randrange(0,1000)),
    'origin' : 'Python',
    'time' : dt.datetime.now(dt.timezone(offset=-dt.timedelta(hours=2)))
}

db.collection('Message').add(nm)

print("Geting last 3 messages")

#last_5_mins = dt.datetime.now(dt.timezone(offset=-dt.timedelta(hours=2) - dt.timedelta(minutes=5)

#query = messages_ref.where(u'origin', u'>=', u'Python')
query = messages_ref.order_by(u'time', direction=firestore.Query.DESCENDING).limit(3)

q_res = query.stream()

for m in q_res:
    print(f'{m.id} => {m.to_dict()}')



